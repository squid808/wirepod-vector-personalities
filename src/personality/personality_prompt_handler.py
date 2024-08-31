from utils import file_io
from openai_utils import refine_personality
from personality import personality_generator
import vector_sdk_interface

create_personality_prompt_text = [
    'create a personality', 'create personality', 'create your personality', 'new personality'
]

get_personality_prompt_text = [
    'what\'s your personality', 'what is your personality', 'tell me your personality', 'get personality'
]

list_personality_prompt_text = [
    'list your personalities', 'list personalities', 'what other personalities'
]

change_personality_prompt_text = [
    'change your personality', 'change personality', 
    'update your personality', 'update personality', 
    'set your personality', 'set personality'
]

INTENT_CREATE = "intent_create_personality"
INTENT_GET = "intent_get_personality"
INTENT_LIST = "intent_list_personalities"
INTENT_CHANGE = "intent_change_personality"

def combine_personality_prompts():
    # return [*create_personality_prompt_text, *get_personality_prompt_text, *list_personality_prompt_text, *change_personality_prompt_text]
    return [INTENT_CREATE, INTENT_CHANGE, INTENT_GET, INTENT_LIST]

def handle_personality_prompts(bot_serial, speech_text, intent, locale):
    if intent == INTENT_CREATE:
        try:
            #create and save the personality
            personality_profile = personality_generator.generate_personality_profile()
            revised_personality_details = refine_personality.create_quirk_messages(personality_profile)
            personality_profile['personality_quirk']['selected'] = revised_personality_details['quirk']
            personality_profile['nickname'] = revised_personality_details['nickname']
            personality_id = file_io.save_personality(personality_profile)
            
            #associate the personality to the bot
            file_io.save_bot_personality_mapping(bot_serial, personality_id)
            
            #create the folder structure
            file_io.initialize_bot_personality(locale, bot_serial, personality_id)
            
            vector_sdk_interface.say_text(bot_serial, "Success! You're now looking at " + personality_profile['nickname'])
        except:
            vector_sdk_interface.say_text(bot_serial, "Uh-oh, there was an error creating a new personality. I think that means I'm having an identity crisis!")
    
    elif intent == INTENT_GET:
        personality_profile = file_io.get_bot_personality(bot_serial)
        if personality_profile:
            vector_sdk_interface.say_text(bot_serial, "My personality is " + personality_profile['nickname'])
        else:
            vector_sdk_interface.say_text(bot_serial, "Hmm, I don't seem to have a personality right now. Nothing specific, anyways.")
        pass
    
    elif intent == INTENT_LIST:
        pass
    
    elif intent == INTENT_CHANGE:
        pass