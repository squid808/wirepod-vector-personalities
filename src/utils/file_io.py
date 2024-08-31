import os
import json
import random
import uuid
from datetime import datetime

# Hardcoded location variable
LOCATION = "" #os.path.dirname(os.path.abspath(__file__))
PERSONALITIES_FOLDER = os.path.join(LOCATION, 'personalities')
BOT_MAPPING_FILE = os.path.join(PERSONALITIES_FOLDER, 'bot_mapping.json')
PERSONALITY_IDS_FILE = os.path.join(PERSONALITIES_FOLDER, 'personality_ids.json')
CONFIGS_FILE_PATH = os.path.join(LOCATION, "config", "configs.json")  #WORK ON THIS NEXT

#region Initialization Functions
def initialize_main():
    # Ensure main personalities folder exists
    create_folder(PERSONALITIES_FOLDER)
    create_json_file(BOT_MAPPING_FILE)
    create_json_file(PERSONALITY_IDS_FILE)
    initialize_backup_folder()

def initialize_region(region):
    region_path = os.path.join(PERSONALITIES_FOLDER, region)
    create_folder(region_path)
    return region_path 

def initialize_bot(region, bot_id):
    region_path = initialize_region(region)
    bot_path = os.path.join(region_path, bot_id)
    create_folder(bot_path)
    return bot_path

def initialize_bot_personality(region, bot_id, personality_id):
    bot_path = initialize_bot(region, bot_id)
    bot_personality_path = os.path.join(bot_path, personality_id)
    create_folder(bot_personality_path)
    create_json_file(os.path.join(bot_personality_path, "intent_index.json"))
    return bot_personality_path
    
def initialize_backup_folder():
    backup_folder_path = os.path.join(PERSONALITIES_FOLDER, 'backup')
    create_folder(backup_folder_path)
    return backup_folder_path
#endregion

#region Utility Functions
def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def check_file_exists(file_path):
    return os.path.exists(file_path)

def create_json_file(file_path):
    if not check_file_exists(file_path):
        with open(file_path, 'w') as f:
            json.dump({}, f)

def load_json_file(file_path):
    if not check_file_exists(file_path):
        return {}
    with open(file_path, 'r') as f:
        return json.load(f)

def update_json_file(file_path, data):
    current_data = load_json_file(file_path)
    #TODO update this logic a bit more
    if type(current_data) is list:
        current_data = data
    else:
        current_data.update(data)
    with open(file_path, 'w') as f:
        json.dump(current_data, f, indent=4)
#endregion

#region Path Handlers
def get_personalities_path(region, bot_id, personality_id):
    return os.path.join(PERSONALITIES_FOLDER, region, bot_id, personality_id)

def get_intent_index_path(region, bot_id, personality_id):
    return os.path.join(get_personalities_path(region, bot_id, personality_id), 'intent_index.json')

def get_response_file_path(region, bot_id, personality_id, response_id):
    return os.path.join(get_personalities_path(region, bot_id, personality_id), f'{response_id}.json')

def get_config_file_path():
    return CONFIGS_FILE_PATH
#endregion

#region Config File
def load_config_file():
    if check_file_exists(CONFIGS_FILE_PATH):
        with open(CONFIGS_FILE_PATH, 'r') as f:
            return json.load(f)

def get_custom_intents_file_path():
    config = load_config_file()
    if config.get('custom_intents_file_path'):
        return config.get('custom_intents_file_path')
    
def get_open_ai_key():
    config = load_config_file()
    if config.get('openai_api_key'):
        return config.get('openai_api_key')
    
def get_custom_intents_file():
    """
    Returns: the loaded json
    """
    custom_intents_file_path = get_custom_intents_file_path()
    if check_file_exists(custom_intents_file_path):
        with open(custom_intents_file_path, 'r') as f:
            return json.load(f)
        
def save_custom_intent(intent):
    custom_intents = get_custom_intents_file()
    custom_intents.append(intent)
    update_json_file(get_custom_intents_file_path(), custom_intents)
#endregion

#region Personality Management
# def list_personalities():
#     personalities_path = os.path.join(LOCATION, 'personalities', 'personality_ids.json')
#     personality_data = load_json_file(personalities_path)
#     return [{"id": key, "name": value.get("short_name", "")} for key, value in personality_data.items()]

def get_personality(personality_id):
    personality_data = load_json_file(PERSONALITY_IDS_FILE)
    return personality_data.get(personality_id, None)

def save_personality(personality_details):
    personality_data = load_json_file(PERSONALITY_IDS_FILE)
    new_id = uuid.uuid4().hex[:15]
    
    # make sure there are no uuid collisions
    while new_id in personality_data:
        new_id = uuid.uuid4().hex[:15]
    
    personality_data[new_id] = personality_details
    update_json_file(PERSONALITY_IDS_FILE, personality_data)
    return new_id

# def update_personality(personality_id, updated_details):
#     personality_ids_path = os.path.join(LOCATION, 'personalities', 'personality_ids.json')
#     personality_data = load_json_file(personality_ids_path)
#     personality_data[personality_id] = updated_details
#     update_json_file(personality_ids_path, personality_data)

# def remove_personality(personality_id):
#     personalities_path = os.path.join(LOCATION, 'personalities', 'personality_ids.json')
    
#     # Load and back up the personality
#     personality_data = load_json_file(personalities_path)
#     removed_personality = personality_data.pop(personality_id, None)
    
#     if removed_personality:
#         backup_path = os.path.join(LOCATION, 'backup', f"{personality_id}.json")
#         create_folder(os.path.dirname(backup_path))
#         with open(backup_path, 'w') as f:
#             json.dump(removed_personality, f, indent=4)

#     # Update the personality list
#     update_json_file(personalities_path, personality_data)
#endregion

#region Bot Personality Mapping
def get_bot_personality_id(bot_id):
    bot_mapping = load_json_file(BOT_MAPPING_FILE)
    return bot_mapping.get(bot_id, {}).get('personality_id', None)

def get_bot_personality(bot_id):
    bot_personality_id = get_bot_personality_id(bot_id)
    return get_personality(bot_personality_id)

def save_bot_personality_mapping(bot_id, personality_id):
    bot_mapping = load_json_file(BOT_MAPPING_FILE)
    
    if bot_id not in bot_mapping:
        bot_mapping[bot_id] = {"history": []}
    
    previous_id = bot_mapping[bot_id].get('personality_id', None)
    history_entry = {"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "previous_id": previous_id}
    
    bot_mapping[bot_id]['history'].append(history_entry)
    bot_mapping[bot_id]['personality_id'] = personality_id
    
    update_json_file(BOT_MAPPING_FILE, bot_mapping)
#endregion

#region Intent and Response Management
def get_response(region, bot_id, personality_id, intent):
    # TODO: Increment the counter 
    responses = get_responses(region, bot_id, personality_id, intent)
    return random.choice(responses) if responses else None

def check_intent_index_exists(region, bot_id, personality_id):
    index_intent_path = get_intent_index_path(region, bot_id, personality_id)
    if not check_file_exists(index_intent_path):
        create_json_file(index_intent_path)
    return index_intent_path

def get_responses(region, bot_id, personality_id, intent):
    index_data_path = check_intent_index_exists(region, bot_id, personality_id)
    intent_index = load_json_file(index_data_path)
    # I think we need to pick an intent at random here, and then proceed.
    intent_id = intent_index.get(intent) #['response_file']
    if intent_id:
        response_file_id = intent_id['response_file']
        response_file_path = get_response_file_path(region, bot_id, personality_id, response_file_id)
        intent_index[intent]["times_used"] += 1
        update_json_file(index_data_path, intent_index)

        # response_file_path = get_response_file_path(region, bot_id, personality_id, intent_id)
        responses = load_json_file(response_file_path).get("responses", [])
        return responses # if responses else None
    else:
        return None

def save_intent_responses(region, bot_id, personality_id, intents, responses):
    response_file_id = uuid.uuid4().hex[:15]
    response_file_path = get_response_file_path(region, bot_id, personality_id, response_file_id)

    if not check_file_exists(response_file_path):
        create_json_file(response_file_path)

    # Append new responses to the file
    response_data = load_json_file(response_file_path)
    
    if "responses" not in response_data:
        response_data["responses"] = []
    
    response_data["responses"].extend(responses)
    update_json_file(response_file_path, response_data)
    
    # now update the index
    index_data_path = get_intent_index_path(region, bot_id, personality_id)
    if not check_file_exists(index_data_path):
        create_json_file(index_data_path)
        
    index_data = load_json_file(index_data_path)
    
    for intent in intents:
        index_data[intent] = {
            "response_file": response_file_id,
            "times_used": 0
        }
    
    update_json_file(index_data_path, index_data)
    
    return response_file_id

# def update_intent_mapping(bot_id, intent, region, response_file_id):
#     intent_index_path = get_intent_index_path(bot_id, region)
#     create_json_file(intent_index_path)
    
#     intent_index = load_json_file(intent_index_path)
#     intent_index[intent] = {
#         "response_file": response_file_id,
#         "times_used": 0
#     }
    
#     update_json_file(intent_index_path, intent_index)
#endregion

#region Example Usage
# if __name__ == "__main__":
#     bot_id = "example_bot_001"
#     region = "en_us"
#     intent = "greeting"
#     responses = ["Hello!", "Hi there!", "Greetings!"]

#     # Ensure paths exist
#     create_folder(get_personalities_path(bot_id, region))
    
#     # Check if intent exists
#     if not check_intent_exists(bot_id, intent, region):
#         # Save the responses and update intent mapping
#         response_file_id = save_intent_responses(bot_id, intent, region, responses)
#         update_intent_mapping(bot_id, intent, region, response_file_id)
    
#     # Fetch a random response for the intent
#     random_response = get_random_response(bot_id, intent, region)
#     print(f"Random response: {random_response}")
    
#     # Manage personalities
#     new_personality = {
#         "short_name": "CuriousBot",
#         "description": "A curious and friendly personality."
#     }
#     personality_id = save_personality(new_personality)
#     print(f"Saved personality with ID: {personality_id}")
    
#     # Get bot personality ID and update it
#     current_personality_id = get_bot_personality_id(bot_id)
#     save_bot_personality(bot_id, personality_id)
#endregion