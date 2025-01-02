from datetime import datetime, timedelta
from math import floor


def add_group(original_work_groups, group_name=None, group_priority=None):
    """
    # TODO create a file and store the information
    with open(file="./previous_schedule_tracker", mode="w") as file:
        file.
    """

    work_groups = original_work_groups

    # Takes input from the user if not provided in the function
    if group_name is None:
        group_name = input("Name of group: ")
    if group_priority is None:
        while True:
            try:
                group_priority = int(input("What priority level would you like " + group_name + " to have? (integer) "))
                break
            except TypeError:
                print("Please enter an integer!")

    # Adds the work group, if it already doesn't exist
    if group_name not in work_groups:
        work_groups[group_name] = [group_priority]
        print(f"Work Group '{group_name}' has been added.")
    else:
        print("Work group already exists!")

    return work_groups


def add_work(work_groups, group=None, name=None, time_for_work=None):
    # Takes input from user if not already provided
    if group is None:
        if work_groups != {}:
            # Shows the options to choose a group
            work_group_number = 0
            for key, value in work_groups.items():
                work_group_number += 1
                print(f"{work_group_number}. {key} (Priority: {value[0]})")
                work_number = 0
                if len(value) > 1:
                    for work, time in value[1].items():
                        work_number += 1
                        print(f"    {work_number}. {work}, Time: {time} minutes")
            print(f"{work_group_number+1}. This option adds a new group. Then you can add a work to this group.")

            # Asks user to choose from list of groups
            group_number = int(input("What work group would you like to add your work to? "
                                     "(type in # that corresponds): "))

            # Checks if the user choose the option of adding a new group
            if group_number != work_group_number + 1:
                # Takes that number and finds the name of the group
                work_group_number = 0
                for key in work_groups:
                    work_group_number += 1
                    if work_group_number == group_number:
                        group = key
            # Allows the user to add a new group and a work for the group
            else:
                work_groups = add_group(work_groups)
                work_groups = add_work(work_groups)
                return work_groups
        else:
            print("No work groups detected.")
            print("You will need to add a work group first.")
            work_groups = add_group(work_groups)
            work_groups = add_work(work_groups)
            return work_groups

    if name is None:
        name = input("Please enter the name of this work: ")

    if time_for_work is None:
        time_for_work = int(input("About how many minutes that does this work take? "))

    # Checks if a provided group is not in work_groups
    if group not in work_groups:
        group_response = input(f"Group not found. Would you like to add a group called '{group}'? (y/n) ").lower()
        while group_response != "y" and group_response != "n":
            group_response = input(
                "Group not found. Would you like to add a group called " + group + " ? (y/n) ").lower()
        if group_response == "y":
            # Adds the group
            work_groups = add_group(group_name=group, original_work_groups=work_groups)

    # Add the work to the specific group
    else:
        work_groups[group].append({name: time_for_work})
        print(f"Work '{name}' has been added to the work group '{group}'.")

    # Testing:
    # print(work_groups)
    return work_groups


"""
Testing Purposes: To test the show_schedule function, the work_groups class has a pre-defined value.


"""


def format_time(time):
    # Formating for the time so the minutes section would be '09' instead of '9'
    if time.minute < 10:
        time_minute = f"0{time.minute}"
    else:
        time_minute = time.minute

    # Formating of the time hour section, so it displays in the 12-hour format
    if time.hour == 24:
        time_str = f"{time.hour - 12}:{time_minute} PM"
    elif time.hour > 12:
        time_str = f"{time.hour - 12}:{time_minute} PM"
    elif time.hour == 12:
        time_str = f"{time.hour}:{time_minute} PM"
    else:
        time_str = f"{time.hour}:{time_minute} AM"

    return time_str


def print_work(work, starting_time, minutes):
    ending_time = starting_time + timedelta(minutes=minutes)

    starting_time_str = format_time(starting_time)
    ending_time_str = format_time(ending_time)

    # Prints out the time for the work
    print(f"{work}: {starting_time_str} -- {ending_time_str}")

    # Returns the ending time which is going to be the starting time of the next work
    return ending_time


def update_schedule(work_groups, original_schedule, break_time):
    # Creates a list of works in order of priority ()
    priority_ordered_work = []

    # A copy list made to order works by priority level
    len_of_groups = len(work_groups)
    copy_work_groups = {}

    for i in range(len_of_groups):
        priority = 0
        priority_works = None
        priority_work_group = None
        for key, value in work_groups.items():
            if priority < value[0]:
                priority = value[0]
                if len(value) != 1:
                    priority_works = value[1]
                else:
                    priority_works = {}
                priority_work_group = key
        priority_ordered_work.append(priority_works)
        copy_work_groups[priority_work_group] = work_groups[priority_work_group]
        del work_groups[priority_work_group]

    count = 0
    updated_schedule = []
    if original_schedule:
        for group_of_work in priority_ordered_work:
            for work, time in group_of_work.items():
                if work in original_schedule[count]:
                    updated_schedule.insert(count, {work: [time, break_time]})
                else:
                    updated_schedule.append({work: [time, break_time]})
    else:
        for group_of_work in priority_ordered_work:
            for work, time in group_of_work.items():
                updated_schedule.append({work: [time, break_time]})

    return_items = {
        "work_groups": copy_work_groups,
        "updated_schedule": updated_schedule,
    }

    return return_items


def show_schedule(work_groups, break_time: int, original_schedule: list, starting_time: datetime = None, organize=True):
    print("Here is your schedule for today.")

    if starting_time is None:
        starting_time = datetime.now()

    # A blank line for spacing
    print("")

    if organize:
        return_items = update_schedule(work_groups=work_groups, original_schedule=original_schedule, break_time=break_time)

        updated_schedule = return_items["updated_schedule"]
        work_groups = return_items["work_groups"]
    else:
        updated_schedule = original_schedule

    # Prints the schedule in 'Work_Name: Start-Time -- End-Time' format
    for work in updated_schedule:
        for work_name, work_details in work.items():
            # Prints the work timings
            starting_time = print_work(work_name, starting_time, work_details[0])

            # Blank line for spacing
            print("")

            # Prints break time timings
            starting_time = print_work("BREAK TIME", starting_time, work_details[1])

            # Blank line for spacing
            print("")

    return_items = {
        "work_groups": work_groups,
        "schedule": updated_schedule
    }

    return return_items


def show_options(work_groups):
    work_groups_list = []
    group_count = 0
    for group, work_section in work_groups.items():
        work_list = [group]
        group_count += 1
        print(f"{group_count}. {group}")
        work_count = 0
        if len(work_groups[group]) != 1:
            for work, time in work_section[1].items():
                work_count += 1
                print(f"    {work_count}. {work}, time: {time} min")
                work_list.append(work)
        work_groups_list.append(work_list)

    return work_groups_list


def remove_group(work_groups: dict, removing_group=None) -> dict:
    if removing_group is None:
        work_groups_list = show_options(work_groups)
        group_access_integer = (
                int(input("Enter the number corresponding to the group you want to remove: ")) - 1
        )
        group_key = work_groups_list[group_access_integer]
    else:
        group_key = removing_group
    del work_groups[group_key]
    print(f"The group '{group_key}' has been removed.")
    return work_groups


def remove_work(work_groups: dict, removing_work: list = None) -> dict:
    if removing_work is None:
        work_groups_list = show_options(work_groups)
        group_access_integer = (
                int(input("Enter the number corresponding to the group of the work you want to remove: ")) - 1
        )
        group_key = work_groups_list[group_access_integer][0]
        if len(work_groups_list[group_access_integer]) == 1:
            print("There are no works to remove in this work group.")
            user_choice = input("Do you want to remove the entire group (y/n)? ").lower()
            if user_choice == "y":
                work_groups = remove_group(work_groups, group_key)
            return work_groups
        else:
            work_access_integer = (
                int(input("Enter the number corresponding to the work you want to remove: "))
            )

            work_key = work_groups_list[group_access_integer][work_access_integer]
    else:
        group_key = removing_work[0]
        work_key = removing_work[1]

    del work_groups[group_key][1][work_key]
    print(f"The work '{work_key}' has been removed from the group '{group_key}'.")

    return work_groups


def change_default_settings(break_time: int, starting_time: datetime = datetime.now()) -> dict:
    print(f"1. Break Time: {break_time}")
    if starting_time is None:
        print(f"2. Starting_Time: Current Time")
    else:
        print(f"Starting Time: {format_time(starting_time)}")

    user_choice = int(input("Choose the number corresponding to the setting you want to change (1-2): "))

    if user_choice == 1:
        change = int(input("What would you like to change the default break time to (minutes)? "))
        break_time = change
        print(f"'Break Time' has been changed to {break_time}.")
    elif user_choice == 2:
        change = input("What time do you want to change the starting time to ((0-23):(0-59))? ")
        hour = int(change.split(sep=":")[0])
        minute = int(change.split(sep=":")[1])
        today = datetime.now()
        starting_time = datetime(year=today.year, month=today.month, day=today.day, hour=hour, minute=minute)
        print(f"'Starting Time' has been changed to {format_time(starting_time)}.")

    change_again = input("Do you want to change another default setting (y/n)? ").lower()

    if change_again == "y":
        default_settings = change_default_settings(break_time, starting_time)
        return default_settings

    default_settings = {
        "break_time": break_time,
        "starting_time": starting_time,
    }

    return default_settings


def change_schedule(work_groups, original_schedule, break_time, starting_time=None):

    if starting_time is None:
        starting_time = datetime.now()

    original_starting_time = starting_time
    """
    original_starting_time = (
        datetime(starting_time.year, starting_time.month, starting_time.day, starting_time.hour, starting_time.minute))
    """
    if not original_schedule:
        return_items = update_schedule(work_groups=work_groups, original_schedule=original_schedule, break_time=break_time)

        original_schedule = return_items["updated_schedule"]
        work_groups = return_items["work_groups"]

    count = 0
    work_list_including_break = []
    for work in original_schedule:
        for work_name, work_details in work.items():
            # Prints the work timings
            count += 1
            print(f"{count}. ", end="")
            starting_time = print_work(work_name, starting_time, work_details[0])
            print(f"Time: {work_details[0]} minutes")
            work_list_including_break.append({work_name: work_details[0]})

            # Blank line for spacing
            print("")

            # Prints break time timings
            count += 1
            print(f"{count}. ", end="")
            starting_time = print_work("BREAK TIME", starting_time, work_details[1])
            print(f"Time: {work_details[1]} minutes")
            work_list_including_break.append({"break_time": work_details[1]})

            # Blank line for spacing
            print("")

    user_choice = int(input("Select the number corresponding to the part you want to change: "))

    for work_name, time in work_list_including_break[user_choice-1].items():
        time_change = int(input("What would you like to change the time to (minutes)? "))
        if (user_choice-1) % 2 == 0:
            original_schedule[floor((user_choice-1)/2)][work_name][0] = time_change
        else:
            original_schedule[floor((user_choice - 1)/2)][work_name][1] = time_change

    # Formatted like {work_group_name: [priority, {work_name : time_for_work}]}
    return_items = show_schedule(work_groups, break_time, original_schedule, original_starting_time, False)
    work_groups = return_items["work_groups"]
    original_schedule = return_items["schedule"]

    change_again = input("Do you want to change something else (y/n)? ").lower()

    if change_again == "y":
        return_items = change_schedule(work_groups, original_schedule, break_time, original_starting_time)
        work_groups = return_items["work_groups"]
        original_schedule = return_items["original_schedule"]

    return_items = {
        "original_schedule": original_schedule,
        "work_groups": work_groups,
    }

    return return_items
