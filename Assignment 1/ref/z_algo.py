
from re import I


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


def period_old(string):
    """
    z_algo = O(n)
    BM = O(n + m)
    """
    z_arr = z_algo(string) # O(n)
    len_string = z_arr[0]
    
    p = 0
    expected_k = len_string
    while expected_k:
        p = len_string//expected_k
        
        actual_k = 0
        for i in z_arr:
            if i >= p:
                actual_k += 1
        
        if actual_k == expected_k:
            break
        
        expected_k -= 1
        while expected_k and len_string//expected_k == p:
            p = len_string//expected_k
            expected_k -= 1
    
    result = p
    if expected_k == 1:
        result = "string not periodic"
        
    return result

def period(string):
    """
    z_algo = O(n)
    BM = O(n + m)
    """
    z_arr = z_algo(string) # O(n)
    len_string = z_arr[0]
    
    i = len_string - 1
    while z_arr[i] == 0 and i >= 0:
        i -= 1
    p = z_arr[i]
    
    if p + z_arr[p] == len_string:
        return p 
    
    return "string not periodic"
    

if __name__ == "__main__":
    print(period("abcdabcdabcdabcdabcdabcd"))
    print(z_algo("bbccaebbcabd"))