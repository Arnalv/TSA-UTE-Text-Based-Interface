from google import genai
from dotenv import load_dotenv
import os
import json


def ai_parsing(prompt, work_groups, previous_works_list, dictionary_with_break_times):
    work_groups_text = json.dumps(work_groups)
    dictionary_with_break_times_text = json.dumps(dictionary_with_break_times)
    previous_works_list_text = "[" + ", ".join(map(str, previous_works_list)) + "]"
    ai_prompt = f"""
    You are an intelligent assistant designed to parse user input and determine their intent within a scheduling system.
    Your task is to identify the purpose behind the user's message and extract the necessary inputs based on predefined
    commands.
    
    If you cannot determine the user's intent, return:
    False
    If you can determine the user's intent, return a structured JSON object with the required inputs.
    
    Command Breakdown & Expected Outputs
    Help:
    Trigger Words: "Help", "help"
    Purpose: Gives a list of usable commands to the user
    Response:
    {{
      "command": "help",
      "inputs_needed": "none"
    }}
    
    Starter Guide:
    
    Trigger Words: "starter guide"
    Purpose: Runs through the tutorial.
    Response:
    {{
      "command": "starter guide",
      "inputs_needed": "none"
    }}
    
    Add Work (a):
    
    Trigger Words: "add work", "a"
    Inputs Needed: group_name, work_name, time_of_work
    Response:
    {{
      "command": "add work",
      "inputs_needed": {{"group_name": "string_value" or "none",
                        "work_name": "string_value" or "none",
                        "time_of_work": "integer" or "none"}}
    }}
    
    Add Previous Work (ap):
    
    Trigger Words: "add previous work", "ap"
    Action: Identify the previously added work's index in this list (previous works) {previous_works_list_text}. You can
    do this by first finding the work name given by the user in the list and then find the position of the
    work in the list. 
    Example: 
    [{{"work1": "time"}}, {{"work2": "time2"}}] 
    user input: "I want to add the previous work work1 in the hello1 group."
    response:
    {{
      "command": "add previous work",
      "inputs_needed": {{"index_number": 0 (the first dictionary in the list contains "work1"),
                         "work_name": work1,
                         "group_name": hello1}}
    }}
    If found, return:
    {{
      "command": "add previous work",
      "inputs_needed": {{"index_number": "integer",
                         "work_name": "work_name",
                         "group_name": "none"}}
    }}
    Example: 
    If unable identify all three return:
    {{
      "command": "add previous work",
      "inputs_needed": {{"index_number": "none",
                         "work_name": "none",
                         "group_name": "none"}}
    }}
    
    Add Group (ag):
    
    Trigger Words: "add group", "ag"
    Inputs Needed: group_name, priority_number (1-10)
    Response:
    {{
      "command": "add group",
      "inputs_needed": {{"group_name": string,
                        "priority_number": integer}}
    }}
    
    Remove Work (r):
    
    Trigger Words: "remove work", "r"
    Action: Identify the group_name and work_name from this dictionary (work_groups_dictionary) {work_groups_text}.
    If found, return:
    {{
      "command": "remove work",
      "inputs_needed": {{"removing_work": ["group_name", "work_name"]}}
    }}
    else if unable to identify group that needs to be removed
    {{
      "command": "remove work",
      "inputs_needed": {{"removing_work": "none"}}
    }}
    
    Remove Group (rg):
    
    Trigger Words: "remove group", "rg"
    Inputs Needed: group_name
    Response:
    {{
      "command": "remove group",
      "inputs_needed": {{"group_name": "group_name"}}
    }}
    
    Change Default Settings (ch_d):
    Trigger Words: "change default settings", "ch_d"
    Response:
    {{
      "command": "change default settings",
      "inputs_needed": {{"change_option": integer,
                         "change_value": integer or military time depending on change_option}}
    }}
    Extra Instructions: 
    There are two default settings the user can change. They are break_time and start_time. If you can't specify if the
    user wants to change break_time or start_time, return 'none' for both change_option and change_value.
    
    If the user wants to change break_time, return the value of change_option to be 1 and the value of change_option to
    be an integer representing the time in minutes the user wants to change the duration of the break times.
    
    If the user want to change start_time, return the value of change_option to be 2 and the value of change_option to
    be an string that represents time in military time (ex: 24:40 equals 12:40 pm) that represents when the start time
    is going to be. If the user wants to change the time to the current time return a string containing 'ct' instead.
    
    Important: If the user doesn't specify the change_value value, make the change_value equal to 'none'.
    
    Change Schedule (ch_s):
    Trigger Words: "change schedule", "ch_s"
    Extra Instructions: Using this dictionary {dictionary_with_break_times_text} which is organized like 
    {{work: time, break1: time, work: time, break2: time}}, you should identify which one the user wants to change.
    After you identified which value the user wants to change in the dictionary, you must return the position of the key
    in the dictionary. Ex: if the user wanted to change break1, the position of the key would be 2. This is because the 
    break1 value is the second key in the dictionary. 
    
    You will also try to find a value that is an integer that is given in minutes that represents the change_value.
    Return 'none' to any values you are unable to find.
    
    Response:
    {{
      "command": "change schedule",
      "inputs_needed": {{"position": integer,
                         "change_value": integer}}
    }}
    
    clear Schedule (c):
    Trigger Words: "clear", "c"
    Response:
    {{
      "command": "clear",
      "inputs_needed": "none"
    }}
    
    Exit Application:
    Trigger Words: "exit"
    Response:
    {{
      "command": "exit",
      "inputs_needed": "none"
    }}
    
    Additional Instructions
    Always return the appropriate JSON format based on the identified command.
    If the command is unclear return False without additional explanations.
    Important:
        If some of the inputs needed for the command are unclear, return "none" for the input value.
        This is a example for the add work command. Since the group is not provided, it is 'none'.
        Ex: if user inputs: playground 30 minutes
        Output: {{
        "command": "add work".
        "inputs_needed": {{
            "group_name": 'none',
            "work_name": playground,
            "time_for_work": 30
            }}
        }}
    When identifying a previously added work, match it against previously_added_works_list.
    When identifying work for removal, locate it in work_groups.
    If the user names a work or a group in the process of creating it, make sure the name doesn't have 
    leading or ending spaces. Ex: user_input = " work_name ", interpret it as "work_name"
    This is how the variables will be formated.
    work_groups = {{"work_group_name": [priority, {{"work_name" : time_for_work}}]}}
    priority_list = [{{work, time}}, {{work, time}}]
    Now, parse the following user input and return the structured JSON response:
    "{prompt}"
    """

    load_dotenv()

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=ai_prompt,
    )
    # print(response.text.lstrip("```json").rstrip("```").strip())
    # Convert response.text into a dictionary
    try:
        response_json = json.loads(response.text.lstrip("```json").rstrip("```").strip())
    except json.decoder.JSONDecodeError:
        response_json = {}
    return response_json
