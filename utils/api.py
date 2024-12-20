from flask import jsonify
import requests
import json

class APIUtils:
    # Generate Response
    def generate_response(status=True, data=None, message=None, error=None, status_code=200):
        response = {
            "status": status,
            "data": data,
            "message": message,
            "error": error
        }
        # Remove keys with None values
        response = {k: v for k, v in response.items() if v is not None}
        return jsonify(response), status_code
    
    # Call the API
    def make_api(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        return requests.get(url, headers=headers)

    # Check Response
    def check_response(response):
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            print("Error: ", response.status_code)
            return None