from flask import Flask, request, jsonify, g
import logging
from logging.handlers import WatchedFileHandler
import os 

def create_app(config_filename=None):
    app= Flask(__name__)
    setup_routes(app)
    setup_logging(app)

    return app

def setup_routes(app):
    @app.route('/')
    def index():
        return 'Index Page'

    @app.route('/hello')
    def hello():
        return 'Hello, World'

def setup_logging(app):
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = WatchedFileHandler('debug.log')
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

    @app.after_request
    def after_request(response):
        app.logger.info('%s %s %s %s %s', request.remote_addr, request.method, request.scheme, request.full_path, response.status)
        return response
