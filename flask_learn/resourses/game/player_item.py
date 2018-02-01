from flask_restful import Api, Resource, url_for, reqparse, abort, marshal_with, fields, marshal
from flask import current_app, g, request
from flask_learn.extensions import db
from flask_learn.common.decorators import token_required
from flask_learn.common.util import get_response
from flask_learn.model.model import DBUser, DBGuild, DBPlayer, DBItem, DBPlayerItem

player_item_parser = reqparse.RequestParser()
player_item_parser.add_argument('item_id', 
                                    type = int, 
                                    location = 'json', 
                                    required=True, 
                                    help='item_id')
player_item_parser.add_argument('player_id', 
                                    type = int, 
                                    location = 'json', 
                                    required=True,
                                    help='player_id')

player_item_fields = {
    'id': fields.Integer,
    'item_id': fields.Integer,
    'player_id': fields.Integer,
}

class PlayerItem(Resource):
    method_decorators = [token_required] 
    def post(self):
        args = player_item_parser.parse_args()
        current_player = DBPlayer.query.get(args['player_id'])
        if not current_player:
            return get_response(404, 'Not exists.')
        current_item = DBItem.query.get(args['item_id'])
        if not current_item:
            return get_response(404, 'Not exists.')
        if args['item_id'] in current_player.items:
            return get_response(412, 'Already have this item')
        try:
            player_item = DBPlayerItem(**args)
            db.session.add(player_item)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return get_response(400,  "{e}".format(e=str(e)))
        return get_response(201, 'done!')
    