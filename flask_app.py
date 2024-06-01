from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    missing_fields = [field for field in ['username', 'content', 'avatar_url', 'webhook_url'] if field not in data]
    
    if missing_fields:
        return jsonify({
            'status': 'error',
            'message': 'Missing data fields',
            'missing_fields': missing_fields
        }), 400
    
    payload = {
        'username': data['username'],
        'content': data['content'],
        'avatar_url': data['avatar_url']
    }
    
    response = requests.post(data['webhook_url'], json=payload)
    if response.status_code == 204:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Failed to send message via webhook',
            'error_details': response.text,
            'status_code': response.status_code
        }), 500

if __name__ == '__main__':
    app.run(port=5000)
