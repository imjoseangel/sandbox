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


class Blockchain:
    def __init__(self):
        self.chain = [Block(str(datetime.now()))]

    def getLastBlock(self):
        return self.chain[-1]

    def addBlock(self, block):
        block.prevHash = self.getLastBlock().hash
        block.hash = block.getHash()
        self.chain.append(block)


def main():
    pass


if __name__ == '__main__':
    main()
