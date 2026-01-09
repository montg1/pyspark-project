#!/bin/bash
# Script to run read_output.py with proper environment setup

# Set Java environment
export PATH="/opt/homebrew/opt/openjdk@11/bin:$PATH"
export JAVA_HOME="/opt/homebrew/opt/openjdk@11"

# Activate virtual environment
source .venv/bin/activate

# Run the script
python scripts/read_output.py