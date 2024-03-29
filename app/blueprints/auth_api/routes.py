from . import auth_api
from flask import request, jsonify
from app.models import db, User
from werkzeug.security import check_password_hash
from flask_login import login_required, login_user, logout_user

# Create User
@auth_api.post('/signup')
def signup_api():
    '''
    payload should include
    {
    "username": "string",
    "password": "string"
    }
    '''
    data = request.get_json()
    queried_user = User.query.filter(User.username == data['username']).first()
    if not queried_user:
        new_user = User(username = data['username'], password=data['password'])

        new_user.save()
        return jsonify({
            'status': 'ok',
            'message': 'User was successfully created'
        })
    else:
        return jsonify({
            'status': 'not ok',
            'message': 'Username already exists'
        })

@auth_api.get('/login')
def login_api():
    '''
    payload should include
    {
    "username": "string",
    "password": "string"
    }
    '''
    data = request.get_json()
    queried_user = User.query.filter(User.username == data['username']).first()
    if queried_user and check_password_hash(queried_user.password, data['password']):
        login_user(queried_user)
        return jsonify({
            'status': 'ok',
            'message': 'User was successfully logged in'
        })
    else:
        return jsonify({
            'status': 'not ok',
            'message': 'Username or password are incorrect'
        })
    
@auth_api.get('/logout')
@login_required
def logout_api():
    '''
    payload should include
    {
    "username": "string",
    }
    '''
    data = request.get_json()
    queried_user = User.query.filter(User.username == data['username']).first()
    if queried_user:
        logout_user()
        return jsonify({
            'status': 'ok',
            'message': 'User was successfully logged out'
        })
    else:
        return jsonify({
            'status': 'not ok',
            'message': 'User does not exist'
        })