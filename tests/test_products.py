import pytest

@pytest.mark.asyncio
async def test_create_product_authenticated(client):
    # Création de l'utilisateur
    await client.post("/register", json={
        "username": "testuser",
        "password": "password"
    })

    # Connexion de l'utilisateur
    res = await client.post("/login", data={
        "username": "testuser",
        "password": "password"
    })
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Création du produit
    response = await client.post("/api/v1/products/", json={
        "name": "Produit testé",
        "description": "Test automatisé",
        "price": 12.5,
        "stock": 10
    }, headers=headers, follow_redirects=False)

    print(response.status_code)
    print(response.headers.get("location"))

    assert "Authorization" in headers
    assert headers["Authorization"].startswith("Bearer ")

    print("📤 Requête POST /products/ envoyée")
    print("Headers:", headers)
    print("Payload:", response.request.content)
    print("📥 Réponse :", response.status_code)
    print("Body:", response.text)

    assert response.status_code == 200
    assert response.json()["name"] == "Produit testé"
