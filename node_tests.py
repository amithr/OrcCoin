import unittest
from Block import Block
from Blockchain import Blockchain
from Wallet import Wallet
import time

class NodeTest(unittest.TestCase):

    def test_mining(self):
        wallet = Wallet('http://192.168.0.0.1:8001')
        recipient_public_key = type('', (), {})()
        recipient_public_key.x = 48439561293906451759052585252797914202762949526041747995844080717082404635287
        recipient_public_key.y = 36134250956749795798585127919587881956611106672985015071877198253568414405101
        transaction = wallet.create_new_transaction(recipient_public_key, 2.0)
        blockchain = Blockchain()
        newBlock = blockchain.mine_block(transaction)
        self.assertIsInstance(Block, newBlock, "The block was created.")

if __name__ == '__main__':
    unittest.main()