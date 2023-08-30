import unittest
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from app import app, mongo


class TestTaskManagerAPI(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.db = mongo.db
        self.collection = self.db["tasks"]
        self.token = self.get_auth_token()

    def get_auth_token(self):
        response = self.client.post(
            "/login", json={"username": "test_user", "password": "test_password"}
        )
        token = response.json.get("access_token")
        return token

    def test_create_task(self):
        data = {
            "title": "Test Task",
            "description": "This is a test task",
            "status": "in progress",
            "due_date": "2023-09-15",
        }
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.post("/tasks", json=data, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.json)
        task_id = response.json.get("task_id")
        self.assertIsNotNone(task_id)

    def test_create_task_missing_field(self):
        data = {
            "title": "Test Task",
            "description": "This is a test task"
            # Missing 'status' field
        }
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.post("/tasks", json=data, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.json)

    def test_get_all_tasks(self):
        task_data = [
            {
                "title": "Task 1",
                "description": "Description 1",
                "status": "in progress",
            },
            {"title": "Task 2", "description": "Description 2", "status": "completed"},
        ]
        self.collection.insert_many(task_data)
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get("/tasks", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_task_valid_id(self):
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "status": "in progress",
        }
        inserted_task = self.collection.insert_one(task_data)
        task_id = str(inserted_task.inserted_id)
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get(f"/tasks/{task_id}", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("_id", response.json)

    def test_get_task_invalid_id(self):
        invalid_task_id = "64ef988eb11065f6d46fb9a0"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get(f"/tasks/{invalid_task_id}", headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn("message", response.json)


if __name__ == "__main__":
    unittest.main()
