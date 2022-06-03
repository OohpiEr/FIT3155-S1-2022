import unittest
from suffix_tree import SuffixTree
from functools import cmp_to_key
import random


def index(char):
    # Shift chars before $ by 1
    if 0 <= ord(char) <= 35:
        return ord(char) + 1

    # Set $ to 0
    elif ord(char) == 36:
        return 0

    # Set lower case alphabets to upper case
    elif 97 <= ord(char) <= 122:
        return ord(char) - 32

    # Shift chars after lowercase letters to ensure no gaps
    elif 123 <= ord(char) <= 127:
        return ord(char) - 26

    # Every other char is unchanged
    else:
        return ord(char)


def compare(string1, string2):
    i = 0
    j = 0
    while i < len(string1) and j < len(string2):
        if index(string1[i]) < index(string2[i]):
            return -1
        elif index(string1[i]) > index(string2[i]):
            return 1
        i += 1
        j += 1
    return len(string1) - len(string2)


def naive_suffix_array(string):
    string += "$"
    suffixes = []
    suffix_ids = []
    for i in range(len(string)):
        suffixes.append(string[i:])
    suffixes = sorted(suffixes, key=cmp_to_key(compare))
    for suffix in suffixes:
        suffix_ids.append(len(string) - len(suffix))
    return suffix_ids


def random_string(length):
    chars = []
    ascii_list = range(0, 127)
    for i in range(length):
        chars.append(chr(random.choice([ele for ele in ascii_list if ele != 36])))
    return "".join(chars)


class TestUkkonen(unittest.TestCase):
    def process(self, expected, string):
        suffix_tree = SuffixTree(string)
        actual = suffix_tree.suffix_array()
        try:
            # print("\n")
            # suffix_tree.display(string)
            self.assertEqual(expected, actual)
        except Exception as e:
            print("\n")
            suffix_tree.display(string)
            raise e

    def test_sample_1(self):
        """ From Ian's video """
        expected = [12, 10, 0, 6, 3, 11, 1, 7, 4, 2, 8, 5, 9]
        string = "abcabxabcyab"
        self.process(expected, string)

    def test_sample_2(self):
        """ My random example """
        expected = [4, 0, 2, 1, 3]
        string = "abac"
        self.process(expected, string)

    def test_sample_3(self):
        """ From Skip Count Trick doc """
        string = "xabdxacabexabdy"
        expected = naive_suffix_array(string)
        self.process(expected, string)

    def test_sample_4(self):
        """ From Tutorial """
        string = "xabdxacxabe"
        expected = naive_suffix_array(string)
        self.process(expected, string)

    def test_sample_5(self):
        """ From Taylor's Notes """
        string = "abacabad"
        expected = naive_suffix_array(string)
        self.process(expected, string)

    def test_sample_6(self):
        """ From Ser Ng """
        string = "ezqpzqpzq"
        expected = naive_suffix_array(string)
        self.process(expected, string)

    def test_sample_7(self):
        """ Another random example """
        string = "xabdxayurtyrut"
        expected = naive_suffix_array(string)
        self.process(expected, string)

    def test_sample_8(self):
        """ From Michelle """
        string = "aPpapap"
        expected = naive_suffix_array(string)
        self.process(expected, string)

    def test_empty_string(self):
        """ Empty string """
        expected = [0]
        string = ""
        self.process(expected, string)

    def test_single_char(self):
        """ One char string """
        expected = [1, 0]
        string = "\n"
        self.process(expected, string)

    def test_backwards_suffix_link(self):
        """ Suffix Link points backwards """
        expected = [4, 1, 0, 2, 3]
        string = "BABC"
        self.process(expected, string)

    def test_all_same_char(self):
        """ All chars same """
        expected = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        string = "888888888"
        self.process(expected, string)

    def test_all_different_chars(self):
        """ All chars different """
        string = "!@#%^&*()_+-=[]{}\|:;'"
        expected = naive_suffix_array(string)
        self.process(expected, string)

    def test_rule_2a_not_root(self):
        """ Rule 2a reached but not root """
        string = "AABCAX"
        expected = naive_suffix_array(string.upper())
        self.process(expected, string)

    def test_case_insensitive_all_same(self):
        """ Test case insensitiveness for all same chars """
        string = "AAAaaa"
        expected = naive_suffix_array(string.upper())
        self.process(expected, string)

    def test_case_insensitive_all_different(self):
        """ Test case insensitiveness for all different chars """
        string = "aBcVgTyPOKh"
        expected = naive_suffix_array(string.upper())
        self.process(expected, string)

    def test_case_insensitive_general(self):
        """ Test case insensitiveness for mixed """
        string = "vfndgnfdoubUDHFbfelID\nF99849tu-/-*/*-/4562^*%&yfjef__DC{k   rsgr\n"
        expected = naive_suffix_array(string.upper())
        self.process(expected, string)

    def test_small_random(self):
        """ Small Random Case """
        random.seed(1)
        string = random_string(50)
        expected = naive_suffix_array(string.upper())
        self.process(expected, string)

    def test_medium_random(self):
        """ Medium Random Case """
        random.seed(2)
        string = random_string(1000)
        expected = naive_suffix_array(string.upper())
        self.process(expected, string)

    def test_large_random(self):
        """ Large Random Case """
        random.seed(3)
        string = random_string(10000)
        expected = naive_suffix_array(string.upper())
        self.process(expected, string)

    # def test_extra_large_random(self):
    #     """ Extra Large Random Case """
    #     random.seed(4)
    #     string = random_string(1000000)
    #     tree = SuffixTree(string).suffix_array()
    #     # expected = naive_suffix_array(string.upper())
    #     # self.process(expected, string)


if __name__ == '__main__':
    unittest.main()
