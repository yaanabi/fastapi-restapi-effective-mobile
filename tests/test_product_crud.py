from app.models import Product


def test_create_read_product(test_client, db_session):
    data = {
        'name': 'Product 1',
        'description': 'Product 1 description',
        'price': 10,
        'quantity_in_stock': 100
    }
    response = test_client.post("/products", data=data)
    assert response.status_code == 201
    assert response.json()['name'] == 'Product 1'
    assert response.json()['description'] == 'Product 1 description'
    assert response.json()['price'] == 10
    assert response.json()['quantity_in_stock'] == 100
    product_id = response.json()['id']
    # Test read product
    response = test_client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()['name'] == 'Product 1'
    assert response.json()['description'] == 'Product 1 description'
    assert response.json()['price'] == 10
    assert response.json()['quantity_in_stock'] == 100


def test_create_read_products(test_client, db_session):
    response = test_client.get("/products")
    assert response.status_code == 200
    # Already have 1 product in db from conftest setup
    assert len(response.json()) == 1

    data = {'name': 'Product 1', 'price': 10, 'quantity_in_stock': 100}
    response = test_client.post("/products", data=data)
    assert response.status_code == 201
    assert response.json()['name'] == 'Product 1'
    assert response.json()['description'] is None
    assert response.json()['price'] == 10
    assert response.json()['quantity_in_stock'] == 100
    product_id = response.json()['id']

    response = test_client.get("/products")
    assert response.status_code == 200
    response_product = [
        product for product in response.json() if product['id'] == product_id
    ][0]
    assert len(response.json()) == 2
    assert response_product['name'] == 'Product 1'
    assert response_product['price'] == 10
    assert response_product['quantity_in_stock'] == 100


def test_create_update_product(test_client, db_session):
    data = {
        'name': 'Product 1',
        'description': 'Product 1 description',
        'price': 10,
        'quantity_in_stock': 100
    }
    response = test_client.post("/products", data=data)
    assert response.status_code == 201
    assert response.json()['name'] == 'Product 1'
    assert response.json()['description'] == 'Product 1 description'
    assert response.json()['price'] == 10
    assert response.json()['quantity_in_stock'] == 100
    product_id = response.json()['id']

    data_update = {
        'name': 'Product Updated',
        'description': 'Product description updated',
        'price': 10.5,
        'quantity_in_stock': 1000
    }
    response = test_client.put(f"/products/{product_id}", data=data_update)
    assert response.status_code == 200
    assert response.json()['name'] == 'Product Updated'
    assert response.json()['description'] == 'Product description updated'
    assert response.json()['price'] == 10.5
    assert response.json()['quantity_in_stock'] == 1000


def test_create_delete_product(test_client, db_session):
    data = {
        'name': 'Product 1',
        'description': 'Product 1 description',
        'price': 10,
        'quantity_in_stock': 100
    }
    response = test_client.post("/products", data=data)
    assert response.status_code == 201
    assert response.json()['name'] == 'Product 1'
    assert response.json()['description'] == 'Product 1 description'
    assert response.json()['price'] == 10
    assert response.json()['quantity_in_stock'] == 100
    product_id = response.json()['id']

    response = test_client.get(f"/products")
    len_before = len(response.json())

    response = test_client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()['name'] == 'Product 1'
    assert response.json()['description'] == 'Product 1 description'
    assert response.json()['price'] == 10
    assert response.json()['quantity_in_stock'] == 100
    len_before -= 1
    response = test_client.get(f"/products/{product_id}")
    assert response.status_code == 404

    product = db_session.query(Product).filter(
        Product.id == product_id).first()
    assert product.is_deleted == True

    response = test_client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == len_before


def test_create_invalid_product(test_client, db_session):
    data = {
        'name': 'Product 1',
        'description': 'Product 1 description',
        'price': -1,
        'quantity_in_stock': -1,
    }
    response = test_client.post("/products", data=data)
    assert response.json()['detail'][0]['loc'][1] == 'price'
    assert response.json(
    )['detail'][0]['msg'] == 'Input should be greater than or equal to 0'
    assert response.json()['detail'][1]['loc'][1] == 'quantity_in_stock'
    assert response.json(
    )['detail'][1]['msg'] == 'Input should be greater than or equal to 0'
    assert response.status_code == 422


def test_create_update_invalid_product(test_client, db_session):
    data = {
        'name': 'Product 1',
        'description': 'Product 1 description',
        'price': 10,
        'quantity_in_stock': 100
    }
    response = test_client.post("/products", data=data)
    assert response.status_code == 201
    assert response.json()['name'] == 'Product 1'
    assert response.json()['description'] == 'Product 1 description'
    assert response.json()['price'] == 10
    assert response.json()['quantity_in_stock'] == 100
    product_id = response.json()['id']

    data_update = {
        'name': 'Product Updated',
        'description': 'Product description updated',
        'price': -1,
        'quantity_in_stock': -1
    }
    response = test_client.put(f"/products/{product_id}", data=data_update)
    assert response.json()['detail'][0]['loc'][1] == 'price'
    assert response.json(
    )['detail'][0]['msg'] == 'Input should be greater than or equal to 0'
    assert response.json()['detail'][1]['loc'][1] == 'quantity_in_stock'
    assert response.json(
    )['detail'][1]['msg'] == 'Input should be greater than or equal to 0'
    assert response.status_code == 422
