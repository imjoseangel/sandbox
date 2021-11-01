#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from hashlib import sha256
import json
from datetime import datetime


class Block:
    def __init__(self, timestamp="", data=[]):
        self.timestamp = timestamp
        self.data = data
        self.hash = self.getHash()
        self.prevHash = ""

    def getHash(self):
        return sha256(self.prevHash + self.timestamp + json(self.data)).hexdigest()

    def mine(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.getHash()


class Blockchain:
    def __init__(self):
        self.chain = [Block(str(datetime.now()))]
        self.difficulty = 1
        self.blockTime = 1000

    def getLastBlock(self):
        return self.chain[-1]

    def addBlock(self, block):
        block.prevHash = self.getLastBlock().hash
        block.hash = block.getHash()
        block.mine(self.difficulty)
        self.chain.append(block)
        miningTime = datetime.now() - int(self.getLastBlock().timestamp)
        self.difficulty = round(
            self.difficulty * self.blockTime / (miningTime, 1)[miningTime <= 0])

    def isValid(self):
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            prevBlock = self.chain[i - 1]

            if currentBlock.hash != currentBlock.getHash() or prevBlock.hash != currentBlock.prevHash:
                return False

        return True


def main():
    JeChain = Blockchain()
    print(JeChain)


if __name__ == '__main__':
    main()
