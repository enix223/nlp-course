#!/usr/bin/env python3

"""
=============
LRU Algorithm
=============

LRU is short for 'Least recently used'. LRU algorithm is based on the
priciple of:
The probability of least used items in the past which being access in
the future is also not high.

So we can sort the items from left to right by last accessing time.
New node is being inserted in the end of the list. If the list size
exceed the size limit, then we can discard the node on the first position.

================
Hash Linked List
================

Hash Linked List is a structure combining Hash table with double linked list.

Access Time early --------->  Access time recently

+------+    +------+    +------+    +------+
| Key1 |--->| Key2 |--->| Key3 |--->| Key4 |
+------+    +------+    +------+    +------+
| Val1 |--->| Val2 |--->| Val3 |<---| Val4 |
+------+    +------+    +------+    +------+

The LRU algorithm describe as below:

1. Search Hash linked list with given key, eg., Key2, when the key is found
in the hash table, then pull the node out from the hash linked list, and
insert it back to the end of the list, so the Hash linked list would look
like this now:

+------+    +------+    +------+    +------+
| Key1 |--->| Key3 |--->| Key4 |--->| Key2 |
+------+    +------+    +------+    +------+
| Val1 |--->| Val3 |--->| Val4 |--->| Val2 |
+------+    +------+    +------+    +------+

2. Suppose the key is not in the hash linked list, we need to insert the new
key-value node at the end of the list, and check whether the size of list
after inserted excceed the limit size or not. eg., we need to insert a new
key-value pair (Key5, Val5), and suppose our list limit is equal to 4:

Hash linked list after (Key5, Val5) being inserted:

+------+    +------+    +------+    +------+    +------+
| Key1 |--->| Key3 |--->| Key4 |--->| Key2 |--->| Key5 |
+------+    +------+    +------+    +------+    +------+
| Val1 |--->| Val3 |--->| Val4 |--->| Val2 |--->| Val5 |
+------+    +------+    +------+    +------+    +------+

And we need to remove the left most node from the list to keep the list size
not excceeding the list limit:

+------+    +------+    +------+    +------+
| Key3 |--->| Key4 |--->| Key2 |--->| Key5 |
+------+    +------+    +------+    +------+
| Val3 |--->| Val4 |--->| Val2 |--->| Val5 |
+------+    +------+    +------+    +------+
"""


class PtNode(object):
    """
    Pointer version
    """
    def __init__(self, key, prev, nxt, value):
        self.key = key
        self.prev = prev
        self.nxt = nxt
        self.value = value

    def __repr(self):
        return 'PtNode({})'.format(self.key)

    def __str__(self):
        return self.key


class PtHashLinkedList(object):
    """
    Pointer version
    """
    def __init__(self, size):
        self.size = size
        self.hash_table = {}
        self.tail = None
        self.head = None

    def __getitem__(self, key):
        node = self.hash_table.get(key, None)
        if node is None:
            return node

        self._refresh_node(node)
        return node.value

    def __setitem__(self, key, value):
        prev = self.tail
        node = PtNode(key, prev, None, value)
        self.hash_table[key] = node
        self.tail = node

        if prev is not None:
            prev.nxt = node

        if self.head is None:
            self.head = node

        self._purge_list()

    def _purge_list(self):
        if len(self.hash_table) > self.size:
            head_node = self.head
            if head_node is not None:
                nxt_node = head_node.nxt
                self.head = nxt_node
                nxt_node.prev = None
                del self.hash_table[head_node.key]

    def _refresh_node(self, node):
        if node == self.tail:
            return

        prev_node = node.prev
        nxt_node = node.nxt

        if self.head == node:
            self.head = nxt_node

        if prev_node is not None:
            prev_node.nxt = nxt_node

        if nxt_node is not None:
            nxt_node.prev = prev_node

        last_node = self.tail
        last_node.nxt = node

        node.nxt = None
        node.prev = self.tail
        self.tail = node

    def __str__(self):
        head = self.head
        res = 'HEAD'
        while head:
            res += ' -> {}'.format(head.key)
            head = head.nxt
        return res


class Node(object):
    """
    Key as previous/next pointer
    """
    def __init__(self, prev, nxt, value):
        self.value = value
        self.prev = prev
        self.nxt = nxt

    def __str__(self):
        return 'P: {}, N: {}, V: {}'.format(
            self.prev, self.nxt, self.value)


class HashLinkedList(object):
    def __init__(self, size):
        self.size = size
        self.hash_table = {}
        self.head = None
        self.tail = None

    def __getitem__(self, key):
        node = self.hash_table.get(key, None)
        if node is None:
            return None

        self._refresh_node(key, node)
        return node.value

    def _refresh_node(self, key, node):
        if key == self.tail:
            return

        # Deal with the head pointer
        if key == self.head:
            self.head = node.nxt

        # Deal with prev node
        if node.prev is not None:
            prev_node = self.hash_table[node.prev]
            prev_node.nxt = node.nxt

        # Deal with next node
        if node.nxt is not None:
            nxt_node = self.hash_table[node.nxt]
            nxt_node.prev = node.prev

        # Deal with current node
        node.nxt = None
        node.prev = self.tail

        # Deal with the last node
        last_node = self.hash_table[self.tail]
        last_node.nxt = key

        # Deal with tail pointer
        self.tail = key

    def _purge_list(self):
        if len(self.hash_table) > self.size:
            if self.head is not None:
                head_node = self.hash_table[self.head]      # first node
                nxt_key = head_node.nxt                     # second node
                if nxt_key is not None:
                    nxt_node = self.hash_table[nxt_key]
                    # second node become first node
                    nxt_node.prev = None
                    del self.hash_table[self.head]
                    self.head = nxt_key

    def __setitem__(self, key, value):
        node = Node(self.tail, None, value)
        self.hash_table[key] = node
        prev_node = self.hash_table.get(self.tail, None)
        if prev_node is not None:
            prev_node.nxt = key

        if len(self.hash_table) == 1:
            self.head = key

        self.tail = key

        self._purge_list()

    def __str__(self):
        pt = self.head
        res = 'HEAD'
        while pt is not None:
            res += ' <-> {}'.format(pt)
            node = self.hash_table[pt]
            pt = node.nxt
        return res


if __name__ == '__main__':
    import unittest

    class Test(unittest.TestCase):
        def setUp(self):
            self.hl = HashLinkedList(4)

        def test_get_item(self):
            self.assertIsNone(self.hl['aa'])

        def test_set_item(self):
            self.hl['aa'] = 1
            self.assertEqual(self.hl['aa'], 1)

        def test_set_items(self):
            self.hl['aa'] = 1
            self.hl['bb'] = 2
            self.hl['cc'] = 3
            self.hl['dd'] = 4
            self.hl['ee'] = 5

            self.assertIsNone(self.hl['aa'])

        def test_sequence(self):
            self.hl['aa'] = 1
            self.hl['bb'] = 2
            self.hl['cc'] = 3
            self.hl['dd'] = 4

            self.hl['dd']
            self.hl['cc']
            self.hl['bb']
            self.hl['aa']

            self.hl['ee'] = 5
            self.assertIsNone(self.hl['dd'])
            self.hl['ff'] = 6
            self.assertIsNone(self.hl['dd'])
            self.assertIsNone(self.hl['cc'])

            self.assertEqual(self.hl['bb'], 2)
            self.assertEqual(self.hl['aa'], 1)
            self.assertEqual(self.hl['ee'], 5)
            self.assertEqual(self.hl['ff'], 6)

    unittest.main()
