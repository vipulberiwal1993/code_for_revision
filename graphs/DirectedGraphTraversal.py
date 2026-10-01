from collections import defaultdict, deque

class DirectedGraphTraversal():
	def __init__(self, input):
		self.input = input

	def buildAdjacencyList(self):
		adjList = defaultdict(list)
		for edge in self.input:
			adjList[edge[1]].append(edge[0])
		return adjList


	def dfs(self):
		currPath = set()
		adjList = self.buildAdjacencyList()
		visited = set()

		hasCyle = False
		for vertex in adjList:
			if vertex not in visited:
				visited.add(vertex)
				currPath.add(vertex)
				hasCyle |= self.dfs_impl(adjList, visited, vertex, currPath)
				currPath.remove(vertex)

				if hasCyle:
					break

		if hasCyle:
			print("DFS: Cycle has been detected")
		else:
			print("DFS: No Cycle.")

	def dfs_impl(self, adjList, visited, node, currPath):
		hasCyle = False
		
		for nei in adjList[node]:
			if nei in currPath:
				hasCyle = True
				break
			elif nei not in visited:
				visited.add(nei)
				currPath.add(nei)
				hasCyle |= self.dfs_impl(adjList, visited, nei, currPath)
				currPath.remove(nei)

		return hasCyle

	def bfs(self):
		pass


if __name__ == "__main__":
	obj = DirectedGraphTraversal([[1,0],[0,1]])
	obj.dfs()
