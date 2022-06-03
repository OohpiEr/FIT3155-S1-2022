"""
FIT3155 Assignment 2 Question 2

__author__ = "Er Tian Ru"

References:
http://codeforces.com/blog/entry/19674
https://www.quora.com/How-do-I-find-the-second-best-minimum-spanning-tree
"""

from math import inf
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

def write_output(mst1, mst1_w, mst2, mst2_w):
    """Prints the msts to a file output_spanning.txt

    Args:
        mst1 (list): list of edges of the best mst
        mst1_w (int): weight of the best mst
        mst2 (list): list of edges of the 2nd best mst
        mst2_w (int): weight of the 2nd best mst
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
    """Reads a txt file as a graph 

    Args:
        filename (str): name of the file to read

    Returns:
        tuple: (number of vertices in the graph, number of edges in the graph, list of edges in the graph)
    """
    lines = read_file(filename)
    edges = []
    num_vertices_edges = list(map(int, lines[0].strip().split()))

    for i in range(1, len(lines)):
        edge = lines[i].strip().split()
        edges.append(list(map(int, edge)))
    return (num_vertices_edges[0], num_vertices_edges[1], edges)


class BestTwoMst:
    """Class for best two mst"""

    def __init__(self, num_vertices, num_edges):
        """Constructor

        Args:
            num_vertices (int): number of vertices
            num_edges (int): number of edges
        """
        # self.graph = Graph(argv_vertices_count)
        self.parent_path_comp = [-1] * (num_vertices+1)
        self.parent_no_path_comp = [(-1, None)] * (num_vertices+1)
        self.num_vertices = num_vertices
        self.num_edges = num_edges
        self.mst1_edges = []
        self.mst2_edges = []
        self.mst1_weight = 0
        self.mst2_weight = 0
        self.graph = []

    def _find(self, v):
        """Find the root of vertex v with path compression

        Args:
            v (int): vertex v

        Returns:
            int: The root of vertex v
        """
        # find root of the tree containing ‘v’
        if (self.parent_path_comp[v] < 0):
            return v
        else:
            self.parent_path_comp[v] = self._find(self.parent_path_comp[v])
            return self.parent_path_comp[v]

    def _get_e_index_in_cut_aux(self, v, e_index):   
        """auxiliary function for getting the edge in the cut 

        Args:
            v (int): vertex v
            e_index (int): index of the edge

        Returns:
            int: index of the edge in the cut
        """
        # root found
        if self.parent_no_path_comp[v][0] < 0:  
            return e_index
        else:
            e_index = self.parent_no_path_comp[v][1]
            return self._get_e_index_in_cut_aux(self.parent_no_path_comp[v][0], e_index)

    def _get_e_index_in_cut(self, edges, i):
        """Finds the index of the edge in the cut (max in the cycle) by getting the index of the previous
         edge that connected v to its parent recursively.

        Args:
            edges (list): list of edges in the mst
            i (int): index of the current edge

        Returns:
            int: index of the edge in the cut
        """
        e_1 = self._get_e_index_in_cut_aux(edges[i][0], self.parent_no_path_comp[edges[i][0]][1])
        e_2 = self._get_e_index_in_cut_aux(edges[i][1], self.parent_no_path_comp[edges[i][1]][1])
        if e_1 and e_2:
            return max(e_1, e_2)
        elif not e_1:
            return e_2
        elif not e_2:
            return e_1
    
    def _lca(self, v, u):   
        # Finds the lowest common ancestor of v and u, then finds the largest of the edges that last connected v and u's
        # respective trees to this ancestor's tree

        # Get the last trees that each node was a parent of before that tree became a child of another tree
        vTree = self.parent_no_path_comp[v]
        uTree = self.parent_no_path_comp[u]
        
        if uTree[2] > vTree[2]: # If u's tree's height is less than v's tree's height
            uConnectingEdgeIndex = uTree[1]  # The edge that connected this tree to it's parent tree
            uNextTree = self.parent_no_path_comp[uTree[0]]   # This tree's parent tree
            if uNextTree == vTree:  # This tree's parent tree is v's tree
                return uConnectingEdgeIndex
            else:   # The two trees are still disconnected. u goes up 1 tree and checks again
                return self._lca(v, uTree[0], self.parent_no_path_comp)
        
        elif vTree[2] > uTree[2]:   # If v's tree's height is less than u's tree's height
            vConnectingEdgeIndex = vTree[1]  # The edge that connected this tree to it's parent tree
            vNextTree = self.parent_no_path_comp[vTree[0]]   # This tree's parent tree
            if vNextTree == uTree:  # This tree's parent tree is v's tree
                return vConnectingEdgeIndex
            else:   # The two trees are still disconnected. v goes up 1 tree and checks again
                return self._lca(vTree[0], u, self.parent_no_path_comp)
            
        else:   # Both tree's heights are the same. 
            vNextTree = self.parent_no_path_comp[vTree[0]]   # Look up one tree from v's tree
            uNextTree = self.parent_no_path_comp[uTree[0]]   # Look up one tree from u's tree
            
            uConnectingEdgeIndex = uTree[1]
            vConnectingEdgeIndex = vTree[1]
            
            if uNextTree == vTree:  # v's tree is u's tree's parent tree
                return uConnectingEdgeIndex
            
            elif vNextTree == uTree:    # u's tree is v's tree's parent tree
                return vConnectingEdgeIndex
            
            elif uNextTree == vNextTree:   # Neither are each other's parent trees, but they share the same parent tree
                return max(uConnectingEdgeIndex, vConnectingEdgeIndex)
            
            else:   # The two trees are still disconnected. Both v and u go up by 1 tree and check again
                return self._lca(vTree[0], uTree[0], self.parent_no_path_comp)    


    def _union(self, a, b, e_index):
        """union by rank of vertex a and b

        Args:
            a (int): vertex a
            b (int): vertex b
            e_index (int): edge index

        Returns:
            boolean: True when union is successful, false otherwise
        """
        root_a = self._find(a)
        root_b = self._find(b)

        if (root_a == root_b):    # a and b in the same tree
            return False

        height_a = self.parent_path_comp[root_a] * -1  # height+1 of tree containing ‘a’
        height_b = self.parent_path_comp[root_b] * -1  # height+1 of tree containing ‘b’
        
        if height_a > height_b:
            # link shorter tree’s root to taller
            self.parent_path_comp[root_b] = root_a
            self.parent_no_path_comp[root_b] = (root_a, e_index) # edge index stored in b
            return True
        elif height_b > height_a:
            # link shorter tree’s root to taller
            self.parent_path_comp[root_a] = root_b
            self.parent_no_path_comp[root_a] = (root_b, e_index) # edge index stored in b
            return True
        else:   
            # if (height_a == height_b)
            self.parent_path_comp[root_a] = root_b
            self.parent_path_comp[root_b] = -1 * (height_b + 1) 
            self.parent_no_path_comp[root_a] = (root_b, e_index)
            self.parent_no_path_comp[root_b] = (
                self.parent_no_path_comp[root_b][0] - 1, self.parent_no_path_comp[root_b][1])
            return True

    def _kruskal(self, num_vertices, edges):
        """Modified kruskal's algorithm for finding the best and 2nd best mst

        Args:
            num_vertices (int): number of vertices+
            edges (list): list of edges in the graph
        """
        mst1_edges = [] # best mst
        mst2_edges = [] # 2nd best mst
        mst1_w = 0
        mst2_w = inf
        e_new = None # new edge to replace old edge
        e_old = None # old edge to be replaced

        edges.sort(key=lambda tup: tup[2])  # sorts in place

        i = 0
        num_mst_edges = 0
        while i < self.num_edges and not (num_mst_edges >= num_vertices - 1 and mst2_w <= mst1_w):
            if num_mst_edges < self.num_vertices - 1 and self._union(edges[i][0], edges[i][1], i):
                mst1_edges.append(edges[i])
                num_mst_edges += 1
                mst1_w += edges[i][2]
                mst2_w += edges[i][2]
            else:
                # this edge is skipped in mst1
                # e_cut_index = self._lca(edges, i) # find index of edge in cut (max weight edge in cycle)
                e_cut_index = self._get_e_index_in_cut(edges, i) # find index of edge in cut (max weight edge in cycle)
                new_w = mst1_w - edges[e_cut_index][2] + edges[i][2]

                # replace old edge with new edge
                if new_w < mst2_w:
                    e_new = edges[i]
                    e_old = edges[e_cut_index]
                    mst2_w = new_w
            i += 1

        # build mst2
        for e in mst1_edges:
            if e != e_old:
                mst2_edges.append(e)
        mst2_edges.append(e_new)

        # update variables
        self.mst1_edges = mst1_edges
        self.mst2_edges = mst2_edges
        self.mst1_weight =  mst1_w
        self.mst2_weight =  mst2_w
    
    def add_mst(self, num_vertices, edges):
        """Adds the best and 2nd best mst 

        Args:
            num_vertices (int): number of vertices
            edges (list): list of edges
        """
        self.graph = edges
        self._kruskal(num_vertices, edges)



if __name__ == "__main__":
    filename = sys.argv[1]   # text_file_name = "text.txt"
    num_vertices, num_edges, edges = read_graph_file(filename)
    # num_vertices, num_edges, edges = read_graph_file("graph.txt")
    mst = BestTwoMst(num_vertices, num_edges)
    mst.add_mst(num_vertices, edges)
    write_output(mst.mst1_edges, mst.mst1_weight, mst.mst2_edges, mst.mst2_weight)