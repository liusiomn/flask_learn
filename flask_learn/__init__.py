from flask import Flask, Blueprint, request, jsonify
from flask_migrate import Migrate, MigrateCommand
from .extensions import db
import os
import click
from .resourses.route import auth_bp, game_bp


APP_NAME = 'flask_learn'

def configure_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)

def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

def configure_error_handlers(app):
    @app.errorhandler(400)
    def valid_request_args(error):
        return jsonify(message='Bad Request!'), 400

    @app.errorhandler(401)
    def login_required(error):
        return jsonify(message="Login required!"), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify(message="Permission Denied!"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify(message="Page/Resource not found!"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return jsonify(message="Internal Server error!"), 500

def configure_data(app):
    env = os.environ
    app_config = app.config
    SQLALCHEMY_DATABASE_URI = \
    "mysql://{db_username}:{db_passwd}@{db_host}/{db_name}?charset=utf8".format(
        db_username = env.get('DB_USERNAME', app_config.get('DB_USERNAME')),
        db_passwd = env.get('DB_PASSWORD', app_config.get('DB_PASSWORD')),
        db_host = env.get('DB_HOST', app_config.get('DB_HOST')),
        db_name = env.get('DB_NAME', app_config.get('DB_NAME')),
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

def create_app(config_name='default'):
    app = Flask(APP_NAME)
    root_dir = os.path.abspath(os.path.dirname(__file__))
    config_file = os.path.join(root_dir, '..', 'config', 'flask_learn.cfg')
    app.config.from_pyfile(config_file)
    configure_data(app)
    configure_extensions(app)
    configure_blueprints(app, [auth_bp, game_bp])
    configure_error_handlers(app)
    return app

