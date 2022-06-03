import os
import unittest
import math
import random
import numpy as np
# from threeprimes import <MILLER_RABIN>  # You may import your own Miller Rabin Algo here


random.seed(1)


def naive_primality_test(n):
    if n < 2:
        return False
    else:
        for k in range(2, int(math.sqrt(n)) + 1):
            if n % k == 0:
                return False
        return True

def mod_exp(a, b, n):
    result = 1
    a = a % n

    if (a == 0) :
        return 0
    while b > 0:
        if (b & 1 == 1) :
            result = (result * a) % n
        
        b >>= 1
        a = (a * a) % n
    
    return result

def miller_rabin(n, k = None):
    k = round(np.log(n)) if k == None else k

    if (n % 2) == 0:
        return False 
    
    s, t = 0, n-1
    while t & 1 == 0:
        s += 1
        t //= 2
    for _ in range(k):
        try:
            a = random.randint(2, n-2)
        except ValueError:
            if n == 3:
                return True

        prev = mod_exp(a, t, n)
        for i in range(1, s+1):
            curr = (prev*prev) % n
            if i == s and curr != 1:
                return False
            if (curr == 1 and ((prev != 1) and (prev != n-1))):
                return False
            if curr == 1:
                break

            prev = curr
    return True # accuracy depends on k


# Replace this with your imported Miller Rabin if you wish to
is_prime = miller_rabin


class TestQ1(unittest.TestCase):
    N = 1000

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            os.remove("output_threeprimes.txt")
        except FileNotFoundError:
            pass

    def test_all(self):
        """ Test for all odd integers n, where 9 <= n <= N """
        # Store Outliers that do not have sums
        outliers = []

        # Begin Tests
        for n in range(9, self.N + 1, 2):
            # Remove file if exists
            try:
                os.remove("output_threeprimes.txt")
            except FileNotFoundError:
                pass

            # Execute Program and Read Output
            os.system('cmd /c python threeprimes.py ' + str(n))
            file = open("output_threeprimes.txt", "r")
            raw = file.read()
            primes = raw.split()
            file.close()

            # Number of values computed is correct
            if len(primes) == 3:
                # Convert to int and check if even non-primes exist
                for i in range(len(primes)):
                    primes[i] = int(primes[i])
                    if primes[i] & 1 == 0 or not is_prime(primes[i]):
                        self.fail(msg="(n=" + str(n) + ") Result contains an even/non-prime number: " + str(primes))

                # Check if sorted
                self.assertEqual(sorted(primes), primes, msg="(n=" + str(n) + ") Output is not sorted")

                # Check if sum is correct
                self.assertEqual(n, sum(primes), msg="(n=" + str(n) + ") Output does not sum to n")

            # No primes were computed disproving the conjecture, tell us if this happens
            elif len(primes) == 0:
                outliers.append(n)

            # Output format is wrong
            else:
                self.fail(msg="(n=" + str(n) + ") Number of outputs is incorrect or is of incorrect format: " + str(raw))

        # Print Outliers
        if len(outliers) > 0:
            print("\n\nNo Primes Computed For:")
            for outlier in outliers:
                print(outlier)
        else:
            print("\n\nAll n values have appropriate sum. Agrees with Conjecture.")


if __name__ == '__main__':
    unittest.main()
