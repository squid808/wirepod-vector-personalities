import json
import os
from openai import OpenAI

class OpenAIHelper:
    def __init__(self, api_key_file=None):
        self.client = self._initialize_client(api_key_file)

    def _initialize_client(self, api_key_file):
        if api_key_file and os.path.exists(api_key_file):
            with open(api_key_file, 'r') as file:
                api_key = json.load(file).get('api_key')
        else:
            api_key = ''  # Replace with your actual API key or handle as needed

        return OpenAI(api_key=api_key)

    def build_messages(self, system_content=None, user_content=None, assistant_content=None):
        messages = []
        if system_content:
            messages.append({"role": "system", "content": system_content})
        if user_content:
            messages.append({"role": "user", "content": user_content})
        if assistant_content:
            messages.append({"role": "assistant", "content": assistant_content})
        return messages

    def call_openai(self, model, messages, max_tokens=1000, max_results=1):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                n=max_results
            )

            results = []
            for choice in response.choices:
                json_content = choice.message.content
                try:
                    json_output = json.loads(json_content)
                    results.append(json_output)
                except json.JSONDecodeError:
                    print("Invalid JSON output.")
            return results

        except Exception as e:
            print(f"Error: {e}")
            return []

# Example usage:
if __name__ == "__main__":
    api_key_file = 'config/openai_key.json'
    helper = OpenAIHelper(api_key_file)

    # Build messages
    messages = helper.build_messages(
        system_content="You are a helpful assistant.",
        user_content="Generate a phrase."
    )

    # Call OpenAI
    results = helper.call_openai("gpt-4o-mini", messages, max_tokens=1500, max_results=5)
    print(results)
