# filename: dijkstra_shortest_path.py

import heapq

def dijkstra_shortest_path(N, roads, blocked_road, start, end):
    INF = float('inf')
    dist = [INF] * N
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, node = heapq.heappop(pq)
        
        if node == end:
            return d
        
        if node == blocked_road:
            continue
        
        for neighbor, weight in roads[node]:
            if dist[node] + weight < dist[neighbor]:
                dist[neighbor] = dist[node] + weight
                heapq.heappush(pq, (dist[neighbor], neighbor))
    
    return -1

# Input example
N = 5
roads = {0: [(1, 4), (3, 2)], 1: [(2, 3)], 3: [(4, 6)], 2: [(4, 5)]}
blocked_road = 1
start = 0
end = 4

result = dijkstra_shortest_path(N, roads, blocked_road, start, end)
print(result)