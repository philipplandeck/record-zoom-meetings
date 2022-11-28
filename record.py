#!/usr/bin/env python3
"""
Record a Zoom meeting via NVIDIA ShadowPlay by using its Invitation Link or
Meeting-ID and Password.

See "python3 record.py -h" for more information.

Copyright (c) 2022 Philipp Landeck
"""
import argparse
import os
import sys
from pathlib import Path

from Recorder import Recorder


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Record a Zoom meeting via NVIDIA ShadowPlay by using its "
        "Invitation Link or Meeting-ID and Password.")
    invitation_type = parser.add_mutually_exclusive_group(required=True)
    invitation_type.add_argument(
        "--link",
        dest="link",
        type=str,
        help="Invitation link")
    invitation_type.add_argument(
        "--id",
        dest="id",
        type=str,
        help="Meeting-ID")
    parser.add_argument(
        "--pw",
        dest="pw",
        required='--id' in sys.argv,
        type=str,
        help="Password")
    parser.add_argument(
        "--zoom-dir",
        dest="zoom_dir",
        type=Path,
        default=Path(rf"{os.path.expanduser('~')}\AppData\Roaming\Zoom\bin\Zoom.exe"),
        help="Path of Zoom.exe if not default")
    parser.add_argument(
        "--start-time",
        dest="start_time",
        type=str,
        help="Start time of the meeting in the format HH:MM")
    parser.add_argument(
        "--record-time",
        dest="record_time",
        type=int,
        default=100,
        help="Record time in minutes")
    return parser.parse_args()


def main():
    args = parse_arguments()
    Recorder(args).record()


if __name__ == '__main__':
    main()
