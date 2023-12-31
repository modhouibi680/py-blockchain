#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import datetime
import hashlib
import json
from urllib.parse import urlparse
import requests


class GeneralBlockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.gen_block(nonce = 1, prev_hash = '0')
        self.nodes = set()
        
    def gen_block(self, nonce, prev_hash):
        block = { 
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'nonce': nonce,
            'prev_hash': prev_hash,
            'transactions': self.transactions       
            }
        self.transactions = []
        self.chain.append(block)
        return block
    
    def get_last_block(self):
        return self.chain[-1]

# simple proof of work operation 
    
    def proof_of_work(self, prev_nonce):
        next_nonce = 1
        nonce_found = False
        
        while nonce_found is False:
            hash_work = hashlib.sha256(str(next_nonce**2 - prev_nonce**2).encode()).hexdigest()
            if hash_work[:2] == '00':
                nonce_found = True
            else:
                next_nonce += 1
                
        return next_nonce

    def hash_block(self, block):
        stringified_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(stringified_block).hexdigest()
    
    def is_valid_chain(self, chain):
        prev_block = chain[0]
        block_index = 1
        
        while block_index < len(chain):
            current_block = chain[block_index]
            if current_block['prev_hash'] != self.hash_block(prev_block):
                return False
            prev_nonce = prev_block['nonce']
            current_nonce = current_block['nonce']
            hash_work = hashlib.sha256(str(current_nonce**2 - prev_nonce**2).encode()).hexdigest()
            if hash_work[:2] != '00':
                return False
            prev_block = current_block
            block_index += 1
        return True

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender':sender, 
            'receiver': receiver,
            'amount': amount
            })
        prev_block = self.get_last_block()
        return prev_block['index'] + 1
    
# nodes
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        
        for node in network:
            resp = requests.get(f'http://{node}/chain')
            if resp.status_code == 200:
                length_chain_in_response= resp.json()['length']
                chain_in_response = resp.json()['chain']
                if self.is_valid_chain(chain_in_response) and length_chain_in_response > max_length:
                    max_length = length_chain_in_response
                    longest_chain = chain_in_response
        if longest_chain:
            self.chain = longest_chain
            return True
        
        return False
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            