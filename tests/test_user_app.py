import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

random_users = [
    {
        "username": "elizabeth.smith",
        "password": "V&b7z%3J6u",
        "email": "elizabeth.smith@example.com"
    },
    {
        "username": "michael.johnson",
        "password": "T&c4n%9D2p",
        "email": "michael.johnson@example.com"
    },
    {
        "username": "jessica.williams",
        "password": "G&f8k%1M7w",
        "email": "jessica.williams@example.com"
    },
    {
        "username": "david.brown",
        "password": "L&r2b%4T5x",
        "email": "david.brown@example.com"
    },
    {
        "username": "sarah.jones",
        "password": "P&n3q%7W8y",
        "email": "sarah.jones@example.com"
    },
    {
        "username": "james.garcia",
        "password": "R&k6m%8J3z",
        "email": "james.garcia@example.com"
    },
    {
        "username": "mary.martinez",
        "password": "Q&s1v%2H4x",
        "email": "mary.martinez@example.com"
    },
    {
        "username": "john.davis",
        "password": "F&t9p%5L6u",
        "email": "john.davis@example.com"
    },
    {
        "username": "patricia.rodriguez",
        "password": "S&w2q%3G7y",
        "email": "patricia.rodriguez@example.com"
    },
    {
        "username": "robert.miller",
        "password": "K&d4c%9J1v",
        "email": "robert.miller@example.com"
    }
]

user_ids = []

def test_create_user():
    for user in random_users:
        response = client.post("/user/create-user", headers=user)
        user_ids.append(response.headers.get("User-Id"))
        assert response.status_code == 201
        assert response.json() == {"status": "success", "message": "User was successfully created"}


def test_get_users_all():
    response = client.get("/user/info-users-all")
    assert response.status_code == 200


def test_update_users_all():
    for user in user_ids:
        response = client.put(f"/user/update-user?email={user[1:3]}@email.ru", headers={"User-Id": user})
        assert response.status_code == 200

def test_delete_users():
    for i in range(len(user_ids)):
        response = client.delete("/user/delete-user", headers={"User-Id": user_ids[i]})
        assert response.status_code == 200
        assert response.json() == {"status": "success", "message": "User was successfully deleted"}