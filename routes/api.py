from flask import Blueprint, request, jsonify
from datetime import datetime
from utils.rfid_utils import is_rfid_verified
from utils.log_utils import log_request
from utils.vegetable_utils import increment_vegetable

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

@api_bp.route('/api/increment_vegetable', methods=['POST'])
def increment_vegetable_api():
    """Increment quantity and weight for any vegetable. Body: {name, quantity, weight}"""
    try:
        data = request.get_json(silent=True) or {}
        name = (data.get('name') or data.get('vegetable') or '').strip().lower()
        qty_inc = int(data.get('quantity') or 0)
        weight_inc = float(data.get('weight') or 0)

        if not name:
            return jsonify({"error": "name_required"}), 400

        updated = increment_vegetable(name, qty_inc, weight_inc)
        if not updated:
            return jsonify({"error": "update_failed"}), 500

        return jsonify(updated)
    except Exception:
        return jsonify({"error": "update_failed"}), 500
