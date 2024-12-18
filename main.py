from datetime import datetime

# default settings
starting_work_time = None
ending_work_time = None
break_time = 10

# starting variables

# Formatted like {work_group_name: [priority, {work_name : time_for_work}]}
# work_groups = {}

"""
def validator(prompt, ):
"""


def add_work(group=None, name=None, time_for_work=None):
    # Takes input from user if not already provided
    if group is None:
        if work_groups != {}:
            # Shows the options to choose a group
            work_group_number = 0
            for key, value in work_groups.items():
                work_group_number += 1
                print(f"{work_group_number}. {key}")
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
                add_group()
                add_work()
                return
        else:
            print("No work groups detected.")
            print("You will need to add a work group first.")
            add_group()
            add_work()
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
            add_group(group_name=group)

    # Add the work to the specific group
    else:
        work_groups[group].append({name: time_for_work})
        print(f"Work '{name}' has been added to the work group '{group}'.")

    print(work_groups)


def add_group(group_name=None, group_priority=None):
    """
    # TODO create a file and store the information
    with open(file="./previous_schedule_tracker", mode="w") as file:
        file.
    """

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


"""
Testing Purposes: To test the show_schedule function, the work_groups class has a pre-defined value.
"""
work_groups = {"A": [5, {"HW": 20}], "B": [9, {"HW2": 30}]}


def show_schedule():
    global work_groups
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
        del work_groups[priority_work_group]
        copy_work_groups[priority_work_group] = priority_works

    print(priority_ordered_work)
    """
    time = datetime.now()
    hour_and_minutes = [time.hour, time.minute]
    """
    work_groups = copy_work_groups


def print_commands():
    # TODO figure out how to clear the screen (ask Arnav)
    print("Here are a list of commands with descriptions:\n"
          "a\n"
          "Adds work to specific group depending on inputs\n\n"
          "r\n"
          "Removes a work from a specific group depending on the inputs\n\n"
          "ag\n"
          "Adds a new group for work\n\n"
          "ch_d\n"
          "Changes default settings such as break time depending on the inputs\n\n"
          "ch_b\n"
          "Allows you to edit specific break times or work times (please remember that adding too much time may cause "
          "the total work time to increase)\n\n"
          "s\n"
          "Shows completed schedule.\n\n"
          "exit\n"
          "Exits application.")


def check_user_input(user_input):
    match user_input:
        case "exit":
            return True
        case "help":
            print_commands()
        case "ag":
            add_group()
        case "a":
            add_work()
        case "s":
            show_schedule()


while True:
    # TODO need to add code on checking for new user
    command = input("Please type 'Help' to see what commands you can use: ").lower()
    if check_user_input(command):
        # store_information()
        break

print(work_groups)
