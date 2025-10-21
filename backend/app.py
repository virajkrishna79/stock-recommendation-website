from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize extensions first (without app context)
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///stock_recommendations.db')
    # Railway provides DATABASE_URL for Postgres. Ensure sqlite path is absolute when using file.
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///'):
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        abs_path = os.path.join(os.path.dirname(__file__), db_path)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{abs_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    CORS(app)
    
    # Import and register blueprints inside the function to avoid circular imports
    from api.routes import main_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Create tables (best-effort, ignore failures in read-only envs)
    try:
        with app.app_context():
            db.create_all()
    except Exception:
        pass
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
