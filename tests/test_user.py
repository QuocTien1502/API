import pytest
from routers import schemas
from tests.database import client, session

def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "hello world"
    assert res.status_code == 200

@pytest.fixture
def test_user(client):
    user_data = {"username": "tien",
                "email": "tien@gmail.com",
                "password": "tien",
                "role": "user"}
    res = client.post("/user/", json=user_data)
    assert res.status_code == 200
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

def test_create_user(client):
    res = client.post("/user/",json={"username": "test",
                                        "email": "test@gmail.com",
                                        "password": "test",
                                        "role": "user"})
    new_user = schemas.UserDisplay(**res.json())
    assert new_user.username == "test"
    assert new_user.email == "test@gmail.com"
    assert res.status_code == 200

def test_login_user(test_user, client):
    res = client.post("/login", data={"username": test_user["username"],"password": test_user["password"]})
    print(res.json())
    assert res.status_code == 200

def test_incorrect_login(test_user,client):
    res = client.post("/login", data={"username": test_user["username"],"password": "wrongPassword"})
    assert res.status_code == 404
    assert res.json().get('detail') == "Incorrect password"