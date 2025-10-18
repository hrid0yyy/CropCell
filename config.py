import os
import json
from gradio_client import Client

# Path to files
CREDENTIALS_FILE = 'data/credentials.json'
RFID_CARDS_FILE = 'data/rfid_cards.json'
REQUESTS_LOG_FILE = 'data/requests_log.json'
VEGETABLES_FILE = 'data/vegetables.json'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Initialize Firebase Firestore using local service account file or env var
try:
    import firebase_admin
    from firebase_admin import credentials, firestore

    FIRESTORE_DB = None
    base_dir = os.path.dirname(os.path.abspath(__file__))
    service_account_path = os.path.join(base_dir, "cropbox-18f90-firebase-adminsdk-fbsvc-cdf63a8cf1.json")
    cred = None

    if os.path.exists(service_account_path):
        cred = credentials.Certificate(service_account_path)
        print(f"✓ Using Firebase service account file: {service_account_path}")
    else:
        cred_json = os.environ.get("FIREBASE_CREDENTIALS")
        if cred_json:
            cred = credentials.Certificate(json.loads(cred_json))
            print("✓ Using Firebase credentials from FIREBASE_CREDENTIALS env var")

    if cred:
        firebase_admin.initialize_app(cred)
        FIRESTORE_DB = firestore.client()
        print("✓ Firebase Firestore initialized successfully")
    else:
        FIRESTORE_DB = None
        print("✗ Firebase not configured. Provide local service account file or FIREBASE_CREDENTIALS env var")
except Exception as e:
    FIRESTORE_DB = None
    print(f"✗ Failed to initialize Firebase: {e}")

# Initialize Gradio client at startup
try:
    GRADIO_CLIENT = Client("hrid0yyy/yolo-veggie-detector")
    print("✓ Gradio YOLO client initialized successfully")
except Exception as e:
    GRADIO_CLIENT = None
    print(f"✗ Failed to initialize Gradio client: {e}")
