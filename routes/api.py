from flask import Blueprint, request, jsonify
from datetime import datetime
from utils.rfid_utils import is_rfid_verified
from utils.log_utils import log_request

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/verify_rfid', methods=['POST'])
def verify_rfid():
    """API endpoint for ESP32 to verify RFID cards"""
    try:
        data = request.get_json()
        if not data or 'rfid_number' not in data:
            return jsonify({"error": "RFID number required"}), 400
        
        rfid_number = data['rfid_number']
        verified = is_rfid_verified(rfid_number)
        
        # Log the request
        log_request(rfid_number, verified, request.remote_addr)
        
        return jsonify({
            "rfid_number": rfid_number,
            "verified": verified,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
