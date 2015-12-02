#This is where my automated tests go!!!

import unittest
import json
from todoserver import app
app.testing = True

def json_body(resp):
    return json.loads(resp.data.decode("utf-8"))

class TestTodoserver(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        """ Verify test pre-conditions """
        resp = self.client.get("/tasks/")
        self.assertEqual([], json_body(resp))

    def test_get_empty_list_of_tasks(self):
        resp = self.client.get("/tasks/")
        self.assertEqual(200, resp.status_code)
        data = json.loads(resp.data.decode("utf-8"))
        self.assertEqual([], data)

    def test_create_a_task_and_get_its_details(self):

        """ verify test pre-conditions """
        
        resp = self.client.get("/tasks/")

        """ create a new task """
        new_task_data = {
            "summary": "Get milk",
            "description": "One gallon organic whole milk"
        }
        resp = self.client.post("/tasks/",
                           data=json.dumps(new_task_data))
        self.assertEqual(201, resp.status_code)
        data = json_body(resp)
        self.assertIn("id", data)
        task_id = data["id"]
        resp = self.client.get("/tasks/{:d}/".format(task_id))

        self.assertEqual(200, resp.status_code)

        task = json_body(resp)
        self.assertEqual(task_id, task["id"])
        self.assertEqual("Get milk", task["summary"])
        self.assertEqual("One gallon organic whole milk", task["description"])

    def test_create_multiple_tasks_and_fetch_list(self):
        client = app.test_client


