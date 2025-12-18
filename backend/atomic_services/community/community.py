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

# Retrieve all community service records
@app.route('/community', methods=['GET'])
def get_community():
    try:
        response = supabase.schema('public').table('community_service').select('*').execute()
        return jsonify({'data': response.data, 'count': len(response.data)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Retrieve a single community service record by ID
@app.route('/community/<int:item_id>', methods=['GET'])
def get_community_item(item_id):
    try:
        response = supabase.schema('public').table('community_service').select('*').eq('id', item_id).execute()
        if response.data:
            return jsonify(response.data[0]), 200
        return jsonify({'error': 'Community service record not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create new community service record
@app.route('/community', methods=['POST'])
def create_community():
    try:
        data = request.get_json()

        if not data.get('programme_name') or not data.get('role') or not data.get('description'):
            return jsonify({'error': 'programme_name, role, description are required'}), 400

        new_item = {
            'programme_name': data.get('programme_name'),
            'role': data.get('role'),
            'description': data.get('description')
        }

        response = supabase.schema('public').table('community_service').insert(new_item).execute()
        return jsonify({'data': response.data, 'message': 'Community service record created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update community service record
@app.route('/community/<int:item_id>', methods=['PUT'])
def update_community(item_id):
    try:
        data = request.get_json()
        update_data = {}
        for key in ['programme_name', 'role', 'description']:
            if key in data:
                update_data[key] = data[key]
        if not update_data:
            return jsonify({'error': 'No fields to update'}), 400
        response = supabase.schema('public').table('community_service').update(update_data).eq('id', item_id).execute()
        if response.data:
            return jsonify({'data': response.data, 'message': 'Community service record updated'}), 200
        return jsonify({'error': 'Community service record not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete community service record
@app.route('/community/<int:item_id>', methods=['DELETE'])
def delete_community(item_id):
    try:
        response = supabase.schema('public').table('community_service').delete().eq('id', item_id).execute()
        if response.data:
            return jsonify({'message': 'Community service record deleted'}), 200
        return jsonify({'error': 'Community service record not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5003)
