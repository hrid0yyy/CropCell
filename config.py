import os
import json
import base64
from gradio_client import Client

# Path to files
CREDENTIALS_FILE = 'data/credentials.json'
RFID_CARDS_FILE = 'data/rfid_cards.json'
REQUESTS_LOG_FILE = 'data/requests_log.json'
VEGETABLES_FILE = 'data/vegetables.json'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Initialize Firebase Firestore using env vars first; use local file only for dev
try:
    import firebase_admin
    from firebase_admin import credentials, firestore

    FIRESTORE_DB = None
    cred = None

    # 1) Prefer base64-encoded credentials
    b64 = os.environ.get("FIREBASE_CREDENTIALS_BASE64")
    if b64:
        try:
            svc_dict = json.loads(base64.b64decode(b64).decode("utf-8"))
            cred = credentials.Certificate(svc_dict)
            print("✓ Using Firebase credentials from FIREBASE_CREDENTIALS_BASE64")
        except Exception as e:
            print(f"✗ Failed to parse FIREBASE_CREDENTIALS_BASE64: {e}")

    # 2) Fallback to raw JSON string env
    if cred is None:
        raw = os.environ.get("FIREBASE_CREDENTIALS")
        if raw:
            try:
                svc_dict = json.loads(raw)
                cred = credentials.Certificate(svc_dict)
                print("✓ Using Firebase credentials from FIREBASE_CREDENTIALS")
            except Exception as e:
                print(f"✗ Failed to parse FIREBASE_CREDENTIALS: {e}")

    # 3) Dev-only: local file if not on Vercel and allowed
    if cred is None and not os.environ.get("VERCEL"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        service_account_path = os.path.join(base_dir, "cropbox-18f90-firebase-adminsdk-fbsvc-cdf63a8cf1.json")
        if os.path.exists(service_account_path) and os.environ.get("ALLOW_LOCAL_FIREBASE", "1") == "1":
            cred = credentials.Certificate(service_account_path)
            print(f"✓ Using Firebase service account file (dev): {service_account_path}")

    if cred:
        # Avoid re-initialization in dev server reloads
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        FIRESTORE_DB = firestore.client()
        print("✓ Firebase Firestore initialized successfully")
    else:
        FIRESTORE_DB = None
        print("✗ Firebase not configured. Set FIREBASE_CREDENTIALS(_BASE64) or use local file in dev")
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
