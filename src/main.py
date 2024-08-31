#!/usr/bin/env python3

import os
import platform
import sys

def set_pythonpath():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Points to 'package' directory

    # Check the OS and set the appropriate PYTHONPATH
    if platform.system() == 'Windows':
        os.environ['PYTHONPATH'] = f"{project_root};{os.environ.get('PYTHONPATH', '')}"
    else:  # Assume Linux/macOS
        os.environ['PYTHONPATH'] = f"{project_root}:{os.environ.get('PYTHONPATH', '')}"

    # Optionally append to sys.path to ensure imports work in the current session
    if project_root not in sys.path:
        sys.path.append(project_root)

# Call this function at the start of your script
set_pythonpath()

import argparse
from request_handler import handle_request

# Ensure src directory is in the import path
# sys.path.insert(0, 'src')

def main(bot_serial, speech_text, intent_name, locale):
    handle_request(bot_serial, speech_text, intent_name, locale)

def parse_args(args):
    parser = argparse.ArgumentParser(description="The main function to be called for Vector Personalities")
    parser.add_argument("bot_id", help="The serial number of the Vector bot.")
    parser.add_argument("speech_text", help="The text spoken and interpreted by the user")
    parser.add_argument("intent", help="The name of the wirepod intent being called")
    parser.add_argument("locale", help="The locale for the wirepod server")
    return parser.parse_args(args)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.bot_id, args.speech_text, args.intent, args.locale)