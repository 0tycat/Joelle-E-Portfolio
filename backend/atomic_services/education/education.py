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

# Get all education records
@app.route('/education', methods=['GET'])
def get_education():
    try:
        response = supabase.schema('public').table('education').select('*').order('start_date', desc=True).execute()
        return jsonify({'data': response.data, 'count': len(response.data)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get single education record by ID
@app.route('/education/<int:edu_id>', methods=['GET'])
def get_education_item(edu_id):
    try:
        response = supabase.schema('public').table('education').select('*').eq('id', edu_id).execute()
        if response.data:
            return jsonify(response.data[0]), 200
        return jsonify({'error': 'Education record not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create new education record
@app.route('/education', methods=['POST'])
def create_education():
    try:
        data = request.get_json()

        if not data.get('institute_name') or not data.get('certification') or not data.get('start_date'):
            return jsonify({'error': 'institute_name, certification, start_date are required'}), 400

        new_item = {
            'institute_name': data.get('institute_name'),
            'certification': data.get('certification'),
            'start_date': data.get('start_date'),
            'finish_date': data.get('finish_date')
        }

        response = supabase.schema('public').table('education').insert(new_item).execute()
        return jsonify({'data': response.data, 'message': 'Education record created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/education/<int:edu_id>', methods=['PUT'])
def update_education(edu_id):
    try:
        data = request.get_json()

        update_data = {}
        for key in ['institute_name', 'certification', 'start_date', 'finish_date']:
            if key in data:
                update_data[key] = data[key]

        if not update_data:
            return jsonify({'error': 'No fields to update'}), 400

        response = supabase.schema('public').table('education').update(update_data).eq('id', edu_id).execute()
        if response.data:
            return jsonify({'data': response.data, 'message': 'Education record updated'}), 200
        return jsonify({'error': 'Education record not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/education/<int:edu_id>', methods=['DELETE'])
def delete_education(edu_id):
    try:
        response = supabase.schema('public').table('education').delete().eq('id', edu_id).execute()
        if response.data:
            return jsonify({'message': 'Education record deleted'}), 200
        return jsonify({'error': 'Education record not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
