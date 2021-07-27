from flask import request, Response, jsonify, g
from app import app
from project.db import get_db
from bson.json_util import dumps
import re

@app.route('/books')
def books():
    sort_on = request.args.get("sort-on") # id, author, title, image_url, small_image_url, price
    sort_order = request.args.get("sort-order") # 1, -1
    
    db = get_db()
    if not sort_on and not sort_order:
        result = db['SomeCollection'].find({}, {'_id': False})
    else:
        if not sort_on: sort_on = 'id'
        sort_order = int(sort_order) if sort_order else 1
        result = db['SomeCollection'].find({}, {'_id': False}) \
                                    .sort(sort_on, sort_order)
    
    return format_response(result)

@app.route('/books/search')
def books_search():
    if not request.args:
        return 'No search parameters were provided.'

    name = request.args.get("name")
    price = request.args.get("price")
    language = request.args.get("language")
    isbn = request.args.get("isbn")
    query_conditions = []
    if name:
        regex_pattern = re.compile(rf'.*{name}.*', re.I)
        query_conditions.append({"author": {'$regex': regex_pattern}})
        query_conditions.append({"title": {'$regex': regex_pattern}})
    if price:
        query_conditions.append({"price": {'$eq': int(price)}})
    if language:
        regex_pattern = re.compile(rf'.*{language}.*', re.I)
        query_conditions.append({"language_code": {'$regex': regex_pattern}})
    if isbn:
        regex_pattern = re.compile(rf'\d*{isbn}\d*', re.I)
        query_conditions.append({"isbn": {'$regex': regex_pattern}})
        query_conditions.append({"isbn13": {'$regex': regex_pattern}})
    
    #todo return filtered result 'or'
    db = get_db()
    result = db['SomeCollection'].find({'$or': query_conditions}, {'_id': False})
    return format_response(result)

@app.route('/books/<int:book_id>')
def books_id(book_id):
    db = get_db()
    result = db['SomeCollection'].find({'id': book_id}, {'_id': False})
    return format_response(result)

def format_response(data):
    return Response(dumps(data), mimetype='application/json')
