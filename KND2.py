import streamlit as st
import pandas as pd

# Load the external Excel file containing valid account numbers and divisions
valid_accounts_df = pd.read_excel('/Users/punit/Downloads/5to9Consummer.xlsx')  # Ensure this file exists with the correct path

# Create a dictionary for fast lookup of account numbers and their corresponding divisions
account_division_dict = dict(zip(valid_accounts_df['ACCT_ID'].astype(str), valid_accounts_df['DIV_NAME']))

def save_response_to_excel(response):
    # Load the existing responses file or create a new DataFrame if it doesn't exist
    try:
        responses_df = pd.read_excel('responses.xlsx')
    except FileNotFoundError:
        responses_df = pd.DataFrame(columns=['Account Number', 'Division', 'Reading KWH', 'Reading KVAH', 'UC KW', 'UC KVA', 'Meter No', 'Meter Make', 'Meter Type', 'Bill Date', 'Exception', 'Reader Name'])
    
    # Append the new response
    responses_df = pd.concat([responses_df, pd.DataFrame([response])], ignore_index=True)
    
    # Save the DataFrame back to the Excel file
    responses_df.to_excel('responses.xlsx', index=False)

# Streamlit app
st.image('/Users/punit/Desktop/ss.png', use_column_width=True)  # Replace 'meter_reading_image.png' with your image file name
st.title('Meter Reading Form')

with st.form(key='meter_reading_form'):
    account_no = st.text_input('Account Number')
    division = st.text_input('Division', disabled=True)
    reading_kwh = st.number_input('Reading KWH', min_value=0.0, step=0.1)
    reading_kvah = st.number_input('Reading KVAH', min_value=0.0, step=0.1)
    uc_kw = st.number_input('UC KW', min_value=0.0, step=0.1)
    uc_kva = st.number_input('UC KVA', min_value=0.0, step=0.1)
    meter_no = st.text_input('Meter No')
    meter_make = st.selectbox('Meter Make', ['AVON', 'ALLIED', 'BENTEK', 'CAPITAL', 'EDMI', 'EISTER', 'EMC', 'FLASH', 'GENUS', 'HPL', 'LNG', 'LNT', 'MTPL', 'OMEGA', 'PMPL', 'POWERTECH', 'SECURE', 'VISIONTEK', 'OTHER'])
    meter_type = st.radio('Meter Type', ['Single Phase', 'Three Phase'])
    bill_date = st.date_input('Bill Date')
    exception = st.selectbox('Exception', ['CONSUMER NOT CORPORATE', 'LINE DISCONNECTED', 'METER AT HEIGHT', 'METER BOX DIRTY', 'METER CHANGE', 'METER DEFECTIVE', 'NO DISPLAY', 'NO METER NO CABLE', 'PERMANENT LOCK', 'ROUND OVER', 'TEMPORARY LOCK', 'UNREADABLE READING'])
    reader_name = st.text_input('Reader Name')
    
    submit_button = st.form_submit_button(label='Submit')

    if account_no:
        division = account_division_dict.get(account_no, '')
        st.text_input('Division', value=division, disabled=True)
    
    if submit_button:
        if account_no in account_division_dict:
            response = {
                'Account Number': account_no,
                'Division': division,
                'Reading KWH': reading_kwh,
                'Reading KVAH': reading_kvah,
                'UC KW': uc_kw,
                'UC KVA': uc_kva,
                'Meter No': meter_no,
                'Meter Make': meter_make,
                'Meter Type': meter_type,
                'Bill Date': bill_date,
                'Exception': exception,
                'Reader Name': reader_name
            }
            save_response_to_excel(response)
            st.success('Response saved successfully!')
        else:
            st.error('Invalid Account Number. Please check and try again.')
