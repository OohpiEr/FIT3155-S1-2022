"""
FIT3155 Assignment 3 Question 2

__author__ = "Er Tian Ru"
student_id = "30881668"

References:
binary tree from FIT2085-S1-2021 Week 11 Workshop by Brendon Taylor
"""
import sys


class HuffmanBinaryTreeNode():
    """Class for binary tree nodes used for Huffman Decoding
    """
    def __init__(self) -> None:
        """
        Initialise the node with an optional item

        and sets the left and right pointers to None
        :complexity: O(1)
        """
        self.char = None
        self.left = None
        self.right = None

    def __str__(self) -> str:
        """
        Returns the string representation of a node

        :complexity: O(N) where N is the size of the item
        """
        return str(self.item)

    def is_leaf(self):
        """Returns True if node is a leaf

        :return: true if node is a leaf
        """
        return True if (not self.left and not self.right) else False


class HuffmanBinaryTree():
    """Class for Huffman Binary Tree
    """
    def __init__(self) -> None:
        """
        Initialise an empty Binary Tree

        :complexity: O(1)
        """
        self.root = HuffmanBinaryTreeNode()

    def is_empty(self) -> bool:
        """
        Checks to see if the tree is empty

        :complexity: O(1)
        """
        return self.root is None

    def insert_char(self, char, huffman_codeword):
        """Inserts a character to the tree

        :param char: character to insert
        :param huffman_codeword: huffman codeword of the character
        """
        curr = self.root
        leaf = None
        for i in range(len(huffman_codeword)):
            if huffman_codeword[i] == 0:
                if curr.left == None:
                    curr.left = HuffmanBinaryTreeNode()
                curr = curr.left
            elif huffman_codeword[i] == 1:
                if curr.right == None:
                    curr.right = HuffmanBinaryTreeNode()
                curr = curr.right
            # leaf = curr
        if curr:
            curr.char = char


def read_file(filename):
    """Reads a file "filename"

    :param filename: filename
    :return: file contents as bytes
    """
    # Open and read the text file
    txtFile = open(filename, 'rb')
    bytes = txtFile.read()
    # Remember to close the file
    txtFile.close()
    # Return the pattern and text
    return bytes


def write_output(filename, data):
    """Write data to a file "filename""

    :param filename: file to be written to
    :param data: data to be written
    """
    outputFile = open(filename, 'w', encoding="utf-8")

    outputFile.write(data)

    # Remember to close the file
    outputFile.close()
    # print("{0:b}".format(int.from_bytes(bytes, 'big')))


def run_myunzip(filename=None):
    """Runs myunzip

    :param filename: name of the file to be decoded, defaults to sys.argv[1]
    """
    # python myunzip.py <filename>.bin
    if not filename:
        filename = sys.argv[1]

    bytes = read_file(filename)
    decoded_filename, filedata = decode(bytes)
    write_output(decoded_filename, filedata)


def bits_generator(bytes):
    """Generator function for iterating through bits in bytes   

    :param bytes: bytes to be iterated through
    :yield: current bit
    """
    for num in bytes:
        # print(bin(num))
        pad_zeros = 8 - int.bit_length(num)
        while pad_zeros > 0:
            yield 0
            pad_zeros -= 1

        if num != 0:
            bit = 1 << int.bit_length(num) - 1
            while bit > 0:
                if num & bit:
                    # current bit = 1
                    yield 1
                else:
                    # current bit = 0
                    yield 0
                bit >>= 1


def decode_elias(bits_generator):
    """Algorithm to decode elias omega encoding

    :param bits_generator: bits generator function
    :return: decoded number
    """
    n = 1
    while n > 0:
        # check first bit
        bit = next(bits_generator)
        if bit == 0:
            # flip first bit
            bit = 1
            # look at next n bits
            for i in range(n - 1):
                bit = (bit << 1) | next(bits_generator)
            # plus 1
            n = bit + 1
        else:
            # length
            for i in range(n - 1):
                bit = (bit << 1) | next(bits_generator)
            return bit - 1


def decode_8bit_ascii(bits_generator, len_string):
    """Algorithm to decode string encoded in 8-bit ASCII

    :param bits_generator: bits generator function
    :param len_string: length of string
    :return: decoded string
    """
    string_arr = []
    i = 0
    while i < len_string:
        bits = 0
        for _ in range(8):
            bits = (bits << 1) | next(bits_generator)
        string_arr.append(chr(bits))
        i += 1

    return "".join(string_arr)


def get_huffman_binary_tree(bits_generator):
    """Returns a huffman binary tree.

    :param bits_generator: bits generator function
    :return: huffman binary tree.
    """
    huff_binary_tree = HuffmanBinaryTree()
    num_unique_char = decode_elias(bits_generator)
    for i in range(num_unique_char):
        # statement of char
        bits = 0
        for _ in range(8):
            bits = (bits << 1) | next(bits_generator)
        char = chr(bits)

        # length of huffman codeword
        len_huff_code = decode_elias(bits_generator)

        # huffman codeword
        huff_code = []
        for _ in range(len_huff_code):
            huff_code.append(next(bits_generator))
        huff_binary_tree.insert_char(char, huff_code)
    return huff_binary_tree


def decode_huffman(bits_generator, huffman_binary_tree):
    """Algorithm to decode a Huffman codeword

    :param bits_generator: bits generator function
    :param huffman_binary_tree: huffman binary tree.
    :return: decoded character
    """
    curr = huffman_binary_tree.root
    while not curr.is_leaf():
        bit = next(bits_generator)
        if bit == 0:
            curr = curr.left
        elif bit == 1:
            curr = curr.right
    return curr.char


def decode_lz77(bits_generator, huffman_binary_tree, len_filesize):
    """Algorithm to decode lz77 encoded bytes

    :param bits_generator: bits generator function
    :param huffman_binary_tree: huffman binary tree.
    :param len_filesize: length of files to be decoded
    :return: Decoded bytes
    """
    filedata = []
    i = 0
    while i < len_filesize:
        offset = decode_elias(bits_generator)
        length = decode_elias(bits_generator)
        char = decode_huffman(bits_generator, huffman_binary_tree)

        # print('{} {} {}'.format(offset, length, char))

        if offset == 0:
            filedata.append(char)
        else:
            for _ in range(length):
                filedata.append(filedata[len(filedata) - offset])
            filedata.append(char)
            # offset -= 1
        i += length + 1

    return ''.join(filedata)


def decode(bytes):
    """Decodes a file encoded with LZ77, elias omega and huffman

    :param bytes: bytes of the file to be decoded
    :return: filename of the decoded file and data of decoded file
    """
    bits_gen = bits_generator(bytes)
    len_filename = decode_elias(bits_gen)
    filename = decode_8bit_ascii(bits_gen, len_filename)
    len_filesize = decode_elias(bits_gen)
    huff_binary_tree = get_huffman_binary_tree(bits_gen)
    filedata_str = decode_lz77(bits_gen, huff_binary_tree, len_filesize)
    return filename, filedata_str


if __name__ == "__main__":
    run_myunzip()
