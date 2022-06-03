import sys
from math import inf

"""
Author: Jeremy Yoon Zhe Min
Student ID: 30885043
"""


def write_output(mst1, mst1Weight, mst2, mst2Weight):

    outputFile = open('output_spanning.txt', 'w')

    outputFile.write("Smallest Spanning Tree Weight = " + str(mst1Weight) +
                     "\n#List of edges in the smallest spanning tree:")
    for edge in mst1:
        outputFile.write("\n{} {} {}".format(edge[0], edge[1], edge[2]))

    outputFile.write("\nSecond-smallest Spanning Tree Weight = " +
                     str(mst2Weight) + "\n#List of edges in the second smallest spanning tree:")
    for edge in mst2:
        outputFile.write("\n{} {} {}".format(edge[0], edge[1], edge[2]))

    outputFile.close()


def find(v, parentArray):

    if parentArray[v] < 0:  # Found parent
        return v
    else:
        parentArray[v] = find(parentArray[v], parentArray)
        return parentArray[v]


def findLastConnectingEdgeIndex(v, parentUtilArray, lastConnectingEdgeIndex):   
    # Finds the index of the edge that last connected v to its parent

    if parentUtilArray[v][0] < 0:  # Found parent
        return lastConnectingEdgeIndex
    else:
        connectingEdgeIndex = parentUtilArray[v][1]
        return findLastConnectingEdgeIndex(parentUtilArray[v][0], parentUtilArray, connectingEdgeIndex)


def union(a, b, parentArray, parentUtilArray, edgeIndex):

    aParent = find(a, parentArray)
    bParent = find(b, parentArray)

    if (aParent == bParent):    # a and b in the same tree
        return False

    # a tree taller than b tree (Rmb height stored as negative numbers)
    if parentArray[aParent] < parentArray[bParent]:
        # Update b tree height and connecting edge
        parentArray[bParent] = aParent

        parentUtilArray[bParent] = (aParent, edgeIndex)

        return True
    elif parentArray[aParent] > parentArray[bParent]:   # b tree taller than a tree
        # Update a tree height and connecting edge
        parentArray[aParent] = bParent

        parentUtilArray[aParent] = (bParent, edgeIndex)

        return True
    else:   # a tree and b tree same height
        parentArray[aParent] = bParent
        parentArray[bParent] = parentArray[bParent] - 1  # Update b tree height and connecting edge

        parentUtilArray[aParent] = (bParent, edgeIndex)
        parentUtilArray[bParent] = (
            parentUtilArray[bParent][0] - 1, parentUtilArray[bParent][1])

        return True


def kruskalWithSecondMst(numVertices, edges):

    edges.sort(key=lambda edge: edge[2])  # sort list of edges by weight

    parentArray = [-1 for i in range(numVertices+1)]
    
    # Special parent array that doesn't use path compression to allow for searching of cuts in the graph. Is not used for regular find operations to keep the benefits of path compression
    parentUtilArray = [(-1, None) for i in range(numVertices+1)]    

    mstEdges = []
    secondMstEdges = []
    weight = 0
    secondWeight = inf

    replacingEdge = None
    replacedEdge = None

    numEdges = 0
    i = 0
    while i < len(edges) and not (numEdges >= numVertices - 1 and secondWeight <= weight):
        if numEdges < numVertices - 1 and union(edges[i][0], edges[i][1], parentArray, parentUtilArray, i):
            mstEdges.append(edges[i])
            numEdges += 1
            weight += edges[i][2]
            secondWeight += edges[i][2]
        else:
            # Get the two possible edges that might've connected the two cuts that the current edge would connect if the other edge didn't exist
            firstCandidateEdgeIndex = findLastConnectingEdgeIndex(
                edges[i][0], parentUtilArray, parentUtilArray[edges[i][0]][1])
            firstCandidateEdgeIndex = -1 if not firstCandidateEdgeIndex else firstCandidateEdgeIndex

            secondCandidateEdgeIndex = findLastConnectingEdgeIndex(
                edges[i][1], parentUtilArray, parentUtilArray[edges[i][1]][1])
            secondCandidateEdgeIndex = - 1 if not secondCandidateEdgeIndex else secondCandidateEdgeIndex

            # Edge to be replaced is the last edge that connected the two cuts that the current edge would've connected
            replacedEdgeIndex = max(firstCandidateEdgeIndex, secondCandidateEdgeIndex)

            newSecondWeight = weight - edges[replacedEdgeIndex][2] + edges[i][2]

            if newSecondWeight < secondWeight:
                replacingEdge = edges[i]
                replacedEdge = edges[replacedEdgeIndex]
                secondWeight = newSecondWeight

        i += 1

    for edge in mstEdges:
        if edge != replacedEdge:
            secondMstEdges.append(edge)
        else:
            secondMstEdges.append(replacingEdge)

    return mstEdges, weight, secondMstEdges, secondWeight


def getArguments():
    # Get edges from input file

    # graphSpecificationFileName = sys.argv[1]
    graphSpecificationFileName = "graph.txt"
    graphSpecificationFile = open(graphSpecificationFileName, 'r')

    numVertices, numEdges = graphSpecificationFile.readline().strip("\n").split(" ")
    numVertices, numEdges = int(numVertices), int(numEdges)
    edges = [graphSpecificationFile.readline().strip('\n')
             for i in range(numEdges)]
    for i in range(len(edges)):
        edges[i] = list(map(int, edges[i].strip().split()))

    graphSpecificationFile.close()

    return numVertices, edges

numVertices, edges = getArguments()
mst1, mst1Weight, mst2, mst2Weight = kruskalWithSecondMst(numVertices, edges)
write_output(mst1, mst1Weight, mst2, mst2Weight)
