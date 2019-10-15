from src import app, mongo
from flask import json, request
from flask_restplus import Resource, Api
from bson import json_util, errors
from bson.objectid import ObjectId
from .user import namespace

@namespace.route('/post/<string:id>/comments')
class PostComment(Resource):
    @namespace.doc(description='get all comments in a post')
    def get(self, id):
        try:
            pipeline = [{"$match": {"postId":ObjectId(id),"isDelete": False}},{ "$lookup": { "from": "posts", "localField": "postId", "foreignField": "_id", "as": "post"}}]
            comments_collection = mongo.db.comments.aggregate(pipeline)
            return [ json.loads(json_util.dumps(doc, default=json_util.default)) for doc in comments_collection ]
        except Exception as e:
            return {"error": str(e)}

    @namespace.doc(description='make a new comment under a post')
    def post(self, id):
        try:
            comment_info = request.get_json()
            comment_info['postId'] = ObjectId(id)
            comment_info["isDelete"] = False
            mongo.db.comments.insert(comment_info)
            return 'added comment'
        except Exception as e:
            return {"error": str(e)}

@namespace.route('/post/<string:id>/comment/<string:commentId>')
class SinglePostComment(Resource):
    @namespace.doc(description='get a single comment under a post')
    def get(self, id, commentId):
        try:
            pipeline = [{"$match": {"_id":ObjectId(commentId),"isDelete": False}},{ "$lookup": { "from": "posts", "localField": "postId", "foreignField": "_id", "as": "post"}}]
            comments_collection = mongo.db.comments.aggregate(pipeline)
            return [ json_util.dumps(doc, default=json_util.default) for doc in comments_collection if doc.isDelete == False]
        except Exception as e:
            return {"error": str(e)}

    @namespace.doc(description='update a single comment under a post')
    def patch(self, id, commentId):
        try:
            comment_info = request.get_json()
            mongo.db.comments.update({"_id":ObjectId(commentId)},{"$set":comment_info})
            return 'updated comment'
        except Exception as e:
            return {"error": str(e)}

    @namespace.doc(description='Delete a comment')
    def delete(self, id, commentId):
        try:
            mongo.db.comments.update({"_id":ObjectId(commentId)},{"$set":{"isDelete":True}})
            return 'comment is deleted'
        except Exception as e:
            return {"error": str(e)}