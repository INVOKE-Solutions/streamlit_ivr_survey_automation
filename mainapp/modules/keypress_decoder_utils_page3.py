import re
import streamlit as st
import json

import re

def parse_text_to_json(text_content):
    """
    Parses structured text containing survey questions and answers into a JSON-like dictionary.
    Adjusts FlowNo to start from 1 for each question's first answer and increments sequentially.
    """
    data = {}
    current_question = None
    global_flow_no = 2  # Start FlowNo from 2 as specified

    # Regular expressions for identifying questions and answers
    question_re = re.compile(r'^(\d+[a-zA-Z]?)\.\s*(.*)')  # Matches question numbers with optional alpha suffix
    answer_re = re.compile(r'^\s*[-(]\s*(.*)')  # Matches answers with leading dash or parenthesis

    for line in text_content.splitlines():
        question_match = question_re.match(line)
        answer_match = answer_re.match(line)

        if question_match:
            # New question found
            q_number, q_text = question_match.groups()
            current_question = f"Q{q_number}"  # Handles identifiers like 'Q5', 'Q5a', etc.
            data[current_question] = {"question": q_text, "answers": {}}
            # Increment global_flow_no only for questions
            global_flow_no += 1
        elif answer_match and current_question:
            # Answer found for the current question
            answer_text = answer_match.groups()[0].strip('() ')
            answer_flow_no = len(data[current_question]["answers"]) + 1  # FlowNo starts at 1 for each question's answers
            flow_no_key = f"FlowNo_{global_flow_no - 1}={answer_flow_no}"  # Use global_flow_no - 1 to align numbering
            data[current_question]["answers"][flow_no_key] = answer_text

    return data

def custom_sort(col):
    # Improved regex to capture question and flow numbers accurately
    match = re.match(r"FlowNo_(\d+)=*(\d*)", col)
    if match:
        question_num = int(match.group(1))  # Question number
        flow_no = int(match.group(2)) if match.group(2) else 0  # Flow number, default to 0 if not present
        return (question_num, flow_no) 
    else:
        return (float('inf'), 0)

def classify_income(income):
    if income == 'RM4,850 & below':
        return 'B40'
    elif income == 'RM4,851 to RM10,960':
        return 'M40'
    elif income in ['RM15,040 & above', 'RM10,961 to RM15,039']:
        return 'T20'
import json

def process_file_content(uploaded_file):
    """Process the content of the uploaded file."""
    try:
        if uploaded_file and uploaded_file.type == "application/json":
            # Handle JSON file
            flow_no_mappings = json.loads(uploaded_file.getvalue().decode("utf-8"))
        else:
            # Handle plain text file
            flow_no_mappings = parse_text_to_json(uploaded_file.getvalue().decode("utf-8"))
        return flow_no_mappings, "Questions and answers parsed successfully.✨", None
    except Exception as e:
        return None, None, f"Error processing file: {e}"

def flatten_json_structure(flow_no_mappings):
    """Flatten the JSON structure to simplify the mapping access."""
    if not flow_no_mappings:
        return {}
    # Flattening the JSON structure to a single dictionary with FlowNo as keys
    return {k: v for question in flow_no_mappings.values() for k, v in question["answers"].items()}

def drop_duplicates_from_dataframe(df):
    """
    Drops duplicate rows from the DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame from which duplicates will be removed.

    Returns:
    - pd.DataFrame: A DataFrame with duplicates removed.
    """
    return df.drop_duplicates()