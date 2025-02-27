from termcolor import cprint

WARNING_COLOR = "red"


def yes_or_no(prompt):
    user_answer = input(prompt).lower()
    while user_answer != 'y' and user_answer != 'n':
        cprint("Please enter 'y' or 'n'!", WARNING_COLOR)
        user_answer = input(prompt).lower()

    return user_answer


def integer_validator(prompt, minimum=None, maximum=None):
    while True:
        try:
            user_input = int(input(prompt))

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
                cprint(f"Please make sure the integer is above {minimum}!")
            else:
                cprint(f"Please make sure the integer is in the range of {minimum}-{maximum}.", WARNING_COLOR)
        except TypeError:
            cprint(f"Please enter an integer in the range of {minimum}-{maximum}!", WARNING_COLOR)

    return user_input
