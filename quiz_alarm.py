"""Quiz Alarm for EECS496"""

import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pygame
from priv_sets import access_token, course_id
import json
from plyer import notification


def play_alarm():

    print("Quiz status changed!!!", flush=True)
    notification.notify(
        title="Quiz Status Changed",
        message="The quiz status for the course has changed! Checkout whether the quiz is released or has started NOW!",
        app_name="Quiz Alert",
        timeout=60,
    )

    pygame.mixer.init()
    pygame.mixer.music.load("oversimplified-alarm-clock-113180.mp3")
    pygame.mixer.music.play()


play_alarm()


def get_soup_from_url(url):
    response = requests.get(
        url,
        params={"access_token": access_token},
        timeout=10,
    )
    return BeautifulSoup(response.text, "html.parser")


def check_is_working(soup):
    obj = json.loads(str(soup))
    # print(obj)
    if "errors" in obj:
        print("Error!!!")
        play_alarm()
        while pygame.mixer.music.get_busy() == True:
            continue


def get_all_quiz():
    soup = get_soup_from_url(
        f"https://umich.instructure.com/api/v1/courses/{course_id}/quizzes"
    )
    check_is_working(soup)
    # print(json.loads(str(soup)))
    return json.loads(str(soup))


def check():
    old = get_all_quiz()
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"Checking ... {current_time}")
        new = get_all_quiz()
        if new != old:
            play_alarm()
        old = new
        time.sleep(20)


check()
