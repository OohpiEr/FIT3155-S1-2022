"""
FIT3155 Assignment 2 Question 2

__author__ = "Er Tian Ru"

References:
http://codeforces.com/blog/entry/19674
https://www.quora.com/How-do-I-find-the-second-best-minimum-spanning-tree
"""

from json.encoder import INFINITY
import math
from re import T
import re
import sys


def read_file(filename):
    """
    Reads a file "filename"
    """
    # Open and read the text file
    file = open(filename, "r")
    lines = file.readlines()

    # Remember to close the file
    file.close()
    # Return the pattern and text
    return lines


def write_output(mst_1, mst_1_weight):
    """
    TODO: desc
    Writes a list occurrences to a file output_spanning.txt

    :param occurrences: 
    """
    small_txt = "Smallest Spanning Tree Weight = {}\n#List of edges in the smallest spanning tree:".format(
        mst_1_weight)
    # Open output file with correct name
    outputFile = open('output_spanning.txt', 'w')
    outputFile.write(small_txt)

    # Iterate through the occurrence list and write results to an output file
    if mst_1:
        for edge in mst_1:
            outputFile.write("\n{} {} {}".format(edge[0], edge[1], edge[2]))
    # Remember to close the file
    outputFile.close()


def read_graph_file(filename):
    lines = read_file(filename)
    edges = []
    num_vertices_edges = list(map(int, lines[0].strip().split()))

    for i in range(1, len(lines)):
        edge = lines[i].strip().split()
        edges.append(list(map(int, edge)))
    return (num_vertices_edges[0], num_vertices_edges[1], edges)

class Edge:
    def __init__(self, u, v, w) -> None:
        self.u = u
        self.v = v
        self.w = w

    def __str__(self) -> str:
        return_string = str(self.u.id) + "," + str(self.v.id) + "," + str(self.w)
        return return_string

class Vertex:
    def __init__(self, id) -> None:
        self.id = id
        # list
        self.edges = []
        # for traversal
        self.discovered = False
        self.visited = False
        # distance
        self.distance = 0
        # backtracking / where i was from
        self.previous = None

    def add_edge(self, edge):
        self.edges.append(edge)
    
    def __str__(self) -> str:
        return_string = str(self.id)
        for edge in self.edges:
            return_string += "\n with edges " + str(edge)
        return return_string

class Graph:
    def __init__(self, argv_vertices_count) -> None:
        self.vertices = [None] * (argv_vertices_count + 1) #
        for i in range(argv_vertices_count + 1):
            self.vertices[i] = Vertex(i)

    def add_edges(self, argv_edges, argv_direct=False):
        for edge in argv_edges:
            u = edge[0]
            v = edge[1]
            w = edge[2]
            # add u to v
            current_edge = Edge(self.vertices[u], self.vertices[v], w)
            current_vertex = self.vertices[u]
            current_vertex.add_edge(current_edge)
            # add v to u
            if not argv_direct:
                current_edge = Edge(self.vertices[v], self.vertices[u], w)
                current_vertex = self.vertices[v]
                current_vertex.add_edge(current_edge)
    
    def dfs(self, source, target):
        path = [[]]*len(self.vertices)
        return_dfs = []
        discovered = []  # this is a stack (LNFO)
        discovered.append(source)  # append = push
        source.discovered =  True
        while len(discovered) > 0:
            # serve from queue
            # u = discovered.serve()
            u = discovered.pop(0)  # pop(0) same as serve
            u.visited = True  # means I have visited u
            return_dfs.append(u)
            if u.id == target:
                break
            for edge in u.edges:
                v = edge.v
                if v.discovered == False:
                    discovered.append(v)
                    v.discovered = True  # means I have discovered v, adding it to queue
                    path[v.id] = path[u.id] + [u]
        return path
    
    def __str__(self) -> str:
        return_string = ""
        for vertex in self.vertices:
            return_string = return_string + "Vertex " + str(vertex) + "\n"
        return return_string

class Mst:
    """union-by-rank disjoint set data structure with path compression. """

    def __init__(self, argv_vertices_count):
        # self.graph = Graph(argv_vertices_count)
        self.parent = [-1] * (argv_vertices_count+1)
        self.num_vertices = argv_vertices_count
        self.edges = []
        self.weight = 0
        self.skipped_edges = []

    def find(self, v):
        """Find the root of vertex v with path compression

        Args:
            v (int): vertex v

        Returns:
            int: The root of vertex v
        """
        # find root of the tree containing ‘v’
        # root is reached
        if (self.parent[v] < 0):
            return v
        else:
            self.parent[v] = self.find(self.parent[v])
            return self.parent[v]
        # while self.parent[v] >= 0:
        #     v  = self.parent[v]
        # return v

    def union(self, a, b):
        """union by rank of vertex a and b

        Args:
            a (int): vertex a
            b (int): vertex b

        Returns:
            boolean: True when union is successful, false otherwise
        """
        root_a = self.find(a)  # find root of tree containing ‘a’
        root_b = self.find(b)  # find root of tree containing ‘b’

        # ‘a’ and ‘b’ in the same tree
        if (root_a == root_b):
            return False

        height_a = self.parent[root_a] * -1  # height+1 of tree containing ‘a’
        height_b = self.parent[root_b] * -1  # height+1 of tree containing ‘b’
        if (height_a > height_b):
            # link shorter tree’s root to taller
            self.parent[root_b] = root_a
            return True
        elif height_b > height_a:
            self.parent[root_a] = root_b
            return True
        else:
            # if (height_a == height_b)
            self.parent[root_a] = root_b
            self.parent[root_b] = (height_b + 1) * - \
                1  # update: height grows by 1
            return True

    def _kruskal(self, num_vertices, edges):
        # TODO: put parent arr in kruskal
        mst_edges = []
        skipped_edges = []
        weight = 0
        edges.sort(key=lambda tup: tup[2])  # sorts in place
        print("sorted edges {}".format(edges))
        i = 0
        num_edges = 0
        while num_edges < num_vertices-1:
            if self.union(edges[i][0], edges[i][1]):
                mst_edges.append(edges[i])
                num_edges += 1
                weight += edges[i][2]
            else:
                skipped_edges.append(edges[i])
            i += 1
        while i < len(edges):
            skipped_edges.append(edges[i])
            i += 1
        self.edges = mst_edges
        print("skipped {}".format(skipped_edges))
        print("parent {}".format(self.parent))
        print("mst {}".format(mst_edges))

        return (weight, mst_edges, skipped_edges)

    def add_mst(self, num_vertices, edges: list):
        self.weight, self.mst, self.skipped_edges = self._kruskal(num_vertices, edges)

    def get_2nd_mst(self, target):
        if len(self.mst) == 0:
            return

        # mst_2 = self.mst.copy()
        delta_T = math.inf
        e_new = -1
        e_old = -1
        for e in self.skipped_edges:
            # Add the edge to the tree, creating a cycle.
            # mst_2.append(e)
            g  = Graph(self.num_vertices)
            g.add_edges(self.edges)
            [[print(u) for u in v] for v in g.dfs(g.vertices[e[0]], target)]
            print("=========================")
            
            # Find k the maximum weight edge in the cycle such that k not equal to e.
            # k_weight, k  = self._find_max_in_cycle(mst_2, e)
            # Remove k - temporarily.
            # Compute the change in the tree weight δ = weight(e) − weight(k).
            
            # If δ < ∆|T| then ∆|T| = δ and Enew = e and Eold = k.
        # [print(v) for v in g.dfs(g.vertices[4])]

    # def _find_max_in_cycle(self, mst, e):


    def lca(self, root, p, q):
        path_p = self.get_path(root, p)
        path_q = self.get_path(root, q)
        # we can check from the front for the last such node which is common in both the lists. starting from i=1 since one node is always common in the list the root
        i = 1
        while(i < len(path_p) and i < len(path_q) and path_p[i] == path_q[i]):
                i += 1
        return path_p[i - 1] 

    def get_path(self, root, target):
        # stack = [(v,[path])]
        stack = [(root,[root])]
        while(stack):
            path = []
            v, path=stack.pop()
            if(v == target):
                break
            if(v.left):
                stack.append((v.left, path+[v.left]))
            if(v.right):
                stack.append((v.right, path+[v.right]))
        return path

    def __str__(self) -> str:
        return str(self.mst)


def temp():
    graph_file_name = sys.argv[1]   # text_file_name = "text.txt"
    graph_file = read_graph_file(graph_file_name)
    num_vertices = graph_file[0]
    edges = graph_file[2]

    disjset = Mst(num_vertices)
    mst = disjset._kruskal(num_vertices, edges)
    write_output(mst, disjset._get_weight(mst))


if __name__ == "__main__":
    graph_file = read_graph_file("graph_2.txt")
    num_vertices = graph_file[0]
    edges = graph_file[2]
    mst = Mst(num_vertices)
    mst.add_mst(num_vertices, edges)
    mst.get_2nd_mst(4)
    # print(g)

    

# %%
