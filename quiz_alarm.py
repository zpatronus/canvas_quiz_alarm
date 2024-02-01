"""Quiz Alarm for EECS496"""

import re
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pygame

# TODO
# Log into canvas, open "inspect" (F12), find a tab named "Application", get into Storage->Cookies->https://umich...
# Copy the "value" of the cookie with "name"="canvas_session", and paste it here
value = "PASTE IT HERE"

# TODO
# Get into the Quiz page, copy the url, and paste it here.
# e.g. "https://umich.instructure.com/courses/653106/quizzes"
url = "https://umich.instructure.com/courses/653106/quizzes"

if len(value) < 30 or len(url) < 30:
    print("在quiz_alarm.py中输入value和url变量")
    exit(0)

print("检测第几周的quiz？输入阿拉伯数字：", end="")
week = input()
print(
    "Quiz 发布了吗？输入0：还未发布，则检测Quiz是否发布；1：发布了，"
    "则检测Quiz是否开始   ",
    end="",
)
is_after = input()

cookies = {
    "canvas_session": value,
}


def play_alarm():
    pygame.mixer.init()
    pygame.mixer.music.load("oversimplified-alarm-clock-113180.mp3")
    pygame.mixer.music.play()


def get_soup_from_url(url):
    response = requests.get(
        url,
        cookies=cookies,
        timeout=10,
    )
    return BeautifulSoup(response.text, "html.parser")


def check_is_working(soup):
    matches = soup.find_all(string=re.compile("History"))
    week_string = [re.search("History", match).group(0) for match in matches]
    if len(week_string) != 1:
        print("Error!!!")
        play_alarm()
        while pygame.mixer.music.get_busy() == True:
            continue


def after_open():
    check_is_working(get_soup_from_url(url))
    soup = get_soup_from_url(url)
    line = str(soup)
    key_word = f"Week {week}"

    match = re.search(rf'"Week {week}.*?","html_url":"(.*?)"', line)
    target = ""
    if match:
        target = match.group(1)
    if target == "":
        print("Error!!!")
        play_alarm()
    print(f"Obtained quiz url: {target}")
    key_word = "is locked"
    while 1:
        check_is_working(get_soup_from_url(url))
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"Checking ... {current_time}")

        soup = get_soup_from_url(target)

        matches = soup.find_all(string=re.compile(key_word))
        week_string = [
            re.search(key_word, match).group(0) for match in matches
        ]

        if len(week_string) == 0:
            print("Quiz time!!!")
            play_alarm()
            while pygame.mixer.music.get_busy() == True:
                continue

        time.sleep(20)


def before_open():
    key_word = f"Week {week}"
    while 1:
        check_is_working(get_soup_from_url(url))
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"Checking ... {current_time}")

        soup = get_soup_from_url(url)

        matches = soup.find_all(string=re.compile(key_word))
        week_string = [
            re.search(key_word, match).group(0) for match in matches
        ]

        if len(week_string) > 0:
            print("Quiz time!!!")
            play_alarm()
            while pygame.mixer.music.get_busy() == True:
                continue

        time.sleep(20)


if is_after == "1":
    after_open()
else:
    before_open()
