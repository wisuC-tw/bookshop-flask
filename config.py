import os

class Config(object):
    TESTING = False
    JSON_AS_ASCII = False

class DevelopmentConfig(Config):
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    database_name = os.getenv('DB_NAME')
    DB_SERVER = 'localhost'
    port = 5432

    FLASK_ENV = "dev"
    DATABASE_URI = f'postgresql+psycopg2://{username}:{password}@{DB_SERVER}:{port}/{database_name}'

class ProductionConfig(Config):
    pass

class TestConfig(Config):
    TESTING = True
    DATABASE_URI = 'sqlite:///booklist.db'