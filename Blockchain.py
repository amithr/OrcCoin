from Block import Block
from fastecdsa import curve, ecdsa, keys
from fastecdsa.point import Point
import hashlib, json, time

class Blockchain:
    def __init__(self):
    # Stores the actual blockchain
        self.chain = []
        # Keeps track of completed transactions in a block - each block contains 1 transactions
        self.current_transaction_data = []
        # Creates the first block in the chain
        if len(self.chain) == 0:
            self.construct_genesis()
    
    def construct_genesis(self):
        genesis_block = Block(chain_index=0, proof_of_work_number=0, transaction="{}", previous_hash=0)
        self.chain.append(genesis_block)
        
    

    # Transaction is standard transaction request from wallet with both signature and actual transaction data
    def create_new_block(self, proof_number, previous_hash, transaction):
        # Make sure transaction is valid by cryptographically comparing transaction signature
        # and sender's public key
        # Decode transaction from json to get public keys
        public_keys = json.loads(transaction["data"])
        # Convert the public key coordinates back into a Point object that holds both, in order to use
        # the verify function
        sender_public_key = Point(public_keys["sender_public_key_x"], public_keys["sender_public_key_y"], curve=curve.P256)
        is_transaction_valid = ecdsa.verify(transaction["signature"], transaction["data"], 
                               sender_public_key, curve=curve.P256)

        last_block = self.get_last_block()
        new_block = None
        if is_transaction_valid:
            new_block = Block(
                chain_index = len(self.chain),
                proof_of_work_number = proof_number,
                transaction = transaction["data"],
                previous_hash = previous_hash,
                timestamp=time.time()
            )
        else:
            raise Exception("Transaction invalid.")
        
        # The block has been created, but check whether it's valid before
        # placing it on the blockchain
        is_block_valid = Blockchain.is_new_block_valid(new_block, last_block)

        if is_block_valid:
            self.chain.append(new_block)
        else:
            raise Exception("Block invalid.")

        return new_block
    
    # This is a static method because this is used to provide consent for proposed
    # new blocks from other nodes
    @staticmethod
    def is_new_block_valid(new_block, last_block):
        if ((last_block.chain_index + 1) !=  new_block.chain_index):
            return False
        elif new_block.timestamp <= last_block.timestamp:
            return False
        elif not Blockchain.try_next_proof_of_work_number(new_block.proof_of_work_number, last_block.proof_of_work_number):
            return False
        elif last_block.calculate_hash() != new_block.previous_hash:
            return False

        return True
    
    # Identifies a new proof_no such that the hash of the new proof_no multiplied by the current
    # proof_no has 4 leading zeroes (0000). This is the mining operation.
    def generate_next_proof_of_work_number(self):
        last_block = self.get_last_block()
        new_proof_of_work_number = 0
        # Keep incrementing proof number until we obtain a new hash with 4 leading zeroes
        # This is the the computationally intensive task that makes mining expensive
        while not Blockchain.try_next_proof_of_work_number(new_proof_of_work_number, last_block.proof_of_work_number):
            new_proof_of_work_number += 1
        
        return new_proof_of_work_number

    # Used both to generate the next proof of work number and to verify
    # proposed blocks from other nodes
    @staticmethod
    def try_next_proof_of_work_number(new_proof_number, last_proof_number):
        # Generate a UTF string with both proof numbers
        new_proof_number_guess = f'{new_proof_number}{new_proof_number}'.encode()
        # Hash this
        guess_hash = hashlib.sha256(new_proof_number_guess).hexdigest()
        return guess_hash[:4] == "0000"


    # Do mining and create and attach new block to block chain
    def mine_block(self, transaction):
        proof_of_work_number = self.generate_next_proof_of_work_number()
        previous_hash = self.get_last_block().calculate_hash()
        return self.create_new_block(proof_of_work_number, previous_hash, transaction)
    
    
    def get_last_block(self):
        return self.chain[-1]
    
    def update_blockchain(self, new_blockchain):
        self.chain = new_blockchain