#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Solution:
    def insert(self, head, data):
        p = Node(data)
        if head is None:
            head = p
        elif head.next is None:
            head.next = p
        else:
            start = head
            while(start.next is not None):
                start = start.next
            start.next = p
        return head

    def display(self, head):
        current = head
        while current:
            print(current.data, end=' ')
            current = current.next

    def removeDuplicates(self, head):
        if head is None:
            return head
        else:
            current = head
            while current.next is not None:
                if current.data == current.next.data:
                    current.next = current.next.next
                else:
                    current = current.next
            return head


def main():
    mylist = Solution()
    T = int(input())
    head = None
    for i in range(T):
        data = int(input())
        head = mylist.insert(head, data)
    head = mylist.removeDuplicates(head)
    mylist.display(head)


if __name__ == '__main__':
    main()
