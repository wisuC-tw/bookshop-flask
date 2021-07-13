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
        sort_on = request.args.get("sort-on") # id, author, title, image_url, small_image_url, price
        sort_order = request.args.get("sort-order") # ASC, DESC

        app.logger.info(sort_on)
        app.logger.info(sort_order)
        basic_query = "SELECT id, author, title, image_url, small_image_url, price FROM books50"
        if not sort_on and not sort_order:
            return run_query(f"{basic_query}")
        else:
            return run_query(f"{basic_query} ORDER BY {sort_on} {sort_order or ''}")


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

def run_query(query_string):
        db = get_db()
        rows = db.execute(
            query_string
        ).fetchall()

        column_names = rows[0].keys()
        data = [dict(zip(column_names, row)) for row in rows]
        
        return jsonify(data)