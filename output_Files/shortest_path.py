# filename: shortest_path.py
import heapq

def dijkstra(n, edges, blocked_road, start, end):
    # 构建图
    graph = [[] for _ in range(n)]
    for i, (u, v, w) in enumerate(edges):
        if i == blocked_road:
            continue
        graph[u].append((v, w))
        graph[v].append((u, w))
    
    # 打印图结构以供检查
    print("Graph structure:")
    for i in range(n):
        print(f"Node {i}: {graph[i]}")
    
    # 初始化距离数组
    dist = [float('inf')] * n
    dist[start] = 0
    
    # 优先队列
    pq = [(0, start)]
    
    while pq:
        current_dist, current_vertex = heapq.heappop(pq)
        
        if current_vertex == end:
            return current_dist
        
        if current_dist > dist[current_vertex]:
            continue
        
        for neighbor, weight in graph[current_vertex]:
            new_dist = current_dist + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
    
    return -1

def main():
    input_data = [
        "5",
        "0 1 4",
        "1 2 3",
        "0 3 2",
        "3 4 6",
        "2 4 5",
        "1",
        "0",
        "4"
    ]
    
    n = int(input_data[0])
    edges = [list(map(int, line.split())) for line in input_data[1:n+1]]
    blocked_road = int(input_data[n+1])
    start = int(input_data[n+2])
    end = int(input_data[n+3])
    
    result = dijkstra(n, edges, blocked_road, start, end)
    print(result)

if __name__ == "__main__":
    main()