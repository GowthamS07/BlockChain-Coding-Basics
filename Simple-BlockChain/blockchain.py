# -*- coding: utf-8 -*-
"""
Created on Tue Aug 5 00:00:56 2019
Conda Environment apps
@author: Gowtham S
"""
import datetime
import hashlib
from flask import Flask, jsonify
import json

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    # Creating a Block
    def create_block(self, proof, previous_hash):
        block = {'Index': len(self.chain)+1, 'Timestamp': str(datetime.datetime.now()), 'Proof':proof,'Previous Hash': previous_hash}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_Proof = False
        while check_Proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_Proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['Previous Hash'] != self.hash(previous_block):
                return False
            previous_Proof = previous_block['Proof']
            proof = block['Proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_Proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

# Mining a Block
# Flask creates a Web App
app = Flask(__name__)

blockchain = Blockchain()
# Mining method
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['Proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message':'Block Successfully Mined !', 
                'index': block['Index'],
                'timestamp':block['Timestamp'],
                'proof': block['Proof'],
                'previous_hash':block['Previous Hash']}
    return jsonify(response), 200       # 200 is the HTTP status code for OK

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain':blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

app.run(host='0.0.0.0', port = 5000)
