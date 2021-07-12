from flask import Flask

def create_app(config_filename=None):
    app= Flask(__name__)
    return app