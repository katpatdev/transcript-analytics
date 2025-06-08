from flask import Flask

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    
    # Load configuration from config.py
    app.config.from_object('config.Config')
    
    # Register the original blueprint
    from .routes.analytics import analytics_bp
    app.register_blueprint(analytics_bp)
    
    # Register the new advanced blueprint
    from .routes.analytics_advanced import analytics_advanced_bp
    app.register_blueprint(analytics_advanced_bp)
    
    return app