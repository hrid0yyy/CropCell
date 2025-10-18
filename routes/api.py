from flask import Blueprint, request, jsonify
from datetime import datetime
from utils.rfid_utils import is_rfid_verified
from utils.log_utils import log_request

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/verify_rfid', methods=['POST'])
def verify_rfid():
    """API endpoint for ESP32 to verify RFID cards; returns only true/false."""
    try:
        data = request.get_json(silent=True) or {}
        rfid_number = data.get('rfid_number', '')
        verified = is_rfid_verified(rfid_number) if rfid_number else False

        # Log only when we have an RFID number
        if rfid_number:
            log_request(rfid_number, verified, request.remote_addr)

        # Return only the boolean
        return jsonify(verified)
    except Exception:
        # On any error, just return false
        return jsonify(False)
