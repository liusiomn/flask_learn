from flask_restful import Resource, reqparse, fields
from flask import  request
from flask_learn.extensions import db
from flask_learn.common.decorators import token_required
from flask_learn.common.util import get_response
from flask_learn.model.model import DBUser, DBGuild, DBPlayer, DBItem

player_guild_parser = reqparse.RequestParser()
player_guild_parser.add_argument('guild_id', 
                                    type = int, 
                                    location = 'json', 
                                    required=True, 
                                    help='guild_id')
player_guild_parser.add_argument('player_id', 
                                    type = int, 
                                    location = 'json', 
                                    required=True,
                                    help='player_id')

player_guild_fields = {
    'id': fields.Integer,
    'guild_id': fields.Integer,
    'player_id': fields.Integer,
}

class PlayerGuild(Resource):
    method_decorators = [token_required] 
    
    def post(self):
        args = player_guild_parser.parse_args()
        current_guild = DBGuild.query.get(args['guild_id'])
        if not current_guild:
            return get_response(404, 'guild Not exists.')
        current_player = DBPlayer.query.get(args['player_id'])
        if not current_player:
            return get_response(404, 'player Not exists.')
        if current_player.guild_id == args['guild_id']:
            return get_response(412, 'Already in guild.')
        try:
            current_player.guild_id = args['guild_id']
            db.session.add(current_player)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return get_response(400,  "{e}".format(e=str(e)))
        return get_response(201, 'done!')
    
    def put(self):
        args = player_guild_parser.parse_args()
        current_guild = DBGuild.query.get(args['guild_id'])
        if not current_guild:
            return get_response(404, 'guild Not exists.')
        current_player = DBPlayer.query.get(args['player_id'])
        if not current_player:
            return get_response(404, 'player Not exists.')
        if current_player.guild_id != args['guild_id']:
            return get_response(412, 'Player not in guild')
        try:
            current_player.guild_id = 0
            db.session.add(current_guild)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return get_response(400,  "{e}".format(e=str(e)))
        return get_response(201, 'done!')
        