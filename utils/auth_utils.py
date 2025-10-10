import json
import os
from config import CREDENTIALS_FILE

def load_credentials():
    """Load admin credentials from JSON file"""
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    return {}

def verify_credentials(username, password):
    """Verify username and password"""
    credentials = load_credentials()
    return username in credentials and credentials[username] == password
