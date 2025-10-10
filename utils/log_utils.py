import json
import os
from datetime import datetime
from config import REQUESTS_LOG_FILE

def log_request(rfid_number, verified, ip_address):
    """Log incoming RFID requests"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "rfid_number": rfid_number,
        "verified": verified,
        "ip_address": ip_address
    }
    
    logs = load_requests_log()
    logs.append(log_entry)
    
    # Keep only last 100 requests
    logs = logs[-100:]
    
    with open(REQUESTS_LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

def load_requests_log():
    """Load request logs"""
    if os.path.exists(REQUESTS_LOG_FILE):
        with open(REQUESTS_LOG_FILE, 'r') as f:
            return json.load(f)
    return []

def get_recent_requests(count=10):
    """Get recent requests for dashboard with formatted timestamps"""
    recent_requests = load_requests_log()[-count:]
    
    # Format timestamps for display
    for request in recent_requests:
        try:
            # Parse ISO timestamp and format it nicely
            dt = datetime.fromisoformat(request['timestamp'])
            request['formatted_timestamp'] = dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            # Fallback to original format if parsing fails
            request['formatted_timestamp'] = request['timestamp'][:19]
    
    recent_requests.reverse()  # Show newest first
    return recent_requests

def clear_all_logs():
    """Clear all request logs"""
    with open(REQUESTS_LOG_FILE, 'w') as f:
        json.dump([], f, indent=2)
