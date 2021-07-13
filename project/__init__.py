from flask import Flask, request, jsonify, g
import logging
from logging.handlers import WatchedFileHandler
import os 
from project.db import get_db

def create_app(config_filename=None):
    app= Flask(__name__)
    
    app.config['DATABASE_URI']=os.path.join(app.root_path, "booklist.db")

    setup_routes(app)
    setup_logging(app)

    from project import db
    db.init_app(app)

    return app

def setup_routes(app):
    @app.route('/')
    def index():
        return 'Index Page'

    @app.route('/hello')
    def hello():
        return 'Hello, World'

    @app.route('/books')
    def books():
        db = get_db()
        rows = db.execute(
            "SELECT * FROM books50"
        ).fetchall()

        column_names = rows[0].keys()
        data = [dict(zip(column_names, row)) for row in rows]
        
        return jsonify(data)

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
