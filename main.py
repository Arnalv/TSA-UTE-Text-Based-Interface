from text_parser import *
import os
from functions import *

APPLICATION_NAME = "AutoSchedule"

# default settings
starting_work_time = None
break_time = 10

# starting variables

# Formatted like {work_group_name: [priority, {work_name : [time_for_work, break_time]}]}
work_groups = {}
# For Testing
# work_groups = {"A": [5]}
# work_groups = {"A": [5, {"HW": [20, 5], "HW3": [50, 5]}], "B": [9, {"HW2": [30, 5]}], "C": [10]}

# A variable to store previous works, at the end of the code this will be store in a file for future reference
# Format: [{work, time}, {work, time}]
previously_added_works = []


def print_commands():
    print("QuickStart:")
    print(f"{APPLICATION_NAME} organizes your daily tasks into various groups with different priorities.")
    print(f"You can add specific works to these groups and {APPLICATION_NAME} will automatically create your schedule.")
    print("To get started use 'add group' to create your first group and 'add work' to add your first work.\n")
    print("Here are a full list of commands with descriptions:\n"
          "'add work' or 'a': Adds a work to a group\n"
          "'add group' or 'ag': Adds a new group\n"
          "'remove work' or 'r': Removes a work from a group depending\n"
          "'remove group' or 'rg': Removes a group\n"
          "'change default settings' or 'ch_d': Changes default settings\n"
          "'change schedule' or 'ch_s': Edits specific break times or work times in the schedule\n"
          "'clear' or 'c': Clears your entire schedule\n"
          "'show schedule' or 's': Shows completed schedule\n"
          "'exit': Exits application")


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
        case "add group":
            work_groups = add_group_parser(work_groups)
        case "ag":
            work_groups = add_group_parser(work_groups)
        case "add work":
            return_items = add_work_parser(previous_works=previously_added_works, break_time=break_time,
                                           work_groups=work_groups)

            work_groups = return_items["work_groups"]
            previously_added_works = return_items["previously_added_works"]
        case "a":
            return_items = add_work_parser(previous_works=previously_added_works, break_time=break_time,
                                           work_groups=work_groups)

            work_groups = return_items["work_groups"]
            previously_added_works = return_items["previously_added_works"]
        case "remove work":
            work_groups = remove_work(work_groups)
        case "r":
            work_groups = remove_work(work_groups)
        case "remove group":
            work_groups = remove_group(work_groups)
        case "rg":
            work_groups = remove_group(work_groups)
        case "show schedule":
            work_groups = show_schedule(work_groups, starting_work_time)
        case "s":
            work_groups = show_schedule(work_groups, starting_work_time)
        case "change default settings":
            default_settings = change_default_settings(break_time=break_time, starting_time=starting_work_time)
            break_time = default_settings["break_time"]
            starting_work_time = default_settings["starting_time"]
        case "ch_d":
            default_settings = change_default_settings(break_time=break_time, starting_time=starting_work_time)
            break_time = default_settings["break_time"]
            starting_work_time = default_settings["starting_time"]
        case "change schedule":
            work_groups = change_schedule(work_groups, starting_work_time)
        case "ch_s":
            work_groups = change_schedule(work_groups, starting_work_time)
        case "clear":
            work_groups = {}    
            print("Schedule has been cleared.")
        case "c":
            work_groups = {}
            print("Schedule has been cleared.")
        case "add_previous_work":
            work_groups = add_previous_work(work_groups=work_groups, previous_works=previously_added_works,
                                            break_time=break_time)
        case "ap":
            work_groups = add_previous_work(work_groups=work_groups, previous_works=previously_added_works,
                                            break_time=break_time)

    print("\n")


try:
    with open(mode="r", file="./output_text_files/previous_works.txt") as previous_works_file:
        lines = previous_works_file.readlines()
        for line in lines:
            work_name = line.split(sep=", ")[0]
            time = int(line.split(sep=", ")[1].split(sep="\n")[0])
            previously_added_works.append({work_name: time})
except FileNotFoundError:
    previous_works_file = open(mode="w", file="./output_text_files/previous_works.txt")
    previous_works_file.close()

if os.path.isfile("./output_text_files/default_settings.txt"):
    if os.path.getsize("./output_text_files/default_settings.txt") != 0:
        with open(mode="r", file="./output_text_files/default_settings.txt") as default_settings_file:
            starting_work_time = default_settings_file.readline().split(": ")[1].split("\n")[0]
            if starting_work_time == 'None':
                starting_work_time = None
            else:
                now = datetime.now()
                starting_work_time = starting_work_time.split()[1].split(":")
                starting_work_time = [int(string) for string in starting_work_time]
                starting_work_time = datetime(year=now.year, month=now.month, day=now.day,
                                              hour=starting_work_time[0], minute=starting_work_time[1])
            break_time = int(default_settings_file.readline().split(": ")[1].split("\n")[0])
else:
    default_settings_file = open(mode="x", file="./output_text_files/default_settings.txt")
    default_settings_file.close()

if os.path.isfile("./output_text_files/work_groups.txt"):
    # Formatted like {work_group_name: [priority, {work_name : [time_for_work, break_time]}]}
    with open(mode="r", file="./output_text_files/work_groups.txt") as work_groups_file:
        if os.path.getsize("./output_text_files/work_groups.txt") != 0:
            work_groups_str = work_groups_file.readline().strip().split(sep="Work Groups: ")[1].split()
            works_str = work_groups_file.readline().strip().split("Corresponding Works: ")[1].split("New Group: ")[1:]

            works_list = []
            for work in works_str:
                work_list = [int(work.split(",")[0])]
                all_works_str = work[3:].split("New Work: ")[1:]
                if all_works_str:
                    all_works_str = [text.split(", ")[:len(text.split(", "))] for text in all_works_str]
                    for single_work_details in all_works_str:
                        if "," in single_work_details[-1]:
                            single_work_details[-1] = single_work_details[-1].split(",")[0]
                        if not len(work_list) > 1:
                            work_list.append({single_work_details[0]: [int(single_work_details[1]),
                                                                       int(single_work_details[2])]})
                        else:
                            work_list[1][single_work_details[0]] = [int(single_work_details[1]),
                                                                    int(single_work_details[2])]
                works_list.append(work_list)

            count = 0
            for work_list in works_list:
                work_groups[work_groups_str[count]] = work_list
                count += 1

            print("Your previously saved schedule.")
            work_groups = show_schedule(work_groups, starting_work_time, False)

else:
    work_groups_file = open(mode="x", file="./output_text_files/work_groups.txt")
    work_groups_file.close()

while True:
    command = input("Please type 'Help' to see what commands you can use: ").lower()
    if check_user_input(command):
        with open(mode="w", file="./output_text_files/default_settings.txt") as default_settings_file:
            default_settings_file.write(f"starting_work_time: {starting_work_time}\n"
                                        f"break_time: {break_time}")
        with open(mode="w", file="./output_text_files/previous_works.txt") as previous_works_file:
            for work in previously_added_works:
                for work_name, time in work.items():
                    previous_works_file.write(f"{work_name}, {time}\n")

        with open(mode="w", file="./output_text_files/work_groups.txt") as work_groups_file:
            if work_groups:
                work_groups_file.write("Work Groups: ")
                for work_group in work_groups:
                    work_groups_file.write(work_group + " ")

                work_groups_file.write("\nCorresponding Works: ")
                for work_group, work_group_details in work_groups.items():
                    if len(work_group_details) != 1:
                        work_groups_file.write(f"New Group: {work_group_details[0]}, ")
                        for work, work_details in work_group_details[1].items():
                            work_groups_file.write(f"New Work: {work}, {work_details[0]}, {work_details[1]}, ")
                    else:
                        work_groups_file.write(f"New Group: {work_group_details[0]}, none, ")

        if starting_work_time is None:
            starting_work_time = datetime.now()

        with open(mode="w", file="./output_text_files/schedule.txt") as schedule_file:
            write_lines = ["Here is your schedule for today.\n"]

            # Calls the update schedule function which organizes the works by their priority in the
            # format of [{work: time}, {work: time}].
            # Checks if calling it is needed
            outputs = organize_by_priority(work_groups=work_groups)
            work_groups = outputs["work_groups"]
            priority_ordered_schedule = outputs["priority_ordered_work"]

            # Prints the schedule in 'Work_Name: Start-Time -- End-Time' format
            for work_name, work_details in priority_ordered_schedule.items():
                ending_time = starting_work_time + timedelta(minutes=work_details[0])

                starting_time_str = format_time(starting_work_time)
                ending_time_str = format_time(ending_time)

                # Prints out the time for the work
                write_lines.append(f"{work_name}: {starting_time_str} -- {ending_time_str}\n")
                starting_work_time = ending_time

                # Blank line for spacing
                write_lines.append("\n")

                ending_time = starting_work_time + timedelta(minutes=work_details[1])

                starting_time_str = format_time(starting_work_time)
                ending_time_str = format_time(ending_time)

                # Prints out the time for the work
                write_lines.append(f"BREAK TIME: {starting_time_str} -- {ending_time_str}\n")
                starting_work_time = ending_time

                # Blank line for spacing
                write_lines.append("\n")

            schedule_file.writelines(write_lines)
        break

# Hello world2