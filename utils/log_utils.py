import json
import os
from datetime import datetime
from config import REQUESTS_LOG_FILE, REDIS

def log_request(rfid_number, verified, ip_address):
    """Log incoming RFID requests"""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "rfid_number": rfid_number,
        "verified": bool(verified),
        "ip_address": ip_address,
    }
    if REDIS:
        try:
            REDIS.lpush("requests_log", json.dumps(entry))
            REDIS.ltrim("requests_log", 0, 99)
            return
        except Exception:
            pass
    logs = load_requests_log()
    logs.append(entry)
    logs = logs[-100:]
    with open(REQUESTS_LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

def load_requests_log():
    """Load request logs"""
    if REDIS:
        try:
            items = REDIS.lrange("requests_log", 0, 99)  # newest first
            return [json.loads(i) for i in items]
        except Exception:
            pass
    if os.path.exists(REQUESTS_LOG_FILE):
        with open(REQUESTS_LOG_FILE, 'r') as f:
            return json.load(f)
    return []

def get_recent_requests(count=10):
    """Get recent requests for dashboard with formatted timestamps"""
    if REDIS:
        try:
            items = REDIS.lrange("requests_log", 0, count - 1)  # newest first
            recent_requests = [json.loads(i) for i in items]
            for r in recent_requests:
                try:
                    dt = datetime.fromisoformat(r.get('timestamp', ''))
                    r['formatted_timestamp'] = dt.strftime('%Y-%m-%d %H:%M:%S')
                except Exception:
                    r['formatted_timestamp'] = (r.get('timestamp') or '')[:19]
            return recent_requests
        except Exception:
            pass
    recent_requests = load_requests_log()[-count:]
    for r in recent_requests:
        try:
            dt = datetime.fromisoformat(r.get('timestamp', ''))
            r['formatted_timestamp'] = dt.strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            r['formatted_timestamp'] = (r.get('timestamp') or '')[:19]
    recent_requests.reverse()
    return recent_requests

def clear_all_logs():
    """Clear all request logs"""
    if REDIS:
        try:
            REDIS.delete("requests_log")
            return
        except Exception:
            pass
    with open(REQUESTS_LOG_FILE, 'w') as f:
        json.dump([], f, indent=2)
