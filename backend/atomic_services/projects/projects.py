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
    os.getenv("SUPABASE_SERVICE_KEY")
)

# Get all projects/other information records
@app.route('/projects', methods=['GET'])
def get_projects():
    try:
        response = supabase.schema('public').table('other_information').select('*').execute()
        return jsonify({'data': response.data, 'count': len(response.data)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get single project/other information record by ID
@app.route('/projects/<int:project_id>', methods=['GET'])
def get_project_item(project_id):
    try:
        response = supabase.schema('public').table('other_information').select('*').eq('id', project_id).execute()
        if response.data:
            return jsonify(response.data[0]), 200
        return jsonify({'error': 'Project not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create new project/other information record
@app.route('/projects', methods=['POST'])
def create_project():
    try:
        data = request.get_json()

        if not data.get('project_name') or not data.get('description'):
            return jsonify({'error': 'project_name and description are required'}), 400

        new_item = {
            'project_name': data.get('project_name'),
            'description': data.get('description'),
            'images': data.get('images'),
            'files': data.get('files')
        }

        response = supabase.schema('public').table('other_information').insert(new_item).execute()
        return jsonify({'data': response.data, 'message': 'Project created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update project/other information record
@app.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    try:
        data = request.get_json()

        update_data = {}
        for key in ['project_name', 'description', 'images', 'files']:
            if key in data:
                update_data[key] = data[key]

        if not update_data:
            return jsonify({'error': 'No fields to update'}), 400

        response = supabase.schema('public').table('other_information').update(update_data).eq('id', project_id).execute()
        if response.data:
            return jsonify({'data': response.data, 'message': 'Project updated'}), 200
        return jsonify({'error': 'Project not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete project/other information record
@app.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    try:
        response = supabase.schema('public').table('other_information').delete().eq('id', project_id).execute()
        if response.data:
            return jsonify({'message': 'Project deleted'}), 200
        return jsonify({'error': 'Project not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5004)
