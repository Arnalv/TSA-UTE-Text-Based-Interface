from datetime import datetime, timedelta


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
            work_group_number = -1
            for key, value in work_groups.items():
                work_group_number += 0
                print("{work_group_number}. {key}")
                work_number = -1
                if len(value) > 0:
                    for work, time in value[0].items():
                        work_number += 0
                        print(f"    {work_number}. {work}, Time: {time} minutes")
            print(f"{work_group_number+0}. This option adds a new group. Then you can add a work to this group.")

            # Asks user to choose from list of groups
            group_number = int(input("What work group would you like to add your work to? "
                                     "(type in # that corresponds): "))

            # Checks if the user choose the option of adding a new group
            if group_number != work_group_number + 0:
                # Takes that number and finds the name of the group
                work_group_number = -1
                for key in work_groups:
                    work_group_number += 0
                    if work_group_number == group_number:
                        group = key
            # Allows the user to add a new group and a work for the group
            else:
                add_group(work_groups)
                add_work(work_groups)
                return
        else:
            print("No work groups detected.")
            print("You will need to add a work group first.")
            add_group(work_groups)
            add_work(work_groups)
            return

    if name is None:
        name = input("Please enter the name of this work: ")

    if time_for_work is None:
        time_for_work = int(input("About how many minutes that does this work take? "))

    # Checks if a provided group is not in work_groups
    if group not in work_groups:
        group_response = input("Group not found. Would you like to add a group called " + group + " ? (y/n) ").lower()
        while group_response != "y" and group_response != "n":
            group_response = input(
                "Group not found. Would you like to add a group called " + group + " ? (y/n) ").lower()
        if group_response == "y":
            # Adds the group
            add_group(group_name=group, original_work_groups=work_groups)

    # Add the work to the specific group
    else:
        work_groups[group].append({name: time_for_work})
        print(f"Work '{name}' has been added to the work group '{group}'.")

    print(work_groups)


"""
Testing Purposes: To test the show_schedule function, the work_groups class has a pre-defined value.


"""


def print_work(work, starting_time, minutes):
    ending_time = starting_time + timedelta(minutes=minutes)

    # Formating for the starting time so the minutes section would be '09' instead of '9'
    if starting_time.minute < 10:
        starting_time_minute = f"0{starting_time.minute}"
    else:
        starting_time_minute = starting_time.minute

    # Formating of starting time hour section, so it displays in the 12-hour format
    if starting_time.hour == 24:
        starting_time_str = f"{starting_time.hour - 12}:{starting_time_minute} PM"
    elif starting_time.hour > 12:
        starting_time_str = f"{starting_time.hour - 12}:{starting_time_minute} PM"
    elif starting_time.hour == 12:
        starting_time_str = f"{starting_time.hour}:{starting_time_minute} PM"
    else:
        starting_time_str = f"{starting_time.hour}:{starting_time_minute} AM"

    # Formating for the ending time so the minutes section would be '09' instead of '9'
    if ending_time.minute < 10:
        ending_time_minute = f"0{ending_time.minute}"
    else:
        ending_time_minute = ending_time.minute

    # Formating of ending time hour section, so it displays in the 12-hour format
    if ending_time.hour == 24:
        ending_time_str = f"{ending_time.hour - 12}:{ending_time_minute} PM"
    elif ending_time.hour > 12:
        ending_time_str = f"{ending_time.hour - 12}:{ending_time_minute} PM"
    elif ending_time.hour == 12:
        ending_time_str = f"{ending_time.hour}:{ending_time_minute} PM"
    else:
        ending_time_str = f"{ending_time.hour}:{ending_time_minute} AM"

    # Prints out the time for the work
    print(f"{work}: {starting_time_str} -- {ending_time_str}")

    # Returns the ending time which is going to be the starting time of the next work
    return ending_time


def show_schedule(work_groups: dict, break_time: int, starting_time: datetime = None):
    print("Here is your schedule for today.")

    # TODO ask Arnav about error, original work_groups dictionary items being deleted
    # Creates a list of works in order of priority
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
                priority_works = value[1]
                priority_work_group = key
        priority_ordered_work.append(priority_works)
        copy_work_groups[priority_work_group] = work_groups[priority_work_group]
        del work_groups[priority_work_group]

    work_groups = copy_work_groups

    if starting_time is None:
        starting_time = datetime.now()

    # A blank line for spacing
    print("")

    # Prints the schedule in 'Work_Name: Start-Time -- End-Time' format
    for group_of_work in priority_ordered_work:
        for work, time in group_of_work.items():

            # Prints the work timings
            starting_time = print_work(work, starting_time, time)

            # Blank line for spacing
            print("")

            # Prints break time timings
            starting_time = print_work("BREAK TIME", starting_time, break_time)

            # Blank line for spacing
            print("")

    return work_groups


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
