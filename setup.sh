#!/bin/bash

# Define variables at the top
REPO_DIR=~/wirepod-vector-personalities
CHIPPER_JSON=~/wire-pod/chipper/customIntents.json
CONFIG_FILE=$REPO_DIR/config/configs.json
VENV_DIR=$REPO_DIR/env
REQUIREMENTS_FILE=$REPO_DIR/requirements.txt
BACKUP_DIR=$REPO_DIR/backups/chipper

# Set the default execpath to main.py
DEFAULT_EXEC_PATH="$REPO_DIR/src/main.py"

# Step 1: Check if customIntents.json exists
if [ -f "$CHIPPER_JSON" ]; then
  echo "$CHIPPER_JSON exists. Updating configs.json..."
  # Update configs.json with the custom intents file path
  jq '.custom_intents_file_path = "'$CHIPPER_JSON'"' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
  echo "Updated configs.json with custom_intents_file_path: $CHIPPER_JSON"
fi

# Step 2: Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
if [ -f "$REQUIREMENTS_FILE" ]; then
  pip install -r "$REQUIREMENTS_FILE"
  echo "Dependencies installed."
else
  echo "No requirements.txt found. Skipping dependency installation."
fi
PYTHON_ENV_PATH="$VENV_DIR/bin/python"
echo "Python environment path: $PYTHON_ENV_PATH"

# Step 3: Create a backup of customIntents.json
mkdir -p "$BACKUP_DIR"
cp "$CHIPPER_JSON" "$BACKUP_DIR"
echo "Backup created in $BACKUP_DIR."

# Step 4: Update customIntents.json with new intent
new_entries=$(jq -n \
  --arg exec "$PYTHON_ENV_PATH" \
  --arg execpath "$DEFAULT_EXEC_PATH" \
  '[{
    "name": "create vector personality",
    "description": "Create a personality for your vector, by way of wirepod-vector-personalities.",
    "utterances": ["create a personality", "create personality", "create your personality", "new personality"],
    "intent": "intent_create_personality",
    "params": {"paramname": "", "paramvalue": ""},
    "exec": $exec,
    "execargs": [$execpath, "!botSerial", "!speechText", "!intentName", "!locale"],
    "issystem": false,
    "luascript": ""
  }, {
    "name": "get vector personality",
    "description": "Get the current personality for your vector, by way of wirepod-vector-personalities.",
    "utterances": ["what'\''s your personality", "what is your personality", "tell me your personality", "get personality"],
    "intent": "intent_get_personality",
    "params": {"paramname": "", "paramvalue": ""},
    "exec": $exec,
    "execargs": [$execpath, "!botSerial", "!speechText", "!intentName", "!locale"],
    "issystem": false,
    "luascript": ""
  }, {
    "name": "override_system_unmatched_for_personalities",
    "description": "This overrides the unmatched intent, to direct to wirepod-vector-personalities.",
    "utterances": [""],
    "intent": "intent_system_unmatched",
    "params": {"paramname": "", "paramvalue": ""},
    "exec": $exec,
    "execargs": [$execpath, "!botSerial", "!speechText", "!intentName", "!locale"],
    "issystem": false,
    "luascript": ""
  }]')

# Append new entries to customIntents.json
jq ". += $new_entries" "$CHIPPER_JSON" > "$CHIPPER_JSON.tmp" && mv "$CHIPPER_JSON.tmp" "$CHIPPER_JSON"
echo "Added new intents to $CHIPPER_JSON."


# Step 5: Prompt for OpenAI API key
read -p "Enter your OpenAI API key (leave blank to skip): " openai_key
if [ -n "$openai_key" ]; then
  jq '.openai_api_key = "'$openai_key'"' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv
