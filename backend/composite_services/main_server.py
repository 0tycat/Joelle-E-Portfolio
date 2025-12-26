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
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

# Initialize Supabase client with ANON key for auth operations
supabase_anon: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

# Authentication helper decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid authorization header'}), 401
        token = auth_header.split(' ')[1]
        try:
            user = supabase_anon.auth.get_user(token)
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Invalid token'}), 401
    return decorated_function

# Auth Login endpoint
@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 204
    try:
        data = request.get_json() or {}
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        response = supabase_anon.auth.sign_in_with_password({'email': email, 'password': password})
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

# Auth Logout endpoint
@app.route('/api/auth/logout', methods=['POST', 'OPTIONS'])
@require_auth
def logout():
    if request.method == 'OPTIONS':
        return '', 204
    try:
        supabase_anon.auth.sign_out()
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Auth Validate endpoint
@app.route('/api/auth/validate', methods=['POST', 'OPTIONS'])
def validate_token():
    if request.method == 'OPTIONS':
        return '', 204
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No valid authorization header'}), 401
        token = auth_header.split(' ')[1]
        user = supabase_anon.auth.get_user(token)
        if not getattr(user, 'user', None):
            return jsonify({'error': 'Invalid token'}), 401
        return jsonify({
            'valid': True,
            'user': {
                'id': user.user.id,
                'email': user.user.email
            }
        }), 200
    except Exception:
        return jsonify({'error': 'Invalid token'}), 401

# Auth Refresh endpoint
@app.route('/api/auth/refresh', methods=['POST', 'OPTIONS'])
def refresh_token():
    if request.method == 'OPTIONS':
        return '', 204
    try:
        data = request.get_json()
        refresh_token = data.get('refresh_token')
        if not refresh_token:
            return jsonify({'error': 'Refresh token required'}), 400
        response = supabase_anon.auth.refresh_session(refresh_token)
        return jsonify({
            'access_token': response.session.access_token,
            'refresh_token': response.session.refresh_token
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401

# Skills endpoint with proficiency labels resolved from prof_level table
@app.route('/api/skills', methods=['GET'])
def get_skills():
    try:
        skills_res = supabase.table('skills').select('*').execute()
        skills = skills_res.data or []

        # Attempt to fetch proficiency levels mapping from `prof_lvl`
        try:
            levels_res = supabase.table('prof_lvl').select('*').execute()
            levels = levels_res.data or []
            level_map = {}
            for lvl in levels:
                key_raw = lvl.get('id') or lvl.get('level') or lvl.get('value')
                key_str = str(key_raw).strip() if key_raw is not None else None
                label = (
                    lvl.get('level')
                    or lvl.get('label')
                    or lvl.get('name')
                    or lvl.get('level_name')
                    or key_str
                )
                if key_str:
                    level_map[key_str] = label
            # attach label
            for s in skills:
                prof_val = s.get('proficiency')
                key_lookup = str(prof_val).strip() if prof_val is not None else None
                if key_lookup and key_lookup in level_map:
                    s['proficiency_label'] = level_map.get(key_lookup)
        except Exception:
            # If mapping fails, return skills without labels
            pass

        return jsonify(skills), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Education endpoint
@app.route('/api/education', methods=['GET'])
def get_education():
    try:
        response = supabase.table('education').select('*').order('start_date', desc=True).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Work experience endpoint
@app.route('/api/work', methods=['GET'])
def get_work():
    try:
        response = supabase.table('work_experience').select('*').order('start_date', desc=True).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Community service endpoint
@app.route('/api/community', methods=['GET'])
def get_community():
    try:
        response = supabase.table('community_service').select('*').execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Projects/Other information endpoint
@app.route('/api/projects', methods=['GET'])
def get_projects():
    try:
        response = supabase.table('other_information').select('*').execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# E-Portfolio activities endpoint
@app.route('/api/e-portfolio', methods=['GET'])
def get_e_portfolio():
    try:
        response = supabase.table('e_portfolio').select('*').execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get single e-portfolio activity by ID
@app.route('/api/e-portfolio/<int:item_id>', methods=['GET'])
def get_e_portfolio_item(item_id):
    try:
        response = supabase.table('e_portfolio').select('*').eq('id', item_id).execute()
        if response.data:
            return jsonify(response.data[0]), 200
        return jsonify({'error': 'E-portfolio activity not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create new e-portfolio activity
@app.route('/api/e-portfolio', methods=['POST', 'OPTIONS'])
@require_auth
def create_e_portfolio():
    if request.method == 'OPTIONS':
        return '', 204
    try:
        data = request.get_json()
        if not data.get('activity_name'):
            return jsonify({'error': 'activity_name is required'}), 400

        new_item = {
            'activity_name': data.get('activity_name'),
            'activity_type': data.get('activity_type'),
            'start_date': data.get('start_date'),
            'finish_date': data.get('finish_date'),
            'organisation_module': data.get('organisation_module'),
            'description': data.get('description'),
            'what_i_did': data.get('what_i_did'),
            'skills_tools_acquired': data.get('skills_tools_acquired'),
            'takeaways': data.get('takeaways'),
            'artefacts_evidence_files': data.get('artefacts_evidence_files'),
            'artefacts_evidence_links_texts': data.get('artefacts_evidence_links_texts'),
            'relevance_career': data.get('relevance_career')
        }
        # Remove None values
        new_item = {k: v for k, v in new_item.items() if v is not None}

        response = supabase.table('e_portfolio').insert(new_item).execute()
        return jsonify({'data': response.data, 'message': 'E-portfolio activity created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update e-portfolio activity
@app.route('/api/e-portfolio/<int:item_id>', methods=['PUT', 'OPTIONS'])
@require_auth
def update_e_portfolio(item_id):
    if request.method == 'OPTIONS':
        return '', 204
    try:
        data = request.get_json()
        allowed_fields = [
            'activity_name', 'activity_type', 'start_date', 'finish_date',
            'organisation_module', 'description', 'what_i_did',
            'skills_tools_acquired', 'takeaways', 'artefacts_evidence_files',
            'artefacts_evidence_links_texts', 'relevance_career'
        ]
        update_data = {}
        for key in allowed_fields:
            if key in data:
                update_data[key] = data[key]

        if not update_data:
            return jsonify({'error': 'No fields to update'}), 400

        response = supabase.table('e_portfolio').update(update_data).eq('id', item_id).execute()
        if response.data:
            return jsonify({'data': response.data, 'message': 'E-portfolio activity updated'}), 200
        return jsonify({'error': 'E-portfolio activity not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete e-portfolio activity
@app.route('/api/e-portfolio/<int:item_id>', methods=['DELETE', 'OPTIONS'])
@require_auth
def delete_e_portfolio(item_id):
    if request.method == 'OPTIONS':
        return '', 204
    try:
        response = supabase.table('e_portfolio').delete().eq('id', item_id).execute()
        if response.data:
            return jsonify({'message': 'E-portfolio activity deleted'}), 200
        return jsonify({'error': 'E-portfolio activity not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Proficiency levels endpoint (for Skills dropdown)
@app.route('/api/prof-levels', methods=['GET'])
def get_prof_levels():
    try:
        # Table name: prof_lvl with columns id (varchar/int) and level (text)
        response = supabase.table('prof_lvl').select('*').execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get all portfolio data at once
@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    try:
        skills = supabase.table('skills').select('*').execute()
        education = supabase.table('education').select('*').order('start_date', desc=True).execute()
        work = supabase.table('work_experience').select('*').order('start_date', desc=True).execute()
        community = supabase.table('community_service').select('*').execute()
        projects = supabase.table('other_information').select('*').execute()
        # Try to resolve proficiency labels for portfolio skills as well
        skills_data = skills.data or []
        try:
            levels_res = supabase.table('prof_lvl').select('*').execute()
            levels = levels_res.data or []
            level_map = {}
            for lvl in levels:
                key_raw = lvl.get('id') or lvl.get('level') or lvl.get('value')
                key_str = str(key_raw).strip() if key_raw is not None else None
                label = (
                    lvl.get('level')
                    or lvl.get('label')
                    or lvl.get('name')
                    or lvl.get('level_name')
                    or key_str
                )
                if key_str:
                    level_map[key_str] = label
            for s in skills_data:
                prof_val = s.get('proficiency')
                key_lookup = str(prof_val).strip() if prof_val is not None else None
                if key_lookup and key_lookup in level_map:
                    s['proficiency_label'] = level_map.get(key_lookup)
        except Exception:
            pass

        return jsonify({
            'skills': skills_data,
            'education': education.data,
            'work': work.data,
            'community': community.data,
            'projects': projects.data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
