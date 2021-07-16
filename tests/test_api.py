import unittest
from unittest.mock import patch
from app import app
import json
import logging
from flask import request

class ApiTest(unittest.TestCase):
    
    BASE_URL = "http://127.0.0.1:5000"
    API_URL = BASE_URL + "/books"

    def setUp(self):
        self.c = app.test_client()
        self.c.testing = True

    def test_index(self):
        r = self.c.get('/')
        self.assertEqual(200, r.status_code)
        self.assertEqual(b"Index Page", r.get_data())

    def test_home(self):
        r = self.c.get('/hello')
        self.assertEqual(200, r.status_code)
        self.assertEqual(b"Hello, World", r.get_data())

    def test_books_id_returns_book_details_with_id(self):
        r = self.c.get('/books/1')
        self.assertEqual(200, r.status_code)
        expected_data = [
            {
                "author": "Suzanne Collins", 
                "average_rating": 4.34, 
                "id": 1, 
                "image_url": "https://images.gr-assets.com/books/1447303603m/2767052.jpg", 
                "isbn": "439023483", 
                "isbn13": 9780439023480.0, 
                "language_code": "eng", 
                "original_publication_year": 2008, 
                "original_title": "The Hunger Games", 
                "price": 3583, 
                "small_image_url": "https://images.gr-assets.com/books/1447303603s/2767052.jpg", 
                "title": "The Hunger Games (The Hunger Games, #1)"
            }
        ]
        self.assertEqual(expected_data, json.loads(r.get_data()))

    def test_books_search_no_parameters(self):
        r = self.c.get('/books/search')
        self.assertEqual(200, r.status_code)
        self.assertEqual(b"No search parameters were provided.", r.get_data())

    def test_books_search_name_returns_author_and_title(self):
        r = self.c.get('/books/search?name=ger')
        self.assertEqual(200, r.status_code)
        expected_data = [
            {
                "author": "Suzanne Collins",
                "average_rating": 4.34,
                "id": 1,
                "image_url": "https://images.gr-assets.com/books/1447303603m/2767052.jpg",
                "isbn": "439023483",
                "isbn13": 9780439023480.0,
                "language_code": "eng",
                "original_publication_year": 2008,
                "original_title": "The Hunger Games",
                "price": 3583,
                "small_image_url": "https://images.gr-assets.com/books/1447303603s/2767052.jpg",
                "title": "The Hunger Games (The Hunger Games, #1)"
            },
            {
                "author": "F. Scott Fitzgerald",
                "average_rating": 3.89,
                "id": 5,
                "image_url": "https://images.gr-assets.com/books/1490528560m/4671.jpg",
                "isbn": "743273567",
                "isbn13": 9780743273560.0,
                "language_code": "eng",
                "original_publication_year": 1925,
                "original_title": "The Great Gatsby",
                "price": 1389,
                "small_image_url": "https://images.gr-assets.com/books/1490528560s/4671.jpg",
                "title": "The Great Gatsby"
            },
            {
                "author": "J.D. Salinger",
                "average_rating": 3.79,
                "id": 8,
                "image_url": "https://images.gr-assets.com/books/1398034300m/5107.jpg",
                "isbn": "316769177",
                "isbn13": 9780316769170.0,
                "language_code": "eng",
                "original_publication_year": 1951,
                "original_title": "The Catcher in the Rye",
                "price": 3813,
                "small_image_url": "https://images.gr-assets.com/books/1398034300s/5107.jpg",
                "title": "The Catcher in the Rye"
            },
            {
                "author": "Suzanne Collins",
                "average_rating": 4.3,
                "id": 17,
                "image_url": "https://images.gr-assets.com/books/1358273780m/6148028.jpg",
                "isbn": "439023491",
                "isbn13": 9780439023500.0,
                "language_code": "eng",
                "original_publication_year": 2009,
                "original_title": "Catching Fire",
                "price": 1388,
                "small_image_url": "https://images.gr-assets.com/books/1358273780s/6148028.jpg",
                "title": "Catching Fire (The Hunger Games, #2)"
            },
            {
                "author": "Suzanne Collins",
                "average_rating": 4.03,
                "id": 20,
                "image_url": "https://images.gr-assets.com/books/1358275419m/7260188.jpg",
                "isbn": "439023513",
                "isbn13": 9780439023510.0,
                "language_code": "eng",
                "original_publication_year": 2010,
                "original_title": "Mockingjay",
                "price": 105,
                "small_image_url": "https://images.gr-assets.com/books/1358275419s/7260188.jpg",
                "title": "Mockingjay (The Hunger Games, #3)"
            },
            {
                "author": "Audrey Niffenegger",
                "average_rating": 3.95,
                "id": 38,
                "image_url": "https://images.gr-assets.com/books/1437728815m/14050.jpg",
                "isbn": "965818675",
                "isbn13": 9780965818670.0,
                "language_code": "eng",
                "original_publication_year": 2003,
                "original_title": "The Time Traveler's Wife",
                "price": 1800,
                "small_image_url": "https://images.gr-assets.com/books/1437728815s/14050.jpg",
                "title": "The Time Traveler's Wife"
            }
        ]
        self.assertEqual(expected_data, json.loads(r.get_data()))
    