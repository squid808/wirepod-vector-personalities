from .openai_api import OPENAI_MODEL, OpenAIHelper

utterance_types = [
    'greeting', 'question', 'statement', 'command', 'complaint', 'joke', 'opinion', 
    'observation', 'pop culture quote', 'lyric', 'poetry'
]

expectations = [
    'acknowledge feelings', 'answer question', 'return sentiment', 'give information', 
    'follow command', 'agree or disagree', 'show empathy', 'provide a suggestion', 
    'continue conversation', 'reply in kind'
]

tones = [
    'happy', 'sad', 'neutral', 'joking', 'sarcastic', 'curious', 'playful', 
    'enthusiastic', 'colloquial'
]

topic_alignment = [
    'Science', 'Pop culture', 'History', 'Travel', 'Music', 'Sports', 'Art', 
    'Cooking', 'Reading', 'Movies', 'Technology', 'Fitness', 'Gaming', 
    'Nature', 'Photography', 'Fashion', 'Politics', 'Literature', 'Theater', 
    'Gardening', 'Religion', 'Other'
]

# System message
system_message = """
You are a counterpart for a desktop robot that can receive vocal input and verbalize responses. The user input 
you receive may be inaccurate in spelling, so you need to compensate for phonetics misinterpretation.

Step 1: Analyze the user's input and determine the characteristics of the input.

Step 2: Use the result of the analysis, the personality profile provided, and the user input to generate a 
contextual response.

Step 3: Ensure the response fits the personality profile, and reflect the characteristics of the user input 
determined in the analysis phase. 

DO NOT FORMAT IN MARKDOWN. Json should be in a single line, with no extra padding of spaces, tabs, or new lines.
"""

# Generate Analysis Message
generate_analysis_message = f"""
Analyze the user’s input and determine its characteristics based on the following categories:

1. **Inferred Question**: Clean up the user's input into the most accurate interpretation.
2. **Utterance Types**: Choose from the following list:
{utterance_types}
3. **Expectations**: Choose from the following list:
{expectations}
4. **Tones**: Choose from the following list:
{tones}
5. **Topic Alignment**: Choose from the following list:
{topic_alignment}
6. **Specific References**: Provide up to 3 specific references related to current or historic events, pop culture, 
or specific topics, each in 3 words. Leave blank if not applicable.

Append the results to the JSON results file, with the key "analysis". The JSON structure should look like this:

{{
    "analysis": {{
        "inferred_question": "<cleaned-up user input>",
        "utterance_type": "<chosen utterance type>",
        "expectations": ["<chosen expectation>"],
        "tones": ["<chosen tone>"],
        "topic_alignment": "<chosen topic>",
        "specific_references": ["<reference1>", "<reference2>", "<reference3>"]
    }}
}}
"""

# Keyword Extraction Message
keyword_extraction_message = """
Based on the analysis and the interpreted input, break down these inputs into identifiable 
keywords or key phrases. Results should be as short as possible while remaining largely accurate and unique. 
Full sentences should be avoided if possible. Example Inputs: For an original input of 'what would you do for a 
clowned eye bar' and an interpreted input of 'What would you do for a Klondike bar?', your output 
might include ['what is the meaning of life', 'what is me knee of life', 'what is life's meaning', 
'what is the purpose of life', 'what is life's purpose']. Results are to be all in lower case with apostrophes
as the only accepted punctuation (used for possessive or contraction purposes). Append these result keys to the
results JSON, with the json key of 'keywords', as a list. Include the original interpreted input text in the results.
"""

# Intent Extraction Message
intent_message = """
Consider the keywords created, as well as the question analysis, and come up with a unique string that will be used as
an 'intent'. This should be all lower case, no punctuation. Additonally add some random characters for entropy and to avoid
collision. For example, with the previous questions about the meaning of life, a good intent might be "meaning_of_life_0dy37f".
Append this result to the results JSONS, with the JSON key of 'intent'.
"""

# Generate Responses Message
generate_responses_message = """
You will receive a personality profile in JSON format, along with the user input and context analysis from a 
previous step.

Step 1: Use the personality profile to craft responses. Make sure they fit the personality traits, quirks, and 
regional considerations provided in the profile.

Step 2: Provide responses in the following format:
- One longer, elaborate response that could be a personal observation or an impersonation.
- Seven short retorts, each no more than 1 sentence or 15 words.
- Two responses that are 2-3 sentences long.

All responses must fit the personality profile and match the characteristics from the analysis phase.

Append the results to the JSON results file, with the key "responses", with the following structure:

{
    "responses": [
        "<long response>",
        "<short retort 1>",
        "<short retort 2>",
        "...",
        "<medium-length response 1>",
        "<medium-length response 2>"
    ]
}
"""

return_json_message = """Return the results json object as the output of the query. Ensure that the json is a valid json structure,
and is viable to be loaded in python via json.loads(). The overall json structure should be exactly as described."""

# User Message
user_message = """
Personality Profile: {personality_profile}

User Input: {user_input}
"""

# Combining everything into one structure
def generate_responses_from_openai(personality_profile, user_input):
    helper = OpenAIHelper()

    # Build messages
    helper.append_message(OpenAIHelper.Roles.system, content=system_message)
    helper.append_message(OpenAIHelper.Roles.user, content=user_message.format(personality_profile=personality_profile, user_input=user_input))
    helper.append_message(OpenAIHelper.Roles.assistant, content=generate_analysis_message)
    helper.append_message(OpenAIHelper.Roles.assistant, content=keyword_extraction_message)
    helper.append_message(OpenAIHelper.Roles.assistant, content=generate_responses_message)
    helper.append_message(OpenAIHelper.Roles.assistant, content=intent_message)
    helper.append_message(OpenAIHelper.Roles.assistant, content=return_json_message)

    # Call OpenAI
    results = helper.call_openai(OPENAI_MODEL, max_tokens=2500, max_results=1)
    return results

# # Example use
# if __name__ == "__main__":
#     personality_profile = """
#     This personality has a peculiar habit of quoting lines from 1980s action movies, and is from the United States. 
#     Generally, it is calm and grateful. Occasionally, it might display a frivolous tone, especially during specific 
#     moments. The topic of entertainment is 92% likely to come up.
#     """
    
#     user_input = "What would you do for a Klondike bar?"

#     api_messages = create_api_messages(personality_profile, user_input)
#     print(api_messages)
