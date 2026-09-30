from collections import defaultdict, deque

class UndirectedGraphTraversal():
	def __init__(self, input):
		self.input = input

	def buildAdjacencyList(self, edges):
		adjList = defaultdict(list)
		for edge in edges:
			adjList[edge[0]].append(edge[1])
			adjList[edge[1]].append(edge[0])
		return adjList

	def bfs(self):
		visited = set()
		adjList = self.buildAdjacencyList(self.input)

		# Assuming graph not connected connected
		hasCycle = False
		for vertex in adjList:
			if vertex not in visited:
				visited.add(vertex)
				q = deque([])
				q.append([vertex, None])
				hasCycle |= self.bfs_impl(q, visited, adjList, vertex)

				if hasCycle:
					print("BFS: Cycle has been detected")
					break
		print("BFS: No Cycle Detected")
		return hasCycle


	def bfs_impl(self, q, visited, adjList, node):
		while len(q):
			node, parent = q.popleft()
			for nei in adjList[node]:
				if nei != parent and nei in visited:
					return True
				elif nei != parent:
					visited.add(nei)
					q.append([nei, node])

		return False


	def dfs(self):
		visited = set()
		adjList = self.buildAdjacencyList(self.input)

		hasCycle = False
		for vertex in adjList:
			if vertex not in visited:
				visited.add(vertex)
				hasCycle |= self.dfs_impl(visited, adjList, vertex, None)

				if hasCycle:
					print("DFS: Cycle has been detected")
					break  

		print("DFS: No Cycle Detected")
		return hasCycle


	def dfs_impl(self, visited, adjList, node, parent):
		hasCycle = False
		for nei in adjList[node]:
			if nei != parent and nei in visited:
				hasCycle = True
				break
			elif nei != parent:
				visited.add(nei)
				hasCycle |= self.dfs_impl(visited, adjList, nei, node)
		return hasCycle



if __name__ == "__main__":

    test_cases = [
        # 1. Simple tree
        ("Tree", [(0,1),(0,2),(1,3),(1,4),(2,5)], False),

        # 2. Simple cycle: 0-1-2-0
        ("Simple Cycle", [(0,1),(1,2),(2,0)], True),

        # 3. Larger tree
        ("Large Tree", [(0,1),(0,2),(0,3),(1,4),(1,5),(2,6),(2,7),(3,8),(3,9),(5,10),(6,11)], False),

        # 4. Cycle in middle
        ("Middle Cycle", [(0,1),(1,2),(2,3),(3,1),(3,4)], True),

        # 5. Disconnected graph, no cycles
        ("Disconnected No Cycle", [(0,1),(1,2),(3,4),(4,5),(6,7)], False),

        # 6. Disconnected graph, one component has cycle
        ("Disconnected With Cycle", [(0,1),(1,2),(3,4),(4,5),(5,3),(6,7)], True),

        # 7. Long chain
        ("Long Chain", [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8)], False),

        # 8. Triangle
        ("Triangle", [(0,1),(1,2),(2,0),(2,3)], True),

        # 9. Complex tree
        ("Complex Tree", [(0,1),(0,2),(0,3),(1,4),(1,5),(2,6),(2,7),(3,8),(3,9),(5,10),(6,11),(7,12),(8,13),(9,14)], False),

        # 10. Complex graph with cycle
        ("Complex Cycle", [(0,1),(0,2),(1,3),(2,3),(3,4),(4,5),(5,6),(6,4)], True),
    ]

    for name, edges, expected in test_cases:
	    obj = UndirectedGraphTraversal(edges)

	    print("\n============= DFS =================")
	    actual = obj.dfs()
	    print("Actual cycle:", actual)

	    if actual == expected:
	        print("PASS")
	    else:
	        print("FAIL")

	    print("\n============= BFS =================")
	    actual = obj.bfs()
	    print("Actual cycle:", actual)

	    if actual == expected:
	        print("PASS")
	    else:
	        print("FAIL")