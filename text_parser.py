from functions import *
from text_manager import *

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

# Text Parser Variables

# add_work_parser(text="group: group1, work: work1, time: 10", previous_works=None, break_time=5, work_groups=)
add_work_parser_details = (f"g: {colored("group_name", WORK_GROUPS_COLOR)}, w: {colored("work_name", WORK_COLOR)}"
                           f", t: {colored("time_in_minutes", INSTRUCTIONS_COLOR)}")

# add_group(original_work_groups=work_groups, group_name=name, group_priority=priority)
add_group_parser_details = (f"g: {colored("group_name", WORK_GROUPS_COLOR)}, "
                            f"p: {colored("priority(1-10)", INSTRUCTIONS_COLOR)}")


def add_work_parser(previous_works, break_time, work_groups):
    """
    add_work(previous_works, work_groups, break_time, group=None, name=None, time_for_work=None):
    Expected User Input: group: group_name, work: work_name, time: work_time
    """

    group = None
    work = None
    time = None

    # Gets details from user about work details, if they don't want to add a previously added work
    update_append(f"Format for best results "
                             f"{colored("(g = group, w = work_name, t = time)", INSTRUCTIONS_COLOR)}: "
                             f"{add_work_parser_details}")
    text = prompt_append(f"Please enter {colored("work details", INSTRUCTIONS_COLOR)}: ")

    separated_text = text.split(sep=",")
    if len(separated_text) == 1:
        update_append(colored("Please separate the different sections by a comma next time.", WARNING_COLOR))
    else:
        for text in separated_text:
            if "g" in text:
                split_text = text.split("g")[1:]
                new_text = ""
                for text_segment in split_text:
                    new_text += text_segment
                if new_text.strip(":").strip() != "":
                    group = new_text.strip(":").strip()
            elif "w" in text:
                split_text = text.split("w")[1:]
                new_text = ""
                for text_segment in split_text:
                    new_text += text_segment
                if new_text.strip(":").strip() != "":
                    work = new_text.strip(":").strip()
            elif "t" in text:
                split_text = text.split("t")[1:]
                new_text = ""
                for text_segment in split_text:
                    new_text += text_segment
                if new_text.strip(":").strip() != "":
                    try:
                        time = int(new_text.strip(":").strip())
                    except TypeError:
                        time = None

    if group is None or work is None or time is None:
        update_append("Unable to identify the group name, work name, or the time for the work.")
        update_append("Asking user the remaining details...")

    # Checks if the work added is a previous work. We don't want to append works that already belong
    # in previous works.
    work_exists_in_previous_works = False
    if work is not None and time is not None:
        for previous_work in previous_works:
            if work in previous_work:
                work_exists_in_previous_works = True

    work_groups = add_work(work_groups=work_groups, break_time=break_time, group=group, name=work, time_for_work=time)

    if not work_exists_in_previous_works and work is not None:
        previous_works.append({work: time})

    return_items = {
        "work_groups": work_groups,
        "previously_added_works": previous_works
    }

    return return_items


def add_group_parser(work_groups):

    name = None
    priority = None

    update_append(f"Format for best results: {add_group_parser_details}")
    text = prompt_append(f"Please enter {colored("group details", INSTRUCTIONS_COLOR)}: ")
    # other_text.append(f"Please enter {colored("work details", INSTRUCTIONS_COLOR)}: {text}")

    separated_text = text.split(sep=",")
    separated_text = [text.strip() for text in separated_text]
    if len(separated_text) == 1:
        update_append(colored("Please separate the different sections by a comma.", WARNING_COLOR))
        update_append(f"Expected Format: {add_group_parser_details}")
    else:
        for text in separated_text:
            if "g" in text:
                split_text = text.split("g")[1:]
                new_text = ""
                for text_segment in split_text:
                    new_text += text_segment
                if new_text.strip(":").strip() != "":
                    name = new_text.strip(":").strip()
            elif "p" in text:
                new_text = text.split("p")[1]
                if new_text.strip(":").strip() != "":
                    try:
                        priority = int(new_text.strip(":").strip())
                    except TypeError:
                        priority = None

        if name is None or priority is None:
            update_append("Unable to identify the group name or the priority of the group.")
            update_append("Asking user the remaining details...")

    return add_group(original_work_groups=work_groups, group_name=name, group_priority=priority)
