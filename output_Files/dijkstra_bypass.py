# filename: dijkstra_bypass.py
import heapq

def dijkstra(n, edges, blocked_road, start, end):
    # 构建图
    graph = [[] for _ in range(n)]
    for i, (u, v, w) in enumerate(edges):
        if i == blocked_road:
            continue  # 跳过被封锁的道路
        graph[u].append((v, w))
        graph[v].append((u, w))  # 假设道路是双向的
    
    # 初始化距离数组
    dist = [float('inf')] * n
    dist[start] = 0
    
    # 优先队列
    pq = [(0, start)]  # (distance, vertex)
    
    while pq:
        current_dist, current_vertex = heapq.heappop(pq)
        
        if current_vertex == end:
            return current_dist
        
        if current_dist > dist[current_vertex]:
            continue  # 这个节点已经被访问过了
        
        for neighbor, weight in graph[current_vertex]:
            distance = current_dist + weight
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return -1  # 如果无法到达终点

# 示例输入
input_data = ['5', '0 1 4', '1 2 3', '0 3 2', '3 4 6', '2 4 5', '1', '0', '4']
n = int(input_data[0])
edges = [list(map(int, line.split())) for line in input_data[1:-3]]
blocked_road = int(input_data[-3])
start = int(input_data[-2])
end = int(input_data[-1])

# 计算并打印结果
result = dijkstra(n, edges, blocked_road, start, end)
print(result)