from functions import *

# default settings
starting_work_time = None
ending_work_time = None
break_time = 10

# starting variables

# Formatted like {work_group_name: [priority, {work_name : time_for_work}]}
work_groups = {}
# For Testing
# work_groups = {"A": [5, {"HW": 20}], "B": [9, {"HW2": 30}]}


def print_commands():
    # TODO figure out how to clear the screen (ask Arnav)
    print("Here are a list of commands with descriptions:\n"
          "a\n"
          "Adds work to specific group depending on inputs\n\n"
          "r\n"
          "Removes a work from a specific group depending on the inputs\n\n"
          "rw\n"
          "Removes a work from a work group.\n\n"
          "rg\n"
          "Removes a work group.\n\n"
          "ag\n"
          "Adds a new group for work\n\n"
          "ch_d\n"
          "Changes default settings such as break time depending on the inputs\n\n"
          "ch_b\n"
          "Allows you to edit specific break times or work times (please remember that adding too much time may cause "
          "the total work time to increase)\n\n"
          "s\n"
          "Shows completed schedule.\n\n"
          "exit\n"
          "Exits application.")


def check_user_input(user_input):
    global work_groups
    match user_input:
        case "exit":
            return True
        case "help":
            print_commands()
        case "ag":
            work_groups = add_group(work_groups)
        case "a":
            add_work(work_groups)
        case "rw":
            work_groups = remove_work(work_groups)
        case "rg":
            work_groups = remove_group(work_groups)
        case "s":
            work_groups = show_schedule(work_groups, break_time)


while True:
    # TODO need to add code on checking for new user
    command = input("Please type 'Help' to see what commands you can use: ").lower()
    if check_user_input(command):
        # store_information()
        break
