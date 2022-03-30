"""
FIT3155 Assignment 1 Question 2

__author__ = "Er Tian Ru"

References:
geeksforgeeks z algorithm https://www.geeksforgeeks.org/z-algorithm-linear-time-pattern-searching-algorithm/
"""
# %%

def read_file(filename):
    # Open and read the text file
    txtFile = open(filename, 'r')
    txt = txtFile.read()
    # Remember to close the file
    txtFile.close()
    # Return the pattern and text
    return txt


def write_output(occurrences):
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


def z_algo(string, m):
    
    assert len(string) != 0

    # initialize z array
    z_arr = [0 for _ in range(len(string))]
    ham_arr = [-1 for _ in range(len(string))]

    # length of string stored in first cell
    z_arr[0] = n = len(string)

    l, r, k = 0, 0, 0
    for i in range(1, n):
        ham = 0
        mismatch_index = -1

        # CASE 1: i>R (i outside box or no box)
        # calculate Z[i] naively
        if i > r:
            l, r = i, i

            # compare 
            while r - l < m and r < n and ham <= 1:
                if string[r - l] == string[r]:
                    r += 1
                else:
                    if mismatch_index == -1:
                        mismatch_index = r
                    r += 1
                    ham += 1
            
            # if r - l - 1 == m:
            ham_arr[i] = ham
            # elif mismatch_index - l == m:
            #     ham_arr[i] = 0

            if mismatch_index != -1:
                z_arr[i] = mismatch_index - l
                r = mismatch_index - 1
            else:
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
                ham_arr[i] = ham_arr[k]

            # CASE 2b: z[k] > remaining
            # z[i] = remaining
            elif z_arr[k] > r - i + 1:
                z_arr[i] = r - i + 1
            
            # CASE 2c: Z[k] = remaining
            # compare string[r + 1 ... r + n]
            elif z_arr[k] == r - i + 1:
                l = i
                # while r < n and string[r - l] == string[r]:
                #     r += 1
                # z_arr[i] = r - l
                # r -= 1
                
                while r - l + 1 < m and r < n - 1 and ham <= 1:
                    if string[r - l + 1] == string[r + 1]:
                        r += 1
                    else:
                        if mismatch_index == -1:
                            mismatch_index = r
                        r += 1
                        ham += 1

                ham_arr[i] = ham

                if mismatch_index != -1:
                    z_arr[i] = mismatch_index - l
                    # r = mismatch_index - 1
                    r = mismatch_index 
                else:
                    z_arr[i] = r - l + 1
                    # r -= 1


    print( z_arr)
    print(ham_arr)
    return ham_arr
            
def hamdist1_patmatch(txt, pat):
    # Create concatenated string "pat$txt"
    concat = pat + "$" + txt
    
    ham_arr = z_algo(concat, len(pat))

    # for i in range(len(ham_arr)):


	# # now looping through Z array for matching condition
	# for i in range(l):

	# 	# if Z[i] (matched region) is equal to pattern
	# 	# length we got the pattern
	# 	if z[i] == len(pat):
	# 		print("Pattern found at index",
	# 				i - len(pat) - 1)

# %%
if __name__ == "__main__":
    # the actual argument
    # text_file_name = sys.argv[1]   # text_file_name = "text.txt"
    # pat_file_name = sys.argv[2]   # pat_file_name = "pattern.\txt"

    # hamdist1_patmatch(read_file(text_file_name), read_file(pat_file_name))

    # txt = "abcdyaacaacdaacz"
    # pat = "aacd"
    txt = "zzzzzAAAAAzzz"
    pat = "AAAA"
    hamdist1_patmatch(txt, pat)
