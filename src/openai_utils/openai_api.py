from enum import Enum
import json
import os
from openai import OpenAI
import re
from utils import file_io

OPENAI_MODEL = "gpt-4o-mini"

class MissingOpenaiKeyError(Exception):
    "The API key for OpenAI is missing. The path expected is project/config/openai_key.json, in the format {\"api_key\": \"KEY_HERE\"}"
    pass

class OpenAIHelper:
    messages = []
    
    def __init__(self):
        # api_key_file = 'config/openai_key.json'
        self.client = self._initialize_client()

    def _initialize_client(self):
        api_key = file_io.get_open_ai_key()
        # if api_key_file and os.path.exists(api_key_file):
        #     with open(api_key_file, 'r') as file:
        #         api_key = json.load(file).get('api_key')
        # else:
        #     raise MissingOpenaiKeyError
        #     #api_key = ''  # for quick testing

        return OpenAI(api_key=api_key)
    
    class Roles(Enum):
        system = 1
        assistant = 2
        user = 3

    def append_message(self, message_role:Roles, content):
        self.messages.append({"role": message_role.name.lower(), "content": content})

    def clean_json_string(self, json_string):
        # https://community.openai.com/t/json-returning-with-json/584818/6
        pattern = r'^```json\s*(.*?)\s*```$'
        cleaned_string = re.sub(pattern, r'\1', json_string, flags=re.DOTALL)
        # cleaned_string = cleaned_string.replace('\n    ','').strip()
        return cleaned_string.strip()

    def call_openai(self, model, max_tokens=1000, max_results=1):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=self.messages,
                max_tokens=max_tokens,
                n=max_results
            )

            results = []
            for choice in response.choices:
                json_content = choice.message.content
                clean_json = self.clean_json_string(json_content)
                try:
                    json_output = json.loads(clean_json)
                    results.append(json_output)
                except json.JSONDecodeError:
                    if isinstance(json_content, str):
                        results.append(json_content)
                    else:
                        print("Invalid JSON output and non-string content.")
            self.messages = []
            return results

        except Exception as e:
            self.messages = []
            print(f"Error: {e}")
            return []

# # Example usage:
# if __name__ == "__main__":
#     helper = OpenAIHelper()

#     # Build messages
#     messages = helper.build_messages(
#         system_content="You are a helpful assistant.",
#         user_content="Generate a phrase."
#     )

#     # Call OpenAI
#     results = helper.call_openai("gpt-4o-mini", messages, max_tokens=1500, max_results=5)
#     print(results)
