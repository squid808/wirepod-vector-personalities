#!/usr/bin/env python3

import sys
import os
from openai.openai_api import call_openai  # Assuming this method exists in openai_helpers.py

# Ensure the openai_helpers.py module can be found
sys.path.append(os.path.join(os.path.dirname(__file__), 'openai'))

def main():
    # Ensure the correct number of arguments are provided
    if len(sys.argv) != 5:
        print("Usage: python personality_main.py <botSerial> <speechText> <intentName> <locale>")
        sys.exit(1)

    # Parse positional arguments
    bot_serial = sys.argv[1]
    speech_text = sys.argv[2]
    intent_name = sys.argv[3]
    locale = sys.argv[4]

    # Example debug logging (optional)
    print(f"Bot Serial: {bot_serial}")
    print(f"Speech Text: {speech_text}")
    print(f"Intent Name: {intent_name}")
    print(f"Locale: {locale}")

    # Call a method from openai_helpers.py (from the openai directory)
    result = call_openai(bot_serial, speech_text, intent_name, locale)

    # Output the result (or process it as needed)
    print(result)

if __name__ == "__main__":
    main()
