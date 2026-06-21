from fastapi import status


def test_user_login_invalid_username_response_400(anon_client):
    payload = {"username": "nonexistent", "password": "somepassword"}
    response = anon_client.post("/users/login/", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_user_login_invalid_password_response_400(anon_client):
    payload = {"username": "testuser", "password": "wrongpassword"}
    response = anon_client.post("/users/login/", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_user_login_valid_response_200(anon_client, test_user):
    payload = {"username": "testuser", "password": "testpassword"}
    response = anon_client.post("/users/login/", json=payload)
    assert response.status_code == status.HTTP_200_OK


def test_user_login_case_insensitive_response_200(anon_client, test_user):
    payload = {"username": "TESTUSER", "password": "testpassword"}
    response = anon_client.post("/users/login/", json=payload)
    assert response.status_code == status.HTTP_200_OK


def test_user_register_new_user_response_200(anon_client):
    payload = {
        "username": "newuser",
        "password": "securepass123",
        "password_confirm": "securepass123",
    }
    response = anon_client.post("/users/register/", json=payload)
    assert response.status_code == status.HTTP_200_OK


def test_user_register_existing_username_response_409(anon_client, test_user):
    payload = {
        "username": "testuser",
        "password": "newpassword",
        "password_confirm": "newpassword",
    }
    response = anon_client.post("/users/register/", json=payload)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_user_register_mismatched_passwords_response_422(anon_client):
    payload = {
        "username": "anotheruser",
        "password": "password123",
        "password_confirm": "differentpassword",
    }
    response = anon_client.post("/users/register/", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_user_register_missing_username_response_422(anon_client):
    payload = {
        "password": "password123",
        "password_confirm": "password123",
    }
    response = anon_client.post("/users/register/", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_user_register_missing_password_response_422(anon_client):
    payload = {
        "username": "newuser",
        "password_confirm": "password123",
    }
    response = anon_client.post("/users/register/", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_user_refresh_token_without_cookie_response_401(anon_client):
    response = anon_client.post("/users/refresh-token/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_refresh_token_with_valid_token_response_200(anon_client, test_user):
    from auth.jwt_auth import generate_refresh_token

    refresh_token = generate_refresh_token(test_user.id)
    anon_client.cookies.set("refresh_token", refresh_token)

    response = anon_client.post("/users/refresh-token/")
    assert response.status_code == status.HTTP_200_OK


def test_user_logout_response_200(authenticated_client):
    response = authenticated_client.post("/users/logout/")
    assert response.status_code == status.HTTP_200_OK
