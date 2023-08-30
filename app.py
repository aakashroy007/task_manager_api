from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from config import MONGO_URI

app = Flask(__name__)
app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    task_id = mongo.db.tasks.insert_one(data).inserted_id
    return jsonify({'message': 'Task created successfully', 'task_id': str(task_id)})

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    tasks = list(mongo.db.tasks.find())
    for task in tasks:
        task['_id'] = str(task['_id'])
    return jsonify(tasks)

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    if task:
        task['_id'] = str(task['_id'])
        return jsonify(task)
    else:
        return jsonify({'message': 'Task not found'}), 404

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    result = mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': data})
    if result.modified_count > 0:
        return jsonify({'message': 'Task updated successfully'})
    else:
        return jsonify({'message': 'Task not found'}), 404

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = mongo.db.tasks.delete_one({'_id': ObjectId(task_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Task deleted successfully'})
    else:
        return jsonify({'message': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
