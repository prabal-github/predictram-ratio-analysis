import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import json
from datetime import datetime

LOGGER = get_logger(__name__)

def run():
    income_statements_path = 'income_statements.json'
    with open(income_statements_path, 'r') as file:
        income_statements = json.load(file)
    income_indices = []
    income_statements_data = []
    for index, statements in income_statements.items():
        income_indices.append(index)
        income_statements_data.append(statements)
        
    st.header('Financial Ratio Analysis')

    index = st.selectbox('Select market index symbol', income_indices)
    income_statement = income_statements_data[income_indices.index(index)]

    if income_statement:
        columns = ["Date"] + list(income_statement[next(iter(income_statement))].keys())
        data = []
        for date_str, values in income_statement.items():
            row = [datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")] + list(values.values())
            data.append(row)
        result = {"columns": columns, "data": data}

        # Convert result to JSON
        result_data = json.dumps(result, default=str, indent=2)
        json_data = json.loads(result_data)

        dataframe = pd.DataFrame(json_data['data'], columns=json_data['columns'])
        dataframe = dataframe.sort_values(by="Date")

        dataframe['Gross Margin'] = (dataframe['Gross Profit'] / dataframe['Total Revenue']) * 100
        dataframe['Operating Margin'] = ((dataframe['Total Revenue'] - dataframe['Operating Expense']) / dataframe['Total Revenue']) * 100
        dataframe['Profit Margin'] = ((dataframe['Gross Profit'] - dataframe['Operating Expense'] - dataframe['Interest Expense'] - dataframe['Tax Provision']) / dataframe['Total Revenue']) * 100
        # dataframe['ROA'] = ((dataframe['Profit Margin'] * dataframe['Impairment Of Capital Assets']) / dataframe['Total Revenue'])
        # dataframe['ROE'] = ((dataframe['Profit Margin'] * dataframe['Impairment Of Capital Assets']) / (dataframe['Total Liabilities'] + dataframe['Total Revenue']))
        # dataframe['ROA'] = ((dataframe['Profit Margin'] * dataframe['Total Assets']) / dataframe['Total Revenue'])
        # dataframe['ROE'] = ((dataframe['Profit Margin'] * dataframe['Total Assets']) / (dataframe['Total Liabilities'] + dataframe['Total Revenue']))
        # dataframe['Current Ratio'] = dataframe['Total Assets'] / dataframe['Total Liabilities']
        # dataframe['Quick Ratio'] = ((dataframe['Cash'] + dataframe['Equivalents'] + dataframe['Accounts Receivable']) / dataframe['Total Liabilities'])
        # dataframe['Cash Ratio'] = ((dataframe['Cash'] + dataframe['Equivalents']) / dataframe['Total Liabilities'])
        # dataframe['Debt to Equity Ratio'] = dataframe['Total Liabilities'] / (dataframe['Total Assets'] - dataframe['Total Liabilities'])
        # dataframe['Debt to Asset Ratio'] = dataframe['Total Liabilities'] / dataframe['Total Assets']
        # dataframe['Accounts Receivable Turnover'] = dataframe['Total Revenue'] / dataframe['Accounts Receivable']
        # dataframe['Days in Account Receivables'] = 365 / dataframe['Accounts Receivable Turnover']
        # dataframe['Inventory Turnover'] = dataframe['Cost Of Revenue'] / dataframe['Inventory']
        # dataframe['Days in Inventories'] = 365 / dataframe['Inventory Turnover']
        # dataframe['Operating Cycle'] = dataframe['Days in Account Receivables'] + dataframe['Days in Inventories']
        # dataframe['Total Asset Turnover'] = dataframe['Total Revenue'] / dataframe['Total Assets']


        # # ------------------------------ RAIO RANGE TABLE ------------------------------
        # Ratio Ranges data
        ranges = {
            'Profit_Margin': [(10, float('inf')), (3, 10), (0, 3)],
            'Gross_Margin': [(35, float('inf')), (0, 35), (float('-inf'), 0)],
            'Operating_Margin': [(15, float('inf')), (0, 15), (float('-inf'), 0)],
            'ROA': [(10, float('inf')), (0, 10), (float('-inf'), 0)],
            'ROE': [(20, float('inf')), (0, 20), (float('-inf'), 0)],
            'Current_Ratio': [(3, float('inf')), (0, 3), (float('-inf'), 0)],
            'Quick_Ratio': [(2, 3), (1.5, 2), (0, 1.5)],
            'Cash_Ratio': [(0.25, 0.5), (0.1, 0.25), (0, 0.1)],
            'Debt_to_Equity_Ratio': [(0.5, 1), (1, 1.5), (1.5, float('inf'))],
            'Debt_to_Asset_Ratio': [(0.3, 0.5), (0.5, 0.75), (0.75, float('inf'))],
            'Accounts_Receivable_Turnover': [(6, 12), (4, 6), (0, 4)],
            'Days_in_Account_Receivables': [(30, 60), (60, 90), (90, float('inf'))],
            'Inventory_Turnover': [(4, 8), (2, 4), (0, 2)],
            'Days_in_Inventories': [(45, 90), (90, 135), (135, float('inf'))],
            'Operating_Cycle': [(75, 120), (120, 165), (165, float('inf'))],
            'Total_Asset_Turnover': [(1.0, 2.0), (0.75, 1.0), (0, 0.75)],
        }

        dataframe['Date'] = pd.to_datetime(dataframe['Date'])

        st.subheader('Quaterly Analysis Data')
        st.dataframe(dataframe)

        # Create list of dictionaries for the table
        range_table_data = []

        # Add overall ratio ranges to the table data
        for ratio_name, ranges_list in ranges.items():
            good_range, neutral_range, bad_range = ranges_list
            range_table_data.append({
                'Ratio': ratio_name,
                'Good Range': f'{good_range[0]}+%',
                'Neutral Range': f'{neutral_range[0]}-{neutral_range[1]}%',
                'Bad Range': f'{bad_range[0]}-{bad_range[1]}%'
            })

        # Display the table in Streamlit
        st.subheader('Overall Ratio Ranges')
        st.table(range_table_data)


        # # ------------------------------ AVERAGE RAIO TABLE ------------------------------
        # avg_table_data = []

        # # Calculate the overall average ratios
        # overall_average_ratios = {}
        # for ratio_name in ranges.keys():
        #     overall_average_ratios[ratio_name] = dataframe[ratio_name].mean()

        # def categorize_overall(ratio_name, value):
        #     for label, (lower, upper) in zip(['Good', 'Neutral', 'Bad'], ranges[ratio_name]):
        #         if lower <= value <= upper:
        #             return label
        #     return None

        # for ratio_name, average_value in overall_average_ratios.items():
        #     category = categorize_overall(ratio_name, average_value)
        #     avg_table_data.append({
        #         'Ratio': ratio_name,
        #         'Average Value': f'{average_value:.2f}+%',
        #         'Remarks': f'{category} ({average_value:.2f}%)',
        #     })

        # # Display the table in Streamlit
        # st.subheader('Overall Average Ratios')
        # st.table(avg_table_data)


        # ------------------------------ CHARTS ------------------------------ 
        st.subheader('Comparison of Selected Financial Ratios Graph 1')
        st.area_chart(dataframe, x='Date', y=['Profit Margin', 'Gross Margin', 'Operating Margin'], color=["#45c8a3", "#e65100", "#7a2e9b"], height=600)
        # st.line_chart(dataframe, x='Date', y=['Profit Margin', 'Gross Margin', 'Operating Margin', "ROA"], color=["#7a2e9b", "#45c8a3", "#e65100", "#2f4b7c"], height=600)

        # st.subheader('Comparison of Selected Financial Ratios Graph 2')
        # st.line_chart(dataframe, x='Date', y=['ROE', 'Current Ratio', 'Quick Ratio', "Cash Ratio"], color=["#7a2e9b", "#45c8a3", "#e65100", "#2f4b7c"], height=600)

        # st.subheader('Comparison of Selected Financial Ratios Graph 3')
        # st.line_chart(dataframe, x='Date', y=['Debt to Equity Ratio', 'Debt to Asset Ratio', 'Accounts Receivable Turnover', "Days in Account Receivables"], color=["#7a2e9b", "#45c8a3", "#e65100", "#2f4b7c"], height=600)

        # st.subheader('Comparison of Selected Financial Ratios Graph 4')
        # st.line_chart(dataframe, x='Date', y=['Inventory Turnover', 'Total Asset Turnover'], color=["#7a2e9b", "#45c8a3"], height=600)
    
    else:
        st.warning("Income statement is empty for the selected market index.")

if __name__ == "__main__":
    run()