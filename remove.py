

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
