#!/usr/bin/env python3

import datetime
import logging
import os
import webbrowser
from pathlib import Path
from time import sleep

import pyautogui

logging.basicConfig(level=logging.INFO)


class Recorder:
    """
    This class is responsible for recording the Zoom meeting.
    """

    def __init__(self, args):
        self.test = args.test
        self.zoom_dir = Path(args.zoom_dir)
        if not self.zoom_dir.is_file():
            logging.error('Invalid path for Zoom.exe')
            exit(1)
        if args.start_time:
            self.start_time = args.start_time
            hour_minute = args.start_time.split(":")
            if len(hour_minute) != 2:
                logging.error('Invalid start time')
                exit(1)
            else:
                try:
                    self.start_hour = int(hour_minute[0])
                    self.start_minute = int(hour_minute[1])
                except ValueError:
                    logging.error('Invalid start time')
                    exit(1)
        else:
            self.start_time = False
        self.record_time_minutes = 0.2 if self.test else args.record_time
        self.record_time = 60 * self.record_time_minutes
        if args.link:
            self.meeting_link = args.link
        else:
            self.meeting_id = args.id
            self.meeting_password = args.pw

    def record(self):
        if self.test:
            self.test_run()
        else:
            if self.start_time:
                while self.wait():
                    sleep(60)
            else:
                logging.info('Starting now')
            if self.meeting_link:
                self.start_meeting_link()
            else:
                self.start_meeting_id()
        logging.info('Joined meeting')
        self.record_screen()
        self.leave_meeting()
        logging.info('Session closed')

    def test_run(self):
        logging.info('Test run started')
        webbrowser.open('https://zoom.us/test')
        logging.info('Opening browser')
        sleep(5)
        try:
            x, y = pyautogui.locateCenterOnScreen(
                './images/test-meeting.png')
        except (pyautogui.ImageNotFoundException, TypeError):
            logging.info('Searching for button with german language')
            try:
                x, y = pyautogui.locateCenterOnScreen(
                    './images/test-meeting-ger.png')
            except (pyautogui.ImageNotFoundException, TypeError):
                logging.error('Image for test-meeting not found')
                exit(1)
        pyautogui.click(x, y)
        logging.info('Joining test meeting')
        sleep(10)

    def wait(self):
        time_now = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        hour_now = int(time_now.strftime("%H"))
        minute_now = int(time_now.strftime("%M"))
        diff = (self.start_hour - hour_now) * 60 + (self.start_minute - minute_now)
        if diff > 0:
            logging.info(f'Waiting {diff} minutes from now')
            return True
        else:
            return False

    def start_meeting_link(self):
        logging.info('Joining meeting with link')
        webbrowser.open(self.meeting_link)
        sleep(10)

    def start_meeting_id(self):
        logging.info('Joining meeting with ID and password')
        os.system(f"start {self.zoom_dir}")
        sleep(10)
        try:
            x, y = pyautogui.locateCenterOnScreen('./images/join-button.png')
        except (pyautogui.ImageNotFoundException, TypeError):
            logging.error('Image for join-button not found')
            exit(1)
        pyautogui.click(x, y)
        sleep(1)
        pyautogui.write(self.meeting_id)
        pyautogui.press('enter')
        sleep(1)
        pyautogui.write(self.meeting_password)
        pyautogui.press('enter')

    def record_screen(self):
        pyautogui.hotkey('alt', 'f9')
        if self.record_time_minutes % 1 == 0:
            logging.info(f'Recording started [{self.record_time_minutes} min]')
        else:
            logging.info(f'Recording started [{self.record_time} secs]')
        sleep(self.record_time)
        pyautogui.hotkey('alt', 'f9')
        logging.info('Recording stopped')

    def leave_meeting(self):
        logging.info('Leaving meeting')
        pyautogui.hotkey('alt', 'q')
        pyautogui.press('enter')
