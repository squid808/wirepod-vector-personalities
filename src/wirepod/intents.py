import os
import json
from utils import file_io

def get_custom_intents():
    custom_intents = file_io.get_custom_intents_file()
    # intents_index = {}
    # for intent in custom_intents:
    #     intents_index[intent['name']] = intent
        
    return custom_intents

def add_custom_intent(name, description, utterances, intent,
                      paramname="", paramvalue="", exec_cmd="", exec_args="", luascript=""):
    """
        Add a custom intent to the system, with proper validation for required fields.

        :param name: The name of the custom intent.
        :param description: A description of the intent.
        :param utterances: A list of example utterances for the intent.
        :param intent: The selected intent for this custom intent.
        :param paramname: Parameter name for the intent's parameters.
        :param paramvalue: Parameter value for the intent's parameters.
        :param exec_cmd: The execution command to be run.
        :param exec_args: A list of arguments for the execution command.
        :param luascript: A Lua script to execute if needed.
        :return: JSON response from the API.
        """
        
    new_intent = {
        "name": name,
        "description": description,
        "utterances": utterances,
        "intent": intent,
        "params": {
            "paramname": paramname,
            "paramvalue": paramvalue
        },
        "exec": exec_cmd,
        "execargs": exec_args,
        "luascript": luascript
    }

    file_io.save_custom_intent(new_intent)
    
    
    
    