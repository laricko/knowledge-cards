from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import insert, literal_column, select, update
from sqlalchemy.orm import Session

from db.user import token as token_db
from db.user import user as user_db
from security import decode_access_token, hash_password

from .utils import TEST_USER_PASSWORD

TEST_VALUE_VERIFICATION_TOKEN = "string"


@fixture(scope="session")
def verification_token(unverified_user, db: Session) -> dict:
    query = (
        insert(token_db)
        .values(user_id=unverified_user["id"], value=TEST_VALUE_VERIFICATION_TOKEN)
        .returning(literal_column("*"))
    )
    cur = db.execute(query)
    db.commit()
    return cur.first()._asdict()


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


def test_login(app: FastAPI, client: TestClient, user: dict):
    response = client.post(
        app.url_path_for("auth:login"),
        json={"email": user["email"], "password": TEST_USER_PASSWORD},
    )
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    token = data.get("token")
    assert token is not None

    decoded_token = decode_access_token(token)
    assert decoded_token["sub"] == user["email"]
    assert decoded_token.get("exp") is not None


def test_verification(
    app: FastAPI, client: TestClient, db: Session, verification_token: dict
):
    response = client.get(
        app.url_path_for("verification:verify"),
        params={"token": verification_token["value"]},
    )
    assert response.status_code == status.HTTP_200_OK

    query = select(user_db).where(user_db.c.id == verification_token["user_id"])
    cur = db.execute(query)
    user = cur.first()._asdict()
    assert user["verified"] is True

    # making unverified user back
    query = update(user_db).where(user_db.c.id == user["id"]).values(verified=False)
    db.execute(query)
    db.commit()
