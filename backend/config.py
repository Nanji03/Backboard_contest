import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    BACKBOARD_API_KEY = os.getenv("BACKBOARD_API_KEY", "")
    BACKBOARD_ASSISTANT_ID = os.getenv("BACKBOARD_ASSISTANT_ID", "")
    BACKBOARD_BASE_URL = "https://app.backboard.io/api"
    
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = FLASK_ENV == "development"
    
    # Optional: add database URL later
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///eldercare.db")
    
    # CORS settings
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5173"]
    
    # Session settings
    SESSION_COOKIE_SECURE = FLASK_ENV == "production"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

config = Config()
