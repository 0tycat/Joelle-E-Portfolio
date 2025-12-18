from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")  # Use anon key for auth
)

# User login
@app.route('/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Sign in with Supabase
        response = supabase.auth.sign_in_with_password({
            'email': data.get('email'),
            'password': data.get('password')
        })
        
        return jsonify({
            'message': 'Login successful',
            'access_token': response.session.access_token,
            'refresh_token': response.session.refresh_token,
            'user': {
                'id': response.user.id,
                'email': response.user.email
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 401

# User logout
@app.route('/auth/logout', methods=['POST'])
def logout():
    """Logout user - just return success message"""
    try:
        # Client is responsible for clearing the token
        # Server-side logout is mainly for cleanup if needed
        return jsonify({'message': 'Logout successful'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Get current user info
@app.route('/auth/user', methods=['GET'])
def get_user():
    """Get current user info"""
    try:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        token = auth_header.split(' ')[1]
        
        # Get user from token
        user = supabase.auth.get_user(token)
        
        return jsonify({
            'user': {
                'id': user.user.id,
                'email': user.user.email
            }
        }), 200

@app.route('/auth/refresh', methods=['POST'])
def refresh_token():
    """Refresh access token"""
    try:
        data = request.get_json()
        refresh_token = data.get('refresh_token')
        
        if not refresh_token:
            return jsonify({'error': 'Refresh token required'}), 400
        
        # Refresh session
        response = supabase.auth.refresh_session(refresh_token)
        
        return jsonify({
            'access_token': response.session.access_token,
            'refresh_token': response.session.refresh_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 401
        
    except Exception as e:
        return jsonify({'error': str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5005)
