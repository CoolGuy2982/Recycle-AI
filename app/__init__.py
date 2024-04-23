from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['GOOGLE_MAPS_API_KEY'] = os.getenv('GOOGLE_MAPS_API')
    # Import and register the blueprint from the routes module
    from .routes import main
    app.register_blueprint(main)

    return app
