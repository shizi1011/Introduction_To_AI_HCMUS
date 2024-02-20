import queue
import matplotlib.pyplot as plt


def getHeuristics():
    heristics = {}
    with open("heuristics.txt", 'r') as f:
        for i in f.readlines():
            node_heuristic_val = i.split()
            heristics[node_heuristic_val[0]] = int(node_heuristic_val[1])

    return heristics


def getCity():
    city = {}
    citiesCode = {}
    with open("cities.txt") as f:
        j = 1
        for i in f.readlines():
            node_city_val = i.split()
            city[node_city_val[0]] = [
                int(node_city_val[1]), int(node_city_val[2])]

            citiesCode[j] = node_city_val[0]
            j += 1
    return city, citiesCode


def createGraph():
    graph = {}
    with open("citiesGraph.txt") as file:
        for i in file.readlines():
            node_val = i.split()

            if node_val[0] in graph and node_val[1] in graph:
                c = graph.get(node_val[0])
                c.append([node_val[1], node_val[2]])
                graph.update({node_val[0]: c})

                c = graph.get(node_val[1])
                c.append([node_val[0], node_val[2]])
                graph.update({node_val[1]: c})

            elif node_val[0] in graph:

                c = graph.get(node_val[0])
                c.append([node_val[1], node_val[2]])
                graph.update({node_val[0]: c})

                graph[node_val[1]] = [[node_val[0], node_val[2]]]

            elif node_val[1] in graph:

                c = graph.get(node_val[1])
                c.append([node_val[0], node_val[2]])
                graph.update({node_val[1]: c})

                graph[node_val[0]] = [[node_val[1], node_val[2]]]
            else:
                graph[node_val[0]] = [[node_val[1], node_val[2]]]
                graph[node_val[1]] = [[node_val[0], node_val[2]]]

    return graph


def GBFS(startNode, heuristics, graph, goalNode):
    priorityQueue = queue.PriorityQueue()
    priorityQueue.put((heuristics[startNode], startNode))

    path = []

    while priorityQueue.empty() == False:
        current = priorityQueue.get()[1]
        path.append(current)

        if current == goalNode:
            break

        priorityQueue = queue.PriorityQueue()

        for i in graph[current]:
            if i[0] not in path:
                priorityQueue.put((heuristics[i[0]], i[0]))

    return path

# Thuat toan Astar truoc khi chinh sua
# def Astar(startNode, heuristics, graph, goalNode):
#     priorityQueue = queue.PriorityQueue()
#     distance = 0
#     path = []

#     priorityQueue.put((heuristics[startNode]+distance, [startNode, 0]))
#     while priorityQueue.empty() == False:
#         current = priorityQueue.get()[1]
#         path.append(current[0])
#         distance += int(current[1])

#         if current[0] == goalNode:
#             break

#         priorityQueue = queue.PriorityQueue()

#         for i in graph[current[0]]:
#             if i[0] not in path:
#                 priorityQueue.put((heuristics[i[0]]+int(i[1])+distance, i))

#     return path

# Thuat toan Astart sau khi chinh sua


def Astar(startNode, heuristics, graph, goalNode):
    priorityQueue = queue.PriorityQueue()
    distance = 0
    priorityQueue.put((heuristics[startNode] + distance, [startNode, 0]))
    path = [goalNode]
    parents = {}
    parents['Arad'] = (None, 0)

    while priorityQueue.empty() == False:
        current = priorityQueue.get()[1]

        if current[0] == goalNode:
            break

        g_parent = parents[current[0]][1]
        for i in graph[current[0]]:
            g = g_parent + int(i[1])

            if i[0] not in parents:
                parents[i[0]] = (current[0], g)
                priorityQueue.put((heuristics[i[0]] + g, i))
            else:
                if (g < parents[i[0]][1]):
                    parents[i[0]] = (current[0], g)

    k = (goalNode,)
    while k[0] != None:
        k = parents[k[0]]
        path.insert(0, (k[0]))

    return path


def drawMap(city, gbfs, astar, graph):
    for i, j in city.items():
        plt.plot(j[0], j[1], "ro")
        plt.annotate(i, (j[0]+5, j[1]))

        for k in graph[i]:
            n = city[k[0]]
            plt.plot([j[0], n[0]], [j[1], n[1]], "gray")

    for i in range(len(gbfs)):
        try:
            first = city[gbfs[i]]
            second = city[gbfs[i+1]]

            plt.plot([first[0], second[0]], [first[1], second[1]], "green")
        except:
            continue

    for i in range(len(astar)):
        try:
            first = city[astar[i]]
            second = city[astar[i+1]]

            plt.plot([first[0], second[0]], [first[1], second[1]], "blue")
        except:
            continue

    plt.errorbar(1, 1, label="GBFS", color="green")
    plt.errorbar(1, 1, label="ASTAR", color="blue")
    plt.legend(loc="lower left")

    plt.show()


if __name__ == "__main__":
    heuristic = getHeuristics()
    graph = createGraph()
    city, citiesCode = getCity()

    for i, j in citiesCode.items():
        print(i, j)

    while True:
        inputCode1 = int(input("Nhap dinh bat dau : "))
        inputCode2 = int(input("Nhap dinh ket thuc : "))

        if inputCode1 == 0 or inputCode2 == 0:
            break

        startCity = citiesCode[inputCode1]
        endCity = citiesCode[inputCode2]

        gbfs = GBFS(startCity, heuristic, graph, endCity)
        astar = Astar(startCity, heuristic, graph, endCity)
        print("GBFS => ", gbfs)
        print("ASTAR => ", astar)
        print(astar)

        drawMap(city, gbfs, astar, graph)
