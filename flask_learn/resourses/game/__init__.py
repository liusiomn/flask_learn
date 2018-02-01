
from flask import Flask, Blueprint
from flask_restful import Api

game_bp = Blueprint('game', __name__, url_prefix='/api/game')

game_api = Api(game_bp)

