
# Union-Find (DSU) in Directed Graphs: What Works and What Doesn't

## 1. Can Union-Find Be Used on Directed Graphs?

**Yes.** Union-Find (Disjoint Set Union or DSU) can be applied to directed graphs, but it ignores edge direction.

- It can identify weakly connected components.
- It cannot determine directed reachability.
- It cannot reliably detect cycles in directed graphs.
- It cannot identify strongly connected components.

## 2. Simple Example

Consider the directed graph:

```text
0 → 1 → 2
```

Edges:

```python
edges = [[0, 1], [1, 2]]
```

We want to determine whether nodes 0 and 2 belong to the same weakly connected component.

### Union-Find Algorithm

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a != root_b:
            self.parent[root_b] = root_a


edges = [[0, 1], [1, 2]]
dsu = DSU(3)

for u, v in edges:
    dsu.union(u, v)

print(dsu.find(0) == dsu.find(2))  # True
```

## 3. Step-by-Step Execution

| Step | Operation | Connected Components |
|---|---|---|
| 1 | Initialize | {0}, {1}, {2} |
| 2 | Union(0, 1) | {0,1}, {2} |
| 3 | Union(1, 2) | {0,1,2} |

All three nodes now belong to the same weakly connected component.

## 4. Why Union-Find Cannot Determine Directed Reachability

Consider:

```text
0 → 1 → 2
```

Following directed edges:

- Node 0 can reach node 2.
- Node 2 cannot reach node 0.

However:

```python
dsu.find(0) == dsu.find(2)  # True
```

Union-Find reports that both nodes belong to the same component, regardless of direction.

**Conclusion:** Union-Find identifies weak connectivity, not directed reachability.

## 5. Why Union-Find Cannot Reliably Detect Directed Cycles

Consider this directed acyclic graph:

```text
0 → 1
↓   ↓
2 → 3
```

Edges:

```python
edges = [
    [0, 1],
    [0, 2],
    [1, 3],
    [2, 3]
]
```

This graph has no directed cycle.

However, if we process the edges using standard Union-Find cycle detection:

1. Union(0, 1)
2. Union(0, 2)
3. Union(1, 3)
4. Union(2, 3) finds both nodes already connected.

A standard undirected cycle detector would report a cycle.

But the directed graph is acyclic.

**Conclusion:** Standard Union-Find cycle detection cannot distinguish directed cycles from undirected cycles.

Use DFS with recursion-stack tracking or Kahn's topological sorting algorithm instead.

## 6. Complexity

With path compression and union by rank or size:

- Find: O(α(V)) amortized
- Union: O(α(V)) amortized
- Processing all edges: O((V + E) × α(V))
- Space: O(V)

Here α is the inverse Ackermann function, which grows extremely slowly.

## 7. Interview Cheat Sheet

| Problem | Union-Find Works? |
|---|---|
| Undirected connected components | Yes |
| Undirected cycle detection | Yes |
| Directed weak connectivity | Yes |
| Directed reachability | No |
| Directed cycle detection (general case) | No |
| Strongly connected components | No |

## 8. Key Interview Takeaway

**Union-Find can be used on directed graphs when edge direction is irrelevant.**

Use:

- **Union-Find:** Weakly connected components
- **DFS/BFS:** Directed reachability
- **DFS or Kahn's algorithm:** Directed cycle detection
- **Tarjan's or Kosaraju's algorithm:** Strongly connected components

The important distinction is that Union-Find groups nodes based on connectivity while ignoring edge direction.
