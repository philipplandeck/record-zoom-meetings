#!/usr/bin/env python3
import logging
import os
import webbrowser
from datetime import datetime
from time import sleep

import pyautogui

logging.basicConfig(level=logging.INFO)


class Recorder:
    def __init__(self, args):
        if args.link:
            self.meeting_link = args.link
        else:
            self.meeting_id = args.id
            self.meeting_password = args.pw

        self.zoom_dir = args.zoom_dir
        if not self.zoom_dir.is_file():
            logging.error('Invalid Zoom path')
            exit(1)

        if args.start_time:
            self.start_time = args.start_time
            try:
                hour_minute = args.start_time.split(":")
                if len(hour_minute) != 2:
                    raise ValueError
                self.start_hour = int(hour_minute[0])
                self.start_minute = int(hour_minute[1]) - 1
            except ValueError:
                logging.error('Invalid start time')
                exit(1)
        else:
            self.start_time = None

        self.record_time = args.record_time

    def record(self):
        if self.start_time:
            while self.wait():
                sleep(60)
        logging.info('Session started')
        if self.meeting_link:
            self.start_meeting_link()
        else:
            self.start_meeting_id()
        self.record_screen()
        self.leave_meeting()
        logging.info('Session closed')

    def wait(self):
        hour = int(datetime.now().strftime("%H"))
        minute = int(datetime.now().strftime("%M"))
        diff = (self.start_hour - hour) * 60 + (self.start_minute - minute)
        if diff > 0:
            logging.info(f'Waiting until {self.start_time} ({diff} minutes)')
            return True
        else:
            return False

    def start_meeting_link(self):
        logging.info('Joining meeting via link')
        webbrowser.open(self.meeting_link)
        sleep(10)

    def start_meeting_id(self):
        logging.info('Joining meeting via ID and password')
        os.system(f"start {self.zoom_dir}")
        sleep(10)
        try:
            x, y = pyautogui.locateCenterOnScreen('./images/join-button.png')
        except (pyautogui.ImageNotFoundException, TypeError):
            logging.error('Image join-button.png not found')
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
        logging.info(f'Recording started [{self.record_time} minutes]')
        sleep(self.record_time * 60)
        pyautogui.hotkey('alt', 'f9')
        logging.info('Recording stopped')

    def leave_meeting(self):
        logging.info('Leaving meeting')
        pyautogui.hotkey('alt', 'q')
        pyautogui.press('enter')
