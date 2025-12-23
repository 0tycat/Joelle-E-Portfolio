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

TABLE_NAME = 'e_portfolio'  # Assumes table name is e_portfolio

# Get all e-portfolio activities
@app.route('/e_portfolio', methods=['GET'])
def get_e_portfolio():
    try:
        response = supabase.table(TABLE_NAME).select('*').execute()
        return jsonify({'data': response.data, 'count': len(response.data)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get single activity by ID
@app.route('/e_portfolio/<int:item_id>', methods=['GET'])
def get_e_portfolio_item(item_id: int):
    try:
        response = supabase.table(TABLE_NAME).select('*').eq('id', item_id).execute()
        if response.data:
            return jsonify(response.data[0]), 200
        return jsonify({'error': 'E-portfolio activity not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create new activity
@app.route('/e_portfolio', methods=['POST'])
@require_auth
def create_e_portfolio():
    try:
        data = request.get_json()

        if not data.get('activity_name') or not data.get('description'):
            return jsonify({'error': 'activity_name and description are required'}), 400

        new_item = {
            'activity_name': data.get('activity_name'),
            'description': data.get('description')
        }

        response = supabase.table(TABLE_NAME).insert(new_item).execute()
        return jsonify({'data': response.data, 'message': 'E-portfolio activity created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update activity
@app.route('/e_portfolio/<int:item_id>', methods=['PUT'])
@require_auth
def update_e_portfolio(item_id: int):
    try:
        data = request.get_json()

        update_data = {}
        for key in ['activity_name', 'description']:
            if key in data:
                update_data[key] = data[key]

        if not update_data:
            return jsonify({'error': 'No fields to update'}), 400

        response = supabase.table(TABLE_NAME).update(update_data).eq('id', item_id).execute()
        if response.data:
            return jsonify({'data': response.data, 'message': 'E-portfolio activity updated'}), 200
        return jsonify({'error': 'E-portfolio activity not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete activity
@app.route('/e_portfolio/<int:item_id>', methods=['DELETE'])
@require_auth
def delete_e_portfolio(item_id: int):
    try:
        response = supabase.table(TABLE_NAME).delete().eq('id', item_id).execute()
        if response.data:
            return jsonify({'message': 'E-portfolio activity deleted'}), 200
        return jsonify({'error': 'E-portfolio activity not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5006)
