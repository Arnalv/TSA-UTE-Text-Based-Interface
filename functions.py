from datetime import datetime, timedelta
from math import floor


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


def remove_group(work_groups: dict, removing_group=None) -> dict:
    """
    Removes a group from work groups.
    """

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


def remove_work(work_groups: dict, original_schedule, break_time, removing_work: list = None) -> dict:
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
            return_items = (
                update_schedule(work_groups=work_groups, original_schedule=original_schedule, break_time=break_time))
            return return_items
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

    return_items = (
        update_schedule(work_groups=work_groups, original_schedule=original_schedule, break_time=break_time))
    return return_items


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

    # Returns a work_groups_list formatted [[group_name, work, work],[group_name, work]]
    return work_groups_list


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


def add_work(work_groups, original_schedule, break_time, group=None, name=None, time_for_work=None):
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
            print(f"{work_group_number + 1}. This option adds a new group. Then you can add a work to this group.")

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
                work_groups = add_group(work_groups, original_schedule)
                work_groups = add_work(work_groups, original_schedule, break_time)
                return_items = (
                    update_schedule(work_groups=work_groups, original_schedule=original_schedule,
                                    break_time=break_time))
                return return_items
        # Allows the user to a work group since the dictionary work_groups is empty
        else:
            print("No work groups detected.")
            print("You will need to add a work group first.")
            work_groups = add_group(work_groups)
            work_groups = add_work(work_groups, original_schedule, break_time)
            return_items = (
                update_schedule(work_groups=work_groups, original_schedule=original_schedule, break_time=break_time))
            return return_items

    # Checks if the name of the group is not provided and gets an input from the user if not provided
    if name is None:
        # Checks if the name that the user has given already exists
        duplicate_name = True
        while duplicate_name:
            duplicate_name = False
            name = input("Please enter the name of this work: ")
            for work_group in work_groups:
                for work in work_group:
                    if name == work:
                        duplicate_name = True
            if duplicate_name:
                print("A work or a work group with this name already exists. Please enter another name.")

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

    # Add the work to the specific group
    else:
        work_groups[group].append({name: time_for_work})
        print(f"Work '{name}' has been added to the work group '{group}'.")

    # The items needed to be returned
    return_items = (
        update_schedule(work_groups=work_groups, original_schedule=original_schedule, break_time=break_time))

    # Returns the items
    return return_items


"""
Testing Purposes: To test the show_schedule function, the work_groups class has a pre-defined value.


"""


def update_schedule(work_groups, original_schedule, break_time):
    # Creates a list of works in order of priority
    # Goal: Formatted like {work: time, work: time, work: time}
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
            priority_ordered_work[work] = priority_works[work]

        # Copies the work group into a list
        copy_work_groups[priority_work_group] = work_groups[priority_work_group]
        # Deletes the work_group key in the work_groups list
        del work_groups[priority_work_group]

    # Runs if the original_schedule list contains items,
    # if it doesn't, just fills it with items in the priority_order_work
    if original_schedule:

        # Takes in the lengths of both lists
        original_schedule_length = len(original_schedule)
        priority_ordered_work_length = len(priority_ordered_work)

        # Compares both list to check if something has been added to the priority_order_work
        if priority_ordered_work_length > original_schedule_length:

            # Sets the count to zero to keep track of the placement of the added work
            count = 0

            # Loops through the priority_order_work dict and compares it to original_schedule for the changes
            for work in priority_ordered_work:

                # Keeps track to see if the work exists
                work_exist = False

                # Compares works to see if anything matches
                if len(original_schedule) >= count:
                    for original_work in original_schedule[count]:
                        if work in original_work:
                            work_exist = True
                else:
                    work_exist = True
                    original_schedule.append({work: [priority_ordered_work[work], break_time]})

                # If there isn't a match, then adds the work to the original schedule
                if not work_exist:
                    original_schedule.insert(count, {work: [priority_ordered_work[work], break_time]})
                    break

                # Add one to keep track of the placement
                count += 1

        # Compares both list to check if something got removed in the priority_order_work
        elif priority_ordered_work_length < original_schedule_length:

            # Loops through the works in original_schedule
            for original_work in original_schedule:
                for work in original_work:
                    # Compares the works
                    if work not in priority_ordered_work:
                        # If the work doesn't exist in priority_ordered_work, it removes the work
                        original_schedule.remove(original_work)
                        break
    # If the list is empty it updates the list to contain the same things as priority_ordered_work with the break_times
    else:
        for work, time in priority_ordered_work.items():
            original_schedule.append({work: [time, break_time]})

    # Variable to store the returning variables
    return_items = {
        "work_groups": copy_work_groups,
        "updated_schedule": original_schedule,
    }

    # Returns the variables
    return return_items


def show_schedule(work_groups, break_time: int, original_schedule: list, starting_time: datetime = None, organize=True):
    print("Here is your schedule for today.")

    # Sets the starting time to the current time if not provided.
    if starting_time is None:
        starting_time = datetime.now()

    # A blank line for spacing
    print("")

    # Calls the update schedule function which organizes the works by their priority in the
    # format of [{work: time}, {work: time}].
    # Checks if calling it is needed
    if organize:
        return_items = (
            update_schedule(work_groups=work_groups, original_schedule=original_schedule, break_time=break_time))

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

    # Items for returning
    return_items = {
        "work_groups": work_groups,
        "schedule": updated_schedule
    }

    # Returns the items
    return return_items


def change_schedule(work_groups, original_schedule, break_time, starting_time=None):
    # Sets the starting time to the current time, if it is None
    if starting_time is None:
        starting_time = datetime.now()

    # Creates a duplicate of the starting time for later use
    original_starting_time = starting_time

    # Updates the schedule to
    return_items = update_schedule(work_groups=work_groups, original_schedule=original_schedule, break_time=break_time)

    original_schedule = return_items["updated_schedule"]
    work_groups = return_items["work_groups"]

    # Prints out the schedule for the user to be able to edit
    count = 0
    # [{work, time}, {break: time}]
    work_dict_including_break = {}
    for work in original_schedule:
        for work_name, work_details in work.items():
            # Prints the work timings
            count += 1
            print(f"{count}. ", end="")
            starting_time = print_work(work_name, starting_time, work_details[0])
            print(f"Time: {work_details[0]} minutes")
            work_dict_including_break[work_name] = work_details[0]

            # Blank line for spacing
            print("")

            # Prints break time timings
            count += 1
            print(f"{count}. ", end="")
            starting_time = print_work("BREAK TIME", starting_time, work_details[1])
            print(f"Time: {work_details[1]} minutes")
            work_dict_including_break[f"break_time{count}"] = work_details[1]

            # Blank line for spacing
            print("")

    # After displaying, asks the user to choose the number of the item they want to change
    user_choice = int(input("Select the number corresponding to the part you want to change: "))

    # Makes the changes
    count = 0
    before_break_work_name = ""
    for work_name, time in work_dict_including_break.items():
        count += 1
        if count % 2 == 1:
            before_break_work_name = work_name
        if count == user_choice:
            time_change = int(input("What would you like to change the time to (minutes)? "))
            if (user_choice - 1) % 2 == 0:
                original_schedule[floor((user_choice - 1) / 2)][work_name][0] = time_change
            else:
                original_schedule[floor((user_choice - 1) / 2)][before_break_work_name][1] = time_change

    # Prints that the change has been successful
    print("Change has been successful.")

    # Asks the user if they want to change another item in the schedule
    change_again = input("Do you want to change something else (y/n)? ").lower()

    # Checks the answer and does recursion
    if change_again == "y":
        return_items = change_schedule(work_groups, original_schedule, break_time, original_starting_time)
        work_groups = return_items["work_groups"]
        original_schedule = return_items["original_schedule"]

    # Items to return
    return_items = {
        "original_schedule": original_schedule,
        "work_groups": work_groups,
    }

    # Returns items
    return return_items
