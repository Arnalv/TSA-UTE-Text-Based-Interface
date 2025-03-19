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


def add_work_parser(previous_works, break_time, work_groups, user_inputs):
    """
    add_work(previous_works, work_groups, break_time, group=None, name=None, time_for_work=None):
    Expected User Input: group: group_name, work: work_name, time: work_time
    """

    group = user_inputs["inputs_needed"]["group_name"]
    work = user_inputs["inputs_needed"]["work_name"]
    time = user_inputs["inputs_needed"]["time_of_work"]

    if group == "none" or work == "none" or time == "none":
        update_append("Unable to identify the group name, work name, or the time for the work.")
        update_append("Asking user the remaining details...")

    return_items = add_work(work_groups=work_groups, break_time=break_time, group=group, name=work,
                            time_for_work=time, previous_works=previous_works)
    work_groups = return_items["work_groups"]
    previous_works = return_items["previous_works"]

    return_items = {
        "work_groups": work_groups,
        "previously_added_works": previous_works
    }

    return return_items


def add_group_parser(work_groups, user_inputs):

    name = user_inputs["inputs_needed"]["group_name"]
    priority = user_inputs["inputs_needed"]["priority_number"]

    if name == "none" or priority == "none":
        update_append("Unable to identify the group name or the priority of the group.")
        update_append("Asking user the remaining details...")

    return add_group(original_work_groups=work_groups, group_name=name, group_priority=priority)
