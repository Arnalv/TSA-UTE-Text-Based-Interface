from text_parser import *
from functions import *
from termcolor import colored, cprint
from AI import ai_parsing

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

# Colors
command_color = "green"
SUCCESS_COLOR = "green"

# Text Speed
normal_speed = 0.01
tutorial_speed = 0.03
long_text_speed = 0.005


def print_commands():
    update_append("QuickStart:")
    update_append(f"{APPLICATION_NAME} organizes your daily tasks into various "
                  f"groups with different priorities.")
    update_append(f"{colored("Please use the command '", INSTRUCTIONS_COLOR)}"
                  f"{colored("starter guide", command_color)}"
                  f"{colored("' to run through the tutorial.", INSTRUCTIONS_COLOR)}")
    update_append(f"You can add specific works to these groups and {APPLICATION_NAME} will automatically "
                  f"create your schedule.")
    update_append(f"To get started use '{colored("add group", command_color)}' to create your first group.")
    update_append(f"Then use '{colored("add group", command_color)}' to add your first work.")
    update_append(f"Here are a full list of commands with descriptions:")
    update_append(f"'{colored("add work", command_color)}' or '{colored("a", command_color)}': "
                  f"Adds a work to a group")
    update_append(f"'{colored("add previous work", command_color)}' or '{colored("ap", command_color)}': "
                  f"Allows you to add a previously added work")
    update_append(f"'{colored("add group", command_color)}' or '{colored("ag", command_color)}': "
                  f"Adds a new group")
    update_append(f"'{colored("remove work", command_color)}' or '{colored("r", command_color)}': "
                  f"Removes a work from a group")
    update_append(f"'{colored("remove group", command_color)}' or '{colored("rg", command_color)}': "
                  f"Removes a group")
    update_append(f"'{colored("change default settings", command_color)}' or "
                  f"'{colored("ch_d", command_color)}': Changes default settings")
    update_append(f"'{colored("change schedule", command_color)}' or '{colored("ch_s", command_color)}': "
                  f"Edits specific break times or work times in the schedule")
    update_append(f"'{colored("clear", command_color)}' or '{colored("c", command_color)}': "
                  f"Clears your entire schedule")
    update_append(f"'{colored("exit", command_color)}': Exits application")


def check_user_input(user_input):
    global work_groups
    global break_time
    global starting_work_time
    global previously_added_works

    return_items = make_dictionary_with_break_times(work_groups=work_groups)
    dictionary_with_break_times = return_items["dictionary_including_break_times"]
    work_groups = return_items["work_groups"]
    command_dict = ai_parsing(prompt=user_input, work_groups=work_groups, previous_works_list=previously_added_works,
                              dictionary_with_break_times=dictionary_with_break_times)
    if command_dict:
        match command_dict["command"]:
            case "exit":
                return True
            case "help":
                change_text_speed(long_text_speed)
                print_commands()
                change_text_speed(normal_speed)
            case "add group":
                work_groups = add_group(work_groups, command_dict)
            case "ag":
                work_groups = add_group(work_groups, command_dict)
            case "add work":
                return_items = add_work_parser(previous_works=previously_added_works, break_time=break_time,
                                               work_groups=work_groups, user_inputs=command_dict)

                work_groups = return_items["work_groups"]
                previously_added_works = return_items["previously_added_works"]
            case "a":
                return_items = add_work_parser(previous_works=previously_added_works, break_time=break_time,
                                               work_groups=work_groups, user_inputs=command_dict)

                work_groups = return_items["work_groups"]
                previously_added_works = return_items["previously_added_works"]
            case "remove work":
                work_groups = remove_work(work_groups, command_dict)
            case "r":
                work_groups = remove_work(work_groups, command_dict)
            case "remove group":
                work_groups = remove_group(work_groups, command_dict)
            case "rg":
                work_groups = remove_group(work_groups, command_dict)
            case "change default settings":
                default_settings = change_default_settings(break_time=break_time, starting_time=starting_work_time,
                                                           user_inputs=command_dict)
                break_time = default_settings["break_time"]
                starting_work_time = default_settings["starting_time"]
            case "ch_d":
                default_settings = change_default_settings(break_time=break_time, starting_time=starting_work_time,
                                                           user_inputs=command_dict)
                break_time = default_settings["break_time"]
                starting_work_time = default_settings["starting_time"]
            case "change schedule":
                work_groups = change_schedule(work_groups, command_dict, starting_work_time)
            case "ch_s":
                work_groups = change_schedule(work_groups, command_dict, starting_work_time)
            case "clear":
                work_groups = {}
                cprint("Schedule has been cleared.", SUCCESS_COLOR)
            case "c":
                work_groups = {}
                cprint("Schedule has been cleared.", SUCCESS_COLOR)
            case "add previous work":
                work_groups = add_previous_work(work_groups=work_groups, previous_works=previously_added_works,
                                                break_time=break_time, user_inputs=command_dict)
            case "ap":
                work_groups = add_previous_work(work_groups=work_groups, previous_works=previously_added_works,
                                                break_time=break_time, user_inputs=command_dict)
            case "starter guide":
                starter_guide()
    else:
        update_append(colored(text="I am unable to identify your intentions. Please be a bit more clear.",
                              color=INSTRUCTIONS_COLOR))
        update_append(colored(text="You can type 'help' to see what functionality I have.",
                              color=INSTRUCTIONS_COLOR))

    other_text.append("")
    other_text.append("")


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

            schedule_text.append("Your previously saved schedule.")
            work_groups = show_schedule(work_groups, starting_work_time, False)

else:
    work_groups_file = open(mode="x", file="./output_text_files/work_groups.txt")
    work_groups_file.close()


def starter_guide():
    global command

    change_text_speed(tutorial_speed)
    update_append("I have detected that this is your first time here!")
    update_append(f"Welcome to {APPLICATION_NAME}!")
    update_append("")
    update_append(f"First try to create a work group.")
    update_append("Groups are an umbrella to your works. Ex: Group: Math, would have Work: Math Homework")
    command = string_validator(
        f"Please type '{colored("add group", command_color)}' to add a group: ",
        "add group")
    other_text.append(f"Please type 'Help' to see what commands you can use: {command}")
    command = command.lower().strip()
    check_user_input(command)

    update_append(colored("Congrats!", SUCCESS_COLOR))
    command = string_validator(
        f"Please type '{colored("add work", command_color)}' to add a work: ",
        "add work")
    command = command.lower().strip()
    check_user_input(command)

    update_append(colored("Congrats, you have created your work!", INSTRUCTIONS_COLOR))
    update_append(f"Since this is a tutorial, we have made you input specific inputs to get a feel for the interface.")
    update_append(colored(f"You can have more diversified inputs, but be sure to make sure you have "
                          f"all the information provided in the input.", INSTRUCTIONS_COLOR))
    update_append(f"You can change the starting time by using '{colored("change default settings", command_color)}'.")
    update_append("The default is just the current time.")
    update_append(f"If you want to use the starter guide again, please type "
                  f"'{colored("starter guide", command_color)}'.")
    update_append(colored("Look at your schedule to the right!", INSTRUCTIONS_COLOR))


while True:
    work_groups = show_schedule(work_groups=work_groups, starting_time=starting_work_time)
    show_text()
    if not work_groups and not previously_added_works:
        check_user_input("starter guide")
        work_groups = show_schedule(work_groups=work_groups, starting_time=starting_work_time)
        show_text()
    command = prompt_append("Please type 'Help' to see what commands you can use: ")
    command = command.lower().strip()

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
