from flask_restful import Resource, reqparse
from flask import current_app
import datetime
import jwt
from flask_learn.extensions import db
from flask_learn.model.model import DBUser
from flask_learn.common.util import get_response


class Auth(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type = str, location = 'json')
        self.reqparse.add_argument('password', type = str, location = 'json')
        super(Auth, self).__init__()

    def post(self):
        """Auth by the registered users"""
        args = self.reqparse.parse_args()
        username, password = args['username'], args['password']
        auth_user = DBUser.query.filter_by(
            username = username
            ).first()
        if auth_user is None:
            return get_response(401,  'Auth failed！')
        if not auth_user.verify_password(password) :
            return get_response(401,  'Auth failed！')
        print("xxxxxxxxxxxx")
        token = self._make_token(auth_user)
        print("vvvvvvvvvvvvvvvv")
        response_data = {'token' : token.decode('UTF-8')}
        return get_response(200, 'success', response_data)

    def _make_token(self, auth_user):
        return jwt.encode({
                    'user' : auth_user.username, 
                    'exp' : datetime.datetime.now() + datetime.timedelta(hours=24)
                }, current_app.config['SECRET_KEY']
            )

class Register(Resource):
    def __init__(self):
        super(Register, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type = str, 
                                    location = 'json', required=True)
        self.reqparse.add_argument('password', type = str, 
                                    location = 'json', required=True)
        self.reqparse.add_argument('password2', type = str, 
                                    location = 'json', required=True)
        self.reqparse.add_argument('email', type = str, 
                                    location = 'json', required=True)

    def post(self):
        """Register a new user"""
        args = self.reqparse.parse_args()
        auth_user = DBUser.query.filter_by(
            username = args['username']).first()
        if auth_user:
            return get_response(409,  'User already existed!')
        new_user = DBUser(
            username=args['username'], email=args['email'])
        new_user.password = args['password']
        db.session.add(new_user)
        db.session.commit()
        return get_response(200, 'success')
