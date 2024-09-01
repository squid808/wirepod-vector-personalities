from openai_utils.response_generator import generate_responses_from_openai
from personality.personality_generator import print_natural_language
from personality import personality_prompt_handler
from utils import file_io
from vector_sdk_interface import say_text
import wirepod
import wirepod.intents

def handle_request(bot_serial, speech_text, intent_name, locale):
    
    file_io.initialize_main()
    
    bot_personality_id = file_io.get_bot_personality_id(bot_serial)
    
    # check for personality prompts
    # TODO - tie this to intents
    if intent_name in personality_prompt_handler.combine_personality_prompts():
        personality_prompt_handler.handle_personality_prompts(bot_serial, speech_text, intent_name, locale)
    
    elif not bot_personality_id:
        say_text(bot_serial, "I'm sorry, I don't have a personality configured just yet.")
    
    else:
        response = file_io.get_response(locale, bot_serial, bot_personality_id, intent_name)
        if response:
            say_text(bot_serial, response)
        else:
            handle_new_response(bot_serial, speech_text, intent_name, locale, bot_personality_id)

def handle_new_response(bot_serial, speech_text, intent_name, locale, bot_personality_id):
    create_new_response(bot_serial, speech_text, intent_name, locale, bot_personality_id)
    response = file_io.get_response(locale, bot_serial, bot_personality_id, intent_name)
    if response:
        say_text(response)
    elif not bot_personality_id:
        say_text(bot_serial, "Can't respond to that, I had an oopsie.")
    
def create_new_response(bot_serial, speech_text, intent_name, locale, bot_personality_id):
    # load the personality first
    personality = file_io.get_personality(bot_personality_id)
    
    # create new responses based on the question
    natural_language_personality = print_natural_language(personality)
    results = generate_responses_from_openai(natural_language_personality, speech_text)[0]
    keywords = results["keywords"]
    responses = results["responses"]
    intent = results["intent"]
    file_io.save_intent_responses(locale, bot_serial, bot_personality_id, intent, responses)
    
    #TODO - need to update the intents index file for wirepod
    wirepod.intents.add_custom_intent(intent, intent, keywords, intent)
    # new_intent=wirepod_api.add_custom_intent(intent, intent, keywords, intent)
    
    return results

# if __name__ == "__main__":
#     # create_new_response("0aa12345", "what do you think of me now", "override_unhandled_for_personalities", "en_US", "")
#     personality = """
# This personality has a peculiar habit of quoting lines from 1980s action movies, and is from the United States. 
# Generally, it is calm and grateful. Occasionally, it might display a frivolous tone, especially during specific 
# moments. The topic of entertainment is 92% likely to come up.
# """
#     results = generate_responses_from_openai(personality, "what do you think of me now")
#     print(results)

