from src import app, mongo
from flask import render_template, jsonify, json, request
from flask_restplus import Resource
from bson import json_util, errors
from bson.objectid import ObjectId
from .user import namespace


@namespace.route('/post')
class Post(Resource):
    @namespace.doc(description='<h3>list all posts</h3>')
    def get(self):
        try:
            post_collections = mongo.db.posts
            return [ json.loads(json_util.dumps(doc, default=json_util.default)) for doc in post_collections.find({"isDelete":False})]
        except Exception as e:
            return {"error": str(e)}

    @namespace.doc(description='create a new post')
    def post(self):
        try:
            post_info = request.get_json()
            post_info["isDelete"] = True
            mongo.db.posts.insert(post_info)
            return 'added post'
        except Exception as e:
            return {"error": str(e)}

@namespace.route('/post/<string:id>')
class SinglePost(Resource):
    @namespace.doc(description='get a single post')
    def get(self, id):
        try:
            post_collections = mongo.db.posts        
            return [ json.loads(json_util.dumps(doc, default=json_util.default)) for doc in post_collections.find({"_id":ObjectId(id),"isDelete":False})]
        except Exception as e:
            return {"error": str(e)}

    @namespace.doc(description='update a post')
    def patch(self):
        try:
            post_info = request.get_json()
            mongo.db.posts.update({"_id":ObjectId(id)},{"$set":post_info})
            return {"msg":'updated post'}
        except Exception as e:
            return {"error": str(e)}

    @namespace.doc(description='Delete a post')
    def delete(self, id, commentId):
        try:
            mongo.db.posts.update({"_id":ObjectId(commentId)},{"$set":{"isDelete":True}})
            return 'post is deleted'
        except Exception as e:
            return {"error": str(e)}