import re

def parse_questions_and_answers(json_data):
    """
    Parses questions and their respective answers from a JSON data structure.

    Parameters:
    - json_data (dict): A dictionary containing questions as keys and their details (question text and answers) as values.

    Returns:
    - dict: A dictionary with question numbers as keys and a sub-dictionary containing the question text and a list of answers.
    """

    question_and_answers = {}
    for q_key, q_value in json_data.items():
        question_text = q_value['question']
        answers = [answer for _, answer in q_value['answer'].items()]
        question_and_answers[q_key] = {'question': question_text, 'answers': answers}
    return question_and_answers

def parse_text_to_json(text_content):
    """
    Converts structured text content into JSON-like dictionary, parsing questions and their answers.
    
    Parameters:
    - text_content (str): Text content containing questions and answers in a structured format.
    
    Returns:
    - dict: A dictionary representing the parsed content with questions as keys and their details
            (question text and answers) as values.
    """
    data = {}
    question_count = 1  # Initialize question counter for sequential numbering
    flow_start = False  # Flag to start detection from Call flow 2 onwards
    sub_identifier_map = {}  # Dictionary to track sub-identifiers for repeated questions

     # Regex for questions (Malay and English)
    question_re = re.compile(r'^\s*(Soalan|Question)\s+([^,]+)\s*,\s*(.*?)\s*Call\s+flow\s+(\d+)', re.IGNORECASE)
    # Regex for answers (Malay and English)
    answer_re = re.compile(r'^\s*(Tekan|Press)\s+(\d+)\s+(untuk|for)\s+(.*)', re.IGNORECASE)

    current_question = ""

    for line in text_content.splitlines():
        line = line.strip()
        if not line:
            continue  # Skip empty lines
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

def rename_columns(df, new_column_names):
    """
    Rename dataframe columns based on a list of new column names.

    Parameters:
    - df (pd.DataFrame): The original DataFrame.
    - new_column_names (list): A list of new column names corresponding to the DataFrame's columns.
    
    Returns:
    - pd.DataFrame: A DataFrame with updated column names.
    """

    mapping = {old: new for old, new in zip(df.columns, new_column_names) if new}
    return df.rename(columns=mapping, inplace=False)
