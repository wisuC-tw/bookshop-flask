from flask import request
from app import app
import os

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.after_request
def after_request(response):
    app.logger.info('%s %s %s %s %s', request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response

@app.route('/environment')
def get_environment():
    if os.getenv("CURRENT_ENV"):
        return 'This is ' + os.getenv("CURRENT_ENV")
    return 'No environment variable for "CURRENT_ENV" was defined'