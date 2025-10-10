from flask import Flask
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.rfid import rfid_bp
from routes.api import api_bp
from routes.vegetables import vegetables_bp
from routes.detection import detection_bp

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(rfid_bp)
app.register_blueprint(api_bp)
app.register_blueprint(vegetables_bp)
app.register_blueprint(detection_bp)

if __name__ == '__main__':
    app.run(debug=True)
