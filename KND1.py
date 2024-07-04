import streamlit as st
import pandas as pd

# Load the external Excel file containing valid meter numbers and their corresponding details
valid_accounts_df = pd.read_excel('/Users/punit/Downloads/5to9Consummer.xlsx')  # Ensure this file exists with the correct path

# Create a dictionary for fast lookup of meter numbers and their corresponding details
meter_details_dict = valid_accounts_df.set_index('SERIAL_NBR').T.to_dict()

def save_response_to_excel(response):
    # Load the existing responses file or create a new DataFrame if it doesn't exist
    try:
        responses_df = pd.read_excel('responses.xlsx')
    except FileNotFoundError:
        responses_df = pd.DataFrame(columns=['Account Number', 'Division', 'Customer Name', 'Reading KWH', 'Reading KVAH', 'UC KW', 'UC KVA', 'Meter No', 'Meter Make', 'Meter Type', 'Bill Date', 'Exception', 'Reader Name', 'Remark'])
    
    # Append the new response
    responses_df = pd.concat([responses_df, pd.DataFrame([response])], ignore_index=True)
    
    # Save the DataFrame back to the Excel file
    responses_df.to_excel('responses.xlsx', index=False)

# Streamlit app
# st.image('/Users/punit/Desktop/ss.png', use_column_width=True)  # Replace 'meter_reading_image.png' with your image file name
st.title('KND: Meter Reading Form')

# Initialize session state to store validation status and meter details
if 'validated' not in st.session_state:
    st.session_state.validated = False
    st.session_state.meter_details = {}
if 'allow_proceed' not in st.session_state:
    st.session_state.allow_proceed = False

# Form for meter reading input
with st.form(key='meter_reading_form'):
    meter_no = st.text_input('Meter No')
    validate_button = st.form_submit_button(label='Validate Meter No')

    if validate_button:
        if meter_no in meter_details_dict:
            st.session_state.validated = True
            st.session_state.meter_details = meter_details_dict[meter_no]
            st.session_state.allow_proceed = True
            st.success(f'Meter No validated! Account No: {st.session_state.meter_details["ACCT_ID"]}, Customer Name: {st.session_state.meter_details["CONSUMER_NAME"]}, Division: {st.session_state.meter_details["DIV_NAME"]}')
        else:
            st.session_state.validated = False
            st.session_state.meter_details = {}
            st.session_state.allow_proceed = False

    if not st.session_state.validated:
        continue_process = st.radio("Meter No doesn't match with records. Do you want to continue?", ('Yes', 'No'))
        proceed_button = st.form_submit_button(label='Submit Yes/No')

        if proceed_button:
            if continue_process == 'Yes':
                st.session_state.allow_proceed = True
            else:
                st.session_state.allow_proceed = False
                st.stop()

if st.session_state.allow_proceed:
    with st.form(key='details_form'):
        account_no = st.text_input('Account Number', value=st.session_state.meter_details.get('ACCT_ID', ''), disabled=True)
        customer_name = st.text_input('Customer Name', value=st.session_state.meter_details.get('CONSUMER_NAME', ''), disabled=True)
        division = st.text_input('Division', value=st.session_state.meter_details.get('DIV_NAME', ''), disabled=True)
        reading_kwh = st.number_input('Reading KWH', min_value=0.0, step=0.1)
        reading_kvah = st.number_input('Reading KVAH', min_value=0.0, step=0.1)
        uc_kw = st.number_input('UC KW', min_value=0.0, step=0.1)
        uc_kva = st.number_input('UC KVA', min_value=0.0, step=0.1)
        meter_make = st.selectbox('Meter Make', ['AVON', 'ALLIED', 'BENTEK', 'CAPITAL', 'EDMI', 'EISTER', 'EMC', 'FLASH', 'GENUS', 'HPL', 'LNG', 'LNT', 'MTPL', 'OMEGA', 'PMPL', 'POWERTECH', 'SECURE', 'VISIONTEK', 'OTHER'])
        meter_type = st.radio('Meter Type', ['Single Phase', 'Three Phase'])
        bill_date = st.date_input('Bill Date')
        exception = st.selectbox('Exception', ['NONE','METER NO NOT FOUND','CONSUMER NOT CORPORATE', 'LINE DISCONNECTED', 'METER AT HEIGHT', 'METER BOX DIRTY', 'METER CHANGE', 'METER DEFECTIVE', 'NO DISPLAY', 'NO METER NO CABLE', 'PERMANENT LOCK', 'ROUND OVER', 'TEMPORARY LOCK', 'UNREADABLE READING'])
        reader_name = st.text_input('Reader Name')
        remark = st.text_area('Remark')
        
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            response = {
                'Account Number': st.session_state.meter_details.get('ACCT_ID', ''),
                'Division': st.session_state.meter_details.get('DIV_NAME', ''),
                'Customer Name': st.session_state.meter_details.get('CONSUMER_NAME', ''),
                'Reading KWH': reading_kwh,
                'Reading KVAH': reading_kvah,
                'UC KW': uc_kw,
                'UC KVA': uc_kva,
                'Meter No': meter_no,
                'Meter Make': meter_make,
                'Meter Type': meter_type,
                'Bill Date': bill_date,
                'Exception': exception,
                'Reader Name': reader_name,
                'Remark': remark
            }
            save_response_to_excel(response)
            st.success('Response saved successfully!')
else:
    st.info("Please validate the meter number to proceed.")
