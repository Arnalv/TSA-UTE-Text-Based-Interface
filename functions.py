from datetime import datetime, timedelta
from input_validation import *
from termcolor import colored
from text_manager import other_text, schedule_text

# General Colors
WARNING_COLOR = "red"
INSTRUCTIONS_COLOR = "cyan"
SUCCESS_COLOR = "green"

# Schedule Printing Colors
WORK_COLOR = "blue"
BREAK_TIME_COLOR = "yellow"

# Work groups color
WORK_GROUPS_COLOR = "magenta"

# Commands Color
command_color = "green"


def show_options(work_groups):
    work_groups_list = []
    group_count = 0
    for group, work_section in work_groups.items():
        work_list = [group]
        group_count += 1
        update_append(f"{group_count}. {colored(group, WORK_GROUPS_COLOR)}")
        work_count = 0
        if len(work_groups[group]) != 1:
            for work, time in work_section[1].items():
                work_count += 1
                update_append(f"    {work_count}. {colored(work, WORK_COLOR)}, time: {time[0]} min")
                work_list.append(work)
        work_groups_list.append(work_list)

    # Returns a work_groups_list formatted [[group_name, work, work],[group_name, work]]
    return work_groups_list


def remove_group(work_groups: dict, removing_group=None) -> dict:
    """
    Removes a group from work groups.
    """

    if work_groups:
        # Checks if the removing group has been provided
        if removing_group is None:
            work_groups_list = show_options(work_groups)
            length = len(work_groups)
            group_access_integer = integer_validator(
                prompt=f"Enter the {colored("number", INSTRUCTIONS_COLOR)} corresponding to the "
                       f"{colored("group", INSTRUCTIONS_COLOR)} you want "
                       f"to remove: ",
                minimum=1,
                maximum=length) - 1
            group_key = work_groups_list[group_access_integer][0]
        else:
            group_key = removing_group
        # Removes the group
        del work_groups[group_key]
        # Prints confirmation message to user
        update_append(f"The group '{colored(group_key, INSTRUCTIONS_COLOR)}' has been removed.")
    else:
        update_append(colored("There are no groups to remove.", WARNING_COLOR))
        update_append(f"{colored("To add a group use '", WARNING_COLOR)}"
                                 f"{colored("add group", command_color)}"
                                 f"{colored("'.", WARNING_COLOR)}")

    # Returns the updated work_groups
    return work_groups


def remove_work(work_groups: dict, removing_work: list = None) -> dict:
    if work_groups:
        if removing_work is None:
            work_groups_list = show_options(work_groups)

            length = len(work_groups_list)
            group_access_integer = integer_validator(
                prompt=f"Enter the colored {colored("number", INSTRUCTIONS_COLOR)} corresponding to the group of the "
                       f"{colored("work", INSTRUCTIONS_COLOR)} you want to remove: ",
                minimum=1,
                maximum=length) - 1

            group_key = work_groups_list[group_access_integer][0]
            if len(work_groups_list[group_access_integer]) == 1:
                update_append(colored("There are no works to remove in this work group.", WARNING_COLOR))
                update_append(f"{colored("If you want to remove the group, use '", WARNING_COLOR)}"
                                         f"{colored("remove group", command_color)}"
                                         f"{colored("'.", WARNING_COLOR)}")
                return work_groups
            else:
                length = len(work_groups_list[group_access_integer]) - 1
                work_access_integer = integer_validator(
                    prompt=f"Enter the {colored("number", INSTRUCTIONS_COLOR)} corresponding to the "
                           f"{colored("work", INSTRUCTIONS_COLOR)} you "
                           f"want to remove: ",
                    minimum=1,
                    maximum=length)

                work_key = work_groups_list[group_access_integer][work_access_integer]
        else:
            group_key = removing_work[0]
            work_key = removing_work[1]

        del work_groups[group_key][1][work_key]
        update_append(f"{colored("The work '", SUCCESS_COLOR)}"
                                 f"{colored(work_key, WORK_COLOR)}"
                                 f"{colored("' has been removed from the group '", SUCCESS_COLOR)}"
                                 f"{colored(group_key, WORK_GROUPS_COLOR)}"
                                 f"{colored("'.", SUCCESS_COLOR)}")
    else:
        update_append(colored(f"There are no works added to remove.", WARNING_COLOR))
        update_append(f"{colored("First add a group using ", WARNING_COLOR)}"
                                 f"{colored("add group", command_color)}"
                                 f"{colored(" and then use ", WARNING_COLOR)}"
                                 f"{colored("add work", command_color)}"
                                 f"{colored(" to add a work to the group.", WARNING_COLOR)}")

    return work_groups


def add_group(original_work_groups, group_name=None, group_priority=None):
    work_groups = original_work_groups

    # Takes input from the user if not provided in the function
    if group_name is None:
        group_name = input(f"Name of {colored("group", INSTRUCTIONS_COLOR)}: ")
        update_append(f"Name of {colored("group", INSTRUCTIONS_COLOR)}: {group_name}")

    if group_priority is None:
        group_priority = integer_validator(
            prompt=f"What {colored("priority level", INSTRUCTIONS_COLOR)} would you like "
                   f"'{colored(group_name, WORK_GROUPS_COLOR)}' to have? (1-10) ",
            minimum=1,
            maximum=10
        )

    # Adds the work group, if it already doesn't exist
    if group_name not in work_groups:
        work_groups[group_name] = [group_priority]
        update_append(f"{colored("Work Group '", SUCCESS_COLOR)}"
                                 f"{colored(group_name, WORK_GROUPS_COLOR)}"
                                 f"{colored("' has been added.", SUCCESS_COLOR)}")
    else:
        update_append(colored("Work group already exists!", WARNING_COLOR))

    return work_groups


def check_duplicate(work_groups: dict, work_name: str) -> bool:
    """
    This function checks if the work_name provided exists within the work_groups.
    Returns True if exists.
    """
    # Formatted like {work_group_name: [priority, {work_name : [time_for_work, break_time]}]}
    for work_group_name, works in work_groups.items():
        if len(works) > 1:
            if work_name in works[1]:
                return True

    return False


def add_work(work_groups, break_time, group=None, name=None, time_for_work=None):

    # Takes input from user if not already provided
    if group is None:
        # Checks if work_groups is empty
        if work_groups != {}:

            # Shows the options to choose a group
            work_group_number = 0
            for key, value in work_groups.items():
                work_group_number += 1
                update_append(f"{work_group_number}. {colored(key, WORK_GROUPS_COLOR)} "
                                         f"(Priority: {value[0]})")
                work_number = 0
                if len(value) > 1:
                    for work, time in value[1].items():
                        work_number += 1
                        update_append(f"    {work_number}. {colored(work, WORK_COLOR)}, "
                                                 f"Time: {time} minutes")

            # Asks user to choose from list of groups shown
            group_number = integer_validator(prompt=f"What work group would you like to add your work to? "
                                                    f"{colored("(type in # that corresponds): ", INSTRUCTIONS_COLOR)}",
                                             minimum=1,
                                             maximum=work_group_number)

            # Takes that number and finds the name of the group
            work_group_number = 0
            for key in work_groups:
                work_group_number += 1
                if work_group_number == group_number:
                    group = key
                    break

        # Tells the user that there are no work groups present, and you can't add a work
        else:
            group = input(f"{colored("Group", INSTRUCTIONS_COLOR)} name: ")
            update_append(f"{colored("Group", INSTRUCTIONS_COLOR)} name: {group}")

    # Checks if the name of the group is not provided and gets an input from the user if not provided
    if name is None:
        # Just asks the user a name due to the user not looking through the previous list
        name = input(f"Please enter {colored("a name", INSTRUCTIONS_COLOR)} for this work: ")
        update_append(f"Please enter {colored("a name", INSTRUCTIONS_COLOR)} for this work: {name}")

    # check if the name provided is duplicate name
    if check_duplicate(work_groups=work_groups, work_name=name):
        update_append(colored("The name of the work already exists.", WARNING_COLOR))
        new_name = input(f"Please enter another {colored("name", INSTRUCTIONS_COLOR)} for the work: ")
        update_append(f"Please enter another {colored("name", INSTRUCTIONS_COLOR)} for the work:  {new_name}")
        while name == new_name:
            update_append(colored("That name was the same one as the previous name.", WARNING_COLOR))
            new_name = input("Please enter a new name: ")
            update_append(f"Please enter a new name: {new_name}")
        name = new_name

    # Asks the user for the time of the work if not already provided
    if time_for_work is None:
        time_for_work = integer_validator(
            prompt=f"About how many {colored("minutes", INSTRUCTIONS_COLOR)} that does this work take?", minimum=1)

    # Checks if a provided group is not in work_groups
    if group not in work_groups:
        group_response = yes_or_no(f"Group not found. Would you like to add a group called "
                                   f"'{colored(group, INSTRUCTIONS_COLOR)}' (y/n)? ")
        if group_response == "y":
            # Adds the group
            work_groups = add_group(group_name=group, original_work_groups=work_groups)
        else:
            update_append(colored("Adding work to schedule not successful. Make sure the work you intended "
                                             "to add has a valid work group (spelled correctly).", WARNING_COLOR))
            update_append(f"{colored("If work group is not created yet, please type '", WARNING_COLOR)}"
                                     f"{colored("add group", command_color)}"
                                     f"{colored("' or '", WARNING_COLOR)}"
                                     f"{colored("ag", command_color)}"
                                     f"{colored("' to create one.", WARNING_COLOR)}")
            return work_groups

    # Add the work to the work group
    # Checks if it needs to append the dictionary or add to an already provided dictionary
    if len(work_groups[group]) == 1:
        work_groups[group].append({name: [time_for_work, break_time]})
    else:
        work_groups[group][1][name] = [time_for_work, break_time]

    update_append(f"Work '{colored(name, WORK_COLOR)}' has been added to the work group "
                             f"'{colored(group, WORK_GROUPS_COLOR)}'.")

    # Returns the items
    return work_groups


def format_time(time):
    # Formating for the time so the minutes section would be '09' instead of '9'
    if time.minute < 10:
        time_minute = f"0{time.minute}"
    else:
        time_minute = time.minute

    # Formating of the time hour section, so it displays in the 12-hour format
    if time.hour == 24:
        time_str = f"{time.hour - 12}:{time_minute} AM"
    elif time.hour > 12:
        time_str = f"{time.hour - 12}:{time_minute} PM"
    elif time.hour == 12:
        time_str = f"{time.hour}:{time_minute} PM"
    else:
        time_str = f"{time.hour}:{time_minute} AM"

    return time_str


def print_work_with_time(work, starting_time, minutes):
    ending_time = starting_time + timedelta(minutes=minutes)

    starting_time_str = format_time(starting_time)
    ending_time_str = format_time(ending_time)

    # Returns the ending time which is going to be the starting time of the next work
    return {"starting_time": ending_time,
            "text": f"{work}: {starting_time_str} -- {ending_time_str}"}


def change_default_settings(break_time: int, starting_time: datetime = None) -> dict:
    # Prints the current options
    update_append(f"1. {colored("Break Time", BREAK_TIME_COLOR)}: {break_time}")
    if starting_time is None:
        update_append(f"2. {colored("Starting Time", WORK_GROUPS_COLOR)}: Current Time")
        starting_time = datetime.now()
    else:
        update_append(f"2. {colored("Starting Time", WORK_GROUPS_COLOR)}: {format_time(starting_time)}")

    # Asks the user to choose
    user_choice = integer_validator(prompt=f"Choose the {colored("number", INSTRUCTIONS_COLOR)} "
                                           f"corresponding to the setting you want to change (1-2): ",
                                    minimum=1, maximum=2)

    # Updates the corresponding values with user inputs
    if user_choice == 1:
        change = integer_validator(
            prompt=f"What would you like to change the "
                   f"{colored("default break time", INSTRUCTIONS_COLOR)} to (minutes)? ",
            minimum=0)
        break_time = change
        update_append(f"'Break Time' has been changed to {break_time}.")
    elif user_choice == 2:
        change = input(
            f"What time do you want to change the starting time to "
            f"{colored("((0-23):(0-59) or ct for current time)", INSTRUCTIONS_COLOR)}? ")
        update_append(f"What time do you want to change the starting time to "
                          f"{colored("((0-23):(0-59) or ct for current time)", INSTRUCTIONS_COLOR)}? {change}")
        while True:
            try:
                if change.lower() == "ct":
                    starting_time = datetime.now()
                    update_append(colored("Default Setting changed to current time.", SUCCESS_COLOR))
                else:
                    hour = int(change.split(sep=":")[0])
                    minute = int(change.split(sep=":")[1])
                    today = datetime.now()
                    starting_time = datetime(year=today.year, month=today.month, day=today.day,
                                             hour=hour, minute=minute)
                    update_append(colored(f"'Starting Time' has been changed to "
                                                     f"{format_time(starting_time)}.",
                                                     SUCCESS_COLOR))
                break
            except TypeError:
                update_append(colored("Please enter the details as required! ((0-23):(0-59) or ct for "
                                                 "current time)", WARNING_COLOR))
                change = input(
                    f"What time do you want to change the starting time to "
                    f"{colored("((0-23):(0-59) or ct for current time)", INSTRUCTIONS_COLOR)}? ")
                update_append(f"What time do you want to change the starting time to "
                                         f"{colored("((0-23):(0-59) or ct for current time)", INSTRUCTIONS_COLOR)}?"
                                         f" {change}")
            except ValueError:
                update_append(colored("Please enter the details as required! ((0-23):(0-59) or ct for "
                                                 "current time)", WARNING_COLOR))
                change = input(
                    f"What time do you want to change the starting time to "
                    f"{colored("((0-23):(0-59) or ct for current time)", INSTRUCTIONS_COLOR)}? ")
                update_append(f"What time do you want to change the starting time to "
                                         f"{colored("((0-23):(0-59) or ct for current time)", INSTRUCTIONS_COLOR)}?"
                                         f" {change}")

    # Asks the user if they want to change something else
    change_again = yes_or_no(f"Do you want to {colored("change another default setting", INSTRUCTIONS_COLOR)} (y/n)? ")

    # Does recursion if true
    if change_again == "y":
        default_settings = change_default_settings(break_time, starting_time)
        return default_settings

    # Returning values
    default_settings = {
        "break_time": break_time,
        "starting_time": starting_time,
    }

    # Returns the values
    return default_settings


def organize_by_priority(work_groups):
    # Creates a list of works in order of priority
    # Goal: Formatted like {work: [time, break], work: [time, break], work: [time, break]}
    priority_ordered_work = {}

    # A copy list made to order works by priority level by sorting
    copy_work_groups = {}

    # Loops through the code equal to the amount of work_groups
    for i in range(len(work_groups)):

        # Variables to store the details of a work_group
        priority = 0
        priority_works = None
        priority_work_group = None

        # Loops through each of the works in the work_group
        # Goal: Find the work_group with the greatest priority level
        # and store the details of the work_group.
        for key, value in work_groups.items():
            # Checks if the priority value of the current group is greater
            # than the priority stored in the priority variable.
            if priority < value[0]:

                # Stores the information of the greater priority work_group
                priority = value[0]

                # Check if there are any works in the work_groups
                if len(value) != 1:
                    priority_works = value[1]
                else:
                    priority_works = {}

                # Stores the information of the greater priority group
                priority_work_group = key

        # Appends the works in the priority_ordered_works dictionary
        for work in priority_works:
            # print(work)
            priority_ordered_work[work] = priority_works[work]

        # Copies the work group into a list
        copy_work_groups[priority_work_group] = work_groups[priority_work_group]
        # Deletes the work_group key in the work_groups list
        del work_groups[priority_work_group]

    # Variable to store the returning variables
    return_items = {
        "work_groups": copy_work_groups,
        "priority_ordered_work": priority_ordered_work,
    }

    # print(original_schedule)
    # Returns the variables
    return return_items


def works_exist(work_groups):
    if work_groups:
        for work_group, works in work_groups.items():
            if len(works) > 1:
                return True
    else:
        return False


def show_schedule(work_groups, starting_time: datetime = None, use_intro=True):
    schedule_text.clear()
    if works_exist(work_groups=work_groups):
        if use_intro:
            schedule_text.append(colored("Here is your schedule for today.", INSTRUCTIONS_COLOR))

        # Sets the starting time to the current time if not provided.
        if starting_time is None:
            starting_time = datetime.now()

        # A blank line for spacing
        schedule_text.append("")

        # Calls the update schedule function which organizes the works by their priority in the
        # format of [{work: time}, {work: time}].
        # Checks if calling it is needed
        return_items = organize_by_priority(work_groups=work_groups)
        work_groups = return_items["work_groups"]
        priority_ordered_schedule = return_items["priority_ordered_work"]

        # Prints the schedule in 'Work_Name: Start-Time -- End-Time' format
        for work_name, work_details in priority_ordered_schedule.items():
            # Prints the work timings
            return_items = print_work_with_time(colored(work_name, WORK_COLOR),
                                                starting_time, work_details[0])
            starting_time = return_items["starting_time"]
            schedule_text.append(return_items["text"])
            # Blank line for spacing
            schedule_text.append("")
            # Prints break time timings
            return_items = print_work_with_time(colored("BREAK TIME", BREAK_TIME_COLOR), starting_time,
                                                work_details[1])
            starting_time = return_items["starting_time"]
            schedule_text.append(return_items["text"])
            # Blank line for spacing
            schedule_text.append("")
    else:
        schedule_text.append(colored("Your schedule is empty.", INSTRUCTIONS_COLOR))

    # Returns the items
    return work_groups


def change_schedule(work_groups, starting_time=None):
    if works_exist(work_groups=work_groups):
        # Sets the starting time to the current time, if it is None
        if starting_time is None:
            starting_time = datetime.now()

        # Creates a duplicate of the starting time for later use
        original_starting_time = starting_time

        return_items = organize_by_priority(work_groups=work_groups)
        work_groups = return_items["work_groups"]
        priority_ordered_schedule = return_items["priority_ordered_work"]

        # Prints out the schedule for the user to be able to edit
        count = 0
        # [{work, time}, {break: time}]
        work_dict_including_break = {}
        for work_name, work_details in priority_ordered_schedule.items():
            # Prints the work timings
            count += 1
            update_append(f"{count}. ", end="")

            return_items = print_work_with_time(colored(work_name, WORK_COLOR), starting_time, work_details[0])
            starting_time = return_items["starting_time"]
            update_append(return_items["text"])

            update_append(f"Time: {work_details[0]} minutes")
            work_dict_including_break[work_name] = work_details[0]

            # Blank line for spacing
            update_append("")

            # Prints break time timings
            count += 1
            update_append(f"{count}. ", end="")
            return_items = print_work_with_time(colored("BREAK TIME", BREAK_TIME_COLOR), starting_time,
                                                work_details[1])
            starting_time = return_items["starting_time"]
            update_append(return_items["text"])
            update_append(f"Time: {work_details[1]} minutes")
            work_dict_including_break[f"break_time{count}"] = work_details[1]

            # Blank line for spacing
            update_append("")

        # After displaying, asks the user to choose the number of the item they want to change
        user_choice = integer_validator(prompt="Select the number corresponding to the part you want to change: ",
                                        minimum=1, maximum=count)

        # Makes the changes in the actual work_groups
        count = 0
        before_break_work_name = ""
        for work_name, time in work_dict_including_break.items():
            count += 1
            if count % 2 == 1:
                before_break_work_name = work_name
            if count == user_choice:
                time_change = integer_validator(prompt=f"What would you like to change the "
                                                       f"{colored("time", INSTRUCTIONS_COLOR)} to (minutes)? ")
                for work_group, works in work_groups.items():
                    if len(works) > 1:
                        for actual_work_name, work_details in works[1].items():
                            if actual_work_name == before_break_work_name:
                                if count % 2 == 0:
                                    work_groups[work_group][1][actual_work_name][1] = time_change
                                else:
                                    work_groups[work_group][1][actual_work_name][0] = time_change

        # Prints that the change has been successful
        update_append(colored("Change has been successful.", SUCCESS_COLOR))

        # Asks the user if they want to change another item in the schedule
        change_again = yes_or_no(f"Do you want to {colored("change", INSTRUCTIONS_COLOR)} something else (y/n)? ")

        # Checks the answer and does recursion
        if change_again == "y":
            return_items = change_schedule(work_groups, original_starting_time)
            work_groups = return_items["work_groups"]
    else:
        update_append(colored("Current schedule doesn't contain anything to change.", WARNING_COLOR))
        update_append(f"To add a group, use '{colored("add group", command_color)}'.")
        update_append(f"To add a work, use '{colored("add work", command_color)}'.")

    # Returns items
    return work_groups


def add_previous_work(work_groups, previous_works, break_time):

    if previous_works:
        work = None
        time = None

        # Displays to the user the options
        count = 0
        for work in previous_works:
            count += 1
            update_append(f"{count}. {colored("work", WORK_COLOR)}")

        # Asks user about their choice
        user_choice = integer_validator(
            prompt=f"Which {colored("previously added work", INSTRUCTIONS_COLOR)} do you want to add? ",
            minimum=0, maximum=count)

        # Updates the values accordingly
        for work_name, time in previous_works[user_choice - 1].items():
            # Updates the name
            work = work_name
            # Asks the user if they want to change the time of the given work
            user_choice = yes_or_no(prompt=f"Do you want to change the "
                                           f"{colored("amount of time", INSTRUCTIONS_COLOR)} this work takes (y/n)? ")
            if user_choice == "y":
                new_time = integer_validator(prompt=f"What do you want to change the "
                                                    f"{colored("time", INSTRUCTIONS_COLOR)} to? ")
            else:
                new_time = time
            # Updates the time
            time = new_time

        if check_duplicate(work_groups=work_groups, work_name=work):
            update_append(colored("A work already exists with a name as this previous work.", WARNING_COLOR))
            update_append(colored("The previous work has not been added.", WARNING_COLOR))
            return work_groups
        else:
            group = input(f"What {colored("group", INSTRUCTIONS_COLOR)} do want to enter this "
                          f"{colored("work", INSTRUCTIONS_COLOR)} to? ")
            update_append(f"What {colored("group", INSTRUCTIONS_COLOR)} do want to enter this "
                              f"{colored("work", INSTRUCTIONS_COLOR)} to? {group}")

        work_groups = add_work(work_groups=work_groups, break_time=break_time, group=group, name=work,
                               time_for_work=time)
    else:
        update_append(colored("There are no previous works add.", WARNING_COLOR))
        update_append(f"When you use '{colored("add work", command_color)}' or "
                                 f"'{colored("a", command_color)}', "
                                 f"that work will be {colored("saved into your previous work.", INSTRUCTIONS_COLOR)}")

    return work_groups
