"""Routes package – register all blueprints here."""

from .chat_routes import chat_bp
from .med_routes import med_bp
from .appointment_routes import appointment_bp
from .request_routes import request_bp
from .auth_routes import auth_bp

__all__ = [
    "chat_bp",
    "med_bp",
    "appointment_bp",
    "request_bp",
    "auth_bp",
]
