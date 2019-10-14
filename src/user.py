from src import app, mongo
from flask import render_template, jsonify, json, request
from flask_restplus import Resource, Api, fields
from bson import json_util, errors
from bson.objectid import ObjectId
from validator_collection import checkers

api = Api(app, version='1.0', title='Blog API', description="A Simple Blog API")

namespace = api.namespace('', description='Main API  Routes')

user_fields = namespace.model("User", {"name": fields.String, "email": fields.String, "dateOfBirth": fields.String})

@namespace.route('/user')
class User(Resource):
    @namespace.doc(description='list all users')
    def get(self):
        user_collections = mongo.db.users        
        return [ json.loads(json_util.dumps(doc, default=json_util.default)) for doc in user_collections.find({"isDelete":False})]

    @namespace.doc(description='create a new user')
    @namespace.expect(user_fields)
    def post(self):
        user_info = request.get_json()
        params = ['name', 'email', 'dateOfBirth']
        for i in user_info.keys():
            if i not in params:
                return {"msg": "invalid request"}
        if checkers.is_string(user_info['name']) == False \
            or checkers.is_email(user_info['email']) == False \
                or checkers.is_date(user_info['dateOfBirth']) == False:
            return {"msg": "invalid request"}, 400
        user_info["isDelete"] = False
        mongo.db.users.insert(user_info)
        return 'added user'

@namespace.route('/user/<string:id>')
class SingleUser(Resource):
    @namespace.doc(description='get a single user using id')
    def get(self, id):
        user_collections = mongo.db.users
        try:        
            return [ json.loads(json_util.dumps(doc, default=json_util.default)) for doc in user_collections.find({"_id":ObjectId(id),"isDelete":False})]
        except errors.InvalidId as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}

    @namespace.doc(description='update a user')
    def patch(self, id):
        user_info = request.get_json()
        if user_info.get('name'):
            if not checkers.is_string(user_info.get('name')):
                return {"msg": "invalid request"}, 400
        if user_info.get('email'):
            if not checkers.is_email(user_info.get('email')):
                return {"msg": "invalid request"}, 400

        if user_info.get('dateOfBirth'):
            if not checkers.is_date(user_info.get('dateOfBirth')):
                return {"msg": "invalid request"}, 400
        try:
            mongo.db.users.update({"_id":ObjectId(id)},{"$set":user_info})
            return {"msg":'updated user'}
        except Exception as e:
            return {"error": str(e)}

    @namespace.doc(description='Delete a user')
    def delete(self, id, commentId):
        try:
            mongo.db.users.update({"_id":ObjectId(id)},{"$set":{"isDelete":True}})
            return {"msg":'user is deleted'}
        except Exception as e:
            return {"error": str(e)}


