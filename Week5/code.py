from treelib import Node, Tree
import sys

# Final
# Structure to represent tree nodes in the A* expansion


class TreeNode(object):
    def __init__(self, c_no, c_id,  f_value, h_value, parent_id):
        self.c_no = c_no
        self.c_id = c_id
        self.f_value = f_value
        self.h_value = h_value
        self.parent_id = parent_id

# Structure to represent fringe nodes in the A* fringle list


class FringeNode(object):
    def __init__(self, c_no,  f_value):
        self.f_value = f_value
        self.c_no = c_no


class Graph():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

    # A ultility function to print the constructed MST stored in parent[]
    def printMST(self, parent, g, d_temp, t):
        #print("Edge \tWeight")
        sum_weight = 0
        min1 = 10000
        min2 = 10000
        r_temp = {}  # Reverse dictionary
        for k in d_temp:
            r_temp[d_temp[k]] = k
        for i in range(1, self.V):
            # print(parent[i], "-",i, "\t",self.graph[i][parent[i]])
            sum_weight = sum_weight + self.graph[i][parent[i]]
            if (g[0][r_temp[i]] < min1):
                min1 = g[0][r_temp[i]]
            if (g[0][r_temp[parent[i]]] < min1):
                min1 = g[0][r_temp[parent[i]]]
            if (g[t][r_temp[i]] < min2):
                min2 = g[t][r_temp[i]]
            if (g[t][r_temp[parent[i]]] < min2):
                min2 = g[t][r_temp[parent[i]]]
        return (sum_weight + min1 + min2) % 10000

    # A ultility funciton to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minKey(self, key, mstSet):

        # Initilaize min value
        min = sys.maxsize
        for v in range(self.V):
            if key[v] < min and mstSet[v] == False:
                min = key[v]
                min_index = v

        return min_index

    # Function to construct and print MST for a graph
    # represented using adjacency matrix representation
    def primMST(self, g, d_temp, t):

        # Key values used to pick minimum weight edge in cut
        key = [sys.maxsize] * self.V
        parent = [None] * self.V  # Array to store construct MST
        # Make key 0 so that this vertext is picked as first vertex
        key[0] = 0
        mstSet = [False] * self.V
        sum_weight = 10000
        parent[0] = -1  # First node is always the root of

        for c in range(self.V):

            # Pick theo minimum distance vertex form theo set of vertices not yet processd.
            # u is always equal to src in first iteration
            u = self.minKey(key, mstSet)

            # Put the minimun distance vertex in the shortest path tree
            mstSet[u] = True

            # Update dist value of the adjacent vertices of the picked vertex only if the current distance if greater than new distance and
            # the vertex in not in the shortest path tree
            for v in range(self.V):
                # graph[u][v] is non zero only for adjacent vertices of m
                # mstSet[v] is false for vertices not yet included in MST
                # Update the key only if graph[u][v] is smaller than key[v]
                if self.graph[u][v] > 0 and mstSet[v] == False and key[v] > self.graph[u][v]:
                    key[v] = self.graph[u][v]
                    parent[v] = u

        return self.printMST(parent, g, d_temp, t)


# Idea here is to form a graph of all unvisited nodes and make MST from that.
# Determine weight of that mst and connect it with the visited node and 0th node
# Prim's Algorithm used for MST (Greedy approach)
def heuristic(tree, p_id, t, V, graph):
    visited = set()  # Set to store visited nodes
    visited.add(0)
    visited.add(t)
    if (p_id != -1):
        tnode = tree.get_node(str(p_id))
        # Find all visited nodes and add them to the set
        while (tnode.data.c_id != 1):
            visited.add(tnode.data.c_no)
            tnode = tree.get_node(str(tnode.data.parent_id))
    l = len(visited)
    num = V - l  # No of unvisited nodes
    if (num != 0):
        g = Graph(num)
        d_temp = {}
        key = 0
        # d_temp dictionary stores mappings of original city no as (key) and new sequential no as value for MST to work
        for i in range(V):
            if (i not in visited):
                d_temp[i] = key
                key = key + 1

        i = 0
        for i in range(V):
            for j in range(V):
                if ((i not in visited) and (j not in visited)):
                    g.graph[d_temp[i]][d_temp[j]] = graph[i][j]
        mst_weight = g.primMST(graph, d_temp, t)
        return mst_weight
    else:
        return graph[t][0]


def checkPath(tree, toExpand, V):
    # Get the node expand from the tree
    tnode = tree.get_node(str(toExpand.c_id))
    list1 = list()  # For 1st node
    if (tnode.data.c_id == 1):
        #print("In If")
        return 0
    else:
        #print("In else")
        depth = tree.depth(tnode)  # Check depth of the tree
        s = set()  # Set to store nodes in the path
        # Go up in the tree using the parent pointer and add all nodes in the way to the set and list
        while (tnode.data.c_id != 1):
            s.add(tnode.data.c_no)
            list1.append(tnode.data.c_no)
            tnode = tree.get_node(str(tnode.data.parent_id))
        list1.append(0)
        if (depth == V and len(s) == V and list1[0] == 0):
            print("Path complete")
            list1.reverse()
            print(list1)
            return 1
        else:
            return 0


def startTSP(graph, tree, V):
    goalState = 0
    times = 0
    toExpand = TreeNode(0, 0, 0, 0, 0)  # Node to expand
    key = 1  # Unique Identifier for a node in the tree
    heu = heuristic(tree, -1, 0, V, graph)  # Heuristic for node 0 in the tree
    tree.create_node("1", "1", data=TreeNode(0, 1, heu, heu, -1))
    fringe_list = {}
    fringe_list[key] = FringeNode(0, heu)
    key = key + 1
    while (goalState == 0):
        minf = sys.maxsize
        # Pick node having min f_value from the fringe list
        for i in fringe_list.keys():
            if (fringe_list[i].f_value < minf):
                toExpand.f_value = fringe_list[i].f_value
                toExpand.c_no = fringe_list[i].c_no
                toExpand.c_id = i
                minf = fringe_list[i].f_value

        # Heuristic value of selected node
        h = tree.get_node(str(toExpand.c_id)).data.h_value
        val = toExpand.f_value - h
        path = checkPath(tree, toExpand, V)
        # If node to expand is 0 and path is complete, we are done
        # We check node at the time of expansion and not at the time of generation
        if (toExpand.c_no == 0 and path == 1):
            goalState = 1
            cost = toExpand.f_value  # Total actual cost incurred
        else:
            del fringe_list[toExpand.c_id]  # Remove node from FL
            j = 0
            # Evaluate f_values and h_values of adjacent nodes of the node to expand
            while (j < V):
                if (j != toExpand.c_no):
                    h = heuristic(tree, toExpand.c_id, j, V,
                                  graph)  # Heuristic calc
                    f_val = val + graph[j][toExpand.c_no] + h
                    fringe_list[key] = FringeNode(j, f_val)
                    tree.create_node(str(toExpand.c_no), str(key), parent=str(
                        toExpand.c_id), data=TreeNode(j, key, f_val, h, toExpand.c_id))
                    key = key + 1
                j = j+1
    return cost


if __name__ == '__main__':
    #graph = [[0,300],[300,0]]
    #graph = [[0,300,200],[300,0,500],[200,500,0]]
    V = 4
    graph = [[0, 5, 2, 3], [5, 0, 6, 3], [2, 6, 0, 4], [3, 3, 4, 0]]
    # graph = [[0, 10, 15, 20], [10, 0, 20, 25],
    #          [15, 20, 0, 30], [20, 25, 30, 0]]

    tree = Tree()
    ans = startTSP(graph, tree, V)
    print("Ans is "+str(ans))
