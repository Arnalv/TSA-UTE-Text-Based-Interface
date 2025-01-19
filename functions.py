from datetime import datetime, timedelta


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
                print(f"    {work_count}. {work}, time:   {time} min")
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
            group_access_integer = (
                    int(input("Enter the number corresponding to the group you want to remove: ")) - 1
            )
            group_key = work_groups_list[group_access_integer][0]
        else:
            group_key = removing_group
        # Removes the group
        del work_groups[group_key]
        # Prints confirmation message to user
        print(f"The group '{group_key}' has been removed.")

    # Returns the updated work_groups
    return work_groups


def remove_work(work_groups: dict, removing_work: list = None) -> dict:
    if work_groups:
        if removing_work is None:
            work_groups_list = show_options(work_groups)
            group_access_integer = (
                    int(input("Enter the number corresponding to the group of the work you want to remove: ")) - 1
            )
            group_key = work_groups_list[group_access_integer][0]
            if len(work_groups_list[group_access_integer]) == 1:
                print("There are no works to remove in this work group.")
                print("If you want to remove the group, use remove_group.")
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
    else:
        print("There are no works added to remove.")
        print("First add a group using add_group and then use add_work to add a work to the group.")
    return work_groups


def add_group(original_work_groups, group_name=None, group_priority=None):
    work_groups = original_work_groups

    # Takes input from the user if not provided in the function
    if group_name is None:
        group_name = input("Name of group: ")

    if group_priority is None:
        while True:
            try:
                group_priority = int(input("What priority level would you like " + group_name + " to have? (1-10) "))
                if 1 <= group_priority <= 10:
                    break
            except TypeError:
                print("Please enter an integer between 1 and 10!")

    # Adds the work group, if it already doesn't exist
    if group_name not in work_groups:
        work_groups[group_name] = [group_priority]
        print(f"Work Group '{group_name}' has been added.")
    else:
        print("Work group already exists!")

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
                print(f"{work_group_number}. {key} (Priority: {value[0]})")
                work_number = 0
                if len(value) > 1:
                    for work, time in value[1].items():
                        work_number += 1
                        print(f"    {work_number}. {work}, Time: {time} minutes")

            # Asks user to choose from list of groups shown
            group_number = int(input("What work group would you like to add your work to? "
                                     "(type in # that corresponds): "))

            # Takes that number and finds the name of the group
            work_group_number = 0
            for key in work_groups:
                work_group_number += 1
                if work_group_number == group_number:
                    group = key
                    break

        # Tells the user that there are no work groups present, and you can't add a work
        else:
            print("No work groups detected.")
            print("You will need to add a work group first using 'add_group' or provide name of the group when asked.")

            return work_groups

    # Checks if the name of the group is not provided and gets an input from the user if not provided
    if name is None:
        # Just asks the user a name due to the user not looking through the previous list
        name = input("Please enter a name for this work: ")

    # check if the name provided is duplicate name
    if check_duplicate(work_groups=work_groups, work_name=name):
        print("The name of the work already exists.")
        new_name = input("Please enter another name for the work: ")
        while name == new_name:
            print("That name was the same one as the previous name.")
            new_name = input("Please enter a new name: ")
        name = new_name

    # Asks the user for the time of the work if not already provided
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
        else:
            print("Adding work to schedule not successful. Make sure the work you intended to add has a valid "
                  "work group (spelled correctly).")
            print("If work group is not created yet, please type 'add_group' to create one.")
            return work_groups

    # Add the work to the work group
    # Checks if it needs to append the dictionary or add to an already provided dictionary
    if len(work_groups[group]) == 1:
        work_groups[group].append({name: [time_for_work, break_time]})
    else:
        work_groups[group][1][name] = [time_for_work, break_time]

    print(f"Work '{name}' has been added to the work group '{group}'.")

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

    # Prints out the time for the work
    print(f"{work}: {starting_time_str} -- {ending_time_str}")

    # Returns the ending time which is going to be the starting time of the next work
    return ending_time


def change_default_settings(break_time: int, starting_time: datetime = datetime.now()) -> dict:
    # Prints the current options
    print(f"1. Break Time: {break_time}")
    if starting_time is None:
        print(f"2. Starting_Time: Current Time")
    else:
        print(f"Starting Time: {format_time(starting_time)}")

    # Asks the user to choose
    user_choice = int(input("Choose the number corresponding to the setting you want to change (1-2): "))

    # Updates the corresponding values with user inputs
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

    # Asks the user if they want to change something else
    change_again = input("Do you want to change another default setting (y/n)? ").lower()

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


def show_schedule(work_groups, starting_time: datetime = None):
    if works_exist(work_groups=work_groups):
        print("Here is your schedule for today.")

        # Sets the starting time to the current time if not provided.
        if starting_time is None:
            starting_time = datetime.now()

        # A blank line for spacing
        print("")

        # Calls the update schedule function which organizes the works by their priority in the
        # format of [{work: time}, {work: time}].
        # Checks if calling it is needed
        return_items = organize_by_priority(work_groups=work_groups)
        work_groups = return_items["work_groups"]
        priority_ordered_schedule = return_items["priority_ordered_work"]

        # Prints the schedule in 'Work_Name: Start-Time -- End-Time' format
        for work_name, work_details in priority_ordered_schedule.items():
            # Prints the work timings
            starting_time = print_work_with_time(work_name, starting_time, work_details[0])
            # Blank line for spacing
            print("")
            # Prints break time timings
            starting_time = print_work_with_time("BREAK TIME", starting_time, work_details[1])
            # Blank line for spacing
            print("")
    else:
        print("There are no works added. Use 'add work' to add a work.")

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
            print(f"{count}. ", end="")
            starting_time = print_work_with_time(work_name, starting_time, work_details[0])
            print(f"Time: {work_details[0]} minutes")
            work_dict_including_break[work_name] = work_details[0]
            # Blank line for spacing
            print("")
            # Prints break time timings
            count += 1
            print(f"{count}. ", end="")
            starting_time = print_work_with_time("BREAK TIME", starting_time, work_details[1])
            print(f"Time: {work_details[1]} minutes")
            work_dict_including_break[f"break_time{count}"] = work_details[1]
            # Blank line for spacing
            print("")

        # After displaying, asks the user to choose the number of the item they want to change
        user_choice = int(input("Select the number corresponding to the part you want to change: "))

        # Makes the changes in the actual work_groups
        count = 0
        before_break_work_name = ""
        for work_name, time in work_dict_including_break.items():
            count += 1
            if count % 2 == 1:
                before_break_work_name = work_name
            if count == user_choice:
                time_change = int(input("What would you like to change the time to (minutes)? "))
                for work_group, works in work_groups.items():
                    if len(works) > 1:
                        for actual_work_name, work_details in works[1].items():
                            if actual_work_name == before_break_work_name:
                                if count % 2 == 0:
                                    work_groups[work_group][1][actual_work_name][1] = time_change
                                else:
                                    work_groups[work_group][1][actual_work_name][0] = time_change

        # Prints that the change has been successful
        print("Change has been successful.")

        # Asks the user if they want to change another item in the schedule
        change_again = input("Do you want to change something else (y/n)? ").lower()

        # Checks the answer and does recursion
        if change_again == "y":
            return_items = change_schedule(work_groups, original_starting_time)
            work_groups = return_items["work_groups"]
    else:
        print("Current schedule doesn't contain anything to change.")
        print("To add a group, use 'add group'.")
        print("To add a work, use 'add work'.")

    # Returns items
    return work_groups
