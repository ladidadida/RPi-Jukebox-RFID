#!/usr/bin/env bash

# Runner script to ensure
# - correct venv activation
# - independent from working directory

# Change working directory to project root
SOURCE=${BASH_SOURCE[0]}
SCRIPT_DIR="$(dirname "$SOURCE")"
PROJECT_ROOT="$SCRIPT_DIR"/../../..
cd "$PROJECT_ROOT" || { echo "Could not change directory"; exit 1; }

uv run python migrate_to_cli/scripts/run_register_rfid_reader.py $@
