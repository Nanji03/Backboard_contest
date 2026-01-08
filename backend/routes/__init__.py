"""API routes for ElderCare Companion."""

from flask import Blueprint

def register_routes(app):
    """Register all blueprints with the Flask app."""
    from .med_routes import med_bp
    from .appointment_routes import appt_bp
    from .chat_routes import chat_bp
    
    app.register_blueprint(med_bp)
    app.register_blueprint(appt_bp)
    app.register_blueprint(chat_bp)
