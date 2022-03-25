import hashlib
from fastecdsa import curve, ecdsa, keys
import time

class Block:
    def __init__(self,  chain_index, proof_of_work_number, transaction, previous_hash, timestamp=time.time()):
        self.chain_index = chain_index
        self.proof_of_work_number = proof_of_work_number
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.timestamp = timestamp
    
    def calculate_hash(self):
        block_string = "{}{}{}{}{}".format(self.chain_index, 
            self.proof_of_work_number, self.transaction, self.previous_hash, self.timestamp).encode()
        hash = hashlib.sha256(block_string).hexdigest()
        return hash

    # Verify signature using transaction, signature tuple, and public key
    # Curve should match curve specified in the wallet
    @staticmethod
    def verify_transaction(signature, transaction, public_key):
        valid = ecdsa.verify(signature, transaction, public_key, curve=curve.P256)
        return valid
    
    def __repr__(self):
        return "{} - {} - {} - {} - {}".format(self.chain_index, self.proof_of_work_number, self.transaction, self.previous_hash, self.timestamp)
        