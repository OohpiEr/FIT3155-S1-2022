"""
FIT3155 Assignment 2 Question 2

__author__ = "Er Tian Ru"

References:
http://codeforces.com/blog/entry/19674
https://www.quora.com/How-do-I-find-the-second-best-minimum-spanning-tree
"""
import sys
from math import inf


def write_output(mst1, mst1_w, mst2, mst2_w):
    """Prints the msts to a file output_spanning.txt

    Args:
        mst1 (list): list of edges of the best mst
        mst1_w (int): weight of the best mst
        mst2 (list): list of edges of the 2nd best mst
        mst2_w (int): weight of the 2nd best mst
    """
    txt_mst1 = "Smallest Spanning Tree Weight = {}\n#List of edges in the smallest spanning tree:".format(
        mst1_w)
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
        self.graph = []  # list of sorted edges in graph

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

    def _get_new_edge(self, v, u):
        """Finds the lca of v and u, then finds the edge with max weight that previously
        connected the trees of v and u this ancestor tree.

        Args:
            v (int): vertex v
            u (int): vertex u

        Returns:
            int: index of the edge with the highest weight 
        """
        # Get the last trees that each node was a parent of before that tree became a child of another tree
        v_tree = self.parent_no_path_comp[v]
        u_tree = self.parent_no_path_comp[u]

        # u_tree's height < than v_tree's height
        if u_tree[2] > v_tree[2]:  
            # The edge that connected this tree to it's parent tree
            u_edge_index = u_tree[1]
            # This tree's parent tree
            u_parrent_tree = self.parent_no_path_comp[u_tree[0]]
            
            # if this tree's parent tree is v tree
            if u_parrent_tree == v_tree:  
                return u_edge_index
            else:   
                # u_parrent_tree and v_tree are disconnected
                # u goes up 1 tree and checks again
                return self._get_new_edge(v, u_tree[0])
        
        # v_tree's height < than u_tree's height
        elif v_tree[2] > u_tree[2]:
            # The edge that connected this tree to it's parent tree
            v_edge_index = v_tree[1]
            # This tree's parent tree
            v_parent_tree = self.parent_no_path_comp[v_tree[0]]

            # if This tree's parent tree is u tree
            if v_parent_tree == u_tree:  
                return v_edge_index
            else:   
                # v_parent_tree u_tree are disconnected.
                # v goes up 1 tree and checks again
                return self._get_new_edge(v_tree[0], u)
        
        # Both tree's heights are the same.
        else:   
            # Look up one tree from v's tree
            v_parent_tree = self.parent_no_path_comp[v_tree[0]]
            # Look up one tree from u's tree
            u_parrent_tree = self.parent_no_path_comp[u_tree[0]]

            u_edge_index = u_tree[1]
            v_edge_index = v_tree[1]

            if u_parrent_tree == v_tree:  
                # v tree == u tree's parent tree
                return u_edge_index
            elif v_parent_tree == u_tree:    
                # u tree == v tree's parent tree
                return v_edge_index
            elif u_parrent_tree == v_parent_tree:   
                # u tree and v tree share the same parent tree
                return max(u_edge_index, v_edge_index)
            else:   
                # u_tree and v_tree not connected
                # Both v and u go up by 1 tree and check again
                return self._get_new_edge(v_tree[0], u_tree[0])

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

        # a and b in the same tree
        if (root_a == root_b):
            return False

        height_a = self.parent_path_comp[root_a] * -1
        height_b = self.parent_path_comp[root_b] * -1
        # a tree taller than b tree (Rmb height stored as negative numbers)
        if height_a > height_b:
            # link shorter tree’s root to taller
            self.parent_path_comp[root_b] = root_a
            self.parent_no_path_comp[root_b] = (
                root_a, e_index, self.parent_no_path_comp[root_b][0])
            return True
        elif height_b > height_a:
            # link shorter tree’s root to taller
            self.parent_path_comp[root_a] = root_b
            self.parent_no_path_comp[root_a] = (
                root_b, e_index, self.parent_no_path_comp[root_a][0])
            return True
        else:
            # if (height_a == height_b)
            self.parent_path_comp[root_a] = root_b
            self.parent_path_comp[root_b] = -1 * (height_b + 1)
            self.parent_no_path_comp[root_a] = (
                root_b, e_index, self.parent_no_path_comp[root_a][0])
            self.parent_no_path_comp[root_b] = (self.parent_no_path_comp[root_b][0] - 1,
                                                self.parent_no_path_comp[root_b][1], self.parent_no_path_comp[root_b][0] - 1)
            return True

    def _kruskal(self):
        """Modified kruskal's algorithm for finding the best and 2nd best mst
        """

        # Special parent array that doesn't use path compression to allow for searching of cuts in the graph. Is not used for regular find operations to keep the benefits of path compression
        # (Parent node without path compression, Edge that connected it to parent node, Height when it was a parent node]

        mst1_edges = []  # best mst
        mst2_edges = []  # 2nd best mst
        mst1_w = 0
        mst2_w = inf
        e_new = None  # new edge to replace old edge
        e_old = None  # old edge to be replaced

        # sort list of edges by weight
        self.graph.sort(key=lambda edge: edge[2])

        num_mst_edges = 0
        i = 0
        while i < len(self.graph) and not (num_mst_edges >= self.num_vertices - 1 and mst2_w <= mst1_w):
            if num_mst_edges < self.num_vertices - 1 and self._union(self.graph[i][0], self.graph[i][1], i):
                mst1_edges.append(self.graph[i])
                num_mst_edges += 1
                mst1_w += self.graph[i][2]
                mst2_w += self.graph[i][2]
            else:
                # this edge is skipped in mst1
                # Find the smallest tree that joined the two nodes. Then find the edge that created the tree
                e_new_index = self._get_new_edge(self.graph[i][0], self.graph[i][1])

                new_w = mst1_w - self.graph[e_new_index][2] + self.graph[i][2]

                # replace old edge with new edge
                if new_w < mst2_w:
                    e_new = self.graph[i]
                    e_old = self.graph[e_new_index]
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
    
    def add_mst(self, edges):
        """Adds the best and 2nd best mst 

        Args:
            edges (list): list of edges
        """
        self.graph = edges
        return self._kruskal()


if __name__ == "__main__":
    filename = sys.argv[1]   # text_file_name = "text.txt"
    num_vertices, num_edges, edges = read_graph_file(filename)
    mst = BestTwoMst(num_vertices, num_edges)
    mst.add_mst(edges)
    write_output(mst.mst1_edges,  mst.mst1_weight, mst.mst2_edges, mst.mst2_weight)
