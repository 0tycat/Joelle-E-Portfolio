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

# Get all skills
@app.route('/skills', methods=['GET'])
def get_skills():
    try:
        response = supabase.schema('public').table('skills').select('*').execute()
        return jsonify({'data': response.data, 'count': len(response.data)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get skill by ID
@app.route('/skills/<int:skill_id>', methods=['GET'])
def get_skill(skill_id):
    try:
        response = supabase.schema('public').table('skills').select('*').eq('id', skill_id).execute()
        if response.data:
            return jsonify(response.data[0]), 200
        return jsonify({'error': 'Skill not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create new skill
@app.route('/skills', methods=['POST'])
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
        
        response = supabase.schema('public').table('skills').insert(new_skill).execute()
        return jsonify({'data': response.data, 'message': 'Skill created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update skill
@app.route('/skills/<int:skill_id>', methods=['PUT'])
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
        
        response = supabase.schema('public').table('skills').update(update_data).eq('id', skill_id).execute()
        
        if response.data:
            return jsonify({'data': response.data, 'message': 'Skill updated successfully'}), 200
        return jsonify({'error': 'Skill not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete skill
@app.route('/skills/<int:skill_id>', methods=['DELETE'])
def delete_skill(skill_id):
    try:
        response = supabase.schema('public').table('skills').delete().eq('id', skill_id).execute()
        
        if response.data:
            return jsonify({'message': 'Skill deleted successfully'}), 200
        return jsonify({'error': 'Skill not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)