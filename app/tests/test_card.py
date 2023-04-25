from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.card import card as card_db

from .utils import get_auth_token

TEST_CARD_TITLE = "Card question"


def test_card(app: FastAPI, client: TestClient, db: Session, unverified_user, user):
    # test unverified user
    unverified_token = get_auth_token(unverified_user)
    response = client.post(
        app.url_path_for("create_card"),
        headers={"Authorization": f"Bearer {unverified_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # test create
    data = {
        "title": TEST_CARD_TITLE,
        "description": "Card answer",
        "category_id": None,
        "need_chatgpt": False,
    }
    token = get_auth_token(user)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(app.url_path_for("create_card"), headers=headers, json=data)
    assert response.status_code == status.HTTP_201_CREATED
    query = select(card_db).where(card_db.c.title == TEST_CARD_TITLE)
    cur = db.execute(query)
    card = cur.first()
    assert card.user_id == user["id"]

    # test update
    updated_description = "UPDATED card answer"
    data = {"description": updated_description}
    response = client.patch(
        app.url_path_for("update_card", id=card.id), headers=headers, json=data
    )
    assert response.status_code == status.HTTP_200_OK
    query = select(card_db).where(card_db.c.title == TEST_CARD_TITLE)
    cur = db.execute(query)
    card = cur.first()
    assert card.user_id == user["id"]
    assert card.description == updated_description

    # test fetch my cards
    response = client.get(app.url_path_for("my_cards"), headers=headers)
    response_data = response.json()
    assert updated_description in [data["description"] for data in response_data]

    # test delete card
    response = client.delete(
        app.url_path_for("delete_card", id=card.id), headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    query = select(card_db).where(card_db.c.title == TEST_CARD_TITLE)
    cur = db.execute(query)
    assert cur.first() is None
