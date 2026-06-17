from fastapi import status


def test_expenses_list_response_200(authenticated_client):
    response = authenticated_client.get("/expenses")
    assert response.status_code == status.HTTP_200_OK


def test_expense_create_response_201(authenticated_client):
    expense_data = {
        "description": "Internet",
        "amount": 120000.50,
    }
    response = authenticated_client.post("/expenses", json=expense_data)
    assert response.status_code == status.HTTP_201_CREATED


def test_expense_detail_response_200(authenticated_client):
    create_response = authenticated_client.post(
        "/expenses",
        json={"description": "Water", "amount": 95000.00},
    )
    expense_id = create_response.json()["id"]

    response = authenticated_client.get(f"/expenses/{expense_id}")
    assert response.status_code == status.HTTP_200_OK


def test_expense_detail_response_404(authenticated_client):
    response = authenticated_client.get("/expenses/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_expense_update_response_200(authenticated_client):
    create_response = authenticated_client.post(
        "/expenses",
        json={"description": "Gas", "amount": 200000.00},
    )
    expense_id = create_response.json()["id"]

    response = authenticated_client.put(
        f"/expenses/{expense_id}",
        json={"description": "Gasoline", "amount": 250000.00},
    )
    assert response.status_code == status.HTTP_200_OK


def test_expense_update_response_404(authenticated_client):
    response = authenticated_client.put(
        "/expenses/999",
        json={"description": "Updated", "amount": 100.0},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_expense_delete_response_200(authenticated_client):
    create_response = authenticated_client.post(
        "/expenses",
        json={"description": "Food", "amount": 85000.00},
    )
    expense_id = create_response.json()["id"]

    response = authenticated_client.delete(f"/expenses/{expense_id}")
    assert response.status_code == status.HTTP_200_OK


def test_expense_delete_response_404(authenticated_client):
    response = authenticated_client.delete("/expenses/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND