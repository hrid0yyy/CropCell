from flask import Blueprint, request, jsonify
import os
import tempfile
from gradio_client import handle_file
from config import GRADIO_CLIENT

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
            
            # Return the result
            return jsonify({
                "success": True,
                "result": result,
                "message": "Vegetable detection completed successfully"
            })
            
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
