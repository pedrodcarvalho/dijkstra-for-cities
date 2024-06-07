from collections import defaultdict, namedtuple
import heapq
import osmnx as ox
import sys
import timeit

Edge = namedtuple('Edge', ['to_node', 'weight'])


class Graph:
    def __init__(self):
        self.adjacency_list = defaultdict(list)

    def add_edge(self, from_node, to_node, weight):
        self.adjacency_list[from_node].append(Edge(to_node, weight))


class Dijkstra:
    def __init__(self, graph):
        self.graph = graph
        self.distances = defaultdict(lambda: float('inf'))
        self.visited = set()

    def run(self, start):
        self.distances[start] = 0
        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_node in self.visited:
                continue
            self.visited.add(current_node)

            for neighbor in self.graph.adjacency_list[current_node]:
                distance = current_distance + neighbor.weight
                if distance < self.distances[neighbor.to_node]:
                    self.distances[neighbor.to_node] = distance
                    heapq.heappush(
                        priority_queue, (distance, neighbor.to_node))

            yield current_node


def execute_dijkstra(dijkstra, start_node, graph):
    with open('coordinates.csv', 'w') as file:
        for node in dijkstra.run(start_node):
            file.write(f'{graph.nodes[node]['y']}, {graph.nodes[node]['x']}\n')


def main() -> None:
    if len(sys.argv[1:]) != 1:
        print('Usage: python3 dijkstra.py <query>')
        sys.exit(1)

    graph = ox.graph_from_place(
        f'{sys.argv[1:]}', network_type='drive', simplify=True)

    dijkstra_graph = Graph()

    for u, v, data in graph.edges(data=True):
        dijkstra_graph.add_edge(u, v, data['length'])

    dijkstra = Dijkstra(dijkstra_graph)

    start_node = list(graph.nodes)[0]

    time = timeit.timeit(lambda: execute_dijkstra(
        dijkstra, start_node, graph), number=1, globals=globals())

    print(f'Time taken to execute Dijkstra algorithm to find shortest path in {sys.argv[1]}: {time * 1000:.2f}ms')


if __name__ == '__main__':
    main()
