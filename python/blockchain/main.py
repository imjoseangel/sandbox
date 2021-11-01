#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from hashlib import sha256
import json
from time import time


class Block:
    def __init__(self, timestamp=str(int(time())), data=[]):
        self.timestamp = timestamp
        self.data = data
        self.prevHash = ""
        self.nonce = 0
        self.hash = self.getHash()

    def getHash(self):
        return sha256((self.prevHash + self.timestamp +
                       json.dumps(self.data, separators=(',', ':')) +
                       str(self.nonce)).encode('utf-8')).hexdigest()

    def mine(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.getHash()


class Blockchain:
    def __init__(self):
        self.chain = [Block(str(int(time())))]
        self.difficulty = 1
        self.blockTime = 1000

    def getLastBlock(self):
        return self.chain[len(self.chain) - 1]

    def addBlock(self, block):
        block.prevHash = self.getLastBlock().hash
        block.hash = block.getHash()
        block.mine(self.difficulty)
        self.chain.append(block)
        miningTime = int(time()) - \
            int(self.getLastBlock().timestamp)
        # self.difficulty = round(
        #     self.difficulty * self.blockTime / (miningTime, 1)[miningTime <= 0])

    def isValid(self):
        for index in range(1, len(self.chain)):
            currentBlock = self.chain[index]
            prevBlock = self.chain[index - 1]

            if (currentBlock.hash != currentBlock.getHash()):
                print('Block has changed')
                return False
            if (currentBlock.prevHash != prevBlock.hash):
                print('Block link invalid')
                return False

        return True

    def __str__(self):

        return json.dumps([{'timestamp': item.timestamp, 'data': item.data,
                           'prevHash': item.prevHash, 'hash': item.hash,
                            'nonce': item.nonce} for item in self.chain], indent=4)


def main():
    blockchain = Blockchain()
    blockchain.addBlock(Block(data=({"amount": 40})))
    blockchain.addBlock(Block(data=({"amount": 60})))

    print(blockchain)
    # print(blockchain.isValid())


if __name__ == '__main__':
    main()
