"""
FIT3155 Assignment 3 Question 2

__author__ = "Er Tian Ru"

References:
"""
import heapq
import sys
import heapq


class HuffmanFreqTuple():
    def __init__(self, freq, chars):
        self.freq = freq
        self.chars = chars

    def __lt__(self, other):
        if self.freq == other.freq:
            return len(self.chars) < len(other.chars)
        else:
            return self.freq < other.freq

    def __gt__(self, other):
        if self.freq == other.freq:
            return len(self.chars) > len(other.chars)
        else:
            return self.freq > other.freq


def read_file(filename):
    """
    Reads a file "filename"
    """
    # Open and read the text file
    txtFile = open(filename, 'r', encoding="utf-8")
    txt = txtFile.read()
    # Remember to close the file
    txtFile.close()
    # Return the pattern and text
    return txt


def write_output(filename, bytes):
    outputFile = open('{}.bin'.format(filename), 'wb')

    outputFile.write(bytes)

    # Remember to close the file
    outputFile.close()
    # print("{0:b}".format(int.from_bytes(bytes, 'big')))


def run_myzip():
    # python myzip.py <filename> <window> <lookahead>
    filename = sys.argv[1]
    window = sys.argv[2]
    lookahead = sys.argv[3]
    bytes = encode(filename, read_file(filename), int(window), int(lookahead))
    write_output(filename, bytes)


def xor(a, b):
    return (a & ~b) or (~a & b)


def encode_elias(n, prefix=0):
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
        if output_bit_len != 1:
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
    encoding_arr = [0] * 256
    freq_arr = []  # contains list of (frequency, [ord(char)])
    for char in txt:
        encoding_arr[ord(char)] += 1
    for i in range(len(encoding_arr)):
        if encoding_arr[i] != 0:
            freq_arr.append(HuffmanFreqTuple(encoding_arr[i], [i]))
            unique_char_count += 1
        encoding_arr[i] = []

    # heapify freq_arr
    heapq.heapify(freq_arr)
    while freq_arr:
        serve1 = heapq.heappop(freq_arr)
        # print("serve1 {} {}".format(serve1.freq, [chr(c) for c in serve1.chars]))
        for i in serve1.chars:
            encoding_arr[i].append(0)

        if freq_arr:
            serve2 = heapq.heappop(freq_arr)
            # print("serve2 {} {}".format(serve2.freq, [chr(c) for c in serve2.chars]))
            for i in serve2.chars:
                encoding_arr[i].append(1)

            heapq.heappush(freq_arr, HuffmanFreqTuple(
                serve1.freq + serve2.freq, serve1.chars + serve2.chars))

    return encoding_arr, unique_char_count


def encode_huffman(text, prefix=0):
    encoding_arr, unique_char_count = huffman(text)
    prefix = encode_elias(unique_char_count, prefix)

    for i in range(len(encoding_arr)):
        if encoding_arr[i]:
            prefix = (prefix << 8) | i
            prefix = encode_elias(len(encoding_arr[i]), prefix)
            for j in range(len(encoding_arr[i])-1, -1, -1):
                prefix = (prefix << 1) | encoding_arr[i][j]
    return prefix, encoding_arr


def z_algo(string, window_p, lookahead_p, lookahead_size):
    assert len(string) != 0

    # initialize z array
    len_string = (lookahead_p - window_p) + (lookahead_size * 2)
    z_arr = [0] * len_string

    # length of string stored in first cell
    z_arr[0] = n = len_string

    ref_arr = [0] * len_string
    for i in range(lookahead_size):
        ref_arr[i] = lookahead_p + i
    for i in range(lookahead_size, lookahead_size + (lookahead_p - window_p)):
        ref_arr[i] = window_p + i - lookahead_size
    for i in range(lookahead_size + (lookahead_p - window_p), len_string):
        ref_arr[i] = lookahead_p + i - \
            (lookahead_size + (lookahead_p - window_p))

    l, r, k = 0, 0, 0
    for i in range(1, n):

        # CASE 1: i>R (i outside box or no box)
        # calculate Z[i] naively
        if i > r:
            l, r = i, i

            # compare
            while r < n and string[ref_arr[r - l]] == string[ref_arr[r]]:
                r += 1
            z_arr[i] = r - l
            r -= 1

        # CASE 2: i<=R (i inside box)
        else:
            # k = i-L so k corresponds to number which
            # matches in [L,R] interval.
            k = i - l

            # CASE 2a: Z[k] < remaining
            # Z[i] equal to Z[k]
            if z_arr[k] < r - i + 1:
                z_arr[i] = z_arr[k]

            # CASE 2b: z[k] > remaining
            # z[i] = remaining
            elif z_arr[k] > r - i + 1:
                z_arr[i] = r - i + 1

            # CASE 2c: Z[k] = remaining
            # compare string[r + 1 ... r + n]
            elif z_arr[k] == r - i + 1:
                l = i
                while r < n and string[ref_arr[r - l]] == string[ref_arr[r]]:
                    r += 1
                z_arr[i] = r - l
                r -= 1
    return z_arr, ref_arr


def lz77(text, window, lookahead):
    lookahead_p = 0  # separator
    window_p = 0
    output = []
    while lookahead_p < len(text):
        window_p = max(0, lookahead_p - window)
        lookahead_size = min(lookahead, len(text) - lookahead_p)
        window_size = lookahead_p - window_p
        z_arr, ref_arr = z_algo(text, window_p, lookahead_p, lookahead_size)
        # print(z_arr)

        match_len = 0
        match_i = -1
        for i in range(lookahead_size + window_size-1, lookahead_size-1, -1):
            if z_arr[i] > match_len and z_arr[i] <= lookahead_size:
                match_len = z_arr[i]
                match_i = i

        if match_len > 0:
            try:
                output.append(
                    (lookahead_p - ref_arr[match_i], match_len, text[lookahead_p + match_len]))
            except IndexError:
                if match_len-1 == 0:
                    output.append((0, 0, text[-1]))
                else:
                    output.append(
                        (lookahead_p - ref_arr[match_i], match_len-1, text[-1]))

            lookahead_p = lookahead_p + match_len + 1
        else:
            output.append((0, 0, text[lookahead_p]))
            lookahead_p += 1
    # print(output)
    return output


def encode_lz77(text, huff_encoding_arr, window, lookahead):
    tuples = lz77(text, window, lookahead)
    bits = 0
    for tup in tuples:
        bits = encode_elias(tup[0], bits)
        bits = encode_elias(tup[1], bits)

        for j in range(len(huff_encoding_arr[ord(tup[2])])-1, -1, -1):
            bits = (bits << 1) | huff_encoding_arr[ord(tup[2])][j]
    # print(bin(bits))
    return bits


def encode_8bit_ascii(filename, prefix=0):
    for char in filename:
        prefix = (prefix << 8) | ord(char)
    return prefix


def header(filename, text):
    # encoding of the length of input filename
    header_bits = encode_elias(len(filename), 1)  # 1st bit not flipped yet

    # encoding of the filename
    header_bits = encode_8bit_ascii(filename, header_bits)

    # encoding of the size
    header_bits = encode_elias(len(text), header_bits)

    # encoding constructed set of Huffman codewords
    header_bits, huff_encoding_arr = encode_huffman(text, header_bits)

    return header_bits, huff_encoding_arr


def encode(filename, text, window, lookahead):
    header_bits, huff_encoding_arr = header(filename, text)
    data_bits = encode_lz77(text, huff_encoding_arr, window, lookahead)
    concat_bits = header_bits << int.bit_length(data_bits) | data_bits

    # convert concatenated_bits to bytes
    while int.bit_length(concat_bits) % 8 != 1:
        concat_bits = concat_bits << 1

    concat_bits = concat_bits ^ (1 << (int.bit_length(concat_bits) - 1))
    bytes = concat_bits.to_bytes((int.bit_length(concat_bits) + 7) // 8, 'big')

    return bytes


def run_test_myzip(filename, window, lookahead):
    # python myzip.py <filename> <window> <lookahead>
    bytes = encode(filename, read_file(filename), int(window), int(lookahead))
    write_output(filename, bytes)


if __name__ == "__main__":
    run_myzip()
    # run_test_myzip("large_random.txt", 244, 455)
