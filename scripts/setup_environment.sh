#!/bin/bash

# scripts/setup_environment.sh

set -e  # Exit immediately if a command exits with a non-zero status

# Variables
VENV_DIR="venv"  # Name of the virtual environment directory
REQUIREMENTS_FILE="requirements.txt"  # Change if your requirements file has a different name

# Function to log messages
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1"
}

log "Setting up the environment..."

# Create a virtual environment
log "Creating a virtual environment in $VENV_DIR..."
python3 -m venv $VENV_DIR

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Install dependencies
log "Installing dependencies from $REQUIREMENTS_FILE..."
pip install -r $REQUIREMENTS_FILE

# Create a .env file if it doesn't exist
if [ ! -f ".env" ]; then
    log "Creating .env file..."
    echo "DATABASE_URL=sqlite:///mydatabase.db" > .env
    echo "API_KEY=your_api_key_here" >> .env
    log ".env file created with default values."
else
    log ".env file already exists."
fi

log "Environment setup completed successfully."
