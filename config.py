import os
from gradio_client import Client

# Path to files
CREDENTIALS_FILE = 'data/credentials.json'
RFID_CARDS_FILE = 'data/rfid_cards.json'
REQUESTS_LOG_FILE = 'data/requests_log.json'
VEGETABLES_FILE = 'data/vegetables.json'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Initialize Redis (hardcoded URL, TLS enabled via rediss://)
try:
	import redis
	from urllib.parse import urlparse

	HARDCODED_REDIS_URL = "rediss://default:aWTPTH36pX9bEnLZoFcIjzeAhWBciR7n@redis-19765.crce214.us-east-1-3.ec2.redns.redis-cloud.com:19765"
	parsed = urlparse(HARDCODED_REDIS_URL)
	use_ssl = parsed.scheme == "rediss"
	REDIS = redis.Redis.from_url(HARDCODED_REDIS_URL, decode_responses=True, ssl=use_ssl)
	REDIS.ping()
	print(f"✓ Redis client initialized ({parsed.hostname}:{parsed.port}, ssl={use_ssl})")
except Exception as e:
	REDIS = None
	print(f"✗ Failed to initialize Redis: {e}")

# Initialize Gradio client at startup
try:
	GRADIO_CLIENT = Client("hrid0yyy/yolo-veggie-detector")
	print("✓ Gradio YOLO client initialized successfully")
except Exception as e:
	GRADIO_CLIENT = None
	print(f"✗ Failed to initialize Gradio client: {e}")
