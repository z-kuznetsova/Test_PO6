import requests
import pytest

BASE_URL = "https://reqres.in/api"

# Тест 1: Получение списка пользователей
def test_get_users():
    response = requests.get(f"{BASE_URL}/users?page=2")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0

# Тест 2: Получение конкретного пользователя
def test_get_user():
    response = requests.get(f"{BASE_URL}/users/2")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["id"] == 2
    assert "first_name" in data["data"]
    assert "last_name" in data["data"]

# Тест 3: Создание пользователя
def test_create_user():
    payload = {"name": "John", "job": "QA"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["job"] == payload["job"]

# Тест 4: Обновление данных пользователя
def test_update_user():
    payload = {"name": "John", "job": "Lead QA"}
    response = requests.put(f"{BASE_URL}/users/2", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["job"] == payload["job"]

# Тест 5: Удаление пользователя
def test_delete_user():
    response = requests.delete(f"{BASE_URL}/users/2")
    assert response.status_code == 204

# Тест 6: Авторизация
def test_login():
    payload = {"email": "test@mail.com", "password": "1234"}
    response = requests.post(f"{BASE_URL}/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "token" in data

if __name__ == "__main__":
    pytest.main()
