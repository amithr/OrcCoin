from api import app
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from Wallet import Wallet
import os

client = TestClient(app)

def generate_new_transaction():
    wallet = Wallet(os.getenv("SEED_NODE"))
    recipient_public_key = type('', (), {})()
    recipient_public_key.x = 48439561293906451759052585252797914202762949526041747995844080717082404635287
    recipient_public_key.y = 36134250956749795798585127919587881956611106672985015071877198253568414405101
    transaction = wallet.create_new_transaction(recipient_public_key, 2.0)
    # Returns dict with transaction and signature
    return transaction

def test_receive_new_transaction():
    json_transaction = jsonable_encoder(generate_new_transaction())
    print(json_transaction)
    response = client.post("/new-transaction-request", json=json_transaction)
    assert response.status_code == 200

def give_consent():
    new_transaction = generate_new_transaction()
    new_block = app.state.blockchain.mine_block(new_transaction)
    json_new_block = jsonable_encoder(new_block)
    response = client.post("/new-transaction-request", json=json_new_block)
    response.status_code == 200
    


def test_check_if_alive():
    print("hello")
    response = client.post("/is-alive")
    assert response.status_code == 200
    assert response.json() == {"alive": True}

def test_get_node_list():
    response = client.post("/get-node-list")
    assert response.json() == [os.getenv("SEED_NODE")]

def test_update_node_list():
    response = client.post("/update-node-list", json={"new_node_address": "192.168.0.1:5001"})
    assert response.status_code == 200
    assert response.json() == {"msg": "Thanks!"}

def test_get_last_miner():
    response = client.post("/get-last-miner")
    assert response.status_code == 200