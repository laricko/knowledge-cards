from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.user import user as user_db

from .utils import get_auth_token


def test_self_user(app: FastAPI, client: TestClient, unverified_user):
    token = get_auth_token(unverified_user)
    response = client.get(
        app.url_path_for("user:get-self-user"),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["id"] == unverified_user["id"]


def test_patch_self_user(
    app: FastAPI, client: TestClient, db: Session, unverified_user
):
    token = get_auth_token(unverified_user)
    data = {"first_name": "UPDATED NAME"}
    response = client.patch(
        app.url_path_for("user:update-self-user"),
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["id"] == unverified_user["id"]
    query = select(user_db).where(user_db.c.id == unverified_user["id"])
    cur = db.execute(query)
    user = cur.first()
    unverified_user["first_name"] != user.first_name
    unverified_user["last_name"] == user.last_name
