from backend.models import Product
from backend.app import db


def test_get_products(client):
    # Seed a product
    with client.application.app_context():
        db.session.add(
            Product(
                name="Test Product",
                description="A test",
                price=9.99,
                category="Test Category",
                image_url="http://example.com/image.png",
                stock=10,
            )
        )
        db.session.commit()

    response = client.get("/api/products/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_single_product(client):
    # Seed a product
    with client.application.app_context():
        db.session.add(
            Product(
                name="Test Product",
                description="A test",
                price=9.99,
                category="Test Category",
                image_url="http://example.com/image.png",
                stock=10,
            )
        )
        db.session.commit()

    # Get the first product
    response = client.get("/api/products/")
    assert response.status_code == 200
    products = response.get_json()
    if products:
        product_id = products[0]["id"]
        response = client.get(f"/api/products/{product_id}/")
        assert response.status_code == 200
        product = response.get_json()
        assert product["id"] == product_id
