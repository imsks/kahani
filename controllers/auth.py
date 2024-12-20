from flask import jsonify
from database.models import User
from utils.api import APIUtils

class Auth:
    def add_user(self, data):
        user = User().store_user(data)
        return APIUtils.generate_response(data=user, status_code=200)
    
    def authenticate(self, email):
        user = User().get_user_by_email(email)

        if user is None:
            return APIUtils.generate_response(error="User not found", status_code=404)
        
        return APIUtils.generate_response(data=user, status_code=200)