#!/bin/bash

# scripts/deploy.sh

set -e  # Exit immediately if a command exits with a non-zero status

# Variables
APP_DIR="/path/to/your/app"  # Change this to your application directory
REPO_URL="https://github.com/yourusername/yourrepo.git"  # Change to your repository URL
BRANCH="main"  # Change to your desired branch
ENV_FILE=".env"  # Change to your environment file if needed

# Function to log messages
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1"
}

log "Starting deployment..."

# Navigate to the application directory
cd $APP_DIR

# Pull the latest code
log "Pulling the latest code from $REPO_URL..."
git fetch origin
git checkout $BRANCH
git pull origin $BRANCH

# Install dependencies
log "Installing dependencies..."
pip install -r requirements.txt

# Load environment variables
if [ -f "$ENV_FILE" ]; then
    export $(cat $ENV_FILE | xargs)
    log "Loaded environment variables from $ENV_FILE."
else
    log "No environment file found."
fi

# Start the application (example using Flask)
log "Starting the application..."
# You can replace this with your application start command
nohup python app.py &

log "Deployment completed successfully."
