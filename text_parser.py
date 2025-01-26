from functions import *

# Text Parser Variables

# add_work_parser(text="group: group1, work: work1, time: 10", previous_works=None, break_time=5, work_groups=)
add_work_parser_details = "group: group_name, work: work_name, time: 10"

# add_group(original_work_groups=work_groups, group_name=name, group_priority=priority)
add_group_parser_details = "group: group_name, priority: priority(1-10)"


def add_work_parser(previous_works, break_time, work_groups):
    """
    add_work(previous_works, work_groups, break_time, group=None, name=None, time_for_work=None):
    Expected User Input: group: group_name, work: work_name, time: work_time
    """

    return_items = {
        "work_groups": work_groups,
        "previously_added_works": previous_works
    }

    group = None
    work = None
    time = None

    # Only runs the code if previous works is not empty
    check_previous_works = 'n'
    if previous_works:
        # Asks user if they want to add a previously added work
        check_previous_works = yes_or_no("Do you want to add a previously added work to the group (y/n)? ")

    # Runs the code if the user input yes
    if check_previous_works == "y":

        # Displays to the user the options
        count = 0
        for work in previous_works:
            count += 1
            print(f"{count}. {work}")

        # Asks user about their choice
        user_choice = int(input("Which previously added work do you want to add? "))

        # Updates the values accordingly
        for work_name, time in previous_works[user_choice - 1].items():
            # Updates the name
            work = work_name
            # Asks the user if they want to change the time of the given work
            user_choice = yes_or_no(
                prompt="Do you want to change the amount of time this work takes (y/n)? "
            )
            if user_choice == "y":
                new_time = int(input("What do you want to change the time to? "))
            else:
                new_time = time
            # Updates the time
            time = new_time

        # Checks if it is duplicate name and tells user to that duplicate names can't be added if it is a
        # duplicate
        if check_duplicate(work_groups=work_groups, work_name=work):
            print("A work already exists with a name as this previous work.")
            print("The previous work has not been added.")
            return return_items
        else:
            group = input("What group do want to enter this work to? ")

    else:
        print(f"Format for best results: {add_work_parser_details}")
        text = input("Please enter work details: ")

        separated_text = text.split(sep=",")
        if len(separated_text) == 1:
            print("Please separate the different sections by a comma next time.")
        else:
            for text in separated_text:
                if "group" in text:
                    new_text = text.split("group")[1]
                    if new_text.strip(":").strip() != "":
                        group = new_text.strip(":").strip()
                elif "work" in text:
                    new_text = text.split("work")[1]
                    if new_text.strip(":").strip() != "":
                        work = new_text.strip(":").strip()
                elif "time" in text:
                    new_text = text.split("time")[1]
                    if new_text.strip(":").strip() != "":
                        try:
                            time = int(new_text.strip(":").strip())
                        except TypeError:
                            time = None

        if group is None or work is None or time is None:
            print("Unable to identify the group name, work name, or the time for the work.")
            print("Asking user the remaining details...")

    work_exists_in_previous_works = False
    if work is not None and time is not None:
        for previous_work in previous_works:
            if work in previous_work:
                work_exists_in_previous_works = True

    if not work_exists_in_previous_works and work is not None:
        previous_works.append({work: time})

    work_groups = add_work(work_groups=work_groups, break_time=break_time, group=group, name=work, time_for_work=time)

    return_items = {
        "work_groups": work_groups,
        "previously_added_works": previous_works
    }

    return return_items


def add_group_parser(work_groups):

    name = None
    priority = None

    print(f"Format for best results: {add_group_parser_details}")
    text = input("Please enter work details: ")

    separated_text = text.split(sep=",")
    separated_text = [text.strip() for text in separated_text]
    if len(separated_text) == 1:
        print("Please separate the different sections by a comma.")
        print(f"Expected Format: {add_group_parser_details}")
    else:
        for text in separated_text:
            if "group" in text:
                new_text = text.split("group")[1]
                if new_text.strip(":").strip() != "":
                    name = new_text.strip(":").strip()
            elif "priority" in text:
                new_text = text.split("priority")[1]
                if new_text.strip(":").strip() != "":
                    try:
                        priority = int(new_text.strip(":").strip())
                    except TypeError:
                        priority = None

        if name is None or priority is None:
            print("Unable to identify the group name or the priority of the group.")
            print("Asking user the remaining details...")

    return add_group(original_work_groups=work_groups, group_name=name, group_priority=priority)
