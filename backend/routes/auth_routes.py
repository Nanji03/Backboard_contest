"""Authentication routes."""

from flask import Blueprint, request, jsonify
from ..models import AuthRequest, AuthResponse, UserProfile

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

# Mock user store (replace with DB in production)
_users = {}

@auth_bp.post("/register")
def register():
    """Register a new user."""
    data = request.get_json() or {}
    
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "email and password required"}), 400
    
    if data["email"] in _users:
        return jsonify({"error": "Email already registered"}), 409
    
    _users[data["email"]] = {
        "password": data["password"],
        "role": data.get("role", "senior"),
        "name": data.get("name", ""),
    }
    
    return jsonify({
        "userId": data["email"],
        "role": data.get("role", "senior"),
        "message": "Registered successfully"
    }), 201

@auth_bp.post("/login")
def login():
    """Log in user."""
    data = request.get_json() or {}
    
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "email and password required"}), 400
    
    user = _users.get(data["email"])
    if not user or user["password"] != data["password"]:
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Mock token (use JWT in production)
    response = AuthResponse(
        userId=data["email"],
        token=f"mock_token_{data['email']}",
        role=user["role"]
    )
    
    return jsonify(response.model_dump()), 200

@auth_bp.get("/profile/<user_id>")
def get_profile(user_id):
    """Get user profile."""
    user = _users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    profile = UserProfile(
        userId=user_id,
        role=user["role"],
        name=user["name"],
        email=user_id
    )
    
    return jsonify(profile.model_dump()), 200
