import glob
import os
import unittest
import itertools
import random
from math import comb


def write_file(filename, data):
    # Open and write first line
    output_file = open(filename, "w")
    output_file.write(str(data[0][0]) + " " + str(data[0][1]))

    # Write remaining lines
    for i in range(1, len(data)):
        output_file.write("\n")
        output_file.write(str(data[i][0]) + " " + str(data[i][1]) + " " + str(data[i][2]))

    # Done
    output_file.close()


def read_file(filename):
    # Important Variables
    mst1_weight = 0
    mst1_edges = []
    mst2_weight = 0
    mst2_edges = []
    is_mst1 = True

    # Open and read first line
    file = open(filename, "r")
    lines = file.readlines()

    # Read remaining lines
    for line in lines:
        row = line.strip().split()
        if row[0] == "Smallest":
            mst1_weight = int(row[-1])
        elif row[0] == "Second-smallest":
            mst2_weight = int(row[-1])
            is_mst1 = False
        elif row[0] != "#List":
            if is_mst1:
                mst1_edges.append((int(row[0]), int(row[1]), int(row[2])))
            else:
                mst2_edges.append((int(row[0]), int(row[1]), int(row[2])))

    # Done
    file.close()
    return [(mst1_weight, mst1_edges), (mst2_weight, mst2_edges)]


def random_edges(count):
    # Generate all possible non-repeating edges
    edges = list(itertools.combinations(range(1, count + 1), 2))

    # Randomly shuffle these edges
    random.shuffle(edges)

    # Convert edges to list and add weights
    for i in range(len(edges)):
        edges[i] = [edges[i][0], edges[i][1], random.randint(1, 100)]

    # Done
    return edges


class TestQ2(unittest.TestCase):
    def process(self, graph, expected_output_1, expected_output_2):
        """ Main Testing Process """
        # Execute Program
        write_file("graph.txt", graph)
        os.system('cmd /c python spanning.py graph.txt')
        mst = read_file("output_spanning.txt")

        # Read Output
        mst1_weight, mst1_edges = mst[0]
        mst2_weight, mst2_edges = mst[1]

        # Check if weights are correct
        self.assertEqual(expected_output_1, mst1_weight, msg="1st MST incorrect")
        self.assertEqual(expected_output_2, mst2_weight, msg="2nd MST incorrect")

        # Compute sum of provided edge weights
        actual_weight_1 = 0
        actual_weight_2 = 0
        for _, _, weight in mst1_edges:
            actual_weight_1 += weight
        for _, _, weight in mst2_edges:
            actual_weight_2 += weight

        # Check if actual sum of edge weights is equal to claimed edge weight sum
        self.assertEqual(mst1_weight, actual_weight_1, msg="1st MST edge weight sum inconsistent with claimed weight")
        self.assertEqual(mst2_weight, actual_weight_2, msg="2nd MST edge weight sum inconsistent with claimed weight")

    @classmethod
    def tearDownClass(cls):
        """ Remove All txt files after testing """
        for txt_file in glob.glob(os.path.join(os.getcwd(), '*.txt')):
            os.remove(txt_file)

    def setUp(self):
        """ Remove All txt files before each test case """
        for txt_file in glob.glob(os.path.join(os.getcwd(), '*.txt')):
            os.remove(txt_file)

    def test_sample(self):
        """ From assignment spec """
        expected1 = 6
        expected2 = 7
        graph = [[7, 14],
                 [1, 3, 3],
                 [1, 4, 1],
                 [1, 5, 1],
                 [1, 6, 4],
                 [2, 3, 4],
                 [2, 5, 1],
                 [2, 6, 1],
                 [3, 4, 2],
                 [3, 5, 3],
                 [3, 7, 1],
                 [4, 7, 2],
                 [5, 6, 3],
                 [5, 7, 1],
                 [6, 7, 4]]
        self.process(graph, expected1, expected2)

    def test_mst1_mst2_same(self):
        """ Both 1st and 2nd MSTs have same weight """
        expected1 = 6
        expected2 = 6
        graph = [[7, 14],
                 [1, 3, 3],
                 [1, 4, 1],
                 [1, 5, 1],
                 [1, 6, 4],
                 [2, 3, 4],
                 [2, 5, 1],
                 [2, 6, 1],
                 [3, 4, 1],
                 [3, 5, 3],
                 [3, 7, 1],
                 [4, 7, 2],
                 [5, 6, 3],
                 [5, 7, 1],
                 [6, 7, 4]]
        self.process(graph, expected1, expected2)

    def test_same_edge_weights(self):
        """ All edges have same weight """
        expected1 = 2
        expected2 = 2
        graph = sorted(sorted([[1, 2, 1],
                               [1, 3, 1],
                               [2, 3, 1]], key=lambda edge: edge[1]), key=lambda edge: edge[0])
        graph.insert(0, [3, 3])
        self.process(graph, expected1, expected2)

    def test_gap_not_chosen(self):
        """ A "gap" is present within the edges chosen for the 1st MST. It is not chosen for the 2nd MST """
        expected1 = 7
        expected2 = 7
        graph = sorted(sorted([[1, 2, 1],
                               [2, 3, 2],
                               [1, 3, 3],
                               [2, 4, 4],
                               [3, 4, 4]], key=lambda edge: edge[1]), key=lambda edge: edge[0])
        graph.insert(0, [4, 5])
        self.process(graph, expected1, expected2)

    def test_gap_chosen(self):
        """ A "gap" is present within the edges chosen for the 1st MST. It is chosen for the 2nd MST """
        expected1 = 7
        expected2 = 8
        graph = sorted(sorted([[1, 2, 1],
                               [2, 3, 2],
                               [1, 3, 3],
                               [3, 4, 4],
                               [2, 4, 8]], key=lambda edge: edge[1]), key=lambda edge: edge[0])
        graph.insert(0, [4, 5])
        self.process(graph, expected1, expected2)

    def test_smallest_unchosen_not_optimal(self):
        """ The smallest edge not chosen for 1st MST is not the optimal solution for 2nd MST """
        expected1 = 7
        expected2 = 10
        graph = sorted(sorted([[1, 2, 1],
                               [2, 4, 2],
                               [2, 3, 4],
                               [1, 4, 6],
                               [3, 4, 7]], key=lambda edge: edge[1]), key=lambda edge: edge[0])
        graph.insert(0, [4, 5])
        self.process(graph, expected1, expected2)

    def test_online_1(self):
        """ From online source """
        expected1 = 42
        expected2 = 44
        graph = sorted(sorted([[2, 4, 2],
                               [4, 5, 3],
                               [2, 5, 10],
                               [2, 1, 8],
                               [1, 5, 5],
                               [7, 4, 14],
                               [4, 6, 30],
                               [3, 4, 12],
                               [7, 3, 4],
                               [7, 6, 26],
                               [5, 6, 16],
                               [2, 3, 18]], key=lambda edge: edge[1]), key=lambda edge: edge[0])
        graph.insert(0, [7, 12])
        self.process(graph, expected1, expected2)

    def test_online_2(self):
        """ From online source """
        expected1 = 63
        expected2 = 65
        graph = sorted(sorted([[1, 4, 7],
                               [2, 1, 13],
                               [1, 3, 28],
                               [2, 3, 27],
                               [4, 3, 2],
                               [3, 5, 34],
                               [3, 6, 14],
                               [6, 4, 7],
                               [5, 2, 39],
                               [5, 6, 36]], key=lambda edge: edge[1]), key=lambda edge: edge[0])
        graph.insert(0, [6, 10])
        self.process(graph, expected1, expected2)

    def test_small_random(self):
        """ Small Random Case """
        random.seed(1)
        expected1 = 197  # HARDCODED: These are the value I got. Tell me if you got something else
        expected2 = 198
        graph = random_edges(10)
        graph.insert(0, [10, comb(10, 2)])
        self.process(graph, expected1, expected2)

    def test_medium_random(self):
        """ Medium Random Case """
        random.seed(2)
        expected1 = 169  # HARDCODED: These are the value I got. Tell me if you got something else
        expected2 = 169
        graph = random_edges(100)
        graph.insert(0, [100, comb(100, 2)])
        self.process(graph, expected1, expected2)

    def test_large_random(self):
        """ Large Random Case """
        random.seed(3)
        expected1 = 999  # HARDCODED: These are the value I got. Tell me if you got something else
        expected2 = 999
        graph = random_edges(1000)
        graph.insert(0, [1000, comb(1000, 2)])
        self.process(graph, expected1, expected2)


if __name__ == '__main__':
    unittest.main()
