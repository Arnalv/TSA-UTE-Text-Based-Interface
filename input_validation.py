

def yes_or_no(prompt):
    user_answer = input(prompt).lower()
    while user_answer != 'y' and user_answer != 'n':
        print("Please enter 'y' or 'n'!")
        user_answer = input(prompt).lower()

    return user_answer


def integer_validator(prompt, minimum, maximum):
    while True:
        try:
            user_input = int(input(prompt))
            if minimum <= user_input <= maximum:
                break
            else:
                print(f"Please make sure the integer is in the range of {minimum}-{maximum}.")
        except TypeError:
            print(f"Please enter an integer in the range of {minimum}-{maximum}!")

    return user_input
