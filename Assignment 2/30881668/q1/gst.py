"""
FIT3155 Assignment 2 Question 1

__author__ = "Er Tian Ru"

"""

import sys

def write_output(output):
    """Prints the msts to a file output_spanning.txt"""
    outputFile = open("output_gst.txt", 'w')

    for line in output:
        outputFile.write(line)

    outputFile.close()

    
def read_run_specs_file(filename):
    """Reads a txt file that contains the run specifications

    Args:
        filename (str): name of the file to read

    Returns:
        tuple (list, list): (list of text_list, list of pat_list)
    """
    
    lines = read_file(filename)
    
    txt_files = []
    pat_files = []

    num_textfiles = int(lines[0])
    for i in range(1, num_textfiles + 1):
        line = lines[i].strip().split()
        txt_files.append(line[1])

    for i in range(num_textfiles + 2, len(lines)):
        line = lines[i].strip().split()
        pat_files.append(line[1])

    txt_list = []
    for textFile in txt_files:
        txt_list.append(read_file(textFile)[0])
    
    pat_list = []
    for patFile in pat_files:
        pat_list.append(read_file(patFile)[0])

    return txt_list, pat_list


def read_file(filename):
    """
    Reads a file "filename"
    """
    # Open and read the text file
    file = open(filename, "r")
    lines = file.readlines()

    # Remember to close the file
    file.close()
    # Return the pat and text
    return lines


class Node:
    def __init__(self):
        self.edges = [None] * 128
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
    def __init__(self, text_list):
        self.text_list = [text + '$' for text in text_list]
        self.root_node = Node()

        for text_id in range(len(self.text_list)):
            text = self.text_list[text_id]
            i = End(0)
            j = 0
            linking_edge = None
            active_p = ActivePointer()
            active_p.node = self.root_node
            active_p.node.suffix_link = self.root_node
            
            while i.index < len(text):
                j_char = text[j]
                
                # Case 2: Character doesn't exist 
                if not active_p.node.edges[ord(j_char)]:    
                    new_edge = Edge(text_id, j, i)
                    new_leaf = new_edge.node
                    new_leaf.suffix_ids.append((text_id, j))
                    active_p.node.edges[ord(j_char)] = new_edge
                    j += 1
                    i.index += 1
                
                # Case 3: Character exists --> Show Stopper
                else:   
                    prev_node = None
                    active_p.edge = active_p.node.edges[ord(j_char)]
                    i.index += 1
                    
                    # End of text
                    # insert suffix ids
                    if j_char == '$':  
                        active_p.edge.node.suffix_ids.append((text_id, j))
                        j += 1
                        
                    # Show Stopper
                    while j < i.index:  
                        j_char = text[j]
                        i_chr = text[i.index]
                        
                        if active_p.node == self.root_node:
                            active_p.length = i.index - j
                            active_p.edge = active_p.node.edges[ord(j_char)]

                        # Skip Count
                        while active_p.length > active_p.edge.end.index - active_p.edge.start + 1:  
                            active_p.node = active_p.edge.node
                            skipped_length = active_p.edge.end.index - active_p.edge.start + 1
                            active_p.length -= skipped_length
                            next_chr = self.text_list[linking_edge.text_id][linking_edge.end.index - active_p.length + 1]
                            active_p.edge = active_p.node.edges[ord(next_chr)]
                            
                        # found branch
                        if active_p.length == 0 or active_p.length == active_p.edge.end.index - active_p.edge.start + 1:  
                            # change active Node
                            if not active_p.length == 0:
                                active_p.node = active_p.edge.node
                            
                            # Character found --> new phase & continue show Stopper
                            if active_p.node.edges[ord(i_chr)]:    
                                prev_node = None
                                active_p.edge = active_p.node.edges[ord(i_chr)]
                                
                                # if end of text
                                if i_chr == '$':  
                                    active_p.length = 0
                                    active_p.edge.node.suffix_ids.append((text_id, j))
                                    active_p.node = active_p.node.suffix_link
                                    
                                    # suffix linking during a Case 3
                                    # pretend new node created after active pointer
                                    active_p.edge.end = End(active_p.edge.end.index - 1)    
                                    linking_edge = active_p.edge
                                    j += 1
                                else:   
                                    i.index += 1
                                    active_p.length = 1
                            
                            # Character not found --> Create new edge
                            else:   
                                active_p.length = 0
                                new_edge = Edge(text_id, i.index, i)
                                new_leaf = new_edge.node
                                new_leaf.suffix_ids.append((text_id, j))
                                active_p.node.edges[ord(i_chr)] = new_edge
                                active_p.node = active_p.node.suffix_link
                                linking_edge = active_p.edge
                                j += 1

                        elif text[i.index] != self.text_list[active_p.edge.text_id][active_p.edge.start + active_p.length]:    # Character doesn't exist (Case 2). Perform branch
                            # create edge w/ new suffix
                            second_edge = Edge(text_id, i.index, i)
                            new_leaf = second_edge.node
                            new_leaf.suffix_ids.append((text_id, j))

                            # create edge w/ old suffix
                            first_edge = Edge(active_p.edge.text_id, active_p.edge.start + active_p.length, active_p.edge.end)
                            first_edge.node = active_p.edge.node
                            mismatched_chr = self.text_list[active_p.edge.text_id][active_p.edge.start + active_p.length]
                            
                            # create intermediate node
                            intermediate_node = Node()

                            # update active edge
                            active_p.edge.end = End(active_p.edge.start + active_p.length - 1)
                            active_p.edge.node = intermediate_node                            
                            
                            intermediate_node.edges[ord(mismatched_chr)] = first_edge
                            intermediate_node.edges[ord(i_chr)] = second_edge
                            intermediate_node.is_leaf = False
                            
                            # Add suffix link to root_node
                            intermediate_node.suffix_link = self.root_node    
                            if prev_node is not None:
                                prev_node.suffix_link = intermediate_node
                                
                            prev_node = intermediate_node
                            
                            active_p.node = active_p.node.suffix_link
                            linking_edge = active_p.edge
                            active_p.edge = active_p.node.edges[ord(
                                self.text_list[active_p.edge.text_id][active_p.edge.start])]

                            j += 1
                    
                        # case 3: character exists --> new phase & continue Show Stopper
                        else:   
                            prev_node = None
                            if text[i.index] == '$':
                                active_p.edge.node.suffix_ids.append((text_id, j))
                                active_p.edge.end = End(active_p.edge.end.index - 1)    # We're using suffix linking during a Case 3 instead of a Case 2. Need to pretend like we created a new node after active pointer
                                linking_edge = active_p.edge
                                active_p.node = active_p.node.suffix_link
                                active_p.edge = active_p.node.edges[ord(
                                    self.text_list[active_p.edge.text_id][active_p.edge.start])]
                                j += 1
                            else:
                                i.index += 1
                                active_p.length += 1
            i.index -= 1    

    def find_leaves(self, node):
        suffix_ids = []
        if node.is_leaf:
            suffix_ids.append(node.suffix_ids)
        else:
            # Check for $
            if node.edges[ord('$')] is not None:
                suffix_ids += self.find_leaves(node.edges[36].node)
            for i in range(len(node.edges)):
                if node.edges[i] and i != 36:
                    suffix_ids += self.find_leaves(node.edges[i].node)

        return suffix_ids

    def find_edge(self, node, index, pat):
        matches = []
        edge = node.edges[ord(pat[index])]
        if edge is not None:
            matches = self.traverse_edge(edge, index, pat)
        if pat[index].swapcase() != pat[index]:
            edge = node.edges[ord(pat[index].swapcase())]
            if edge is not None:
                alt_case_match = self.traverse_edge(edge, index, pat)
                matches += alt_case_match
        return matches

    def traverse_edge(self, edge, index, pat):
        i = 1
        p = index + i

        while p < len(pat) and i < edge.end.index - edge.start + 1:
            if pat[p].lower() == self.text_list[edge.text_id][i + edge.start].lower():
                p += 1
                i += 1
            else:
                # pat not found
                return []   

        if p < len(pat):
            # Go to new node
            return self.find_edge(edge.node, p, pat)    
        else:
            # Find suffix IDs
            return self.find_leaves(edge.node)

    def pat_match(self, pat_list):
        """Pattern matching using gst

        Args:
            pat_list (list): list of patterns

        Returns:
            list: a list of matches
        """
        matches = []
        for i in range(len(pat_list)):
            for suffixIds in self.find_edge(self.root_node, 0, pat_list[i]):
                for suffixId in suffixIds:
                    matches.append( "{} {} {}\n".format(i + 1, suffixId[0] + 1, suffixId[1] + 1))

        return matches
    


if __name__ == "__main__":
    filename = sys.argv[1]
    text_list, pat_list = read_run_specs_file(filename)
    gst = GeneralisedSuffixTree(text_list)
    matches = gst.pat_match(pat_list)
    write_output(matches)

    


