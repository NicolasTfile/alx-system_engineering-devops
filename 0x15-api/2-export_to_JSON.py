#!/usr/bin/python3
"""Exports to-do list info for a given emoloyee ID to CSV and JSON"""
import json
import requests
from sys import argv


def to_json():
    """Return API data and export to CSV and JSON formats."""
    users = requests.get("http://jsonplaceholder.typicode.com/users")
    for user in users.json():
        if user.get('id') == int(argv[1]):
            user_id = user.get('id')
            username = user.get('username')
            break

    tasks = []
    todos = requests.get("http://jsonplaceholder.typicode.com/todos")
    for task in todos.json():
        if task.get('userId') == int(argv[1]):
            task_data = {
                "task": task.get('title'),
                "completed": task.get('completed'),
                "username": username
            }
            tasks.append(task_data)

    # Export to JSON
    filename_json = f"{user_id}.json"
    with open(filename_json, "w") as jsonfile:
        json.dump({str(user_id): tasks}, jsonfile)


if __name__ == "__main__":
    to_json()
