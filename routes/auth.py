from flask import request, jsonify
from controllers.auth import Auth

def auth():
    try:
        data = request.get_json()
        auth = Auth()

        if request.method == 'POST':
            return auth.add_user(data)
        elif request.method == 'GET':
            email = request.args.get('email')
            return auth.authenticate(email)
    except Exception as e:
        return jsonify({"error": str(e)})