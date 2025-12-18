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

# get all work experience records
@app.route('/work', methods=['GET'])
def get_work():
    try:
        response = supabase.schema('public').table('work_experience').select('*').order('start_date', desc=True).execute()
        return jsonify({'data': response.data, 'count': len(response.data)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# get single work experience record by ID
@app.route('/work/<int:work_id>', methods=['GET'])
def get_work_item(work_id):
    try:
        response = supabase.schema('public').table('work_experience').select('*').eq('id', work_id).execute()
        if response.data:
            return jsonify(response.data[0]), 200
        return jsonify({'error': 'Work record not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create new work experience record
@app.route('/work', methods=['POST'])
def create_work():
    try:
        data = request.get_json()

        if not data.get('company_name') or not data.get('role') or not data.get('start_date'):
            return jsonify({'error': 'company_name, role, start_date are required'}), 400

        new_item = {
            'company_name': data.get('company_name'),
            'role': data.get('role'),
            'start_date': data.get('start_date'),
            'end_date': data.get('end_date'),
            'description': data.get('description')
        }

        response = supabase.schema('public').table('work_experience').insert(new_item).execute()
        return jsonify({'data': response.data, 'message': 'Work record created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update work experience record
@app.route('/work/<int:work_id>', methods=['PUT'])
def update_work(work_id):
    try:
        data = request.get_json()

        update_data = {}
        for key in ['company_name', 'role', 'start_date', 'end_date', 'description']:
            if key in data:
                update_data[key] = data[key]

        if not update_data:
            return jsonify({'error': 'No fields to update'}), 400

        response = supabase.schema('public').table('work_experience').update(update_data).eq('id', work_id).execute()
        if response.data:
            return jsonify({'data': response.data, 'message': 'Work record updated'}), 200
        return jsonify({'error': 'Work record not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete work experience record
@app.route('/work/<int:work_id>', methods=['DELETE'])
def delete_work(work_id):
    try:
        response = supabase.schema('public').table('work_experience').delete().eq('id', work_id).execute()
        if response.data:
            return jsonify({'message': 'Work record deleted'}), 200
        return jsonify({'error': 'Work record not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)
