from flask import Blueprint, request, jsonify
import os
import tempfile
from gradio_client import handle_file
from config import GRADIO_CLIENT, SUPABASE

detection_bp = Blueprint('detection', __name__)

@detection_bp.route('/api/detect_vegetables', methods=['POST'])
def detect_vegetables():
    """API endpoint to detect vegetables in uploaded image using YOLO model"""
    try:
        # Check if Gradio client is available
        if GRADIO_CLIENT is None:
            return jsonify({
                "error": "Vegetable detection service is not available",
                "details": "Gradio client failed to initialize"
            }), 503
        
        # Check if image file is provided
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        image_file = request.files['image']
        
        # Check if file is selected
        if image_file.filename == '':
            return jsonify({"error": "No image file selected"}), 400
        
        # Check if file has allowed extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
        if not ('.' in image_file.filename and 
                image_file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({"error": "Invalid image format. Allowed: png, jpg, jpeg, gif, bmp, webp"}), 400
        
        # Create temporary file to save uploaded image
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{image_file.filename.rsplit('.', 1)[1].lower()}") as temp_file:
            image_file.save(temp_file.name)
            temp_file_path = temp_file.name
        
        try:
            # Use pre-initialized Gradio client (much faster!)
            result = GRADIO_CLIENT.predict(
                image=handle_file(temp_file_path),
                api_name="/predict"
            )
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            # Extract the first detection only
            vegetable_name = None
            if isinstance(result, list) and result:
                first = result[0]
                if isinstance(first, dict):
                    vegetable_name = first.get("class") or first.get("label") or first.get("name")
                else:
                    vegetable_name = str(first)
            elif isinstance(result, dict):
                candidates = None
                for key in ("result", "detections", "labels"):
                    if key in result:
                        candidates = result[key]
                        break
                if isinstance(candidates, list) and candidates:
                    first = candidates[0]
                    if isinstance(first, dict):
                        vegetable_name = first.get("class") or first.get("label") or first.get("name")
                    else:
                        vegetable_name = str(first)

            # Attempt to persist the last detection into Supabase (single-row upsert).
            try:
                if SUPABASE is not None:
                    SUPABASE.table('last_detection').upsert({
                        'id': 'singleton',
                        'vegetable': vegetable_name
                    }).execute()
            except Exception as _e:
                # Swallow DB errors to avoid breaking detection API; optionally log or handle separately
                print(f"Warning: failed to persist last_detection to Supabase: {_e}")

            return jsonify({"vegetable": vegetable_name})
            # Persist the last detection to Supabase (single-row table)
            try:
                if SUPABASE is not None:
                    # Upsert a singleton row with id 'singleton' so the table always has one row
                    SUPABASE.table('last_detection').upsert({
                        'id': 'singleton',
                        'vegetable': vegetable_name
                    }).execute()
            except Exception as db_error:
                # Don't fail the request if DB write fails; log details in response for debugging
                # (In production you may prefer logging instead of returning DB error details)
                return jsonify({
                    "vegetable": vegetable_name,
                    "db_error": str(db_error)
                }), 500
            
        except Exception as gradio_error:
            # Clean up temporary file in case of error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            return jsonify({
                "error": "Failed to process image with detection model",
                "details": str(gradio_error)
            }), 500
            
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


@detection_bp.route('/getName', methods=['GET'])
def get_last_detected_name():
    """Return the last detected vegetable name from Supabase as plain text."""
    try:
        if SUPABASE is None:
            # Service not configured; return 503
            return jsonify({"error": "Supabase not configured"}), 503

        res = SUPABASE.table('last_detection').select('vegetable').eq('id', 'singleton').limit(1).execute()
        data = getattr(res, 'data', None) or []
        if not data:
            # No record found
            return ('', 204)

        vegetable = data[0].get('vegetable')
        if vegetable is None:
            return ('', 204)

        # Return plain text with the vegetable name
        return (str(vegetable), 200, {'Content-Type': 'text/plain; charset=utf-8'})

    except Exception as e:
        return jsonify({"error": "Failed to read last detection", "details": str(e)}), 500
