from flask import Flask, request
from flask_restful import Api, Resource
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from config import MONGO_URI, JWT_SECRET_KEY
app = Flask(__name__)
app.config['MONGO_URI'] = MONGO_URI
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

mongo = PyMongo(app)
api = Api(app)
jwt = JWTManager(app)

class TaskResource(Resource):
    @jwt_required()
    def get(self, task_id):
        task = mongo.db.tasks.find_one_or_404({'_id': task_id})
        task['_id'] = str(task['_id'])
        return task

    @jwt_required()
    def put(self, task_id):
        task = mongo.db.tasks.find_one_or_404({'_id': task_id})
        data = request.get_json()
        mongo.db.tasks.update_one({'_id': task_id}, {'$set': data})
        return {'message': 'Task updated successfully'}

    @jwt_required()
    def delete(self, task_id):
        mongo.db.tasks.delete_one({'_id': task_id})
        return {'message': 'Task deleted successfully'}

class TaskListResource(Resource):
    @jwt_required()
    def get(self):
        tasks = list(mongo.db.tasks.find())
        for task in tasks:
            task['_id'] = str(task['_id'])
        return tasks

    @jwt_required()
    def post(self):
        data = request.get_json()
        task_id = mongo.db.tasks.insert_one(data).inserted_id
        return {'message': 'Task created successfully', 'task_id': str(task_id)}

api.add_resource(TaskResource, '/tasks/<ObjectId:task_id>')
api.add_resource(TaskListResource, '/tasks')

if __name__ == '__main__':
    app.run(debug=True)
