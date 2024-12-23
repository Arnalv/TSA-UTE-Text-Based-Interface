from datetime import datetime, timedelta

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
