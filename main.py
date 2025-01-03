from functions import *

# default settings
starting_work_time = None
break_time = 10

# starting variables

# Formatted like {work_group_name: [priority, {work_name : time_for_work}]}
# work_groups = {}
# For Testing
work_groups = {"A": [5, {"HW": 20}], "B": [9, {"HW2": 30}], "C": [10]}

# Schedule Variable that contains the schedule with the break times (Allows the user to edit specific break times)
schedule = []


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
          "ch_s\n"
          "Allows you to edit specific break times or work times in the schedule (please remember that adding too "
          "much time may cause the total work time to increase)\n\n"
          "s\n"
          "Shows completed schedule.\n\n"
          "exit\n"
          "Exits application.")


def check_user_input(user_input):
    global work_groups
    global break_time
    global starting_work_time
    global schedule
    match user_input:
        case "exit":
            return True
        case "help":
            print_commands()
        case "ag":
            work_groups = add_group(work_groups)
        case "a":
            return_items = add_work(work_groups, schedule, break_time)
            work_groups = return_items["work_groups"]
            schedule = return_items["updated_schedule"]
        case "rw":
            return_items = remove_work(work_groups, schedule, break_time)
            work_groups = return_items["work_groups"]
            schedule = return_items["updated_schedule"]
        case "rg":
            work_groups = remove_group(work_groups)
        case "s":
            return_items = show_schedule(work_groups, break_time, schedule, starting_work_time)
            work_groups = return_items["work_groups"]
            schedule = return_items["schedule"]
        case "ch_d":
            default_settings = change_default_settings(break_time=break_time, starting_time=starting_work_time)
            break_time = default_settings["break_time"]
            starting_work_time = default_settings["starting_time"]
        case "ch_s":
            return_items = change_schedule(work_groups, schedule, break_time, starting_work_time)
            work_groups = return_items["work_groups"]
            schedule = return_items["original_schedule"]


while True:
    # TODO need to add code on checking for new user
    command = input("Please type 'Help' to see what commands you can use: ").lower()
    if check_user_input(command):
        # store_information()
        break
