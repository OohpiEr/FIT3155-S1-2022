import itertools
import random
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


def findLCALargestEdgeIndex(v, u, parentUtilArray):   
    # Finds the lowest common ancestor of v and u, then finds the largest of the edges that last connected v and u's
    # respective trees to this ancestor's tree

    # Get the last trees that each node was a parent of before that tree became a child of another tree
    vTree = parentUtilArray[v]
    uTree = parentUtilArray[u]
    
    if uTree[2] > vTree[2]: # If u's tree's height is less than v's tree's height
        uConnectingEdgeIndex = uTree[1]  # The edge that connected this tree to it's parent tree
        uNextTree = parentUtilArray[uTree[0]]   # This tree's parent tree
        if uNextTree == vTree:  # This tree's parent tree is v's tree
            return uConnectingEdgeIndex
        else:   # The two trees are still disconnected. u goes up 1 tree and checks again
            return findLCALargestEdgeIndex(v, uTree[0], parentUtilArray)
    
    elif vTree[2] > uTree[2]:   # If v's tree's height is less than u's tree's height
        vConnectingEdgeIndex = vTree[1]  # The edge that connected this tree to it's parent tree
        vNextTree = parentUtilArray[vTree[0]]   # This tree's parent tree
        if vNextTree == uTree:  # This tree's parent tree is v's tree
            return vConnectingEdgeIndex
        else:   # The two trees are still disconnected. v goes up 1 tree and checks again
            return findLCALargestEdgeIndex(vTree[0], u, parentUtilArray)
        
    else:   # Both tree's heights are the same. 
        vNextTree = parentUtilArray[vTree[0]]   # Look up one tree from v's tree
        uNextTree = parentUtilArray[uTree[0]]   # Look up one tree from u's tree
        
        uConnectingEdgeIndex = uTree[1]
        vConnectingEdgeIndex = vTree[1]
        
        if uNextTree == vTree:  # v's tree is u's tree's parent tree
            return uConnectingEdgeIndex
        
        elif vNextTree == uTree:    # u's tree is v's tree's parent tree
            return vConnectingEdgeIndex
        
        elif uNextTree == vNextTree:   # Neither are each other's parent trees, but they share the same parent tree
            return max(uConnectingEdgeIndex, vConnectingEdgeIndex)
        
        else:   # The two trees are still disconnected. Both v and u go up by 1 tree and check again
            return findLCALargestEdgeIndex(vTree[0], uTree[0], parentUtilArray)    


def union(a, b, parentArray, parentUtilArray, edgeIndex):

    aParent = find(a, parentArray)
    bParent = find(b, parentArray)

    if (aParent == bParent):    # a and b in the same tree
        return False

    # a tree taller than b tree (Rmb height stored as negative numbers)
    if parentArray[aParent] < parentArray[bParent]:
        # Update b tree height and connecting edge
        parentArray[bParent] = aParent

        parentUtilArray[bParent] = (aParent, edgeIndex, parentUtilArray[bParent][0])

        return True
    elif parentArray[aParent] > parentArray[bParent]:   # b tree taller than a tree
        # Update a tree height and connecting edge
        parentArray[aParent] = bParent

        parentUtilArray[aParent] = (bParent, edgeIndex, parentUtilArray[aParent][0])

        return True
    else:   # a tree and b tree same height
        parentArray[aParent] = bParent
        parentArray[bParent] = parentArray[bParent] - 1  # Update b tree height and connecting edge

        parentUtilArray[aParent] = (bParent, edgeIndex, parentUtilArray[aParent][0])
        parentUtilArray[bParent] = (parentUtilArray[bParent][0] - 1, parentUtilArray[bParent][1], parentUtilArray[bParent][0] - 1)

        return True


def kruskalWithSecondMst(numVertices, edges):

    edges.sort(key=lambda edge: edge[2])  # sort list of edges by weight

    parentArray = [-1 for i in range(numVertices+1)]
    
    # Special parent array that doesn't use path compression to allow for searching of cuts in the graph. Is not used for regular find operations to keep the benefits of path compression
    parentUtilArray = [(-1, None, -1) for i in range(numVertices+1)]    
    # (Parent node without path compression, Edge that connected it to parent node, Height when it was a parent node]
    
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

            # Find the smallest tree that joined the two nodes. Then find the edge that created the tree
            replacedEdgeIndex = findLCALargestEdgeIndex(edges[i][0], edges[i][1], parentUtilArray)

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

    graphSpecificationFileName = sys.argv[1]
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