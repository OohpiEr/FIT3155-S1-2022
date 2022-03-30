"""
FIT3155 Assignment 1 Question 2

__author__ = "Er Tian Ru"

References:
geeksforgeeks z algorithm https://www.geeksforgeeks.org/z-algorithm-linear-time-pattern-searching-algorithm/
geeksforgeeks edit distance https://www.geeksforgeeks.org/edit-distance-dp-5/
"""
# %%
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
    Writes a list occurrences to a file output_hd1_patmatch.txt

    :param occurrences: a list of tuples where the first cell contains the position_in_txt
                        and the second cell contains the hamming_distance
    """
    # Open output file with correct name
    outputFile = open('output_hd1_patmatch.txt', 'w')
    # Iterate through the occurrence list and write results to an output file
    if occurrences:
        outputFile.write("{} {}".format(occurrences[0][0], occurrences[0][1]))
        for i in range(1, len(occurrences)):
            outputFile.write('\n')
            outputFile.write("{} {}".format(
                occurrences[i][0], occurrences[i][1]))
    # Remember to close the file
    outputFile.close()


def editDistance(str1, str2, m, n):

    # If first string is empty, the only option is to
    # insert all characters of second string into first
    if m == 0:
        return n

    # If second string is empty, the only option is to
    # remove all characters of first string
    if n == 0:
        return m

    # If last characters of two strings are same, nothing
    # much to do. Ignore last characters and get count for
    # remaining strings.
    if str1[m-1] == str2[n-1]:
        return editDistance(str1, str2, m-1, n-1)

    # If last characters are not same, consider all three
    # operations on last character of first string, recursively
    # compute minimum cost for all three operations and take
    # minimum of three values.
    return 1 + min(editDistance(str1, str2, m, n-1),    # Insert
                   editDistance(str1, str2, m-1, n),    # Remove
                   editDistance(str1, str2, m-1, n-1)    # Replace
                   )


def z_algo(string: str) -> list:
    """
    z-algorithm for pattern matching

    :param string: a string 

    :returns: the z array 

    :reference: https://www.geeksforgeeks.org/z-algorithm-linear-time-pattern-searching-algorithm/
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


def hamdist1_patmatch(txt: str, pat: str) -> None:
    """
    Identifies all positions in txt that matches the pat within a Hamming distance of 1 
    using z algorithm and writes it to a file output_hd1_patmatch.txt.

    
    :param txt: the string of text to search through
    :param pat: the pattern string to match with the text
    """
    output = []

    if len(txt) == 0 or len(pat) == 0:
        write_output(output)
        return

    z_arr_pref = z_algo(pat + txt)
    z_arr_suff = get_reversed_z_arr(txt + pat)

    for i in range(len(pat), len(txt) + 1):
        if z_arr_pref[i] >= len(pat):
            output.append((i - len(pat) + 1, 0))
        elif z_arr_suff[i - 1] >= len(pat) - z_arr_pref[i] - 1:
            output.append((i-len(pat)+1, 1))

    write_output(output)


# %%
if __name__ == "__main__":
    text_file_name = sys.argv[1]   # text_file_name = "text.txt"
    pat_file_name = sys.argv[2]   # pat_file_name = "pattern.\txt"

    hamdist1_patmatch(read_file(text_file_name), read_file(pat_file_name))
