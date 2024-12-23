
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


def show_schedule(work_groups, starting_time: datetime = None):
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

    # Prints the schedule in 'Work_Name: Start-Time -- End-Time' format
    for group_of_work in priority_ordered_work:
        for work, time in group_of_work.items():
            ending_time = starting_time + timedelta(minutes=time)

            if starting_time.minute < 10:
                starting_time_minute = f"0{starting_time.minute}"
            else:
                starting_time_minute = starting_time.minute

            if starting_time.hour == 24:
                starting_time_str = f"{starting_time.hour-12}:{starting_time_minute} PM"
            elif starting_time.hour > 12:
                starting_time_str = f"{starting_time.hour-12}:{starting_time_minute} PM"
            elif starting_time.hour == 12:
                starting_time_str = f"{starting_time.hour}:{starting_time_minute} PM"
            else:
                starting_time_str = f"{starting_time.hour}:{starting_time_minute} AM"

            if ending_time.minute < 10:
                ending_time_minute = f"0{ending_time.minute}"
            else:
                ending_time_minute = ending_time.minute

            if ending_time.hour == 24:
                ending_time_str = f"{ending_time.hour-12}:{ending_time_minute} PM"
            elif ending_time.hour > 12:
                ending_time_str = f"{ending_time.hour-12}:{ending_time_minute} PM"
            elif ending_time.hour == 12:
                ending_time_str = f"{ending_time.hour}:{ending_time_minute} PM"
            else:
                ending_time_str = f"{ending_time.hour}:{ending_time_minute} AM"

            print(f"{work}: {starting_time_str} -- {ending_time_str}")
            starting_time = ending_time

    return work_groups
