import os
import re
from wcwidth import wcswidth
from time import sleep

# Schedule and Text Variables
schedule_text = []
other_text = []
text_speed = 0.02


def strip_ansi(text):
    """Removes ANSI escape codes from text."""
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)


def display_animated_text(text):
    for character in text:
        print(character, end="", flush=True)
        sleep(text_speed)
    print()


def prompt_append(prompt):
    for character in prompt:
        print(character, end="", flush=True)
        sleep(text_speed)
    user_input = input()
    other_text.append(f"{prompt}{user_input}")
    return user_input


# def update_append_tutorial_speed(text):
#     global text_speed
#     text_speed = tutorial_speed
#     display_animated_text(text=text)
#     other_text.append(text)
#     text_speed = normal_speed


def update_append(text):
    # print(text)
    display_animated_text(text)
    other_text.append(text)


def show_text():
    global schedule_text, other_text
    os.system('cls')
    half_width = (os.get_terminal_size().columns // 3) * 2
    while len(other_text) <= len(schedule_text):
        other_text.append("")
    schedule_text_length = len(schedule_text)
    other_text_length = len(other_text)
    count = 0
    for index in range(len(other_text)):
        text_left_size = wcswidth(strip_ansi(other_text[index]))

        if index + schedule_text_length >= other_text_length:
            print(f"{other_text[index]}{" "*(half_width-text_left_size)}{schedule_text[count]}")
            count += 1
        else:
            print(other_text[index])


def change_text_speed(speed: float):
    global text_speed
    text_speed = speed
