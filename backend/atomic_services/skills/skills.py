from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client, Client
from functools import wraps
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
    os.getenv("SUPABASE_SERVICE_KEY")
)

# Separate client for auth verification (uses anon key)
auth_supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)


def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Unauthorized'}), 401
        token = auth_header.split(' ')[1]
        try:
            user = auth_supabase.auth.get_user(token)
            if not getattr(user, 'user', None):
                return jsonify({'error': 'Unauthorized'}), 401
        except Exception:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return wrapper

# Get all skills
@app.route('/skills', methods=['GET'])
def get_skills():
    try:
        response = supabase.table('skills').select('*').execute()
        return jsonify({'data': response.data, 'count': len(response.data)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get skill by ID
@app.route('/skills/<int:skill_id>', methods=['GET'])
def get_skill(skill_id):
    try:
        response = supabase.table('skills').select('*').eq('id', skill_id).execute()
        if response.data:
            return jsonify(response.data[0]), 200
        return jsonify({'error': 'Skill not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create new skill
@app.route('/skills', methods=['POST'])
@require_auth
def create_skill():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('skill_name') or not data.get('proficiency'):
            return jsonify({'error': 'skill_name and proficiency are required'}), 400
        
        new_skill = {
            'skill_name': data.get('skill_name'),
            'proficiency': data.get('proficiency')
        }
        
        response = supabase.table('skills').insert(new_skill).execute()
        return jsonify({'data': response.data, 'message': 'Skill created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update skill
@app.route('/skills/<int:skill_id>', methods=['PUT'])
@require_auth
def update_skill(skill_id):
    try:
        data = request.get_json()
        
        update_data = {}
        if 'skill_name' in data:
            update_data['skill_name'] = data['skill_name']
        if 'proficiency' in data:
            update_data['proficiency'] = data['proficiency']
        
        if not update_data:
            return jsonify({'error': 'No fields to update'}), 400
        
        response = supabase.table('skills').update(update_data).eq('id', skill_id).execute()
        
        if response.data:
            return jsonify({'data': response.data, 'message': 'Skill updated successfully'}), 200
        return jsonify({'error': 'Skill not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete skill
@app.route('/skills/<int:skill_id>', methods=['DELETE'])
@require_auth
def delete_skill(skill_id):
    try:
        response = supabase.table('skills').delete().eq('id', skill_id).execute()
        
        if response.data:
            return jsonify({'message': 'Skill deleted successfully'}), 200
        return jsonify({'error': 'Skill not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)