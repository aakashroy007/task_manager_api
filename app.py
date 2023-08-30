from datetime import datetime
from dateutil.parser import parse as parse_date
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from werkzeug.exceptions import BadRequest, NotFound
from config import MONGO_URI

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)


class ValidationError(BadRequest):
    pass


class TaskNotFound(NotFound):
    pass


def validate_task_data(data):
    required_fields = ["title", "description", "status", "due_date"]
    for field in required_fields:
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")

    due_date = data.get("due_date")
    if due_date:
        try:
            parsed_due_date = parse_date(due_date)
            if parsed_due_date < datetime.now():
                raise ValidationError("Due date must be in the future")
        except ValueError:
            raise ValidationError("Invalid due date format")


@app.route("/tasks", methods=["POST"])
def create_task():
    try:
        data = request.json
        validate_task_data(data)
        task_id = mongo.db.tasks.insert_one(data).inserted_id
        return jsonify({'message': 'Task created successfully', 'task_id': str(task_id)}), 201
    except ValidationError as e:
        return jsonify({'message': str(e)}), 400


@app.route("/tasks", methods=["GET"])
def get_all_tasks():
    tasks = list(mongo.db.tasks.find())
    for task in tasks:
        task["_id"] = str(task["_id"])
    return jsonify(tasks)


@app.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    if task:
        task["_id"] = str(task["_id"])
        return jsonify(task)
    else:
        return jsonify({"message": "Task not found"}), 404


@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    try:
        data = request.json
        validate_task_data(data)
        result = mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': data})
        if result.modified_count > 0:
            return jsonify({'message': 'Task updated successfully'}), 200
        else:
            raise TaskNotFound('Task not found')
    except ValidationError as e:
        return jsonify({'message': str(e)}), 400
    except TaskNotFound:
        return jsonify({'message': 'Task not found'}), 404


@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    result = mongo.db.tasks.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Task deleted successfully"})
    else:
        return jsonify({"message": "Task not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
