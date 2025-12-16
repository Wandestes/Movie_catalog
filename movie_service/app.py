import sys
import os
from flask import Flask

# Adding root directory to sys.path to ensure cross-module imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from movie_service.routes import movies_bp
try:
    from user_service.routes import users_bp
except ImportError as e:
    print(f"Import Error: {e}")
    users_bp = None

def create_app(config=None):
    app = Flask(__name__)

    if config:
        app.config.update(config)

    # Registering blueprints
    app.register_blueprint(movies_bp)
    
    if users_bp:
        app.register_blueprint(users_bp)
    else:
        print("Warning: users_bp not registered due to import error")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)