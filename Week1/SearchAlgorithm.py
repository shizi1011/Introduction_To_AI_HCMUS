
from collections import defaultdict
from queue import Queue, PriorityQueue

# đọc dữ liệu từ file txt


def read_txt(file):
    size = int(file.readline())
    start, goal = [int(num) for num in file.readline().split(' ')]
    matrix = [[int(num) for num in line.split(' ')] for line in file]
    return size, start, goal, matrix

# chuyển ma trận kề thành danh sách kề


def convert_graph(matrix):
    adjList = defaultdict(list)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                adjList[i].append(j)
    return adjList


def convert_graph_weight(matrix: list[list[int]]):
    adjList = defaultdict(list)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j]:
                adjList[i].append((j, matrix[i][j]))
    return adjList


# breadth first search
def BFS(graph, start, end):
    visited = []
    frontier = Queue()
    # parent=defaultdict(lambda:None)

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

        for node in graph[current_node]:
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


# depth first search
def DFS(graph, start, end):
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

        for node in graph[current_node]:
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

# uniform cost search


def UCS(graph, start, end):
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
        for nodei in graph[current_node]:
            node, weight = nodei
            if node not in visited:
                frontier.put((current_weight+weight, node))
                parent[node] = current_node
                visited.append(node)
            else:
                #nếu node đã nằm trong visited mà có old_weight > current_weight+weight thì
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
    with open('input.txt', 'r') as file_1:
        size_1, start_1, goal_1, matrix_1 = read_txt(file_1)
    with open('inputUCS.txt', 'r') as file_2:
        size_2, start_2, goal_2, matrix_2 = read_txt(file_2)

    graph_1 = convert_graph(matrix_1)
    graph_2 = convert_graph_weight(matrix_2)

    result_bfs = BFS(graph_1, start_1, goal_1)
    # print('Kết quả sử dụng thuật toán BFS : \n',result_bfs)
    print('Ket qua su dung thuat toan BFS : \n', result_bfs)

    result_dfs = DFS(graph_1, start_1, goal_1)
    # print('Kết quả sử dụng thuật toán DFS : \n',result_dfs)
    print('Ket qua su dung thuat toan DFS : \n', result_dfs)

    cost, result_ucs = UCS(graph_2, start_2, goal_2)
    # print('Kết quả sử dụng thuật toán UCS : \n',result_dfs,result_ufs,'với tổng chi phí là : ',cost)
    print('Ket qua su dung thuat toan UCS : \n', result_ucs,
          'voi tong chi phi la  : ', cost)


if __name__ == '__main__':
    main()
