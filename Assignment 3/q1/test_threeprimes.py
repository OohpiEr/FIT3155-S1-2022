import unittest
import math
import random
from threeprimes import main  # Import main method here by replacing main
# from threeprimes import miller_rabin  # You may import your own Miller Rabin Algo here


random.seed(1)


def naive_primality_test(n):
    if n < 2:
        return False
    else:
        for k in range(2, int(math.sqrt(n)) + 1):
            if n % k == 0:
                return False
        return True


# Replace main with your main method
threeprimes = main

# Replace this with your imported Miller Rabin if you wish to
is_prime = naive_primality_test


class TestThreePrimes(unittest.TestCase):
    N = 1000000

    def test_all(self):
        """ Test for all odd integers n, where 9 <= n <= N """
        # Store Outliers that do not have sums
        outliers = []

        # Begin Tests
        for n in range(9, self.N + 1, 2):
            primes = threeprimes(n)

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
                self.fail(msg="(n=" + str(n) + ") Number of outputs is incorrect or is of incorrect format: " + str(primes))

        # Print Outliers
        if len(outliers) > 0:
            print("\n\nNo Primes Computed For:")
            for outlier in outliers:
                print(outlier)
        else:
            print("\n\nAll n values have appropriate sum. Agrees with Conjecture.")


if __name__ == '__main__':
    unittest.main()
