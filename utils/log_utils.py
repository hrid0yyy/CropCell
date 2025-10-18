from datetime import datetime
from config import FIRESTORE_DB
try:
    from firebase_admin import firestore
except Exception:
    firestore = None

def log_request(rfid_number, verified, ip_address):
    """Log incoming RFID requests to Firestore."""
    if FIRESTORE_DB is None:
        return
    try:
        FIRESTORE_DB.collection("requests_log").add({
            "timestamp": datetime.now().isoformat(),
            "rfid_number": rfid_number,
            "verified": bool(verified),
            "ip_address": ip_address
        })
    except Exception:
        pass

def load_requests_log():
    """Load request logs from Firestore (up to 100 oldest)."""
    if FIRESTORE_DB is None or firestore is None:
        return []
    try:
        snaps = (FIRESTORE_DB.collection("requests_log")
                 .order_by("timestamp", direction=firestore.Query.ASCENDING)
                 .limit(100).stream())
        return [doc.to_dict() for doc in snaps]
    except Exception:
        return []

def get_recent_requests(count=10):
    """Get recent requests for dashboard with formatted timestamps."""
    if FIRESTORE_DB is None or firestore is None:
        return []
    try:
        snaps = (FIRESTORE_DB.collection("requests_log")
                 .order_by("timestamp", direction=firestore.Query.DESCENDING)
                 .limit(count).stream())
        recent_requests = [doc.to_dict() for doc in snaps]
        for request in recent_requests:
            try:
                dt = datetime.fromisoformat(request.get('timestamp', ''))
                request['formatted_timestamp'] = dt.strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                request['formatted_timestamp'] = (request.get('timestamp') or '')[:19]
        return recent_requests
    except Exception:
        return []

def clear_all_logs():
    """Clear all request logs from Firestore."""
    if FIRESTORE_DB is None:
        return
    try:
        batch = FIRESTORE_DB.batch()
        i = 0
        for doc in FIRESTORE_DB.collection("requests_log").stream():
            batch.delete(doc.reference)
            i += 1
            if i % 400 == 0:
                batch.commit()
                batch = FIRESTORE_DB.batch()
        if i % 400 != 0:
            batch.commit()
    except Exception:
        pass
