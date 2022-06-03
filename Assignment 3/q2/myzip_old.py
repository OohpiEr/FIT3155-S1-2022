"""
FIT3155 Assignment 3 Question 2

__author__ = "Er Tian Ru"

References:
"""
from enum import unique
import heapq
import sys


def read_file(filename):
    """
    Reads a file "filename"
    """
    # Open and read the text file
    txtFile = open(filename, 'r')
    txt = txtFile.read()
    # Remember to close the file
    txtFile.close()
    # Return the pattern and text
    return txt


def write_output(primes, n):
    # Open output file with correct name
    outputFile = open('output_threeprimes.txt', 'w')
    # Iterate through the occurrence list and write results to an output file
    try:
        if primes:
            outputFile.write("{} {} {}".format(primes[2], primes[1], primes[0]))
    except IndexError:
        print("problem_n" + n)
    # Remember to close the file
    outputFile.close()


def run_myzip():
        x = sys.argv[1]

def xor(a, b):
    return (a & ~b) or (~a & b)

def encode_elias(n, prefix = 0):
    # + 1 to represent 0
    output = n + 1
    output_bit_len = int.bit_length(output)
    curr_bit_len = output_bit_len - 1
    flip_pointer = 0

    output = (curr_bit_len << output_bit_len) | output
    curr_bit_len = int.bit_length(curr_bit_len)
    output_bit_len = int.bit_length(output)
    curr_bit_len = curr_bit_len - 1
    while curr_bit_len > 0:
        flip_pointer = int.bit_length(output)-1
        output = (curr_bit_len << output_bit_len) | output
        curr_bit_len = int.bit_length(curr_bit_len)
        output_bit_len = int.bit_length(output)
        curr_bit_len = curr_bit_len - 1
        output = xor(output, 1 << flip_pointer)
    
    if prefix != 0:
        output_bit_len = int.bit_length(output)
        output = (prefix << output_bit_len) | output
        output = output ^ (1 << output_bit_len-1)
    return output
    # print(bin(output))
    # bytes = output.to_bytes(2, byteorder="big")
    # print(bin(int.from_bytes(bytes, byteorder="big")))
    # byte_arr = bytearray(bytes)
    # print(byte_arr)

def huffman(txt):
    unique_char_count = 0
    # initialize frequency/probability array 
    encoding_arr = [0] * 255
    freq_arr = [] # contains list of (frequency, [ord(char)])
    for char in txt:
        encoding_arr[ord(char)] += 1
    for i in range(len(encoding_arr)):
        if encoding_arr[i] != 0:
            freq_arr.append((encoding_arr[i], [i]))
            unique_char_count += 1
        encoding_arr[i] = []
    
    # heapify freq_arr
    heapq.heapify(freq_arr)
    print(freq_arr)
    while freq_arr:
        serve1 = heapq.heappop(freq_arr)
        serve2 = heapq.heappop(freq_arr)

        for i in serve1[1]:
            encoding_arr[i].append(0)
        for i in serve2[1]:
            encoding_arr[i].append(1)
        
        if freq_arr:
            heapq.heappush(freq_arr, (serve1[0] + serve2[0], serve1[1] + serve2[1]))
        print(freq_arr)
    print([(chr(i), encoding_arr[i]) for i in range(len(encoding_arr)) if encoding_arr[i]])
    return encoding_arr, unique_char_count

def encode_huffman(text, prefix = 0):
    encoding_arr, unique_char_count = huffman(text)
    prefix = encode_elias(unique_char_count, prefix)

    for i in range(len(encoding_arr)):
        if encoding_arr[i]: 
            prefix = (prefix << 8) | i
            prefix = encode_elias(len(encoding_arr[i]), prefix)
            for j in range(len(encoding_arr[i])-1, -1, -1):
                prefix = (prefix << 1) | encoding_arr[i][j]
    return prefix

def encode_8bit_ascii(filename, prefix = 0):
    for char in filename:
        prefix = (prefix << 8) | ord(char)
    return prefix

def header():
    filename = "x.asc"
    text = "aacaacabcaba"
    
    # encoding of the length of input filename
    header = encode_elias(len(filename)) # 1st bit not flipped yet

    # encoding of the filename
    header = encode_8bit_ascii(filename, header)

    # encoding of the size
    header = encode_elias(len(text), header)

    # encoding constructed set of Huffman codewords
    header = encode_huffman(text, header)
    
    print(bin(header))
    # byte_arr = bytearray(filename,'utf-8')
    # byte_arr_int = int.from_bytes(byte_arr, 'big')
    # print("{0:b}".format(binaryStream))
    
    # header = (len_filename_elias << output_bit_len) | output

if __name__ == "__main__":
    # elias(100)
    # txt = read_file("inputs\sample1.txt")
    # huffman("A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED")
    # huffman("aacaacabcaba")
    header()
