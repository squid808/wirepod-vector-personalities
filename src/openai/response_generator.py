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

Step 1: Analyze the user’s input and determine its characteristics. Return the results in JSON format, as specified:
{
    "analysis": {
        "inferred_question": "<cleaned-up user input>",
        "utterance_type": "<chosen utterance type>",
        "expectations": ["<chosen expectation>"],
        "tones": ["<chosen tone>"],
        "topic_alignment": "<chosen topic>",
        "specific_references": ["<reference1>", "<reference2>", "<reference3>"]
    }
}

Step 2: Use the result of the analysis, the personality profile provided, and the user input to generate a 
contextual response.

Step 3: Ensure the response fits the personality profile, and reflect the characteristics of the user input 
determined in the analysis phase. 
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

Return the result in JSON format with the key "analysis". The JSON structure should look like this:

{
    "analysis": {
        "inferred_question": "<cleaned-up user input>",
        "utterance_type": "<chosen utterance type>",
        "expectations": ["<chosen expectation>"],
        "tones": ["<chosen tone>"],
        "topic_alignment": "<chosen topic>",
        "specific_references": ["<reference1>", "<reference2>", "<reference3>"]
    }
}
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

Return the result in JSON format with the following structure:

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

# User Message
user_message = """
Personality Profile: {personality_profile}

User Input: {user_input}
"""

# # Combining everything into one structure
# def create_api_messages(personality_profile, user_input):
#     # User message passed with personality profile and input
#     user_message_filled = f"""
#     Personality Profile: {personality_profile}
    
#     User Input: {user_input}
#     """
    
#     return {
#         'system_message': system_message,
#         'generate_analysis_message': generate_analysis_message,
#         'generate_responses_message': generate_responses_message,
#         'user_message': user_message_filled
#     }

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
