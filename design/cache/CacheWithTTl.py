
from heapq import heappush, heappop, heapify

class Node:
    def __init__(self, key, value, ttl, prev=None, next=None):
        self.key = key
        self.value = value
        self.ttl = ttl
        self.prev = prev
        self.next = next


class Cache():
    def __init__(self, capacity):
        self.capacity = capacity

        # Doubly linked list: head = MRU, tail = LRU
        self.head = Node(0, 0, 0)
        self.tail = Node(0, 0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

        # Hashmap for O(1) lookup, min-heap for TTL expiration
        self.map = {}
        self.heap = []
        heapify(self.heap)

    def get(self, key, ts):
        self.__purge(ts)

        if key not in self.map:
            return None

        node = self.map[key]
        value = node.value
        ttl = node.ttl

        # Move accessed key to MRU position
        self.__deleteFromLast(key)
        self.__addAtFront(key, value, ttl)
        return value

    def put(self, key, value, ttl, ts):
        # TTL = 0 means no expiration
        if ttl == 0:
            ttl = float('inf')

        self.__purge(ts)

        if len(self.map) < self.capacity:
            if key in self.map:
                self.__deleteFromLast(key)
            self.__addAtFront(key, value, ttl)
        else:
            # Evict LRU entry when cache is full
            self.__deleteFromLast(self.tail.prev.key)
            self.__addAtFront(key, value, ttl)
        return None

    def size(self, ts):
        self.__purge(ts)
        return len(self.map)

    def delete(self, key, ts):
        self.__purge(ts)
        if key in self.map:
            self.__deleteFromLast(key)
            return True
        return False

    def __addAtFront(self, key, value, ttl):
        node = Node(key, value, ttl)
        temp = self.head.next
        node.next = temp
        temp.prev = node
        self.head.next = node
        node.prev = self.head
        self.map[key] = node

        # Old heap records remain until lazily removed during purge
        heappush(self.heap, [ttl, key])

    def __deleteFromLast(self, key):
        node = self.map[key]
        right = node.next
        left = node.prev
        left.next = right
        right.prev = left
        del self.map[key]
        del node

    def __purge(self, ts):
        # Remove expired heap records; ignore stale entries
        while len(self.heap) and self.heap[0][0] <= ts:
            ttl, key = heappop(self.heap)
            if key in self.map:
                currTtl = self.map[key].ttl
                if currTtl <= ts:
                    self.__deleteFromLast(key)


def run_cache(operations, capacity):
    c = Cache(capacity)
    ans = []

    for o in operations:
        if o[0] == "put":
            ans.append(c.put(o[2], o[3], o[4], o[1]))
        elif o[0] == "get":
            ans.append(c.get(o[2], o[1]))
        elif o[0] == "size":
            ans.append(c.size(o[1]))
        elif o[0] == "delete":
            ans.append(c.delete(o[2], o[1]))
        else:
            print("Operation Invalid")

    return ans
