from app.models import Product


def test_create_read_order(test_client, db_session, test_product_id):
    data = [{"product_id": test_product_id, "quantity": 1}]
    response = test_client.post("/orders", json=data)
    assert response.status_code == 201
    assert response.json()['order_items'] == [{
        "product_id": test_product_id,
        "quantity": 1
    }]
    assert response.json()['status'] == 'в процессе'
    order_id = response.json()['id']

    response = test_client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()['order_items'][0]['product_id'] == test_product_id
    assert response.json()['order_items'][0]['quantity'] == 1


def test_create_read_orders(test_client, db_session, test_product_id):
    data = [{
        "product_id": test_product_id,
        "quantity": 1
    }, {
        "product_id": test_product_id,
        "quantity": 1
    }]
    response = test_client.post("/orders", json=data)
    assert response.status_code == 201
    assert response.json()['order_items'] == [{
        "product_id": test_product_id,
        "quantity": 1
    }, {
        "product_id": test_product_id,
        "quantity": 1
    }]
    assert response.json()['status'] == 'в процессе'
    order_id = response.json()['id']

    response = test_client.get("/orders")
    assert response.status_code == 200
    for order in response.json():
        if order['id'] == order_id:
            assert order['order_items'] == [{
                "product_id": test_product_id,
                "quantity": 1
            }, {
                "product_id": test_product_id,
                "quantity": 1
            }]
            assert order['status'] == 'в процессе'
        else:
            assert order['order_items'] == [{
                "product_id": test_product_id,
                "quantity": 1
            }]
            assert order['status'] == 'в процессе'


def test_product_quant_after_create_order(test_client, db_session,
                                          test_product_id):
    # Quantity used in test_create_read_order and test_create_read_orders is 3
    product = db_session.query(Product).filter(
        Product.id == test_product_id).first()
    assert product.quantity_in_stock == 2


def test_create_update_order(test_client, db_session, test_product_id):
    data = [{"product_id": test_product_id, "quantity": 1}]
    response = test_client.post("/orders", json=data)
    assert response.status_code == 201
    assert response.json()['order_items'] == [{
        "product_id": test_product_id,
        "quantity": 1
    }]
    assert response.json()['status'] == 'в процессе'
    order_id = response.json()['id']
    data = {'status': 'отправлен'}

    response = test_client.patch(f"/orders/{order_id}/status", data=data)
    assert response.status_code == 200
    assert response.json()['status'] == 'отправлен'
    assert response.json()['order_items'] == [{
        "product_id": test_product_id,
        "quantity": 1
    }]


def test_create_order_with_invalid_quantity(test_client, db_session,
                                            test_product_id):
    data = [{"product_id": test_product_id, "quantity": -1}]
    response = test_client.post("/orders", json=data)
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'][2] == 'quantity'
    assert response.json(
    )['detail'][0]['msg'] == 'Input should be greater than 0'


def test_create_order_with_quality_over_stock(test_client, db_session,
                                              test_product_id):
    product_quant = db_session.query(Product).filter(
        Product.id == test_product_id).first().quantity_in_stock
    data = [{"product_id": test_product_id, "quantity": 999}]
    response = test_client.post("/orders", json=data)
    assert response.status_code == 400
    assert response.json(
    )['detail'] == f'Insufficient stock for product_id: {test_product_id} (stock: {product_quant})'


def test_create_order_with_invalid_product_id(test_client, db_session):
    data = [{"product_id": -1, "quantity": 1}]
    response = test_client.post("/orders", json=data)
    assert response.status_code == 404
    assert response.json()['detail'] == f'Product(id=-1) not found'
