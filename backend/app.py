"""Main Flask app entry point."""

from flask import Flask, jsonify
from flask_cors import CORS
from .config import config
from .routes import chat_bp, med_bp, appointment_bp, request_bp, auth_bp

def create_app():
    """Create and configure Flask app."""
    app = Flask(__name__)
    app.config.from_object(config)
    
    # Enable CORS for all API routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Health check
    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "environment": config.ENV})
    
    # Register blueprints
    app.register_blueprint(chat_bp)
    app.register_blueprint(med_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(request_bp)
    app.register_blueprint(auth_bp)
    
    # Global error handler
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error"}), 500
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=config.DEBUG)
