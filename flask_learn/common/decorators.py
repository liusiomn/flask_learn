from functools import wraps
from flask import current_app, g, request
import jwt
from flask_learn.common.util import get_response
from flask_learn.model.model import DBUser

# check token to every request

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return get_response(401,  'Auth failed!')
        try: 
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
        except:
            return get_response(401,  'Auth failed!')
        g.current_user = DBUser.query.filter_by(username=data.get('user')).first()
        if g.current_user is None:
            return get_response(401,  'Auth failed!')
        return f(*args, **kwargs)
    return decorated

