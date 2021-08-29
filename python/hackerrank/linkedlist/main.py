#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Solution:
    def display(self, head):
        current = head
        while current:
            print(current.data, end=' ')
            current = current.next

    def insert(self, head, data):
        # Complete this method
        if head is None:
            head = Node(data)
        else:
            current = head
            while current.next is not None:
                current = current.next
            current.next = Node(data)
        return head


def main():

    mylist = Solution()
    T = int(input())
    head = None
    for i in range(T):
        data = int(input())
        head = mylist.insert(head, data)
    mylist.display(head)


if __name__ == '__main__':
    main()
