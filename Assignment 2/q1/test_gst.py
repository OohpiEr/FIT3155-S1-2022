import unittest
from gst import GeneralisedSuffixTree
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


def compare(collection1, collection2):
    string1 = collection1[0]
    string2 = collection2[0]
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


def naive_suffix_array(strings):
    suffixes = []
    suffix_ids = []
    for i in range(len(strings)):
        strings[i] = strings[i].upper()
        for j in range(len(strings[i])):
            suffixes.append((strings[i][j:], i))
    suffixes = sorted(suffixes, key=cmp_to_key(compare))
    for suffix, i in suffixes:
        suffix_ids.append((i, len(strings[i]) - len(suffix)))
    return suffix_ids


def random_strings(count, lo, hi):
    def random_string(length):
        chars = []
        ascii_list = range(0, 127)
        for i in range(length):
            chars.append(chr(random.choice([ele for ele in ascii_list if ele != 36])))
        return "".join(chars)

    strings = []
    for _ in range(count):
        strings.append(random_string(random.randint(lo, hi)))
    return strings


class TestUkkonen(unittest.TestCase):
    def process(self, expected, strings):
        gst = GeneralisedSuffixTree(strings)
        actual = gst.suffix_array()
        try:
            self.assertEqual(expected, actual)
        except Exception as e:
            print("\n")
            gst.display(strings)
            raise e

    def test_sample_1(self):
        """ From Ian's video """
        expected = [(0, 12), (0, 10), (0, 0), (0, 6), (0, 3), (0, 11),
                    (0, 1), (0, 7), (0, 4), (0, 2), (0, 8), (0, 5), (0, 9)]
        strings = ["abcabxabcyab$"]
        self.process(expected, strings)

    def test_sample_2(self):
        """ My random example """
        expected = [(0, 4), (0, 0), (0, 2), (0, 1), (0, 3)]
        strings = ["abac$"]
        self.process(expected, strings)

    def test_sample_3(self):
        """ From Skip Count Trick doc """
        strings = ["xabdxacabexabdy$"]
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_sample_4(self):
        """ From Tutorial """
        strings = ["xabdxacxabe$"]
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_sample_5(self):
        """ From Taylor's Notes """
        strings = ["abacabad$"]
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_sample_6(self):
        strings = ["ezqpzqpzq$"]
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_single_empty_string(self):
        """ Single Empty string """
        expected = [(0, 0)]
        strings = ["$"]
        self.process(expected, strings)

    def test_multiple_empty_string(self):
        """ Multiple Empty strings """
        expected = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        strings = ["$", "$", "$", "$", "$"]
        self.process(expected, strings)

    def test_one_single_char(self):
        """ One single char string """
        expected = [(0, 1), (0, 0)]
        strings = ["\n$"]
        self.process(expected, strings)

    def test_multiple_same_single_char(self):
        """ Multiple single char strings """
        expected = [(0, 1), (1, 1), (2, 1), (0, 0), (1, 0), (2, 0)]
        strings = ["\b$", "\b$", "\b$"]
        self.process(expected, strings)

    def test_multiple_different_single_char(self):
        """ Multiple different char strings """
        expected = [(0, 1), (1, 1), (2, 1), (1, 0), (0, 0), (2, 0)]
        strings = ["2$", "1$", "3$"]
        self.process(expected, strings)

    def test_backwards_suffix_link(self):
        """ Suffix Link points backwards """
        expected = [(0, 4), (0, 1), (0, 0), (0, 2), (0, 3)]
        strings = ["BABC$"]
        self.process(expected, strings)

    def test_all_same_char(self):
        """ All chars same """
        expected = [(0, 9), (0, 8), (0, 7), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
        strings = ["888888888$"]
        self.process(expected, strings)

    def test_all_different_chars(self):
        """ All chars different """
        strings = ["!@#%^&*()_+-=[]{}\|:;'$"]
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_rule_2a_not_root(self):
        """ Rule 2a reached but not root """
        strings = ["AABCAX$"]
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_case_insensitive_all_same(self):
        """ Test case insensitiveness for all same chars """
        strings = ["AAAaaa$", "aaAAA$"]
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_case_insensitive_all_different(self):
        """ Test case insensitiveness for all different chars """
        strings = ["aBcVgTyPOKh$", "bCUDOWq$"]
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_case_insensitive_general(self):
        """ Test case insensitiveness for mixed """
        strings = ["vfndgnfdoubUDHFbfelID\nF99849tu-/-*/*-/4562^*%&yfjef__DC{k   rsgr\n$"]
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_multiple_strings(self):
        """ Multiple Different Strings """
        expected = [(0, 4),
                    (1, 2),
                    (2, 5),
                    (3, 4),
                    (4, 4),
                    (1, 0),
                    (0, 0),
                    (3, 0),
                    (2, 0),
                    (0, 2),
                    (3, 2),
                    (2, 2),
                    (1, 1),
                    (0, 1),
                    (3, 1),
                    (2, 1),
                    (0, 3),
                    (3, 3),
                    (2, 3),
                    (2, 4),
                    (4, 3),
                    (4, 2),
                    (4, 1),
                    (4, 0)]
        strings = ["abac$", "ab$", "abacd$", "abac$", "xxxx$"]
        self.process(expected, strings)

    def test_same_prefix_different_suffix_small(self):
        """ Strings start out same but end different but small """
        strings = ["abac$", "abde$"]
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_same_prefix_different_suffix(self):
        """ Strings start out same but end different """
        strings = ["xabdxacabexabdy$", "xabdxayurtyrut$"]
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_random_small_sample_small_size(self):
        """ Random Case: Small Sample Size, Small Length """
        random.seed(1)
        strings = random_strings(10, 10, 20)
        for i in range(len(strings)):
            strings[i] = "".join([strings[i], "$"])
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_random_small_sample_medium_size(self):
        """ Random Case: Small Sample Size, Medium Length """
        random.seed(2)
        strings = random_strings(10, 50, 100)
        for i in range(len(strings)):
            strings[i] = "".join([strings[i], "$"])
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_random_small_sample_large_size(self):
        """ Random Case: Small Sample Size, Large Length """
        random.seed(3)
        strings = random_strings(10, 500, 1000)
        for i in range(len(strings)):
            strings[i] = "".join([strings[i], "$"])
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_random_medium_sample_small_size(self):
        """ Random Case: Medium Sample Size, Small Length """
        random.seed(4)
        strings = random_strings(50, 10, 20)
        for i in range(len(strings)):
            strings[i] = "".join([strings[i], "$"])
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_random_medium_sample_medium_size(self):
        """ Random Case: Medium Sample Size, Small Length """
        random.seed(5)
        strings = random_strings(50, 50, 100)
        for i in range(len(strings)):
            strings[i] = "".join([strings[i], "$"])
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_random_medium_sample_large_size(self):
        """ Random Case: Medium Sample Size, Large Length """
        random.seed(6)
        strings = random_strings(50, 500, 1000)
        for i in range(len(strings)):
            strings[i] = "".join([strings[i], "$"])
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_random_large_sample_small_size(self):
        """ Random Case: Large Sample Size, Small Length """
        random.seed(7)
        strings = random_strings(100, 10, 20)
        for i in range(len(strings)):
            strings[i] = "".join([strings[i], "$"])
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_random_large_sample_medium_size(self):
        """ Random Case: Large Sample Size, Medium Length """
        random.seed(8)
        strings = random_strings(100, 50, 100)
        for i in range(len(strings)):
            strings[i] = "".join([strings[i], "$"])
        expected = naive_suffix_array(strings)
        self.process(expected, strings)

    def test_random_large_sample_large_size(self):
        """ Random Case: Large Sample Size, Large Length """
        random.seed(9)
        strings = random_strings(100, 500, 1000)
        for i in range(len(strings)):
            strings[i] = "".join([strings[i], "$"])
        expected = naive_suffix_array(strings)
        self.process(expected, strings)


if __name__ == '__main__':
    unittest.main()
