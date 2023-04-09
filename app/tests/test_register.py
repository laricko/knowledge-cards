from fastapi.testclient import TestClient
from fastapi import FastAPI, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from db.user import user as user_db, token as token_db


def test_register(app: FastAPI, client: TestClient, db: Session):
    email = "user@example.com"
    password = "string"
    data = {
        "email": email,
        "password": password,
        "confirm_password": password,
    }
    response = client.post(app.url_path_for("auth:register"), json=data)
    assert response.status_code == status.HTTP_201_CREATED

    # check user created
    query = select(user_db).where(user_db.c.email == email)
    cur = db.execute(query)
    user = cur.first()._asdict()
    assert user["id"] > 0
    assert user["email"] == email
    assert user["password"] != password

    # check verification token is created

    query = select(token_db).where(token_db.c.user_id == user["id"])
    cur = db.execute(query)
    token = cur.first()._asdict()
    assert token["user_id"] == user["id"]
    assert token["value"] is not None
