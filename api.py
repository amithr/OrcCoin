from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from Block import Block
from Blockchain import Blockchain
import requests, os, json

app = FastAPI()
app.state.node_list = [os.getenv('SEED_NODE')]
app.state.blockchain = Blockchain()
app.state.last_miner = os.getenv('SEED_NODE')

@app.on_event("startup")
async def startup_event():
    if len(app.state.node_list) == 1:
        # Get full node list
        node_list_response = requests.post(app.state.node_list[0] + '/send-node-list')
        # Initialize blockchain
        blockchain_response = requests.post(app.state.node_list[0] + '/send-blockchain')


@app.post("/dashboard")
async def display_dashboard():
    return {}

@app.post("/is-alive")
async def check_if_alive():
    json_message = jsonable_encoder({"alive":True})
    return JSONResponse(content=json_message)

@app.post("/new-transaction-request")
async def receive_new_transaction(transaction : Request):
    transaction = await transaction.json()
    new_block = app.state.blockchain.mine_block(transaction)
    json_new_block = jsonable_encoder(new_block)
    return JSONResponse(content=json_new_block)
# Immediately mine
# Send message to network when finished (all /give-consent routes)
# If consent received, add to local blockchain, otherwise remine

@app.post("/give-consent")
async def give_consent(new_block : Request):
    deserialized_block = await new_block.json()
    new_block = Block(     
    )
    is_new_block_valid = Blockchain.is_new_block_valid(new_block, app.state.blockchain.get_last_block())
    # If valid, set last miner address
    json_message = jsonable_encoder({"valid":is_new_block_valid})
    return JSONResponse(content=json_message)
    
    
# Verify, and if true add to local blockchain and send consent
# If false, send remine request

# Receive a request for and send the current node list to whoever wants it
@app.post("/get-node-list")
async def get_node_list():
    json_node_list = jsonable_encoder(app.state.node_list)
    return JSONResponse(content=json_node_list)


@app.post("/send-blockchain")
async def send_blockchain():

    pass

@app.post("/update-node-list")
async def update_node_list(incoming_message : Request):
    incoming_message_dict = await incoming_message.json()
    new_node_address = incoming_message_dict['new_node_address']
    app.state.node_list.append(new_node_address)
    json_message = jsonable_encoder({"msg":"Thanks!"})
    return JSONResponse(content=json_message)

@app.post("/get-last-miner")
async def get_last_miner():
    json_message = jsonable_encoder({"last_miner":app.state.last_miner})
    return JSONResponse(content=json_message)