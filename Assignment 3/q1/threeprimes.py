"""
FIT3155 Assignment 3 Question 1

__author__ = "Er Tian Ru"
student_id = "30881668"

References:
https://www.geeksforgeeks.org/modular-exponentiation-power-in-modular-arithmetic/
"""
# %%
import random
import sys
import numpy as np


def read_file(filename):
    """Reads a file "filename"

    :param filename: filename
    :return: file contents
    """
    # Open and read the text file
    txtFile = open(filename, 'r')
    txt = txtFile.read()
    # Remember to close the file
    txtFile.close()
    # Return the pattern and text
    return txt


def write_output(primes, n):
    """Writes a 3-tuple of prime numbers to a file "output_threeprimes.txt""

    :param primes: 3-tuple of prime numbers
    :param n: number that the prime numbers in primes sums to
    """
    # Open output file with correct name
    outputFile = open('output_threeprimes.txt', 'w')
    # Iterate through the occurrence list and write results to an output file
    try:
        if primes:
            outputFile.write("{} {} {}".format(
                primes[2], primes[1], primes[0]))
    except IndexError:
        print("problem_n: " + n)
    # Remember to close the file
    outputFile.close()


def run_threeprimes():
    """runs threeprimes
    """
    write_output(three_primes(int(sys.argv[1])), sys.argv[1])


def mod_exp(a, b, n):
    """Modular Exponentiation using repeated squaring for (a^b) mod n

    :param a: a
    :param b: b
    :param n: n
    :return: result of (a^b) mod n
    """
    result = 1
    a = a % n

    if (a == 0):
        return 0
    while b > 0:
        # if LSB is 1
        if (b & 1 == 1):
            result = (result * a) % n

        # shift right
        b >>= 1
        a = (a * a) % n

    return result


def miller_rabin(n, k=None):
    """Miller-rabin algorithm to check if n is a prime number

    :param n: n
    :param k: number of random tests, defaults to ln(n)
    :return: True if n is prime, False otherwise
    """
    # special case
    if n == 2 or n == 3:
        return True

    # if n is even -> not prime
    if n & 1 == 0:
        return False

    # k = ln(n)
    k = round(np.log(n)) if k == None else k

    # Factor n-1 as 2^s.t, where t is odd
    s, t = 0, n-1
    # while t is even
    while t & 1 == 0:
        s += 1
        t //= 2
    #  at this stage , n-1 will be 2^s.t, where t is odd

    # k random tests
    for _ in range(k):
        a = random.randint(2, n-2)

        prev = mod_exp(a, t, n)
        for i in range(1, s+1):
            curr = (prev*prev) % n

            if i == s and curr != 1:
                # not prime
                return False

            if (curr == 1 and ((prev != 1) and (prev != n-1))):
                # not prime
                return False

            # if curr == 1, rest of loop curr will also be 1
            # so we know its probably prime
            if curr == 1:
                break

            prev = curr

    # probably prime
    return True  # accuracy depends on k


def three_primes(n):
    """Algorithm to find three prime numbers that sum to n

    :param n: n
    :return: 3-tuple of prime numbers that sum to n
    """
    if n & 1 == 0:
        return
    # loop backwards & check if i is prime
    # start from largest prime smaller than n
    # use miller_rabin to check if i is prime
    primes = []
    i = n - 6
    rem = n
    while i > 2:
        if i & 1 == 1 and miller_rabin(i):
            if rem - i >= 0:
                rem -= i
                primes.append(i)
                i = rem + 1

                if rem == 0 and len(primes) == 3:
                    break
        i -= 1
        if (i <= 2 and len(primes) != 3) or (len(primes) == 3 and rem != 0):
            popped = primes.pop(-1)
            rem += popped
            while popped == 3 and primes:
                popped = primes.pop(-1)
                rem += popped
            i = popped - 1

    return primes


if __name__ == "__main__":
    run_threeprimes()
