from flask_restful import Api, Resource, url_for

from .auth import auth_bp
from .auth.auth import Auth, Register
auth_api = Api(auth_bp)
auth_api.add_resource(Auth, '/signin')
auth_api.add_resource(Register, '/signup')

from .game import game_bp
from .game.guild import GuildList
from .game.guild import Guild
from .game.player import PlayerList
from .game.player import Player
from .game.item import ItemList
from .game.item import Item
game_api = Api(game_bp)
game_api.add_resource(GuildList, '/guilds')
game_api.add_resource(Guild, '/guilds/<int:guild_id>')
game_api.add_resource(PlayerList, '/players')
game_api.add_resource(Player, '/guilds/<int:player_id>')
game_api.add_resource(ItemList, '/items')
game_api.add_resource(Item, '/items/<int:item_id>')
