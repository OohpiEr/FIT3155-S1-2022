"""

Author: 
Student ID:
Date Created:
 
"""

import sys

class Node:

    def __init__(self):
        self.edges = [None for i in range(128)]
        self.suffix_link = None
        self.is_leaf = True
        self.suffix_ids = []
        
class End:

    def __init__(self, index):
        self.index = index

class Edge:

    def __init__(self, text_id, start, end):
        self.node = Node()
        self.text_id = text_id
        self.start = start
        self.end = end

class ActivePointer:
    
    def __init__(self):
        self.length = None
        self.edge = None
        self.node = None

class GeneralisedSuffixTree:

    def __init__(self, texts):
        self.texts = [text+'$' for text in texts]
        self.root_node = Node()

        for text_id in range(len(self.texts)):
            text = self.texts[text_id]
            i = End(0)
            j = 0
            linking_edge = None
            ap = ActivePointer()
            ap.node = self.root_node
            ap.node.suffix_link = self.root_node
            
            while i.index < len(text):
                j_chr = text[j]
                
                if not ap.node.edges[ord(j_chr)]:    # Character doesn't exist. Case 2
                    new_edge = Edge(text_id, j, i)
                    new_leaf = new_edge.node
                    new_leaf.suffix_ids.append((text_id, j))
                    ap.node.edges[ord(j_chr)] = new_edge
                    j += 1
                    i.index += 1
                else:   # Character exists (Case 3). Start Show Stopper
                    prev_node = None
                    ap.edge = ap.node.edges[ord(j_chr)]
                    i.index += 1
                    if j_chr == '$':  # End of this text. Insert suffix ids and go home
                        ap.edge.node.suffix_ids.append((text_id, j))
                        j += 1
                        
                    while j < i.index:  # Continue Show Stopper Phase
                        j_chr = text[j]
                        i_chr = text[i.index]
                        
                        if ap.node == self.root_node:
                            ap.length = i.index - j
                            ap.edge = ap.node.edges[ord(j_chr)]

                        while ap.length > ap.edge.end.index - ap.edge.start + 1:  # Do Skip Count
                            ap.node = ap.edge.node
                            skipped_length = ap.edge.end.index - ap.edge.start + 1
                            ap.length -= skipped_length
                            next_chr = self.texts[linking_edge.text_id][linking_edge.end.index - ap.length + 1]
                            ap.edge = ap.node.edges[ord(next_chr)]
                            
                        if ap.length == 0 or ap.length == ap.edge.end.index - ap.edge.start + 1:  # We hit a branch. Need to change active Node and consider multiple options
                            if not ap.length == 0:
                                ap.node = ap.edge.node
                            
                            if ap.node.edges[ord(i_chr)]:    # Character found. Start new phase. Continue Sow Stopper
                                prev_node = None
                                ap.edge = ap.node.edges[ord(i_chr)]
                                if i_chr == '$':  # End of text
                                    ap.length = 0
                                    ap.edge.node.suffix_ids.append((text_id, j))
                                    ap.node = ap.node.suffix_link
                                    ap.edge.end = End(ap.edge.end.index - 1)    # We're using suffix linking during a Case 3 instead of a Case 2. Need to pretend like we created a new node after active pointer
                                    linking_edge = ap.edge
                                    j += 1
                                else:   
                                    i.index += 1
                                    ap.length = 1
                            else:   # Character (Edge) not found. Create new edge
                                ap.length = 0
                                new_edge = Edge(text_id, i.index, i)
                                new_leaf = new_edge.node
                                new_leaf.suffix_ids.append((text_id, j))
                                ap.node.edges[ord(i_chr)] = new_edge
                                ap.node = ap.node.suffix_link
                                linking_edge = ap.edge
                                j += 1

                        elif text[i.index] != self.texts[ap.edge.text_id][ap.edge.start + ap.length]:    # Character doesn't exist (Case 2). Perform branch
                                
                            # Creating edge with new suffix
                            second_edge = Edge(text_id, i.index, i)
                            new_leaf = second_edge.node
                            new_leaf.suffix_ids.append((text_id, j))

                            # Creating edge with old suffix
                            first_edge = Edge(ap.edge.text_id, ap.edge.start + ap.length, ap.edge.end)
                            first_edge.node = ap.edge.node
                            mismatched_chr = self.texts[ap.edge.text_id][ap.edge.start + ap.length]
                            
                            # Creating intermediate node and adding new edges
                            intermediate_node = Node()

                            # Updating active edge
                            ap.edge.end = End(ap.edge.start + ap.length - 1)
                            ap.edge.node = intermediate_node                            
                            
                            intermediate_node.edges[ord(mismatched_chr)] = first_edge
                            intermediate_node.edges[ord(i_chr)] = second_edge
                            intermediate_node.is_leaf = False
                            
                            intermediate_node.suffix_link = self.root_node    # Add suffix link to root_node
                            if prev_node is not None:
                                prev_node.suffix_link = intermediate_node
                                
                            prev_node = intermediate_node
                            
                            ap.node = ap.node.suffix_link
                            linking_edge = ap.edge
                            ap.edge = ap.node.edges[ord(
                                self.texts[ap.edge.text_id][ap.edge.start])]

                            j += 1
                    
                        else:   # Character exists (Case 3). Start new phase. Continue Show Stopper

                            prev_node = None
                            if text[i.index] == '$':
                                ap.edge.node.suffix_ids.append((text_id, j))
                                ap.edge.end = End(ap.edge.end.index - 1)    # We're using suffix linking during a Case 3 instead of a Case 2. Need to pretend like we created a new node after active pointer
                                linking_edge = ap.edge
                                ap.node = ap.node.suffix_link
                                ap.edge = ap.node.edges[ord(
                                    self.texts[ap.edge.text_id][ap.edge.start])]
                                j += 1
                            else:
                                i.index += 1
                                ap.length += 1

            i.index -= 1    # i is incremented past the length of the current text. Since the leaves' end index relies on i, it has to decrement by one

    def find_leaves(self, node):
        suffix_ids = []
        if node.is_leaf:
            suffix_ids.append(node.suffix_ids)
        else:
            # Check for terminal chracter first
            if node.edges[ord('$')] is not None:
                suffix_ids += self.find_leaves(node.edges[36].node)
            for i in range(len(node.edges)):
                if node.edges[i] and i != 36:
                    suffix_ids += self.find_leaves(node.edges[i].node)

        return suffix_ids

    def find_edge(self, node, index, pattern):
        matches = []
        edge = node.edges[ord(pattern[index])]
        if edge is not None:
            matches = self.traverse_edge(edge, index, pattern)
        if pattern[index].swapcase() != pattern[index]:
            edge = node.edges[ord(pattern[index].swapcase())]
            if edge is not None:
                alt_case_match = self.traverse_edge(edge, index, pattern)
                matches += alt_case_match
        return matches

    def traverse_edge(self, edge, index, pattern):
        
        i = 1
        p = index + i

        while p < len(pattern) and i < edge.end.index - edge.start + 1:
            if pattern[p].lower() == self.texts[edge.text_id][i + edge.start].lower():
                p += 1
                i += 1
            else:
                return []   # Pattern not found

        if p < len(pattern):
            return self.find_edge(edge.node, p, pattern)    # Go to new node
        else:
            return self.find_leaves(edge.node)  # Find suffix IDs

    def pat_match(self, patterns):
        matches = ""
        for i in range(len(patterns)):
            for suffixIds in self.find_edge(self.root_node, 0, patterns[i]):
                for suffixId in suffixIds:
                    matches += "{} {} {}\n".format(i+1, suffixId[0]+1, suffixId[1]+1)

        return matches
    
def getArguments():
    # Get texts and patterns from input file
    
    runSpecificationFileName = "query.txt"

    runSpecificationFile = open(runSpecificationFileName, 'r')

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
output = gst.pat_match(patterns)

outputFile = open("output_gst.txt", 'w')
for line in output:
    outputFile.write(line)
    
outputFile.close()
    


