# This was mainly built for testing purposes to prototype the Wallet
# The real wallet is a Next.js application
# ECC cryptography library
from fastecdsa import keys, curve, ecdsa
import json


class Wallet:
    def __init__(self, seed_node, private_key=None):
        self.seed_node = seed_node
        self.private_key = private_key or keys.gen_private_key(curve.P256)
        self.public_key = keys.get_public_key(self.private_key, curve.P256)
        self.node_list= []
    
    def create_new_transaction(self, recipient_public_key, quantity):
        transaction_data = {
                'sender_public_key_x': self.public_key.x,
                'sender_public_key_y': self.public_key.y,
                'recipient_public_key.x': recipient_public_key.x,
                'recipient_public_key.y': recipient_public_key.y,
                'quantity': quantity
            }
        
        # Convert dictionary to JSON to bytes for signing
        transaction = json.dumps(transaction_data)
        r, s = ecdsa.sign(transaction, self.private_key)
        signature = (r, s)

        # Sends both the actual transaction and the signature
        transaction_request = {
            "data": transaction,
            "signature": signature
        }

        # Returns both transaction and signature
        return transaction_request

    def update_node_list(self, new_node_list):
        self.node_list = new_node_list