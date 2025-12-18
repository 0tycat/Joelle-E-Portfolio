from flask import Flask, jsonify
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
    os.getenv("SUPABASE_SERVICE_KEY")
)

# Skills endpoint with proficiency levels
@app.route('/api/skills', methods=['GET'])
def get_skills():
    try:
        response = supabase.schema('public').table('skills').select('*').execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Education endpoint
@app.route('/api/education', methods=['GET'])
def get_education():
    try:
        response = supabase.schema('public').table('education').select('*').order('start_date', desc=True).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Work experience endpoint
@app.route('/api/work', methods=['GET'])
def get_work():
    try:
        response = supabase.schema('public').table('work_experience').select('*').order('start_date', desc=True).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Community service endpoint
@app.route('/api/community', methods=['GET'])
def get_community():
    try:
        response = supabase.schema('public').table('community_service').select('*').execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Projects/Other information endpoint
@app.route('/api/projects', methods=['GET'])
def get_projects():
    try:
        response = supabase.schema('public').table('other_information').select('*').execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get all portfolio data at once
@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    try:
        skills = supabase.schema('public').table('skills').select('*').execute()
        education = supabase.schema('public').table('education').select('*').order('start_date', desc=True).execute()
        work = supabase.schema('public').table('work_experience').select('*').order('start_date', desc=True).execute()
        community = supabase.schema('public').table('community_service').select('*').execute()
        projects = supabase.schema('public').table('other_information').select('*').execute()
        
        return jsonify({
            'skills': skills.data,
            'education': education.data,
            'work': work.data,
            'community': community.data,
            'projects': projects.data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
