from flask import request, jsonify
from functools import wraps
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

def verify_token(token):
    """Verify JWT token from Supabase"""
    try:
        # Verify the token using Supabase
        user = supabase.auth.get_user(token)
        return user
    except Exception as e:
        return None

def require_auth(f):
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        # Extract token (format: "Bearer <token>")
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({'error': 'Invalid authorization header format'}), 401
        
        # Verify token
        user = verify_token(token)
        
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Add user to request context
        request.current_user = user
        
        return f(*args, **kwargs)
    
    return decorated_function
