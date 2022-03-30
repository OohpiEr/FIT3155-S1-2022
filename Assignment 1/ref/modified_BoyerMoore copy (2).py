"""
FIT3155 Assignment 1 Question 1

__author__ = "Er Tian Ru"

References:
geeksforgeeks boyer moore algorithm bad character https://www.geeksforgeeks.org/boyer-moore-algorithm-for-pattern-searching/
geeksforgeeks z algorithm https://www.geeksforgeeks.org/z-algorithm-linear-time-pattern-searching-algorithm/
geeksforgeeks boyer moore algorithm good suffix https://www.geeksforgeeks.org/boyer-moore-algorithm-good-suffix-heuristic/?ref=rp
"""

import sys


def read_file(filename: str) -> str:
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


def write_output(occurrences: list) -> None:
    """
    Writes a list occurrences to a file output_modified_BoyerMoore.txt

    :param occurrences: a list of numbers
    """
    # Open output file with correct name
    outputFile = open('output_modified_BoyerMoore.txt', 'w')
    # Iterate through the occurrence list and write results to an output file
    if occurrences:
        outputFile.write(str(occurrences[0]+1))
        for i in range(1, len(occurrences)):
            outputFile.write('\n')
            outputFile.write(str(occurrences[i]+1))
    # Remember to close the file
    outputFile.close()


def bad_character(pattern: str) -> list:
    """
    Bad Character Rule for Boyer Moore algorithm.


    :param pattern: the pattern string 

    :returns: the bad character array R
    """
    NO_OF_CHARS = 256

    # initialize 2D matrix
    R = [[-1 for _ in range(len(pattern))] for _ in range(NO_OF_CHARS)]

    # fill R matrix
    for i in range(len(pattern) - 1, -1, -1):
        char_index = ord(pattern[i])
        if R[char_index][i] == -1:
            R[char_index][i] = i
            j = 1
            while (i+j < len(pattern)) and (R[char_index][i+j] == -1):
                R[char_index][i+j] = i
                j += 1

    return R


def good_suffix(pattern: str) -> list:
    """
    Good Suffix Rule for Boyer Moore algorithm.


    :param pattern: the pattern string 

    :returns: the good suffix array 
    """
    m = len(pattern)

    # get reversed z array
    reversed_z_arr = get_reversed_z_arr(pattern)

    # initialize good suffix array
    good_suffix_arr = [[] for _ in range(0, m + 1)]

    # fill in good suffix array
    for p in range(m-2, -1, -1):
        j = m - reversed_z_arr[p]
        good_suffix_arr[j].append(p + 1)

    for list_i in good_suffix_arr:
        if not list_i:
            list_i.append(0)

    return good_suffix_arr


def z_algo(string: str) -> list:
    """
    z-algorithm for pattern matching

    :param string: a string 

    :returns: the z array 
    """
    assert len(string) != 0

    # initialize z array
    z_arr = [0 for _ in range(len(string))]

    # length of string stored in first cell
    z_arr[0] = n = len(string)

    l, r, k = 0, 0, 0
    for i in range(1, n):

        # CASE 1: i>R (i outside box or no box)
        # calculate Z[i] naively
        if i > r:
            l, r = i, i

            # compare
            while r < n and string[r - l] == string[r]:
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
                while r < n and string[r - l] == string[r]:
                    r += 1
                z_arr[i] = r - l
                r -= 1
    return z_arr


def get_reversed_z_arr(string: str) -> list:
    """
    Returns a reversed z array for the good suffix rule.

    :param string: the pattern string to preprocess for good suffix

    :returns: a reversed z array.

    :complexity: O(3m) where m is the length of the string
    """
    return z_algo(string[::-1])[::-1]


def matched_prefix(pattern: str) -> list:
    """
    Matched Prefix condition for the good suffix rule for Boyer Moore algorithm.

    :param pattern: the pattern string 

    :returns: matched prefix array
    """
    matched_prefix_arr = z_algo(pattern)

    for i in range(len(matched_prefix_arr) - 1, -1, -1):
        if (i + 1 <= len(pattern) - 1) and (matched_prefix_arr[i] + i != len(pattern)):
            matched_prefix_arr[i] = matched_prefix_arr[i+1]

    return matched_prefix_arr


def boyer_moore(text: str, pattern: str) -> None:
    """
    Modified Boyer Moore string matching algorithm. Finds each position where pattern
    matches the text and writes it into a file output_modified_BoyerMoore.txt.

    :param text: the string of text to search through
    :param pattern: the pattern string to match with the text
    """

    # initialize variables
    n, m = len(text), len(pattern)
    text_pointer, output = 0, []

    # if either text or pat is empty
    if len(text) == 0 or len(pattern) == 0:
        write_output(output)
        return

    # preprocess pattern
    matched_prefix_arr = matched_prefix(pattern)
    good_suffix_arr = good_suffix(pattern)
    bad_char_arr = bad_character(pattern)

    # Starting with pat[1...m]vs.txt[1...m], in each iteration, scan `right-to-left'
    while (text_pointer <= n - m):
        pat_pointer = m - 1

        # When characters are matching
        # shift + pat_pointer = text_pointer
        while pat_pointer >= 0 and pattern[pat_pointer] == text[text_pointer + pat_pointer]:
            pat_pointer -= 1

        # if all of pattern match text
        # then pat_pointer will become -1 after the above loop
        if pat_pointer < 0:
            output.append(text_pointer)

            # shift by m-matched_prefix_arr[2]
            # TODO: galil's optimisation
            if len(matched_prefix_arr) >= 2:
                text_pointer += (m - matched_prefix_arr[1])
            else:
                text_pointer += 1

        # if mismatch at pat_pointer
        else:
            shift_bad_char = 0
            shift_good_char = 0

            # bad-character rule
            if text_pointer + pat_pointer + 1 < m:
                shift_bad_char = pat_pointer - \
                    bad_char_arr[ord(
                        text[text_pointer + pat_pointer])][pat_pointer]

            # good suffix rule
            # TODO: galil's optimisation
            if good_suffix_arr[pat_pointer + 1][0] > 0:
                shift_good_char = m - good_suffix_arr[pat_pointer + 1][0]
                if pattern[pat_pointer - shift_good_char] != text[text_pointer + pat_pointer]:
                    # X != P --> look for (X)AN
                    for i in range(len(good_suffix_arr[pat_pointer + 1]) - 1):
                        shift = good_suffix_arr[pat_pointer + 1][i]
                        if pattern[pat_pointer - shift] == text[text_pointer + pat_pointer]:
                            shift_good_char = shift
                    
            else:
                # matched prefix
                # TODO: galil's optimisation
                if len(matched_prefix_arr) > pat_pointer + 1:
                    shift_good_char = m - matched_prefix_arr[pat_pointer + 1]
                else:
                    shift_good_char = 1

            # Shift pat to the right by max(shift_bad_char, shift_good_char)
            text_pointer += max(shift_bad_char, shift_good_char)

    write_output(output)


if __name__ == "__main__":
    text_file_name = sys.argv[1]   # text_file_name = "text.txt"
    pat_file_name = sys.argv[2]   # pat_file_name = "pattern.txt"

    boyer_moore(read_file(text_file_name), read_file(pat_file_name))
