def test_create_expense(client, auth_headers):
    response = client.post(
        "/api/v1/expenses",
        headers=auth_headers,
        json={
            "title": "Groceries",
            "amount": 100.5,
            "category": "Food"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Groceries"
    assert data["amount"] == 100.5
    assert data["category"] == "Food"
    assert "id" in data


def test_list_expenses(client, auth_headers):
    client.post(
        "/api/v1/expenses",
        headers=auth_headers,
        json={
            "title": "Shopping",
            "amount": 200,
            "category": "Shopping"
        }
    )

    response = client.get(
        "/api/v1/expenses",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert data["total"] >= 1
    assert len(data["items"]) >= 1


def test_get_expense(client, auth_headers):
    create_res = client.post(
        "/api/v1/expenses",
        headers=auth_headers,
        json={
            "title": "Taxi",
            "amount": 50,
            "category": "Transport"
        }
    )

    assert create_res.status_code == 201

    expense_id = create_res.json()["id"]

    response = client.get(
        f"/api/v1/expenses/{expense_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["id"] == expense_id


def test_update_expense(client, auth_headers):
    create_res = client.post(
        "/api/v1/expenses",
        headers=auth_headers,
        json={
            "title": "Dinner",
            "amount": 75,
            "category": "Food"
        }
    )

    assert create_res.status_code == 201

    expense_id = create_res.json()["id"]

    response = client.put(
        f"/api/v1/expenses/{expense_id}",
        headers=auth_headers,
        json={
            "title": "Dinner Updated",
            "amount": 80,
            "category": "Food"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Dinner Updated"
    assert data["amount"] == 80


def test_delete_expense(client, auth_headers):
    create_res = client.post(
        "/api/v1/expenses",
        headers=auth_headers,
        json={
            "title": "Snacks",
            "amount": 30,
            "category": "Food"
        }
    )

    assert create_res.status_code == 201

    expense_id = create_res.json()["id"]

    response = client.delete(
        f"/api/v1/expenses/{expense_id}",
        headers=auth_headers
    )

    assert response.status_code == 204

    # confirm deletion
    response = client.get(
        f"/api/v1/expenses/{expense_id}",
        headers=auth_headers
    )

    assert response.status_code == 404


def test_expense_requires_auth(client):
    response = client.get("/api/v1/expenses")

    assert response.status_code in [401, 403]


def test_create_expense_invalid_amount(client, auth_headers):
    response = client.post(
        "/api/v1/expenses",
        headers=auth_headers,
        json={
            "title": "Invalid",
            "amount": -10,
            "category": "Food"
        }
    )

    assert response.status_code == 422


def test_create_expense_empty_title(client, auth_headers):
    response = client.post(
        "/api/v1/expenses",
        headers=auth_headers,
        json={
            "title": "",
            "amount": 50,
            "category": "Food"
        }
    )

    assert response.status_code == 422


def test_user_cannot_access_other_users_expense(client):
    # user 1
    res1 = client.post("/api/v1/users/signup", json={
        "email": "user1@test.com",
        "name": "User1",
        "password": "pass123"
    })
    login1 = client.post("/api/v1/users/login", json={
        "email": "user1@test.com",
        "name": "User1",
        "password": "pass123"
    })
    token1 = login1.json()["access_token"]

    headers1 = {"Authorization": f"Bearer {token1}"}

    # user 1 creates expense
    expense = client.post(
        "/api/v1/expenses",
        headers=headers1,
        json={
            "title": "Private",
            "amount": 100,
            "category": "Food"
        }
    )

    expense_id = expense.json()["id"]

    # user 2
    client.post("/api/v1/users/signup", json={
        "email": "user2@test.com",
        "name": "User2",
        "password": "pass123"
    })
    login2 = client.post("/api/v1/users/login", json={
        "email": "user2@test.com",
        "name": "User2",
        "password": "pass123"
    })
    token2 = login2.json()["access_token"]

    headers2 = {"Authorization": f"Bearer {token2}"}

    # user 2 tries to access user 1 expense
    response = client.get(
        f"/api/v1/expenses/{expense_id}",
        headers=headers2
    )

    assert response.status_code == 404


def test_filter_expenses_by_category(client, auth_headers):
    client.post("/api/v1/expenses", headers=auth_headers, json={
        "title": "Food item",
        "amount": 100,
        "category": "Food"
    })

    client.post("/api/v1/expenses", headers=auth_headers, json={
        "title": "Taxi",
        "amount": 50,
        "category": "Transport"
    })

    response = client.get(
        "/api/v1/expenses?category=Food",
        headers=auth_headers
    )

    data = response.json()

    assert len(data["items"]) > 0
    assert all(item["category"] == "Food" for item in data["items"])


