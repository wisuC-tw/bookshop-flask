from flask import Flask

app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')

from project.logger_setup import setup_logging
setup_logging(app)

from project import db
db.init_app(app)

from project import views
_ = views

from project import views_mongo
_ = views_mongo
