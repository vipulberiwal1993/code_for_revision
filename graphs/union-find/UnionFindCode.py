'''
Points to Remember - 
1. Union find cannot be applied to Directed graphs.
2. Starts with N different components (as individual set).
3. If we do union, and union happens, then one components decreases.
4. If we do union, and parents are same, then repeating edge in that component,-> cycle. Component count remains same.
5. Time Complexity of Union Operation - 4(Alpha) ~ Constant, so total time complexity for E edges is - (Ek), where k is the constant. Also worst case without path compression to logN.
6. In order to be Graph to be a Tree
   A: Graph must be connected. Edges must be exactly N-1
   B: No repeating Edge to avoid cycle.
'''



class UnionFind:
    def __init__(self, size):
        self.rank = [0]*size
        self.parent = [i for i in range(size)]

    def findParent(self, node):
        if node != self.parent[node]:
            self.parent[node] = self.findParent(self.parent[node])  # Path Compression
        return self.parent[node]
    
    def union(self, node1, node2):
        p1, p2 = self.findParent(node1), self.findParent(node2)
        if p1 == p2:
            return False/0
        
        if self.rank[p1] > self.rank[p2]:
            self.parent[p2] = p1
        elif self.rank[p2] > self.rank[p1]:
            self.parent[p1] = p2
        else:
            self.parent[p1] = p2
            self.rank[p2] += 1
        
        return True/1
