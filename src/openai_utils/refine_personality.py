from openai_utils.openai_api import OPENAI_MODEL, OpenAIHelper

# System message
system_message = """You are refining a statement related to a personality profile. You are to first update a personality quirk.
Then, you are to come up with a name for the personality. Follow instructions closely. You will provide responses by updating
a json object as follows: {"quirk": "", "nickname": ""} DO NOT FORMAT IN MARKDOWN. Json should be in a single line, with no extra
padding of spaces, tabs, or new lines."""

quirk_refinement = """You are adjusting a personality profile where there is a primary, standout personality quirk
(in personality_quirk.selected). The quirk provide is generic. Your first job is to come up with
a more specific version of that quirk to be referenced in the future. The quirk should be something that can be represented
by way of verbal communications.

The quirk you received may be general or abstract, and your task is to make it more specific if possible. For example:
- If the quirk mentions an animal sound, specify which animal makes that sound.
- If it mentions a time period or place, specify the exact time period or location.
- If the quirk does not need further clarification, you may return the provided quirk as-is.
- If the quirk mentiones a phsyical attribute, adjust it to also include how that influences their speech patterns.

Provide the result as the value to the quirk field in the results json, as a single string.
"""

personality_nickname_message = """Review the entire personality profile, the baseline attributes, and the quirk. Then, with that
information, update the nickname value to be a 3-5 nickname for this kind of personality. Try to make it somewhat unique
and amusing to remember, erring on the side of amusing and quirky over accuracy and representing profile contents. For example, you
might choose a name like 'The Hyper Penguin King' for a negative but excitable personality who really likes arctic animals.

Provide the result as the value to the nickname field in the results json."""

return_json_message = """Return the results json object as the output of the query. Ensure that the json is a valid json structure,
and is viable to be loaded in python via json.loads(). The overall json structure should be exactly as described."""

# User message
user_message_quirk = """
Personality Profile: {personality_profile}
"""
    
def create_quirk_messages(personality_profile):
    user_message_filled = f"""Generic Quirk: {personality_profile}"""
    
    helper = OpenAIHelper()

    # Build messages
    helper.append_message(OpenAIHelper.Roles.system, content=system_message)
    helper.append_message(OpenAIHelper.Roles.user, content=user_message_filled)
    helper.append_message(OpenAIHelper.Roles.assistant, content=quirk_refinement)
    helper.append_message(OpenAIHelper.Roles.assistant, content=personality_nickname_message)
    helper.append_message(OpenAIHelper.Roles.assistant, content=return_json_message)

    # Call OpenAI
    results = helper.call_openai(OPENAI_MODEL, max_tokens=500, max_results=1)
    return results[0]

# # Example use
# if __name__ == "__main__":
#     generic_quirk = "likes to make unusual animal sounds"

#     quirk_messages = create_quirk_messages(generic_quirk)
#     print(quirk_messages)