import sys

class Node:

    def __init__(self):
        self.edges = [None for i in range(128)]
        self.link = None
        self.isLeaf = True
        self.suffixIds = []

    def addEdge(self, texts, edge):
        index = ord(texts[edge.textId][edge.start])
        self.edges[index] = edge
        self.isLeaf = False

    def getEdge(self, char):
        return self.edges[ord(char)]

    def getEdges(self):
        output = []
        for i in range(len(self.edges)):
            if self.edges[i]:
                output += chr(i)
        return output


class Edge:

    def __init__(self, textId, start, end):
        self.textId = textId
        self.start = start
        self.end = end
        self.tail = Node()

    def addTail(self, node):
        self.tail = node
        
    def getChars(self, texts):
        return texts[self.textId][self.start:self.end.value+1]


class End:

    def __init__(self, value):
        self.value = value

    def increment(self):
        self.value += 1


class GeneralisedSuffixTree:

    def __init__(self, texts):
        self.texts = []
        self.root = Node()
        for text in texts:
            self.addText(text+"$")

    def addText(self, text):
        textId = len(self.texts)
        self.texts.append(text)
        i = End(-1)
        j = 0
        activeNode = self.root
        activeNode.link = self.root
        activeEdge = None
        activeLength = None
        referenceEdge = None
        
        while i.value < len(text) - 1:
            i.increment()
            while j < i.value:  # Continue Show Stopper Phase
                if activeNode == self.root:
                    activeLength = i.value - j
                    activeEdge = activeNode.edges[ord(text[j])]

                while activeLength + activeEdge.start - 1 > activeEdge.end.value:  # Skip Count
                    activeNode = activeEdge.tail
                    activeLength -= (activeEdge.end.value - activeEdge.start + 1)
                    if self.texts[referenceEdge.textId][referenceEdge.end.value] == '$':    # We did not create a new node, so the reference edge's end value is one more than normal
                        activeEdge = activeNode.edges[ord(self.texts[referenceEdge.textId][referenceEdge.end.value - activeLength])]
                    else:
                        activeEdge = activeNode.edges[ord(self.texts[referenceEdge.textId][referenceEdge.end.value - activeLength + 1])]

                if activeLength == 0:   # Check active node for character at i
                    ichar = text[i.value]
                    if activeNode.edges[ord(ichar)]:    # Character found. Start new phase. Continue Show Stopper
                        previousNode = None
                        activeEdge = activeNode.edges[ord(ichar)]
                        if ichar != '$':
                            i.increment()
                            activeLength = 1
                        else:   # End of this text. Insert suffix ids and go home
                            activeEdge.tail.suffixIds.append((textId, j))
                            activeNode = activeNode.link
                            referenceEdge = activeEdge
                            activeLength = 0
                            j += 1
                    else:   # Character (Edge) not found. Create new edge
                        newEdge = Edge(textId, i.value, i)
                        newEdge.tail.suffixIds.append((textId, j))
                        activeNode.addEdge(self.texts, newEdge)
                        activeNode = activeNode.link
                        referenceEdge = activeEdge
                        activeLength = 0
                        j += 1

                elif activeLength + activeEdge.start - 1 == activeEdge.end.value:   # We hit a branch. Need to change active Node and consider multiple options
                    ichar = text[i.value]
                    activeNode = activeEdge.tail
                    if activeNode.edges[ord(ichar)]:    # Character found. Start new phase. Continue Show Stopper
                        previousNode = None
                        activeEdge = activeNode.edges[ord(ichar)]
                        if ichar != '$':
                            i.increment()
                            activeLength = 1
                        else:   # End of this text. Insert suffix ids and go home
                            activeEdge.tail.suffixIds.append((textId, j))
                            activeNode = activeNode.link
                            referenceEdge = activeEdge
                            activeLength = 0
                            j += 1
                    else:   # Character (Edge) not found. Create new edge
                        newEdge = Edge(textId, i.value, i)
                        newEdge.tail.suffixIds.append((textId, j))
                        activeNode.addEdge(self.texts, newEdge)
                        activeNode = activeNode.link
                        referenceEdge = activeEdge
                        activeLength = 0
                        j += 1      

                elif text[i.value] == self.texts[activeEdge.textId][activeEdge.start + activeLength]:    # Character exists (Case 3). Start new phase. Continue Show Stopper
                    previousNode = None
                    if text[i.value] != '$':
                        i.increment()
                        activeLength += 1
                    else:   # End of this text. Insert suffix ids and go home
                        activeEdge.tail.suffixIds.append((textId, j))
                        referenceEdge = activeEdge
                        activeNode = activeNode.link
                        activeEdge = activeNode.edges[ord(self.texts[activeEdge.textId][activeEdge.start])]
                        j += 1

                else:   # Character doesn't exist (Case 2). Perform branch

                    # Creating intermediate node and adding new edges
                    newNode = Node()

                    # Creating edge with old suffix
                    newEdge = Edge(activeEdge.textId, activeEdge.start + activeLength, activeEdge.end)
                    newEdge.tail = activeEdge.tail
                    newNode.addEdge(self.texts, newEdge)

                    # Updating active edge
                    activeEdge.end = End(activeEdge.start + activeLength - 1)
                    activeEdge.tail = newNode

                    # Creating edge with new suffix
                    newEdge = Edge(textId, i.value, i)
                    newEdge.tail.suffixIds.append((textId, j))
                    newNode.addEdge(self.texts, newEdge)
                    newNode.link = self.root    # Add suffix link to root

                    if previousNode:
                        previousNode.link = newNode
                    previousNode = newNode
                    referenceEdge = activeEdge
                    activeNode = activeNode.link
                    activeEdge = activeNode.edges[ord(self.texts[activeEdge.textId][activeEdge.start])]

                    j += 1

            char = text[j]
            if not activeNode.edges[ord(char)]: # Character doesn't exist. Case 2
                newEdge = Edge(textId, j, i)
                newEdge.tail.suffixIds.append((textId, j))
                activeNode.addEdge(self.texts, newEdge)
                j += 1
            else:   # Character exists (Case 3). Start Show Stopper
                previousNode = None
                activeEdge = activeNode.edges[ord(char)]
                if char == '$': # End of this text. Insert suffix ids and go home
                    activeEdge.tail.suffixIds.append((textId, j))
                    j += 1

    def getSuffixIds(self, node):
        suffixIds = []
        if node.isLeaf:
            suffixIds += node.suffixIds
        else:
            if node.edges[36]:
                suffixIds += self.getSuffixIds(node.edges[36].tail)
            for i in range(len(node.edges)):
                if node.edges[i] and i != 36:
                    suffixIds += self.getSuffixIds(node.edges[i].tail)
            
        return suffixIds

    def searchEdge(self, edge, index, pattern):
        edgePointer = 1
        patternPointer = index + edgePointer
        while edgePointer < edge.end.value - edge.start + 1 and patternPointer < len(pattern):
            if pattern[patternPointer].lower() == self.texts[edge.textId][edgePointer + edge.start].lower():
                edgePointer += 1
                patternPointer += 1
            else:
                return []   # Mismatched character found. Pattern nonexistant
        if patternPointer >= len(pattern):  # End of pattern reached. Get suffix IDs
            return self.getSuffixIds(edge.tail)
        else:
            return self.searchNode(edge.tail, patternPointer, pattern)


    def searchNode(self, node, index, pattern):
        result = []
        edge = node.getEdge(pattern[index])
        if edge:
            result = self.searchEdge(edge, index, pattern)
        if pattern[index].swapcase() != pattern[index]:
            edge = node.getEdge(pattern[index].swapcase())
            if edge:
                swapCaseResult = self.searchEdge(edge, index, pattern)
                result += swapCaseResult
        return result

    def searchPattern(self, pattern):
        suffixIds = self.searchNode(self.root, 0, pattern)
        return suffixIds
        
    def searchPatterns(self, patterns):
        output = []
        for p in range(len(patterns)):
            results = self.searchPattern(patterns[p])
            for result in results:
                output.append(str(p+1) + " " + str(result[0]+1) + " " + str(result[1]+1) + "\n")
        
        return output
    
def getArguments():
    # Get texts and patterns from input file
    
    runSpecificationFile = sys.argv[1]
    runSpecificationFile = open(runSpecificationFile, 'r')

    numTextFiles = int(runSpecificationFile.readline())
    textFiles = [runSpecificationFile.readline().strip('\n')[2:] for i in range(numTextFiles)]

    numPatternFiles = int(runSpecificationFile.readline())
    patternFiles = [runSpecificationFile.readline().strip('\n')[2:] for i in range(numPatternFiles)]

    texts = []
    for textFile in textFiles:
        file = open(textFile, 'r')
        texts.append(file.read())
        file.close()
        
    patterns = []
    for patternFile in patternFiles:
        file = open(patternFile, 'r')
        patterns.append(file.read())
        file.close()

    return (texts, patterns)

texts, patterns = getArguments()
gst = GeneralisedSuffixTree(texts)
output = gst.searchPatterns(patterns)

outputFile = open("output_gst.txt", 'w')
for line in output:
    outputFile.write(line)
    
outputFile.close()
    


