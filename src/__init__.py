from flask import Flask
from flask_pymongo import PyMongo, pymongo

app = Flask(__name__, instance_relative_config=True)

app.config.from_pyfile('config.py', silent=True)

mongo = PyMongo()

mongo.init_app(app)

from .user import User, SingleUser
from .post import SinglePost, Post
from .comment import PostComment, SinglePostComment

