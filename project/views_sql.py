from flask import request, jsonify, g
from app import app
from project.db import get_db 
import os

@app.route('/environment')
def get_environment():
    if os.getenv("CURRENT_ENV"):
        return 'This is ' + os.getenv("CURRENT_ENV")
    return 'No environment variable for "CURRENT_ENV" was defined'

@app.route('/books')
def books():
    sort_on = request.args.get("sort-on") # id, author, title, image_url, small_image_url, price
    sort_order = request.args.get("sort-order") # ASC, DESC
    basic_query = "SELECT id, author, title, image_url, small_image_url, price FROM books50"
    if not sort_on and not sort_order:
        return run_query(f"{basic_query}")
    else:
        return run_query(f"{basic_query} ORDER BY {sort_on or 'id'} {sort_order or ''}")

@app.route('/books/search')
def books_search():
    if not request.args:
        return 'No search parameters were provided.'

    name = request.args.get("name")
    price = request.args.get("price")
    language = request.args.get("language")
    isbn = request.args.get("isbn")
    
    basic_query = "SELECT * FROM books50"
    query_conditions_list = []
    if name:
        query_conditions_list.append(f"title LIKE '%{name}%'")
        query_conditions_list.append(f"author LIKE '%{name}%'")
    if price:
        query_conditions_list.append(f"price LIKE '%{price}%'")
    if language:
        query_conditions_list.append(f"language_code LIKE '%{language}%'")
    if isbn:
        query_conditions_list.append(f"isbn LIKE '%{isbn}%'")
        query_conditions_list.append(f"isbn LIKE '%{isbn}%'")
    query_conditions_string = ' OR '.join(query_conditions_list)

    return run_query(f"{basic_query} WHERE {query_conditions_string}")

@app.route('/books/<int:book_id>')
def books_id(book_id):
    return run_query(f"SELECT * FROM books50 WHERE id = {book_id}")

def run_query(query_string):
    db = get_db()
    rows = db.execute(
        query_string
    ).fetchall()
    
    if not rows:
        return jsonify([])

    column_names = rows[0].keys()
    data = [dict(zip(column_names, row)) for row in rows]
    
    return jsonify(data)