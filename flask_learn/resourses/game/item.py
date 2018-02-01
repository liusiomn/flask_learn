from flask_restful import Resource, reqparse, fields, marshal
from flask import request
from flask_learn.extensions import db
from flask_learn.common.decorators import token_required
from flask_learn.common.util import get_response
from flask_learn.model.model import DBItem

item_parser = reqparse.RequestParser()
item_parser.add_argument('item_name', 
                                    type = str, 
                                    location = 'json', 
                                    required=True, 
                                    help='item name.')
item_parser.add_argument('skill_points', 
                                    type = int, 
                                    location = 'json', 
                                    required=True,
                                    help='kill_points.')

item_fields = {
    'id': fields.Integer,
    'item_name': fields.String,
    'country_code': fields.Integer,
    'skill_points': fields.Integer 
}

class ItemList(Resource):
    method_decorators = [token_required] 

    def get(self):
        """Get item list."""
        current_page = request.args.get('currentPage', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        items = DBItem.query.order_by(DBItem.id.desc()).paginate(
                    current_page, 
                    page_size, 
                    error_out=False).items
        marshal_records = marshal(items, item_fields)
        return get_response(200, 'success get items', marshal_records)            


    def post(self):
        """Add a new item"""
        args = item_parser.parse_args()
        unique_item = DBItem.query.filter_by(item_name=args['item_name']).first()
        if unique_item:
            return get_response(409,  'item already existed!')
        try:
            new_item = DBItem(**args)
            db.session.add(new_item)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return get_response(400,  "{e}".format(e=str(e)))
        return get_response(201, 'done!')


class Item(Resource):
    method_decorators = [token_required] 

    def get(self, item_id):
        """Get the detail info of the single item."""
        current_item = DBItem.query.get(item_id)
        if not current_item:
            return get_response(404, 'Not exists.')
        results_wrapper = marshal(current_item, item_fields)
        return get_response(200, 'Got.', results_wrapper)
    
    def put(self, item_id):
        """Update the indicated item."""
        current_item = DBItem.query.get(item_id)
        if not current_item:
            return get_response(404, 'Not exists.')
        
        args = item_parser.parse_args()
        try:
            current_item.item_name = args['item_name']
            current_item.skill_points = args['skill_points']
            db.session.add(current_item)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return get_response(400,  "{e}".format(e=str(e)))
        return get_response(200, 'done!')

    def delete(self, item_id):
        """Delete the indicated item."""
        current_item = DBItem.query.get(item_id)
        if not current_item:
            return get_response(404, 'Not exists.')
        try:
            db.session.delete(current_item)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return get_response(400,  "{e}".format(e=str(e)))
        return get_response(200, 'done!')
