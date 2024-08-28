import requests
import json

# Configuration for API endpoints
API_BASE_URL = "http://localhost:8080/api"  # Adjust base URL as needed
INTENTS_ENDPOINT = f"{API_BASE_URL}/intents"
REBOOT_ENDPOINT = f"{API_BASE_URL}/reboot"

# Headers for API requests
HEADERS = {
    'Content-Type': 'application/json'
}

def update_intent(intent_id, intent_data):
    """
    Update an existing intent.
    :param intent_id: ID of the intent to update
    :param intent_data: Dictionary with intent details to update
    :return: Response object from the API request
    """
    url = f"{INTENTS_ENDPOINT}/{intent_id}"
    response = requests.put(url, headers=HEADERS, data=json.dumps(intent_data))
    if response.status_code == 200:
        print("Intent updated successfully.")
        # Reboot system if intent update is successful
        reboot_system()
    else:
        print(f"Failed to update intent: {response.status_code} - {response.text}")
    return response

def create_intent(intent_data):
    """
    Create a new intent.
    :param intent_data: Dictionary with intent details to create
    :return: Response object from the API request
    """
    response = requests.post(INTENTS_ENDPOINT, headers=HEADERS, data=json.dumps(intent_data))
    if response.status_code == 201:
        print("Intent created successfully.")
    else:
        print(f"Failed to create intent: {response.status_code} - {response.text}")
    return response

def delete_intent(intent_id):
    """
    Delete an existing intent.
    :param intent_id: ID of the intent to delete
    :return: Response object from the API request
    """
    url = f"{INTENTS_ENDPOINT}/{intent_id}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        print("Intent deleted successfully.")
    else:
        print(f"Failed to delete intent: {response.status_code} - {response.text}")
    return response

def list_intents():
    """
    List all current intents.
    :return: Response object from the API request
    """
    response = requests.get(INTENTS_ENDPOINT, headers=HEADERS)
    if response.status_code == 200:
        intents = response.json()
        print("Current intents:")
        for intent in intents:
            print(f"ID: {intent['id']}, Name: {intent['name']}")
    else:
        print(f"Failed to list intents: {response.status_code} - {response.text}")
    return response

def reboot_system():
    """
    Reboot the system via the API.
    :return: Response object from the API request
    """
    response = requests.post(REBOOT_ENDPOINT, headers=HEADERS)
    if response.status_code == 200:
        print("System rebooted successfully.")
    else:
        print(f"Failed to reboot system: {response.status_code} - {response.text}")
    return response

# Example usage:
# if __name__ == "__main__":
#     # List all intents
#     list_intents()
    
#     # Create a new intent
#     new_intent_data = {
#         "name": "example_intent",
#         "description": "This is an example intent"
#     }
#     create_intent(new_intent_data)
    
#     # Update an existing intent
#     intent_id_to_update = "example_id"
#     updated_intent_data = {
#         "name": "updated_intent",
#         "description": "This intent has been updated"
#     }
#     update_intent(intent_id_to_update, updated_intent_data)
    
#     # Delete an intent
#     intent_id_to_delete = "example_id"
#     delete_intent(intent_id_to_delete)
