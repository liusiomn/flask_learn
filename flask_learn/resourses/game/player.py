from flask_restful import Api, Resource, url_for, reqparse, abort, marshal_with, fields, marshal
from flask import current_app, g, request
from flask_learn.extensions import db
from flask_learn.common.decorators import token_required
from flask_learn.common.util import get_response
from flask_learn.model.model import DBUser, DBGuild, DBPlayer, DBItem

player_parser = reqparse.RequestParser()
player_parser.add_argument('nickname', 
                                    type = str, 
                                    location = 'json', 
                                    required=True, 
                                    help='nick name.')
player_parser.add_argument('email', 
                                    type = str, 
                                    location = 'json', 
                                    required=True,
                                    help='email address.')

player_fields = {
    'id': fields.Integer,
    'nickname': fields.String,
    'email': fields.String,
    'guild_id': fields.Integer,
    'items': fields.List(fields.Integer)
}

class PlayerList(Resource):
    method_decorators = [token_required] 

    def get(self):
        """Get Player list."""
        args = request.args
        current_page = request.args.get('currentPage', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)

        player = DBPlayer.query.order_by(DBPlayer.id.desc()).paginate(
                    current_page, 
                    page_size, 
                    error_out=False).items
        marshal_records = marshal(player, player_fields)
        return get_response(200, 'success get players', marshal_records)


    def post(self):
        """Add a new player"""
        args = player_parser.parse_args()
        print(args)
        unique_player = DBPlayer.query.filter_by(nickname=args['nickname']).first()
        if unique_player:
            return get_response(409,  'player already existed!')
        try:
            new_player = DBPlayer(**args)
            db.session.add(new_player)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return get_response(400,  "{e}".format(e=str(e)))
        return get_response(201, 'done!')


class Player(Resource):
    method_decorators = [token_required] 

    def get(self, player_id):
        """Get the detail info of the single player."""
        current_player = DBPlayer.query.get(player_id)
        if not current_player:
            return get_response(404, 'Not exists.')
        results_wrapper = marshal(current_player, player_fields)
        return get_response(200, 'Got.', results_wrapper)

    def put(self, player_id):
        """Update the indicated player."""
        current_player = DBPlayer.query.get(player_id)
        if not current_player:
            return get_response(404, 'Not exists.')
        
        args = player_parser.parse_args()
        try:
            current_player.nickname = args['nickname']
            current_player.email = args['email']
            db.session.add(current_player)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return get_response(400,  "{e}".format(e=str(e)))
        return get_response(200, 'done!')

    def delete(self, player_id):
        """Delete the indicated player."""
        current_player = DBPlayer.query.get(player_id)
        if not current_player:
            return get_response(404, 'Not exists.')
        try:
            db.session.delete(current_player)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return get_response(400,  "{e}".format(e=str(e)))
        return get_response(200, 'done!')
