import os
from gradio_client import Client

# Path to files
CREDENTIALS_FILE = 'data/credentials.json'
RFID_CARDS_FILE = 'data/rfid_cards.json'
REQUESTS_LOG_FILE = 'data/requests_log.json'
VEGETABLES_FILE = 'data/vegetables.json'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Initialize Supabase (hardcoded URL and anon key)
try:
    from supabase import create_client, Client as SupabaseClient  # type: ignore
    SUPABASE_URL = "https://kbkurgbbumctjltdibhs.supabase.co"
    SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtia3VyZ2JidW1jdGpsdGRpYmhzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA3NzAyNjQsImV4cCI6MjA3NjM0NjI2NH0.u2B_yv3nZYDSs62kxSy0LIIrM_MMTTmpLBdvyhfL_mQ"
    SUPABASE: SupabaseClient = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    print("✓ Supabase client initialized")
except Exception as e:
    SUPABASE = None  # type: ignore
    print(f"✗ Failed to initialize Supabase: {e}")

# Initialize Gradio client at startup
try:
    GRADIO_CLIENT = Client("hrid0yyy/yolo-veggie-detector")
    print("✓ Gradio YOLO client initialized successfully")
except Exception as e:
    GRADIO_CLIENT = None
    print(f"✗ Failed to initialize Gradio client: {e}")
