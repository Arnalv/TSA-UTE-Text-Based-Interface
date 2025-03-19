from termcolor import colored
from text_manager import *
WARNING_COLOR = "red"


def yes_or_no(prompt):
    user_answer = prompt_append(prompt).lower()
    other_text.append(f"{prompt}{user_answer}")
    while user_answer != 'y' and user_answer != 'n':
        other_text.append(colored("Please enter 'y' or 'n'!", WARNING_COLOR))
        user_answer = prompt_append(prompt).lower()
        other_text.append(f"{prompt}{user_answer}")
    return user_answer


def integer_validator(prompt, minimum=None, maximum=None):
    while True:
        try:
            user_input = int(prompt_append(prompt))
            other_text.append(f"{prompt}{user_input}")
            if minimum is not None:
                if minimum <= user_input:
                    first_condition = True
                else:
                    first_condition = False
            else:
                first_condition = True

            if maximum is not None:
                if user_input <= maximum:
                    second_condition = True
                else:
                    second_condition = False
            else:
                second_condition = True

            if first_condition and second_condition:
                break
            elif first_condition is False and second_condition is True:
                other_text.append(colored(f"Please make sure the integer is above {minimum}!", WARNING_COLOR))
            else:
                other_text.append(colored(f"Please make sure the integer is in the range of {minimum}-{maximum}.", WARNING_COLOR))
        except TypeError:
            other_text.append(colored(f"Please enter an integer in the range of {minimum}-{maximum}!", WARNING_COLOR))

    return user_input


def string_validator(prompt, correct_string):
    user_response = prompt_append(prompt)
    while user_response != correct_string:
        update_append(colored("Please type the right command!", WARNING_COLOR))
        user_response = prompt_append(prompt)

    return user_response
