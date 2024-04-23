from flask import Blueprint, render_template, request, jsonify, current_app
from .utils import analyze_image

# Create a Blueprint instance for the main app
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/camera')
def camera():
    return render_template('camera.html')

@main.route('/scan')
def scan():
    google_maps_api_key = current_app.config.get('GOOGLE_MAPS_API_KEY')
    if not google_maps_api_key:
        raise ValueError("Google Maps API key not found in the configuration")
    return render_template('scan.html', google_maps_api_key=google_maps_api_key)

@main.route('/analyze', methods=['POST'])
def analyze_route():
    data = request.get_json()
    base64_image = data['image']
    result = analyze_image(base64_image)
    return jsonify(result)

# Don't forget to import main in __init__.py and register it using app.register_blueprint(main)
