
from abc import ABC, abstractclassmethod
from queue import Queue, PriorityQueue
from collections import defaultdict


class Graph(ABC):
    def __init__(self, graph_dict=None) -> None:
        self._graph = defaultdict(list, graph_dict)

    # Constructor construct graph từ ma trận kề, là phương thức ảo
    @abstractclassmethod
    def from_matrix(cls, matrix):
        raise NotImplementedError

    # Constructor construct graph từ file
    @classmethod
    def from_file(cls, file):
        with open(file, 'r') as f:
            cls.size = int(f.readline())
            cls.start, cls.goal = [int(num) for num in f.readline().split(' ')]
            matrix = [[int(num) for num in line.split(' ')] for line in f]
            return cls.from_matrix(matrix)
    # Hàm in ra đồ thị dưới dạng danh sách kề (dict)

    def __str__(self) -> str:
        return self._graph.__str__()

    # Hàm thêm một đỉnh và đồ thị
    def add_vertex(self, vertex: int):
        self._graph[vertex] = []

    # Hàm thêm một cạnh vào đồ thị, là phương thức ảo
    @abstractclassmethod
    def add_edge(self, edge: tuple):
        raise NotImplementedError


class UnweightedGraph(Graph):
    @classmethod
    def from_matrix(cls, matrix):
        adjList = defaultdict(list)
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 1:
                    adjList[i].append(j)
        return cls(adjList)

    def add_edge(self, edge: tuple):
        vertex1, vertex2 = edge
        self._graph[vertex1].append(vertex2)

    def BFS(self, start, end):
        visited = []
        frontier = Queue()

        # thêm node start vào frontier và visited
        frontier.put(start)
        visited.append(start)

        # start không có node cha
        parent = dict()
        parent[start] = None

        path_found = False

        while True:
            if frontier.empty():
                raise Exception('No way exception')
            current_node = frontier.get()
            visited.append(current_node)

            # kiểm tra current_node có là end hay không
            if current_node == end:
                path_found = True
                break

            for node in self._graph[current_node]:
                if node not in visited:
                    frontier.put(node)
                    parent[node] = current_node
                    visited.append(node)

        # xây dựng đường đi
        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
        return path

    def DFS(self, start, end):
        visited = []
        frontier = []

        # thêm node start vào frontier và visited
        frontier.append(start)
        visited.append(start)

        # start không có node cha
        parent = dict()
        parent[start] = None

        path_found = False

        while True:
            if not frontier:
                raise Exception('No way exception')
            current_node = frontier.pop()
            visited.append(current_node)

            # kiểm tra current_node có là end hay không
            if current_node == end:
                path_found = True
                break

            for node in self._graph[current_node]:
                if node not in visited:
                    frontier.append(node)
                    parent[node] = current_node

        # xây dựng đường đi
        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
        return path


class WeightedGraph(Graph):
    @classmethod
    def from_matrix(cls, matrix):
        adjList = defaultdict(list)
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j]:
                    adjList[i].append((j, matrix[i][j]))
        return cls(adjList)

    def add_edge(self, edge: tuple):
        vertex1, vertex2, weight = edge
        self._graph[vertex1].append((vertex2, weight))

    def UCS(self, start, end):
        frontier = PriorityQueue()
        visited = []
        # parent=defaultdict(lambda:None)
        parent = dict()
        parent[start] = None
        path_found = False

        frontier.put((0, start))
        visited.append(start)

        while True:
            if frontier.empty():
                raise Exception('No way exception')
            current_weight, current_node = frontier.get()
            visited.append(current_node)

            if current_node == end:
                # if current_node == end and frontier.empty():
                path_found = True
                break
            for nodei in self._graph[current_node]:
                node, weight = nodei
                if node not in visited:
                    frontier.put((current_weight+weight, node))
                    parent[node] = current_node
                    visited.append(node)
                else:
                    # nếu node đã nằm trong visited mà có old_weight > current_weight+weight thì
                    # cập nhập lại frontier và parent
                    for item in frontier.queue:
                        if node == item[1] and current_weight+weight < item[0]:
                            frontier.queue.remove(item)
                            frontier.put((current_weight+weight, node))
                            parent[node] = current_node
                            break

        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
        return current_weight, path


def main():
    graph1 = WeightedGraph.from_file('inputUCS.txt')
    graph2 = UnweightedGraph.from_file('input.txt')

    result_dfs = graph2.DFS(graph2.start, graph2.goal)
    result_bfs = graph2.BFS(graph2.start, graph2.goal)

    print('Ket qua su dung thuat toan BFS : \n', result_bfs)

    # print('Kết quả sử dụng thuật toán DFS : \n',result_dfs)
    print('Ket qua su dung thuat toan DFS : \n', result_dfs)

    cost, result_ucs = graph1.UCS(graph1.start, graph1.goal)
    # print('Kết quả sử dụng thuật toán UCS : \n',result_dfs,result_ufs,'với tổng chi phí là : ',cost)
    print('Ket qua su dung thuat toan UCS : \n', result_ucs,
          'voi tong chi phi la  : ', cost)

    # Code ví dụ thêm cho việc construct graph từ nhiều cách
    # adj_list = {'START': [('d', 3), ('p', 1), ('e', 9)],
    #             'd': [('b', 1), ('c', 8), ('e', 2)],
    #             'p': [('q', 15)],
    #             'b': [('a', 2)],
    #             'c': [('f', 5), ('a', 2)],
    #             'e': [('r', 9), ('h', 1)],
    #             'h': [('q', 4), ('p', 4)],
    #             'f': [('GOAL', 5)],
    #             'q': [('r', 3)],
    #             'a': [],
    #             'r': [('f', 5)],
    #             'GOAL': []
    #             }
    # #Thử construct graph từ một adj_list cho trước
    # graph3 = WeightedGraph(adj_list)
    # print(graph3.UCS('START', 'GOAL'))

    # matrix = [[0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    #           [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    # #Thử construct graph từ một matrix cho trước
    # graph4 = UnweightedGraph.from_matrix(matrix)
    # print(graph4.BFS(0, 17))


if __name__ == '__main__':
    main()
