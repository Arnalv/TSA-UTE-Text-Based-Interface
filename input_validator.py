
# Function for validating and asking the user again to enter an integer
def integer_validator(prompt, minimum=None, maximum=None):
    integer = None
    number = 0
    while number != 2:
        try:
            # Resets this everytime the user does a mistake in entering number
            number = 0

            # Asks user to enter an integer
            integer = int(input(prompt))

            # Checks if there is a minimum requirement
            if minimum is not None:
                # Checks if the integer meets the minimum requirement
                if integer >= minimum:
                    number += 1
                else:
                    print("The integer entered is lower then the available options.")
            # Adds 1 to 'number' to state one condition has been met
            else:
                number += 1

            # Checks if there is a maximum requirement
            if maximum is not None:
                # Checks if the integer meets the maximum requirement
                if integer <= maximum:
                    number += 1
                else:
                    print("The integer entered is higher then the available options.")
            # Adds 1 to 'number' to state one condition has been met
            else:
                number += 1

        except TypeError:
            print("Please enter an integer.")
    return integer


# Checks if the user entered the string they wanted to enter.
def name_checker(prompt, question_subject):
    name = input(prompt)
    question = input(f"Confirm, {question_subject} : {name} (y/n):").lower()
    while True:
        if question != "n" and question != "y":
            print("Please enter 'y' or 'n'!")
            question = input(f"Confirm, {question_subject} : {name} (y/n):").lower()
        else:
            break
    if question == "n":
        name_checker(prompt, question_subject)
    if question == "y":
        return name
