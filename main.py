from functions import *

# default settings
starting_work_time = None
break_time = 10

# starting variables

# Formatted like {work_group_name: [priority, {work_name : [time_for_work, break_time]}]}
work_groups = {}
# For Testing
# work_groups = {"A": [5]}
# work_groups = {"A": [5, {"HW": 20, "HW3": 50}], "B": [9, {"HW2": 30}], "C": [10]}

# A variable to store previous works, at the end of the code this will be store in a file for future reference
# Format: [{work, time}, {work, time}]
previously_added_works = []


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
    global previously_added_works
    match user_input:
        case "exit":
            return True
        case "help":
            print_commands()
        case "add_group":
            work_groups = add_group(work_groups)
        case "add_work":
            return_items = add_work(previously_added_works, work_groups, break_time)
            work_groups = return_items["work_groups"]
            previously_added_works = return_items["previously_added_works"]
        case "remove_work":
            work_groups = remove_work(work_groups, break_time)
        case "remove_group":
            work_groups = remove_group(work_groups)
        case "show_schedule":
            work_groups = show_schedule(work_groups, starting_work_time)
        case "change_default_settings":
            default_settings = change_default_settings(break_time=break_time, starting_time=starting_work_time)
            break_time = default_settings["break_time"]
            starting_work_time = default_settings["starting_time"]
        case "change_schedule":
            work_groups = change_schedule(work_groups, starting_work_time)


# For testing later:
# print(work_groups)
# name = input("What is the name of the work? ")
# time = int(input("What is the time in minutes for this work? "))
#
# return_items = add_work(name=name, time_for_work=time, group="A", previous_works=previously_added_works,
#                         work_groups=work_groups, break_time=break_time)
# work_groups = return_items["work_groups"]
# previously_added_works = return_items["previously_added_works"]
#
# print(work_groups)
#
# name = input("What is the name of the work? ")
# time = int(input("What is the time in minutes for this work? "))
#
# return_items = add_work(name=name, time_for_work=time, group="A", previous_works=previously_added_works,
#                         work_groups=work_groups, break_time=break_time)
# work_groups = return_items["work_groups"]
# previously_added_works = return_items["previously_added_works"]
#
# print(work_groups)


try:
    with open(mode="r", file="./previous_works.txt") as previous_works_file:
        lines = previous_works_file.readlines()
        for line in lines:
            work_name = line.split(sep=", ")[0]
            time = int(line.split(sep=", ")[1].split(sep="\n")[0])
            previously_added_works.append({work_name, time})
except FileNotFoundError:
    previous_works_file = open(mode="x", file="./previous_works.txt")
    previous_works_file.close()

while True:
    # TODO need to add code on checking for new user
    command = input("Please type 'Help' to see what commands you can use: ").lower()
    if check_user_input(command):
        with open(mode="w", file="./previous_works.txt") as previous_works_file:
            for work in previously_added_works:
                for work_name, time in work.items():
                    previous_works_file.write(f"{work_name}, {time}\n")
        break
