import os
from gradio_client import Client

# Path to files
CREDENTIALS_FILE = 'data/credentials.json'
RFID_CARDS_FILE = 'data/rfid_cards.json'
REQUESTS_LOG_FILE = 'data/requests_log.json'
VEGETABLES_FILE = 'data/vegetables.json'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Initialize Gradio client at startup
try:
    GRADIO_CLIENT = Client("hrid0yyy/yolo-veggie-detector")
    print("✓ Gradio YOLO client initialized successfully")
except Exception as e:
    GRADIO_CLIENT = None
    print(f"✗ Failed to initialize Gradio client: {e}")
