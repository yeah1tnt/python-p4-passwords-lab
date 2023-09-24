#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')

        if username and password:
            user = User(username = username)

            user.password_hash = password

            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id
            return user.to_dict(), 201

class CheckSession(Resource):
    
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id == session['user_id']).first()
            user_dict = user.to_dict()
            return user_dict, 200
        return {}, 204

class Login(Resource):
    
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')

        user = User.query.filter(User.username == username).first()
        if user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        return {}, 401

class Logout(Resource):
    
    def delete(self):
        session['user_id'] = None
        return {}, 204


api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
