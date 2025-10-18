from datetime import datetime
from config import SUPABASE

def log_request(rfid_number, verified, ip_address):
    """Log incoming RFID requests to Supabase."""
    if SUPABASE is None:
        return
    try:
        SUPABASE.table("requests_log").insert({
            "timestamp": datetime.now().isoformat(),
            "rfid_number": rfid_number,
            "verified": bool(verified),
            "ip_address": ip_address
        }).execute()
    except Exception:
        pass

def load_requests_log():
    """Load request logs (oldest first, up to 100)."""
    if SUPABASE is None:
        return []
    try:
        res = SUPABASE.table("requests_log").select("*").order("timestamp", desc=False).limit(100).execute()
        return res.data or []
    except Exception:
        return []

def get_recent_requests(count=10):
    """Get recent requests for dashboard with formatted timestamps (newest first)."""
    if SUPABASE is None:
        return []
    try:
        res = SUPABASE.table("requests_log").select("*").order("timestamp", desc=True).limit(count).execute()
        recent_requests = res.data or []
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
    """Clear all request logs from Supabase."""
    if SUPABASE is None:
        return
    try:
        SUPABASE.table("requests_log").delete().gt("timestamp", "").execute()
    except Exception:
        pass
