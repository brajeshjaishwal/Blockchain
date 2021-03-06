# Part 1: Create block chain
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

# Creating a block chain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')

    def create_block(self, proof, previous_hash):
        block = {'index' : len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if(hash_operation[:4] == '0000'):
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = chain[block_index]
            block_index += 1
        return True
    
# Part 2: Mining our block chain

# Creating a web app
app = Flask(__name__)
bc = Blockchain()

# Mine a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = bc.get_previous_block()
    previous_proof = previous_block['proof']
    proof = bc.proof_of_work(previous_proof)
    previous_hash = bc.hash(previous_block)
    block = bc.create_block(proof, previous_hash)
    response = {"message": "Congratulations, you just mined a block",
                "index": block["index"], # length of block chain
                "timestamp": block["timestamp"],
                "proof": block["proof"], #was set from proof passed in create_block
                "previous_hash": block["previous_hash"]}# was set from previous hash passed in create block
    return jsonify(response), 200
    
# Getting the full block chain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {"chain": bc.chain,
                "length": len(bc.chain)}
    return jsonify(response), 200

# Check if the block chain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    checkvalid = bc.is_chain_valid(bc.chain)
    msg = "Chain is valid"
    if checkvalid is False:
        msg = "Chain is not valid"
    response = {"message": msg}
    return jsonify(response), 200

# Running the app
app.run()#host='127.0.0.1', port=5000)

# 3. Creating a decentralized blockchain


