from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, Resource, url_for

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')




