"""
FIT3155 Assignment 2 Question 2

__author__ = "Er Tian Ru"

References:
"""

import math
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


def write_output(mst1, mst1_w, mst2, mst2_w) -> None:
    """
    TODO: desc
    Writes a list occurrences to a file output_spanning.txt

    :param occurrences: 
    """
    txt_mst1 = "Smallest Spanning Tree Weight = {}\n#List of edges in the smallest spanning tree:".format(mst1_w)
    txt_mst2 = "\nSecond-smallest Spanning Tree Weight = {}\n#List of edges in the second smallest spanning tree:".format(
        mst2_w)
    # Open output file with correct name
    outputFile = open('output_spanning.txt', 'w')
    outputFile.write(txt_mst1)

    if mst1:
        for edge in mst1:
            outputFile.write("\n{} {} {}".format(edge[0], edge[1], edge[2]))

    outputFile.write(txt_mst2)
    if mst2:
        for edge in mst2:
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


class Mst:
    """union-by-rank disjoint set data structure with path compression. """

    def __init__(self, argv_vertices_count):
        # self.graph = Graph(argv_vertices_count)
        self.num_vertices = argv_vertices_count
        self.edges = []
        self.graph = []
        self.weight = 0
        self.skipped_edges = []
        

    def find(self, v, parent):
        """Find the root of vertex v with path compression

        Args:
            v (int): vertex v

        Returns:
            int: The root of vertex v
        """
        # find root of the tree containing ‘v’
        # root is reached
        if (parent[v] < 0):
            return v
        else:
            parent[v] = self.find(parent[v], parent)
            return parent[v]

    def union(self, a, b, parent):
        """union by rank of vertex a and b

        Args:
            a (int): vertex a
            b (int): vertex b

        Returns:
            boolean: True when union is successful, false otherwise
        """
        root_a = self.find(a, parent)  # find root of tree containing ‘a’
        root_b = self.find(b, parent)  # find root of tree containing ‘b’

        # ‘a’ and ‘b’ in the same tree
        if (root_a == root_b):
            return False

        height_a = parent[root_a] * -1  # height+1 of tree containing ‘a’
        height_b = parent[root_b] * -1  # height+1 of tree containing ‘b’
        if (height_a > height_b):
            # link shorter tree’s root to taller
            parent[root_b] = root_a
            return True
        elif height_b > height_a:
            parent[root_a] = root_b
            return True
        else:
            # if (height_a == height_b)
            parent[root_a] = root_b
            parent[root_b] = (height_b + 1) * - \
                1  # update: height grows by 1
            return True

    def _kruskal(self, num_vertices, edges):
        parent = [-1] * (num_vertices+1)

        # O(VE)

        mst_edges = []
        skipped_edges = []
        weight = 0
        
        edges.sort(key=lambda tup: tup[2])  # sorts in place
        i = 0
        num_edges = 0
        while num_edges < num_vertices-1:
            if self.union(edges[i][0], edges[i][1], parent):
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

        return (weight, mst_edges, skipped_edges)


    def add_mst(self, num_vertices, edges):
        self.graph = edges
        self.weight, self.mst, self.skipped_edges = self._kruskal(num_vertices, edges)
        return self

    def get_2nd_mst(self):
        if len(self.mst) == 0:
            return

        mst2_edges = self.edges.copy()
        mst2_w = math.inf
        skipped_edges = []
        for skiped_e in self.skipped_edges:
            for i in range(len(mst2_edges)):
                mst2_edges[i] = skiped_e

        return mst2, mst2_w

        # for e in self.edges:
        #     # Add the edge to the tree, creating a cycle.
        #     # mst_2.append(e)
            
        #     # Find k the maximum weight edge in the cycle such that k not equal to e.
        #     k = len(self.edges) - 1
        #     while k >= 0 and self.edges[k][2] <= e[2]:
        #         if self._has_path(self.edges[k][1], e[0]):
        #             return
        #         k -= 1
            # k_weight, k  = self._find_max_in_cycle(mst_2, e)
            # Remove k - temporarily.
            # Compute the change in the tree weight δ = weight(e) − weight(k).
            
            # If δ < ∆|T| then ∆|T| = δ and Enew = e and Eold = k.
        # [print(v) for v in g.dfs(g.vertices[4])]

    def _has_path(self, e_start, target1):
        edges = []
        path_target1 = False
        # path_target2 = False
        for e in self.edges:
            if (e[0] == e_start and e[1] == target1) or (e[0] == target1 and e[1] == e_start): 
                return True
            else:
                self._has_path(e[0], target1)
                self._has_path(e[1], target1)
            # if e[0] == target2 or e[1] == target2:
            #     path_target2 = True

            
if __name__ == "__main__":
    # graph_file_name = sys.argv[1]   # text_file_name = "text.txt"
    graph_file_name = "graph.txt"   # text_file_name = "text.txt"
    graph_file = read_graph_file(graph_file_name)
    num_vertices = graph_file[0]
    edges = graph_file[2]

    mst = Mst(num_vertices)
    mst.add_mst(num_vertices, edges)
    mst2, mst2_w = mst.get_2nd_mst()
    write_output(mst.edges, mst.weight, mst2, mst2_w)




# %%
