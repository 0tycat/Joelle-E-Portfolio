from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client, Client
from functools import wraps
from dotenv import load_dotenv
import os
import io

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
        # Allow OPTIONS requests to pass through without auth
        if request.method == 'OPTIONS':
            return f(*args, **kwargs)
        
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

# Create new skill
@app.route('/api/skills', methods=['POST', 'OPTIONS'])
@require_auth
def create_skill():
    if request.method == 'OPTIONS':
        return '', 204
    try:
        data = request.get_json()
        if not data.get('skill_name'):
            return jsonify({'error': 'skill_name is required'}), 400
        new_skill = {
            'skill_name': data.get('skill_name'),
            'proficiency': data.get('proficiency'),
            'category': data.get('category')
        }
        new_skill = {k: v for k, v in new_skill.items() if v is not None}
        response = supabase.table('skills').insert(new_skill).execute()
        return jsonify({'data': response.data, 'message': 'Skill created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update skill
@app.route('/api/skills/<int:skill_id>', methods=['PUT', 'OPTIONS'])
@require_auth
def update_skill(skill_id):
    if request.method == 'OPTIONS':
        return '', 204
    try:
        data = request.get_json()
        update_data = {}
        for key in ['skill_name', 'proficiency', 'category']:
            if key in data:
                update_data[key] = data[key]
        if not update_data:
            return jsonify({'error': 'No fields to update'}), 400
        response = supabase.table('skills').update(update_data).eq('id', skill_id).execute()
        if response.data:
            return jsonify({'data': response.data, 'message': 'Skill updated'}), 200
        return jsonify({'error': 'Skill not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete skill
@app.route('/api/skills/<int:skill_id>', methods=['DELETE', 'OPTIONS'])
@require_auth
def delete_skill(skill_id):
    if request.method == 'OPTIONS':
        return '', 204
    try:
        response = supabase.table('skills').delete().eq('id', skill_id).execute()
        if response.data:
            return jsonify({'message': 'Skill deleted'}), 200
        return jsonify({'error': 'Skill not found'}), 404
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

# Create new education
@app.route('/api/education', methods=['POST', 'OPTIONS'])
@require_auth
def create_education():
    if request.method == 'OPTIONS':
        return '', 204
    try:
        data = request.get_json()
        new_item = {
            'institute_name': data.get('institute_name'),
            'certification': data.get('certification'),
            'start_date': (None if data.get('start_date') == '' else data.get('start_date')),
            'finish_date': (None if data.get('finish_date') == '' else data.get('finish_date'))
        }
        new_item = {k: v for k, v in new_item.items() if v is not None}
        response = supabase.table('education').insert(new_item).execute()
        return jsonify({'data': response.data, 'message': 'Education created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update education
@app.route('/api/education/<int:edu_id>', methods=['PUT', 'OPTIONS'])
@require_auth
def update_education(edu_id):
    if request.method == 'OPTIONS':
        return '', 204
    try:
        data = request.get_json()
        update_data = {}
        for key in ['institute_name', 'certification', 'start_date', 'finish_date']:
            if key in data:
                # Convert empty strings to None for date fields
                value = data[key]
                if key in ['start_date', 'finish_date'] and value == '':
                    value = None
                update_data[key] = value
        if not update_data:
            return jsonify({'error': 'No fields to update'}), 400
        response = supabase.table('education').update(update_data).eq('id', edu_id).execute()
        if response.data:
            return jsonify({'data': response.data, 'message': 'Education updated'}), 200
        return jsonify({'error': 'Education not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete education
@app.route('/api/education/<int:edu_id>', methods=['DELETE', 'OPTIONS'])
@require_auth
def delete_education(edu_id):
    if request.method == 'OPTIONS':
        return '', 204
    try:
        response = supabase.table('education').delete().eq('id', edu_id).execute()
        if response.data:
            return jsonify({'message': 'Education deleted'}), 200
        return jsonify({'error': 'Education not found'}), 404
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

# Create new work experience
@app.route('/api/work', methods=['POST', 'OPTIONS'])
@require_auth
def create_work():
    if request.method == 'OPTIONS':
        return '', 204
    try:
        data = request.get_json()
        new_item = {
            'company': data.get('company'),
            'position': data.get('position'),
            'start_date': (None if data.get('start_date') == '' else data.get('start_date')),
            'end_date': (None if data.get('end_date') == '' else data.get('end_date')),
            'description': data.get('description')
        }
        new_item = {k: v for k, v in new_item.items() if v is not None}
        response = supabase.table('work_experience').insert(new_item).execute()
        return jsonify({'data': response.data, 'message': 'Work experience created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update work experience
@app.route('/api/work/<int:work_id>', methods=['PUT', 'OPTIONS'])
@require_auth
def update_work(work_id):
    if request.method == 'OPTIONS':
        return '', 204
    try:
        data = request.get_json()
        update_data = {}
        for key in ['company', 'position', 'start_date', 'end_date', 'description']:
            if key in data:
                value = data[key]
                if key in ['start_date', 'end_date'] and value == '':
                    value = None
                update_data[key] = value
        if not update_data:
            return jsonify({'error': 'No fields to update'}), 400
        response = supabase.table('work_experience').update(update_data).eq('id', work_id).execute()
        if response.data:
            return jsonify({'data': response.data, 'message': 'Work experience updated'}), 200
        return jsonify({'error': 'Work experience not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete work experience
@app.route('/api/work/<int:work_id>', methods=['DELETE', 'OPTIONS'])
@require_auth
def delete_work(work_id):
    if request.method == 'OPTIONS':
        return '', 204
    try:
        response = supabase.table('work_experience').delete().eq('id', work_id).execute()
        if response.data:
            return jsonify({'message': 'Work experience deleted'}), 200
        return jsonify({'error': 'Work experience not found'}), 404
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

# Create new community service
@app.route('/api/community', methods=['POST', 'OPTIONS'])
@require_auth
def create_community():
    if request.method == 'OPTIONS':
        return '', 204
    try:
        data = request.get_json()
        new_item = {
            'organization': data.get('organization'),
            'role': data.get('role'),
            'start_date': (None if data.get('start_date') == '' else data.get('start_date')),
            'end_date': (None if data.get('end_date') == '' else data.get('end_date')),
            'description': data.get('description')
        }
        new_item = {k: v for k, v in new_item.items() if v is not None}
        response = supabase.table('community_service').insert(new_item).execute()
        return jsonify({'data': response.data, 'message': 'Community service created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update community service
@app.route('/api/community/<int:comm_id>', methods=['PUT', 'OPTIONS'])
@require_auth
def update_community(comm_id):
    if request.method == 'OPTIONS':
        return '', 204
    try:
        data = request.get_json()
        update_data = {}
        for key in ['organization', 'role', 'start_date', 'end_date', 'description']:
            if key in data:
                value = data[key]
                if key in ['start_date', 'end_date'] and value == '':
                    value = None
                update_data[key] = value
        if not update_data:
            return jsonify({'error': 'No fields to update'}), 400
        response = supabase.table('community_service').update(update_data).eq('id', comm_id).execute()
        if response.data:
            return jsonify({'data': response.data, 'message': 'Community service updated'}), 200
        return jsonify({'error': 'Community service not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete community service
@app.route('/api/community/<int:comm_id>', methods=['DELETE', 'OPTIONS'])
@require_auth
def delete_community(comm_id):
    if request.method == 'OPTIONS':
        return '', 204
    try:
        response = supabase.table('community_service').delete().eq('id', comm_id).execute()
        if response.data:
            return jsonify({'message': 'Community service deleted'}), 200
        return jsonify({'error': 'Community service not found'}), 404
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

# Create new project
@app.route('/api/projects', methods=['POST', 'OPTIONS'])
@require_auth
def create_project():
    if request.method == 'OPTIONS':
        return '', 204
    try:
        data = request.get_json()
        new_item = {
            'project_name': data.get('project_name'),
            'description': data.get('description'),
            'technologies': data.get('technologies'),
            'url': data.get('url')
        }
        new_item = {k: v for k, v in new_item.items() if v is not None}
        response = supabase.table('other_information').insert(new_item).execute()
        return jsonify({'data': response.data, 'message': 'Project created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update project
@app.route('/api/projects/<int:proj_id>', methods=['PUT', 'OPTIONS'])
@require_auth
def update_project(proj_id):
    if request.method == 'OPTIONS':
        return '', 204
    try:
        data = request.get_json()
        update_data = {}
        for key in ['project_name', 'description', 'technologies', 'url']:
            if key in data:
                update_data[key] = data[key]
        if not update_data:
            return jsonify({'error': 'No fields to update'}), 400
        response = supabase.table('other_information').update(update_data).eq('id', proj_id).execute()
        if response.data:
            return jsonify({'data': response.data, 'message': 'Project updated'}), 200
        return jsonify({'error': 'Project not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete project
@app.route('/api/projects/<int:proj_id>', methods=['DELETE', 'OPTIONS'])
@require_auth
def delete_project(proj_id):
    if request.method == 'OPTIONS':
        return '', 204
    try:
        response = supabase.table('other_information').delete().eq('id', proj_id).execute()
        if response.data:
            return jsonify({'message': 'Project deleted'}), 200
        return jsonify({'error': 'Project not found'}), 404
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
            'start_date': (None if data.get('start_date') == '' else data.get('start_date')),
            'finish_date': (None if data.get('finish_date') == '' else data.get('finish_date')),
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
                value = data[key]
                if key in ['start_date', 'finish_date'] and value == '':
                    value = None
                update_data[key] = value

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

# Upload artefact file (stores as hex string in artefacts_evidence_files)
@app.route('/api/e-portfolio/<int:item_id>/upload', methods=['POST', 'OPTIONS'])
@require_auth
def upload_e_portfolio_file(item_id):
    if request.method == 'OPTIONS':
        return '', 204
    try:
        # Optional max size guard (10 MB)
        MAX_BYTES = 10 * 1024 * 1024
        # Allow clearing existing file with clear=true and no file
        clear_flag = request.form.get('clear')
        uploaded = request.files.get('file') if request.files else None

        if clear_flag and clear_flag.lower() == 'true':
            response = supabase.table('e_portfolio').update({'artefacts_evidence_files': None, 'artefacts_evidence_links_texts': None}).eq('id', item_id).execute()
            if response.data:
                return jsonify({'message': 'File cleared'}), 200
            return jsonify({'error': 'E-portfolio activity not found'}), 404

        if not uploaded:
            return jsonify({'error': 'No file provided'}), 400

        content = uploaded.read() or b''
        if len(content) > MAX_BYTES:
            return jsonify({'error': 'File too large (max 10 MB)'}), 413
        hex_value = '\\x' + content.hex()

        try:
            response = supabase.table('e_portfolio').update({'artefacts_evidence_files': hex_value}).eq('id', item_id).execute()
            if response.data:
                return jsonify({'message': 'File uploaded', 'size_bytes': len(content)}), 200
            return jsonify({'error': 'E-portfolio activity not found'}), 404
        except Exception as update_err:
            # Fallback path for PostgREST schema cache miss (PGRST204)
            err_msg = str(update_err)
            if 'PGRST204' not in err_msg and 'schema cache' not in err_msg:
                return jsonify({'error': f'Upload failed: {err_msg}'}), 500

            try:
                bucket_name = 'eportfolio-evidence'
                # Ensure bucket exists (ignore if already present)
                try:
                    buckets = supabase.storage.list_buckets()
                    bucket_names = [b.get('name') or b.get('id') for b in (buckets or [])]
                    if bucket_name not in bucket_names:
                        supabase.storage.create_bucket(bucket_name, public=True)
                except Exception:
                    # If listing fails, attempt to create and ignore errors
                    try:
                        supabase.storage.create_bucket(bucket_name, public=True)
                    except Exception:
                        pass

                path = f"{item_id}/{uploaded.filename or 'evidence'}"
                mime = uploaded.mimetype or 'application/octet-stream'

                # Upload to storage bucket (pass content_type as a dict)
                supabase.storage.from_(bucket_name).upload(
                    path,
                    content,
                    {'content_type': mime}
                )
                public_url_resp = supabase.storage.from_(bucket_name).get_public_url(path)
                public_url = (
                    public_url_resp.get('publicURL')
                    if isinstance(public_url_resp, dict)
                    else public_url_resp
                )

                # Store the URL in links column as a fallback
                link_update = supabase.table('e_portfolio').update({'artefacts_evidence_links_texts': public_url}).eq('id', item_id).execute()
                if link_update.data:
                    return jsonify({'message': 'File stored in bucket (schema cache fallback)', 'storage_url': public_url, 'size_bytes': len(content)}), 200
                return jsonify({'error': 'E-portfolio activity not found'}), 404
            except Exception as fallback_err:
                return jsonify({'error': f'Upload fallback failed: {str(fallback_err)}'}), 500
    except Exception as e:
        # Provide clearer server-side error context
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

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
