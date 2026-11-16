from collections import defaultdict
import heapq

def build_graph(n, links):
    graph = defaultdict(list)

    for u, v, ping in links:
        graph[u].append((v, ping))
        graph[v].append((u, ping))

    return graph


def minimum_broadcast_latencies(n, links, source):
    graph = build_graph(n, links)

    min_heap = [(0, source)]
    distances = [float('inf')] * n
    distances[source] = 0

    while min_heap:
        current_distance, city = heapq.heappop(min_heap)

        if current_distance > distances[city]:
            continue

        for neighbor, ping in graph[city]:
            new_distance = current_distance + ping

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(min_heap, (new_distance, neighbor))

    return [
        -1 if distance == float('inf') else distance
        for distance in distances
    ]
