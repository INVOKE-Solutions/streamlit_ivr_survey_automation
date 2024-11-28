import streamlit as st
from PIL import Image
from datetime import datetime
import pandas as pd
from modules.questionnaire_utils_page2 import parse_text_to_json as parse_text_to_json_qa, rename_columns
from modules.keypress_decoder_utils_page3 import parse_text_to_json as parse_text_to_json_kd, custom_sort, classify_income, drop_duplicates_from_dataframe

# Configure the default settings of the page.
icon = Image.open('./images/invoke_logo.png')
st.set_page_config(
    page_title='IVR Data Cleaner 🧮',
    layout="wide",
    page_icon=icon,
    initial_sidebar_state="expanded"
)

def set_dark_mode_css():
    dark_mode_css = """
    <style>
        html, body, [class*="View"] {
            color: #ffffff;  /* Text Color */
            background-color: #111111;  /* Background Color */
        }
        .stTextInput > div > div > input, .stFileUploader > div > div > button {
            color: #ffffff;
            background-color: #111111;
        }
        .stCheckbox > label, .stButton > button {
            color: #ffffff;
        }
        /* Add other widget-specific styles here */
    </style>
    """
    st.markdown(dark_mode_css, unsafe_allow_html=True)

set_dark_mode_css()  # Apply the dark mode CSS

st.title('Questionnaire Definer and Keypress Decoder 🧮')
st.markdown("### Write the script in the text box below.")


# Initialize session state for 'qa_dict' and 'file_parsed' to prevent KeyError
if 'qa_dict' not in st.session_state:
    st.session_state['qa_dict'] = {}
 

# Replace the file uploader with a text area for input
script_input = st.text_area("Write the questions and answers in the correct format in the text area below. :", height=300)

flow_no_mappings = {}
text_parsed = False

# process the input script automatically
    
if script_input:
    # Assume the text area input is parsed here
    flow_no_mappings = parse_text_to_json_kd(script_input)
    parsed_data = parse_text_to_json_qa(script_input)
    text_parsed = True

    # Store the parsed data in session state
    st.session_state['qa_dict'] = parsed_data
    #st.session_state['file_parsed'] = True  # Set file_parsed to True
    
    # Debug information in a dropdown box
    with st.expander("Show FlowNo Mappings"):
        st.write("FlowNo Mappings:", flow_no_mappings)

    if flow_no_mappings:
        st.success("Questions and answers parsed successfully. ✨")
    else:
        st.error("Parsed data is empty. Check input content and parsing logic.")

else:
    st.info("Please upload a file to parse questions and their answers.")

simple_mappings = {k: v for question in flow_no_mappings.values() for k, v in question["answers"].items()}
for q_key, q_data in flow_no_mappings.items():
    for answer_key, answer_value in q_data["answers"].items():
        simple_mappings[answer_key] = answer_value

# Continue with the renaming and processing logic if file_parsed is True
# Section for manual and auto-filled renaming
st.markdown("## Rename Columns")

if 'cleaned_data' not in st.session_state:
    st.session_state['cleaned_data'] = pd.DataFrame()

cleaned_data = st.session_state['cleaned_data']
if cleaned_data.empty:
    st.warning("No cleaned data available for renaming.")
else:
    column_names_to_display = [col for col in cleaned_data.columns]  # Placeholder for actual column names
    
    # Count matching between columns and questions
    question_keys = list(st.session_state['qa_dict'].keys())  # ['Q1', 'Q2', ..., 'Q4a', 'Q4b', ...]
    question_count = len(question_keys)
    column_count = len(column_names_to_display)

    # Manual input for renaming columns, with special handling for the first and last columns
    new_column_names = []
    for idx, default_name in enumerate(column_names_to_display):
        if idx == 0:
            # First column reserved for "phonenum"
            default_value = "phonenum"
        elif idx == len(column_names_to_display) - 1:
            # Last column reserved for "Set"
            default_value = "Set"
        elif idx <= question_count: 
            # Adjust question numbering to match correctly
            question_key = question_keys[idx - 1]  # Use correct index for question_keys
            question_identifier = question_key.lstrip('Q')  # Remove the 'Q'
            question_text = st.session_state['qa_dict'].get(question_key, {}).get('question', default_name)
            default_value = f"{question_identifier}. {question_text}" 
        else:
            default_value = default_name

        new_column_names.append(default_value)

    if st.button("Apply New Column Names"):
        updated_df = rename_columns(cleaned_data, new_column_names)
        st.session_state['renamed_data'] = updated_df
        st.write("DataFrame with Renamed Columns:")
        st.dataframe(updated_df.head())

# Keypress Decoder Section
st.markdown("## Keypress Decoder")
if 'renamed_data' not in st.session_state:
    st.session_state['renamed_data'] = pd.DataFrame()

def process_data():
    if 'renamed_data' in st.session_state and not st.session_state['renamed_data'].empty:
        renamed_data = st.session_state['renamed_data']
        
        # Sort columns and update session state
        sorted_columns = sorted(renamed_data.columns, key=custom_sort)
        renamed_data = renamed_data[sorted_columns]
        st.session_state['renamed_data'] = renamed_data

        keypress_mappings = {}
        drop_cols = []
        excluded_flow_nos = {}

        # Iterate through question columns (excluding first and last columns)
        question_columns = renamed_data.columns[1:-1]
        for i, col in enumerate(question_columns, start=1):
            st.subheader(f"Q{i}: {col}")
            
            # Check if the question has [SKIP LOGIC]
            is_skip_logic = "[SKIP LOGIC]" in col

            # Handle skip logic and non-skip logic columns
            if is_skip_logic:
                # Include FlowNo_[number]= (even empty ones)
                unique_values = [
                    val for val in renamed_data[col].unique()
                    if pd.notna(val) and val.strip() and '=' in val  # Include all FlowNos, even 'FlowNo_='
                ]
            else:
                # Normal handling for non-skip logic questions
                unique_values = [
                    val for val in renamed_data[col].unique()
                    if pd.notna(val) and val.strip() and '=' in val 
                    and val.split('=')[1].strip()  # Ensure there's something after '='
                ]

            # Filter the dataframe to retain valid FlowNo rows
            renamed_data = renamed_data[renamed_data[col].isin(unique_values)]

            # Replace FlowNo_[number]= (with no value) with blank for skip logic
            if is_skip_logic:
                renamed_data[col] = renamed_data[col].replace(to_replace=r'FlowNo_\d+=$', value='', regex=True)

            # Sort remaining valid values
            sorted_unique_values = sorted(
                unique_values,
                key=lambda x: int(x.split('=')[1]) if '=' in x and x.split('=')[1].isdigit() else float('inf')
            )

            if st.checkbox(f"Drop entire Question {i}", key=f"exclude_{col}"):
                drop_cols.append(col)
                continue

            ### Decoder ###
            all_mappings = {}
            excluded_flow_nos[col] = []

            for idx, val in enumerate(sorted_unique_values):
                if pd.notna(val):
                    autofill_value = simple_mappings.get(val, "")
                    unique_key = f"{col}_{val}_{idx}"
                    if st.checkbox(f"Drop '{val}'", key=f"exclude_{unique_key}"):
                        excluded_flow_nos[col].append(val)
                        continue

                    readable_val = st.text_input(f"Rename '{val}' to:", value=autofill_value, key=unique_key)
                    if readable_val:
                        all_mappings[val] = readable_val

            if all_mappings:
                keypress_mappings[col] = all_mappings

        # Explicitly drop the columns listed in drop_cols from the DataFrame
        if drop_cols:
            st.session_state['renamed_data'] = renamed_data.drop(columns=drop_cols)
                
        if st.button("Decode Keypresses"):
            if drop_cols:
                renamed_data.drop(columns=drop_cols, inplace=True)

            for col, col_mappings in keypress_mappings.items():
                if col in renamed_data.columns:
                    renamed_data[col] = renamed_data[col].map(col_mappings).fillna(renamed_data[col])
                    
                    for val_to_exclude in excluded_flow_nos.get(col, []):
                        renamed_data = renamed_data[renamed_data[col] != val_to_exclude]

            if 'IncomeRange' in renamed_data.columns:
                income_group = renamed_data['IncomeRange'].apply(classify_income)
                income_range_index = renamed_data.columns.get_loc('IncomeRange')
                renamed_data.insert(income_range_index + 1, 'IncomeGroup', income_group)

            renamed_data = drop_duplicates_from_dataframe(renamed_data)
            st.session_state['renamed_data'] = renamed_data
            st.markdown("### Decoded Data")
            st.write("Preview of Decoded Data:")
            st.dataframe(renamed_data)


            today = datetime.now()
            st.write(f'IVR count by Set as of {today.strftime("%d-%m-%Y").replace("-0", "-")}')
            st.write(renamed_data['Set'].value_counts())

            renamed_data.dropna(inplace=True)
            st.session_state['renamed_data'] = renamed_data
            st.write(f'No. of rows after dropping nulls: {len(renamed_data)} rows')
            st.write(f'Preview of Total of Null Values per Column:')
            st.write(renamed_data.isnull().sum())

            st.markdown("### Sanity check for values in each column")
            
            # Initialize session state to track column checks if not already present
            if 'column_checks' not in st.session_state:
                st.session_state['column_checks'] = {}

            # Function to run sanity checks
            def run_sanity_check(index, col, data):
                st.write(f"{index}: {col}")
                value_counts = data[col].value_counts(normalize=True, dropna=False)
                st.write(value_counts)

            # Iterate through the columns with sequential numbering
            for index, col in enumerate(renamed_data.columns, start=0):
                if col != 'phonenum':
                    run_sanity_check(index, col, renamed_data)
                    # Update session state for the checked column
                    st.session_state['column_checks'][col] = True

            formatted_date = datetime.now().strftime("%Y%m%d")
            st.session_state['output_filename'] = f'IVR_Decoded_Data_v{formatted_date}.csv'
            
            def update_output_filename():
                st.session_state['output_filename'] = st.session_state['output_filename_input'] + '.csv' if not st.session_state['output_filename_input'].lower().endswith('.csv') else st.session_state['output_filename_input']

            st.text_input("Edit the filename for download", value=st.session_state['output_filename'], key='output_filename_input', on_change=update_output_filename)
            data_as_csv = renamed_data.to_csv(index=False).encode('utf-8')
            st.download_button("Download Decoded Data as CSV", data=data_as_csv, file_name=st.session_state['output_filename'], mime='text/csv')
    else:
        st.error("No renamed data found. Please go back to the previous step and rename your data first.")

if __name__ == "__main__":
    process_data()
