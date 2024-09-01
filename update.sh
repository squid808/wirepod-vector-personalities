#!/bin/bash

# Path to your repository and important files
REPO_DIR=~/wirepod-vector-personalities
WIREPOD_DIR=~/wire-pod
CHIPPER_JSON=$WIREPOD_DIR/chipper/customIntents.json
PYTHON_ENV=$REPO_DIR/env
REQUIREMENTS_FILE=$REPO_DIR/requirements.txt

# Check if a branch argument is passed
if [ -z "$1" ]; then
  echo "No branch specified. Please use 'main' or 'dev'."
  exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
  echo "jq is not installed. Please install it using: sudo apt-get install jq"
  exit 1
fi

# Change to the repository directory
if [ -d "$REPO_DIR" ]; then
  cd "$REPO_DIR"
else
  echo "Repository directory not found: $REPO_DIR"
  exit 1
fi

# Step 1: Pull the latest code
BRANCH=$1
git checkout $BRANCH
git pull origin $BRANCH
echo "Repository updated on branch: $BRANCH"

# Step 2: Reactivate virtual environment and install any updated dependencies
if [ -d "$PYTHON_ENV" ]; then
  echo "Activating virtual environment..."
  source "$PYTHON_ENV/bin/activate"
else
  echo "Virtual environment not found. Please run setup.sh first."
  exit 1
fi

# Check if requirements.txt has changed, and install new dependencies if needed
pip install -r "$REQUIREMENTS_FILE"
echo "Dependencies updated."

# Step 3: Ensure backups and customIntents.json are updated
BACKUP_DIR=$REPO_DIR/backups/chipper
mkdir -p "$BACKUP_DIR"
cp "$CHIPPER_JSON" "$BACKUP_DIR"

new_entry=$(jq -n \
  --arg exec "$PYTHON_ENV/bin/python" \
  '{name: "override_system_unmatched_for_personalities", description: "This overrides the unmatched intent, to direct to wirepod-vector-personalities.", utterances: [""], intent: "intent_system_unmatched", params: {paramname: "", paramvalue: ""}, exec: $exec, execargs: ["../squid808-personalities/test_log.py", "!botSerial", "!speechText", "!intentName", "!locale"], issystem: false, luascript: ""}')
jq ". += [$new_entry]" "$CHIPPER_JSON" > "$CHIPPER_JSON.tmp" && mv "$CHIPPER_JSON.tmp" "$CHIPPER_JSON"
echo "customIntents.json updated with new intent."

echo "Update completed."
