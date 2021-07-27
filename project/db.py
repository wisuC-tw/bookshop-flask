import click
from flask import current_app, g
from flask.cli import with_appcontext
from sqlalchemy import create_engine, engine
import psycopg2
from pymongo import MongoClient

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db_engine" not in g:
        g.db_engine = MongoClient('mongodb://localhost:27017/')
    
    if "db" not in g:
        g.db = g.db_engine['testingdb']

    return g.db

def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)
    db_engine = g.pop("db_engine", None)
    if db_engine is not None:
        db_engine.close()

    # db_engine = g.pop("db_engine", None)

    # if db_engine is not None:
    #     db_engine.dispose()
        

def init_db():
    db = get_db()

@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")

def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)