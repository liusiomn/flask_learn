from flask_restful import Resource, reqparse, fields, marshal
from flask import  request
from flask_learn.extensions import db
from flask_learn.common.decorators import token_required
from flask_learn.common.util import get_response
from flask_learn.model.model import  DBGuild, DBItem

guild_parser = reqparse.RequestParser()
guild_parser.add_argument('guild_name', 
                                    type = str, 
                                    location = 'json', 
                                    required=True, 
                                    help='guild name.')
guild_parser.add_argument('country_code', 
                                    type = int, 
                                    location = 'json', 
                                    required=True,
                                    help='country code.')

guild_fields = {
    'id': fields.Integer,
    'guild_name': fields.String,
    'country_code': fields.Integer,
    'skill_points': fields.Integer,
    'players': fields.List(fields.Integer),
    'items': fields.List(fields.Integer)
}

skill_point_fields={
    'skill_points': fields.Integer 
    }

class GuildList(Resource):
    method_decorators = [token_required] 

    def get(self):
        """Get guild list."""
        args = request.args
        current_page = request.args.get('currentPage', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)

        guilds = DBGuild.query.order_by(DBGuild.id.desc()).paginate(
                    current_page, 
                    page_size, 
                    error_out=False).items
        marshal_records = marshal(guilds, guild_fields)
        return get_response(200, 'success get guilds', marshal_records)

    def post(self):
        """Add a new guild"""
        args = guild_parser.parse_args()
        unique_guild = DBGuild.query.filter_by(guild_name=args['guild_name']).first()
        if unique_guild:
            return get_response(409,  'guild already existed!')
        try:
            new_guild = DBGuild(**args)
            db.session.add(new_guild)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return get_response(400,  "{e}".format(e=str(e)))
        return get_response(201, 'done!')


class Guild(Resource):
    method_decorators = [token_required] 

    def get(self, guild_id):
        """Get the detail info of the single guild."""
        current_guild = DBGuild.query.get(guild_id)
        if not current_guild:
            return get_response(404, 'Not exists.')
        results_wrapper = marshal(current_guild, guild_fields)
        return get_response(200, 'Got.', results_wrapper)

    def put(self, guild_id):
        """Update the indicated guild."""
        current_guild = DBGuild.query.get(guild_id)
        if not current_guild:
            return get_response(404, 'Not exists.')
        
        args = guild_parser.parse_args()
        try:
            current_guild.guild_name = args['guild_name']
            current_guild.country_code = args['country_code']
            db.session.add(current_guild)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return get_response(400,  "{e}".format(e=str(e)))
        return get_response(200, 'done!')

    def delete(self, guild_id):
        """Delete the indicated guild."""
        current_guild = DBGuild.query.get(guild_id)
        if not current_guild:
            return get_response(404, 'Not exists.')
        try:
            db.session.delete(current_guild)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return get_response(400,  "{e}".format(e=str(e)))
        return get_response(200, 'done!')
    
class GuildSkillPoint(Resource):
    
    method_decorators = [token_required] 
    def get(self, guild_id):
        current_guild = DBGuild.query.get(guild_id)
        if not current_guild:
            return get_response(404, 'Not exists.')
        skill_point = current_guild.skill_point 
        skill_point = skill_point + current_guild.skill_points_dif_by_picking_item
        try:
            db.session.add(current_guild)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return get_response(400,  "{e}".format(e=str(e)))
        results_wrapper = marshal(skill_point_fields, skill_point)
        return get_response(200, 'Got.', results_wrapper)
        
