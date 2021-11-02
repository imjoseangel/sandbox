#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from hashlib import sha256
import json
from time import time


class Block:

    def __init__(self, data=[], previous_hash=None):
        self.timestamp = time()
        self.data = data
        self.prevHash = previous_hash
        self.nonce = 0
        self.hash = self.getHash()

    def getHash(self):

        hash = sha256()
        hash.update(str(self.timestamp).encode('utf-8'))
        hash.update(str(self.data).encode('utf-8'))
        hash.update(str(self.prevHash).encode('utf-8'))
        hash.update(str(self.nonce).encode('utf-8'))
        return hash.hexdigest()

    def mine(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.getHash()

        print(f'Block Mined : {self.hash} in {self.nonce} iterations')

    def __str__(self):
        return json.dumps([{'data': item.data, 'timestamp': item.timestamp,
                           'nonce': item.nonce, 'hash': item.hash, 'prevHash': item.prevHash
                            } for item in self.chain], indent=4)


class Blockchain:
    def __init__(self):
        self.chain = [Block()]
        self.difficulty = 1
        self.blockTime = 30000

    def getLastBlock(self):
        return self.chain[len(self.chain) - 1]

    def addBlock(self, block):
        block.prevHash = self.getLastBlock().hash
        block.hash = block.getHash()
        block.mine(self.difficulty)
        self.chain.append(block)

        self.difficulty += (-1, 1)[int(time()) -
                                   int(self.getLastBlock().timestamp) < self.blockTime]

    def isValid(self):
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            prevBlock = self.chain[i - 1]

            if (currentBlock.hash != currentBlock.getHash() or prevBlock.hash != currentBlock.prevHash):
                return False

        return True

    def __str__(self):
        return json.dumps([{'data': item.data, 'timestamp': item.timestamp,
                           'nonce': item.nonce, 'hash': item.hash, 'prevHash': item.prevHash
                            } for item in self.chain], indent=4)


def main():
    blockchain = Blockchain()
    blockchain.addBlock(Block(data=({"amount": 40})))
    blockchain.addBlock(Block(data=({"amount": 160})))
    blockchain.addBlock(Block(data=({"amount": 510})))

    print(blockchain)


if __name__ == '__main__':
    main()
