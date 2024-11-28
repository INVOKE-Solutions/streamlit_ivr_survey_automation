import re
import json

import re

import re

def parse_text_to_json(text_content):
    """
    Parses structured text containing survey questions and answers into a JSON-like dictionary.
    Adjusts question numbering to start from Q1 and adds sub-identifiers (a, b, c, etc.) only for repeated questions.
    Supports both Malay and English formats.
    """
    data = {}
    question_count = 1  # Initialize question counter for sequential numbering
    current_question = None
    flow_start = False  # Flag to start detection from Call Flow 2 onwards

    # Dictionary to track the occurrences of each question to determine if it’s repeated
    sub_identifier_map = {}

    # Regular expressions for identifying questions and answers
    question_re = re.compile(r'^\s*(Soalan|Question)\s+([^,]+)\s*,\s*(.*?)\s*Call\s+flow\s+(\d+)', re.IGNORECASE)
    answer_re = re.compile(r'^\s*(Tekan|Press)\s+(\d+)\s+(untuk|for)\s+([^\.]*)', re.IGNORECASE)

    for line in text_content.splitlines():
        line = line.strip()  # Clean up any leading/trailing whitespace
        question_match = question_re.match(line)
        answer_match = answer_re.match(line)

        if question_match:
            flow_no = int(question_match.group(4))  # Extract Call Flow number
            if flow_no >= 2:
                flow_start = True  # Enable question and answer parsing from Call Flow 2 onwards

            if flow_start:
                identifier, q_text, _ = question_match.groups()[1:]
                identifier = identifier.strip()  # Normalize the key for consistency

                # Check if this question is repeated
                if identifier in sub_identifier_map:
                    # If repeated, increment sub-identifier
                    sub_identifier_map[identifier] += 1
                    sub_identifier = chr(ord('a') + sub_identifier_map[identifier] - 1)
                    current_question = f"Q{question_count - 1}{sub_identifier}"  # Use current question count with sub-identifier
                else:
                    # First time seeing this question
                    sub_identifier_map[identifier] = 1

                    # Determine if this question needs a sub-identifier
                    if text_content.count(f"{identifier}") > 1:
                        current_question = f"Q{question_count}a"
                    else:
                        current_question = f"Q{question_count}"

                    question_count += 1  # Increment for the next main question

                data[current_question] = {"question": q_text.strip(), "answers": {}}

        elif answer_match and current_question and flow_start:
            keypress = answer_match.group(2)  # Extract keypress (Group 2)
            answer_text = answer_match.group(4)  # Extract answer text (Group 4)
            flow_no_key = f"FlowNo_{flow_no}={keypress}"
            data[current_question]["answers"][flow_no_key] = answer_text.strip()

    return data



def custom_sort(col):
    # Improved regex to capture question and flow numbers accurately
    match = re.search(r"FlowNo_(\d+)=(\d*)", col) 
    if match:
        question_num = int(match.group(1)) # Question Number
        flow_no = int(match.group(2)) if match.group(2) else 0 # Flow number, default to 0 if not present
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
    """Flatten the  JSON structure to simplify the mapping access."""
    if not flow_no_mappings:
        return {}
    # Flattening the JSON structure to a single dictionary with FlowNo keys
    return {k: v for question in flow_no_mappings.values() for k, v in question["answers"].items()}

def drop_duplicates_from_dataframe(df):
    """
    Drops duplicated rows from the DataFrame.
    
    Parameters: The DataFrame from which duplicated will be removed.
    
    Returns:
    - pd.DataFrame: A DataFrame with duplicates removed.
    """
    return df.drop_duplicates()