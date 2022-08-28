#!/usr/bin/env python3
"""
This tool allows you to record a Zoom meeting at a specific time by using its
meeting-ID and password or a link to the meeting.

Copyright (c) 2022 Philipp Landeck
"""

import argparse
import os

from Recorder import Recorder


def parse_arguments():
    # Default path of Zoom
    zoom_path = rf"{os.path.expanduser('~')}\AppData\Roaming\Zoom\bin\Zoom.exe"

    # Structured as a decision tree
    parser = argparse.ArgumentParser(
        description="This tool allows you to record a Zoom meeting at a specific time "
        "by using its meeting-ID and password or a link to the meeting.")
    parser.add_argument(
        "--zoom-dir",
        dest="zoom_dir",
        type=str,
        default=zoom_path,
        help="Enter the path of Zoom.exe on your device if not default")
    parser.add_argument(
        "--start-time",
        dest="start_time",
        type=str,
        help="Enter the start time of the meeting in the format HH:MM")
    parser.add_argument(
        "--record-time",
        dest="record_time",
        type=float,
        default=100,
        help="Enter the time to record in minutes")
    test_or_normal = parser.add_mutually_exclusive_group(required=True)
    test_or_normal.add_argument(
        "--test",
        dest="test",
        action='store_true',
        help="Record a test meeting")
    link_or_id = test_or_normal.add_mutually_exclusive_group()
    link_or_id.add_argument(
        "--link",
        dest="link",
        type=str,
        help="Enter invitation link")
    login_with_id = link_or_id.add_argument_group()
    login_with_id.add_argument(
        "--id",
        dest="id",
        type=str,
        help="Enter meeting-ID")
    login_with_id.add_argument(
        "--pw",
        dest="pw",
        type=str,
        help="Enter password")
    return parser.parse_args()


def main():
    args = parse_arguments()
    Recorder(args).record()


if __name__ == '__main__':
    main()
