from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.card import category as category_db

from .utils import get_auth_token

TEST_CATEGORY_TITLE = "Cooking"
TEST_UPDATED_CATEGORY_TITLE = "Math"


def test_category(app: FastAPI, client: TestClient, db: Session, unverified_user, user):
    # test category api for unverified_user
    data = {"title": TEST_CATEGORY_TITLE, "need_chatgpt": False}
    unverified_token = get_auth_token(unverified_user)
    response = client.post(
        app.url_path_for("create_category"),
        headers={"Authorization": f"Bearer {unverified_token}"},
        json=data,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # test create category
    token = get_auth_token(user)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        app.url_path_for("create_category"),
        headers=headers,
        json=data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    query = select(category_db).where(category_db.c.title == TEST_CATEGORY_TITLE)
    cur = db.execute(query)
    category = cur.first()
    assert category.user_id == user["id"]

    # test add system category
    query = select(category_db).where(category_db.c.user_id == None)
    cur = db.execute(query)
    system_category = cur.first()
    response = client.post(
        app.url_path_for("add_system_category", id=system_category.id),
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK

    # test system category in response
    response = client.get(app.url_path_for("my_categories"), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert system_category.id in [data.get("id") for data in response_data]
    assert system_category.title in [data.get("title") for data in response_data]

    # test remove system category
    response = client.post(
        app.url_path_for("remove_system_category", id=system_category.id),
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK

    # test system category not in response
    response = client.get(app.url_path_for("my_categories"), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert system_category.id not in [data.get("id") for data in response_data]
    assert system_category.title not in [data.get("title") for data in response_data]

    # test patch category
    query = select(category_db).where(category_db.c.title == TEST_CATEGORY_TITLE)
    cur = db.execute(query)
    category = cur.first()
    data = {"title": TEST_UPDATED_CATEGORY_TITLE}
    response = client.patch(
        app.url_path_for("update_category", id=category.id),
        headers=headers,
        json=data,
    )
    assert response.status_code == status.HTTP_200_OK
    query = select(category_db).where(
        category_db.c.title == TEST_UPDATED_CATEGORY_TITLE
    )
    cur = db.execute(query)
    new_category = cur.first()
    assert new_category.id == category.id

    # test delete category
    query = select(category_db).where(
        category_db.c.title == TEST_UPDATED_CATEGORY_TITLE
    )
    cur = db.execute(query)
    category = cur.first()
    token = get_auth_token(user)
    response = client.delete(
        app.url_path_for("delete_category", id=category.id),
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    query = select(category_db).where(
        category_db.c.title == TEST_UPDATED_CATEGORY_TITLE
    )
    cur = db.execute(query)
    category = cur.first()
    assert category is None
