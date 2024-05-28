import pytest
from unittest.mock import patch
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from src.main import app
from src.auth import schemas

client = TestClient(app)


@pytest.fixture
def mock_db_session():
    with patch("src.auth.database.get_db") as mock_db:
        yield mock_db


def test_create_user_success(mock_db_session):
    user_data = {"email": "test@example.com", "first_name": "Mick", "last_name": "Jagger"}
    created_user = schemas.User(
        id=1,
        email="test@example.com",
        first_name="Mick",
        last_name="Jagger",
        api_key='1234'
    )

    with patch("src.auth.crud.create_user", return_value=created_user) as mock_create_user:
        response = client.post("/users/", json=user_data)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == created_user.dict()
    mock_create_user.assert_called_once()


def test_create_user_conflict(mock_db_session):
    user_data = {"email": "test@example.com", "first_name": "Mick", "last_name": "Jagger"}

    with patch("src.auth.crud.create_user", side_effect=IntegrityError("", "", "")) as mock_create_user:
        response = client.post("/users/", json=user_data)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"]["error"] == 409
    assert response.json()["detail"]["message"] == f"User already exists with email {user_data['email']}"
    mock_create_user.assert_called_once()


def test_create_user_internal_server_error(mock_db_session):
    user_data = {"email": "test@example.com", "first_name": "Mick", "last_name": "Jagger"}
    error_message = "Some unexpected error"

    with patch("src.auth.crud.create_user", side_effect=Exception(error_message)) as mock_create_user:
        response = client.post("/users/", json=user_data)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["detail"]["error"] == 500
    assert response.json()["detail"]["message"] == f"Internal server error: ('{error_message}',)"
    mock_create_user.assert_called_once()
