"""
FIT3155 Assignment 2 Question 2

__author__ = "Er Tian Ru"

References:
"""

from re import T
import re
import sys


def read_file(filename: str) -> str:
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


def write_output(mst_1: list, mst_1_weight: int) -> None:
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


class DisjointSet:
    """union-by-rank disjoint set data structure with path compression. """

    def __init__(self, argv_vertices_count):
        # self.graph = Graph(argv_vertices_count)
        self.parent = [-1] * (argv_vertices_count+1)

    def find(self, v: int):
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

    def union(self, a: int, b: int):
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

    def kruskal(self, num_vertices: int, edges: list):
        mst = []
        skipped_edges = []
        edges.sort(key=lambda tup: tup[2])  # sorts in place
        print("sorted edges {}".format(edges))
        i = 0
        num_edges = 0
        while num_edges < num_vertices-1:
            if self.union(edges[i][0], edges[i][1]):
                mst.append(edges[i])
                num_edges += 1
            else:
                skipped_edges.append(edges[i])
            i += 1
        while i < len(edges):
            skipped_edges.append(edges[i])
            i += 1
        print("skipped {}".format(skipped_edges))
        print("parent {}".format(self.parent))
        print("mst {}".format(mst))

        return mst

    def get_weight(self, edges: list):
        """Returns the weight of the mst

        Args:
            edges (list): a list of edges in the mst

        Returns:
            int: weight of the mst
        """
        weight = 0
        for edge in edges:
            weight += edge[2]
        return weight


def temp():
    graph_file_name = sys.argv[1]   # text_file_name = "text.txt"
    graph_file = read_graph_file(graph_file_name)
    num_vertices = graph_file[0]
    edges = graph_file[2]

    disjset = DisjointSet(num_vertices)
    mst = disjset.kruskal(num_vertices, edges)
    write_output(mst, disjset.get_weight(mst))
    # vertices
    # vertex ID 0...9
    # total_vertices = 7
    # my_graph = Graph(total_vertices+1)

    # my_graph.add_edges(edges, False)
    # print(my_graph)


if __name__ == "__main__":
    graph_file = read_graph_file("graph_2.txt")
    num_vertices = graph_file[0]
    edges = graph_file[2]
    disjset = DisjointSet(num_vertices)
    mst = disjset.kruskal(num_vertices, edges)


# %%
