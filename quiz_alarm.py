"""Quiz Alarm for EECS496"""

import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pygame
from priv_sets import access_token, course_id
import json
from click import confirm
from plyer import notification


def connection_error():
    print("Connection error!!!", flush=True)
    if send_notification:
        notification.notify(
            title="Connection Failed",
            message="Connection to Canvas failed. Check the terminal for more information.",
            app_name="Quiz Alert",
            timeout=60,
        )
    if play_sound:
        pygame.mixer.init()
        pygame.mixer.music.load("oversimplified-alarm-clock-113180.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)


def play_alarm():

    print("Quiz status changed!!!", flush=True)

    if send_notification:
        notification.notify(
            title="Quiz Status Changed",
            message="The quiz status for the course has changed! Checkout whether the quiz is released or has started NOW!",
            app_name="Quiz Alert",
            timeout=60,
        )

    if play_sound:
        pygame.mixer.init()
        pygame.mixer.music.load("oversimplified-alarm-clock-113180.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)


# play_alarm()


def get_soup_from_url(url):
    try:
        response = requests.get(
            url,
            params={"access_token": access_token},
            timeout=10,
        )
    except Exception:
        connection_error()
        exit(1)
    if response.status_code != 200:
        connection_error()
        exit(1)
    return BeautifulSoup(response.text, "html.parser")


def check_is_working(soup):
    obj = json.loads(str(soup))
    # print(obj)
    if "errors" in obj:
        connection_error()


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


play_sound = confirm(
    "Play alarm sound when quiz status changes?", default=False
)
send_notification = confirm(
    "Trigger system notification when quiz status changes?", default=True
)

if send_notification:
    notification.notify(
        title="Test",
        message="If you see this notification, the quiz alarm's notification system is working properly. ",
        app_name="Quiz Alert",
        timeout=10,
    )

check()
