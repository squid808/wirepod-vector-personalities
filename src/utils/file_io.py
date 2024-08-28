import os
import json
import random
import uuid
import shutil
from datetime import datetime

# Track default region
region = "en-us"

#region common
def initialize(location):
    personalities_path = os.path.join(location, 'personalities')
    responses_path = os.path.join(personalities_path, 'responses', region)

    create_folder(personalities_path)
    create_folder(responses_path)

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_json_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump({}, f)

def update_json_file(file_path, data):
    current_data = load_json_file(file_path)
    current_data.update(data)
    with open(file_path, 'w') as f:
        json.dump(current_data, f, indent=4)

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def load_json_file(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as f:
        return json.load(f)
#endregion

#region response by bot
def get_bot_response(bot_id, intent):
    personality_id = get_bot_personality_id(bot_id)
    if not personality_id:
        return None
    
    response = get_response(personality_id, intent)
    return response
#endregion

#region personality ids
def get_bot_pesonality_id_mapping_path():
    return os.path.join('personalities', 'bot_mapping.json')

def load_bot_mapping():
    bot_mapping_path = get_bot_pesonality_id_mapping_path()
    return load_json_file(bot_mapping_path)

def get_bot_personality_id(bot_id):
    bot_mapping = load_bot_mapping()
    return bot_mapping.get(bot_id, {}).get('personality_id', None)

def get_bot_personality_history(bot_id):
    bot_mapping = load_bot_mapping()
    return bot_mapping.get(bot_id, {}).get('history', [])

def save_bot_personality(bot_id, personality_id):
    bot_mapping_path = get_bot_pesonality_id_mapping_path()
    bot_mapping = load_bot_mapping()
    
    previous_id = bot_mapping.get(bot_id, {}).get('personality_id', personality_id)
    history_entry = {"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "previous_id": previous_id}
    
    if bot_id not in bot_mapping:
        bot_mapping[bot_id] = {"history": []}
    
    bot_mapping[bot_id]['history'].append(history_entry)
    bot_mapping[bot_id]['personality_id'] = personality_id
    
    update_json_file(bot_mapping_path, bot_mapping)
#endregion

#region personalities
def get_personality(personality_id):
    personality_ids_path = os.path.join('personalities', 'personality_ids.json')
    personality_data = load_json_file(personality_ids_path)
    return personality_data.get(personality_id, None)

def list_personalities():
    personality_ids_path = os.path.join('personalities', 'personality_ids.json')
    personality_data = load_json_file(personality_ids_path)
    return [{"id": key, "name": value.get("short_name", "")} for key, value in personality_data.items()]

def generate_guid():
    return uuid.uuid4().hex[:15]

def save_personality(personality_details):
    personality_ids_path = os.path.join('personalities', 'personality_ids.json')
    personality_data = load_json_file(personality_ids_path)
    
    new_id = generate_guid()
    while new_id in personality_data:
        new_id = generate_guid()
    
    personality_data[new_id] = personality_details
    update_json_file(personality_ids_path, personality_data)
    return new_id

def update_personality(personality_id, updated_details):
    personality_ids_path = os.path.join('personalities', 'personality_ids.json')
    personality_data = load_json_file(personality_ids_path)
    personality_data[personality_id] = updated_details
    update_json_file(personality_ids_path, personality_data)

def remove_personality(personality_id):
    personalities_path = os.path.join('personalities', 'personality_ids.json')
    responses_folder = os.path.join('personalities', 'responses', region)
    
    # Load and back up the personality
    personality_data = load_json_file(personalities_path)
    removed_personality = personality_data.pop(personality_id, None)
    
    if removed_personality:
        backup_path = os.path.join(responses_folder, f"{personality_id}.json")
        with open(backup_path, 'w') as f:
            json.dump(removed_personality, f, indent=4)
        
        # Rename the personality folder
        personality_folder = os.path.join(responses_folder, removed_personality.get("short_name", ""))
        if os.path.exists(personality_folder):
            shutil.move(personality_folder, f"{personality_folder}.REMOVED")
        
        # Remove from bot mappings
        bot_mapping_path = os.path.join('personalities', 'bot_mapping.json')
        bot_mapping = load_json_file(bot_mapping_path)
        bot_mapping = {bot_id: details for bot_id, details in bot_mapping.items() if details['personality_id'] != personality_id}
        update_json_file(bot_mapping_path, bot_mapping)

    # Update the personality list
    update_json_file(personalities_path, personality_data)
#endregion

#region responses
def create_responses(personality_id, intent, responses):
    responses_folder = os.path.join('personalities', 'responses', region, personality_id)
    response_index_path = os.path.join(responses_folder, 'response_index.json')
    
    # Create folder and response_index.json if not present
    create_folder(responses_folder)
    create_json_file(response_index_path)
    
    response_index = load_json_file(response_index_path)
    
    # Check if intent already exists
    if intent not in response_index:
        # Create a new intent file
        safe_intent_name = f"intent_{intent.replace(' ', '_').lower()}.json"
        intent_file_path = os.path.join(responses_folder, safe_intent_name)
        create_json_file(intent_file_path)
        
        # Update the response_index
        response_index[intent] = {
            "file_path": safe_intent_name,
            "index_key": "responses",
            "times_used": 0
        }
    
    # Append responses to the intent file
    intent_file_path = os.path.join(responses_folder, response_index[intent]["file_path"])
    intent_data = load_json_file(intent_file_path)
    
    if "responses" not in intent_data:
        intent_data["responses"] = []
    
    intent_data["responses"].extend(responses)
    update_json_file(intent_file_path, intent_data)
    update_json_file(response_index_path, response_index)

def list_responses(personality_id: str, intent):
    responses_folder = os.path.join('personalities', 'responses', region, personality_id)
    response_index_path = os.path.join(responses_folder, 'response_index.json')
    
    response_index = load_json_file(response_index_path)
    if intent in response_index:
        intent_file_path = os.path.join(responses_folder, response_index[intent]["file_path"])
        intent_data = load_json_file(intent_file_path)
        return intent_data.get("responses", [])
    
    return []

def get_response(personality_id, intent):
    responses_folder = os.path.join('personalities', 'responses', region, personality_id)
    response_index_path = os.path.join(responses_folder, 'response_index.json')
    
    response_index = load_json_file(response_index_path)
    if intent in response_index:
        intent_file_path = os.path.join(responses_folder, response_index[intent]["file_path"])
        intent_data = load_json_file(intent_file_path)
        responses = intent_data.get("responses", [])
        
        if responses:
            selected_response = random.choice(responses)
            response_index[intent]["times_used"] += 1
            update_json_file(response_index_path, response_index)
            return selected_response
    
    return None

def remove_intent(personality_id, intent):
    responses_folder = os.path.join('personalities', 'responses', region, personality_id)
    response_index_path = os.path.join(responses_folder, 'response_index.json')
    removed_folder = os.path.join(responses_folder, 'REMOVED')

    create_folder(removed_folder)
    
    response_index = load_json_file(response_index_path)
    
    if intent in response_index:
        # Move the intent file to REMOVED folder
        intent_file_path = os.path.join(responses_folder, response_index[intent]["file_path"])
        removed_file_path = os.path.join(removed_folder, os.path.basename(intent_file_path))
        
        if os.path.exists(removed_file_path):
            removed_file_path = os.path.join(removed_folder, f"{intent}_{personality_id}_REMOVED.json")
        
        shutil.move(intent_file_path, removed_file_path)
        response_index.pop(intent)
        update_json_file(response_index_path, response_index)
#endregion

if __name__ == "__main__":
    # Example usage
    target_location = os.path.dirname(os.path.abspath(__file__))
    initialize(target_location)
    
    bot_id = "sbv1234"
    intent = "greeting"
    responses = ["Hello!", "Hi there!", "Greetings!"]
    
    # Check if personality exists; if not, create it
    existing_personality_id = get_bot_personality_id(bot_id)
    if not existing_personality_id:
        # Define new personality object
        new_personality = {
            "short_name": "FriendlyBot",
            "details": {
                "personality_profile": {
                    "description": "Friendly and curious personality.",
                    "personality_quirk": {
                        "description": "A single stand-out feature.",
                        "selected": "Loves asking questions"
                    },
                    "region": {
                        "description": "Region of origin.",
                        "selected": "en_us"
                    },
                    "baseline_personality": {
                        "description": "Baseline personality traits.",
                        "selected": {
                            "Curious": 0.75,
                            "Happy": 0.8
                        }
                    }
                }
            }
        }
        personality_id = save_personality(new_personality)
        save_bot_personality(bot_id, personality_id)
    else:
        personality_id = existing_personality_id
    
    # Check if responses for the intent exist; if not, create them
    if not list_responses(personality_id, intent):
        create_responses(personality_id, intent, responses)
    
    # Example of getting a response
    response = get_response(personality_id, intent)
    print(f"Selected response: {response}")

    # Example of getting a bot response
    response2 = get_bot_response(bot_id, intent)
    print(f"Bot response: {response2}")