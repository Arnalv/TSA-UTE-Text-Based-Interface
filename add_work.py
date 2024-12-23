from add_group import add_group


def add_work(work_groups, group=None, name=None, time_for_work=None):
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
