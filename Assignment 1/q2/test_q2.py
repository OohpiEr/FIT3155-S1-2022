import os
import unittest
import random


def read_file(filename):
    data = []
    file = open(filename, "r")
    lines = file.readlines()
    for line in lines:
        row = line.strip().split()
        data.append((int(row[0]), int(row[1])))
    file.close()
    return data


def write_file(filename, data):
    if os.path.exists(filename):
        os.remove(filename)
    output_file = open(filename, "w")
    output_file.write(data)
    output_file.close()


def random_string(length, seed=None):
    random.seed(seed)
    chars = []
    for i in range(length):
        chars.append(chr(random.randint(32, 127)))
    return "".join(chars)


def naive_algo(txt, pat):
    matches = []
    if pat != "":
        for i in range(len(txt) - len(pat) + 1):
            ham = 0
            for j in range(len(pat)):
                if txt[i + j] != pat[j]:
                    ham += 1
                    if ham >= 2:
                        break
            if ham <= 1:
                matches.append((i + 1, ham))
    return matches


class TestQ2(unittest.TestCase):
    def process(self, text, pattern, expected_output):
        write_file("text.txt", text)
        write_file("pattern.txt", pattern)
        os.system('cmd /c python hd1_patmatch.py text.txt pattern.txt')
        self.assertEqual(expected_output, read_file("output_hd1_patmatch.txt"))

    @classmethod
    def tearDownClass(cls):
        os.remove("text.txt")
        os.remove("pattern.txt")
        os.remove("output_hd1_patmatch.txt")

    def setUp(self):
        if os.path.exists("output_hd1_patmatch.txt"):
            os.remove("output_hd1_patmatch.txt")

    def test_given(self):
        """ Given from prac sheet """
        expected = [(1, 1), (6, 1), (9, 0), (13, 1)]
        text = "abcdyaacaacdaacz"
        pattern = "aacd"
        self.process(text, pattern, expected)

    def test_empty_everything(self):
        """ Everything (txt, pat) is empty """
        expected = []
        self.process("", "", expected)

    def test_empty_pat(self):
        """ Pattern is empty """
        expected = []
        self.process("fjjgnebdfuibudtbgtiodbgv", "", expected)

    def test_empty_txt(self):
        """ Text is empty """
        expected = []
        self.process("", "fiwerohgnvfiorteghhtuielbhtr", expected)

    def test_single_zero_ham_match(self):
        """ Everything (txt, pat) is single char zero ham match """
        expected = [(1, 0)]
        self.process("r", "r", expected)

    def test_single_one_ham_match(self):
        """ Everything (txt, pat) is single char one ham match """
        expected = [(1, 1)]
        self.process("z", "u", expected)

    def test_same_length_zero_ham_match(self):
        """ Everything (txt, pat) is same length and zero ham match"""
        expected = [(1, 0)]
        self.process("hello world", "hello world", expected)

    def test_same_length_one_ham_mismatch(self):
        """ Everything (txt, pat) is same length and one ham match """
        expected = [(1, 1)]
        self.process("Some Random Text", "Some Random Test", expected)

    def test_single_char_pattern_zero_ham_match(self):
        """ Pattern is single char zero ham match """
        expected = [(1, 1),
                    (2, 1),
                    (3, 1),
                    (4, 0),
                    (5, 1),
                    (6, 1),
                    (7, 0),
                    (8, 1),
                    (9, 1),
                    (10, 1)]
        self.process("zsdhgrhogb", "h", expected)

    def test_single_char_pattern_one_ham_match(self):
        """ Pattern is single char one ham match """
        expected = [(1, 1),
                    (2, 1),
                    (3, 1),
                    (4, 1),
                    (5, 1),
                    (6, 1),
                    (7, 1),
                    (8, 1),
                    (9, 1),
                    (10, 1),
                    (11, 1),]
        self.process("grgtdhrgreg", "a", expected)

    def test_pat_longer(self):
        """ Pattern is longer than Text """
        expected = []
        self.process("gg", "ggergetbtebhtrbhr", expected)

    def test_bad_character(self):
        """ Test Bad Character Rule (For BM) """
        expected = [(1, 1), (3, 1)]
        self.process("abaaca", "abc", expected)

    def test_single_pattern_always_present(self):
        """ When single char pattern is in every index """
        expected = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]
        self.process("eeeeeeee", "e", expected)

    def test_overlapping_pattern(self):
        """ When pattern match overlaps """
        expected = [(1, 0), (2, 0), (3, 0), (4, 0)]
        self.process("zzzzzz", "zzz", expected)

    def test_long_pattern_always_present(self):
        """ When multiple char pattern is in every index """
        expected = [(1, 0), (3, 0), (5, 0), (7, 0), (9, 0)]
        self.process("abababababab", "aba", expected)

    def test_single_occurrence(self):
        """ One occurrence of pat """
        expected = [(4, 0)]
        self.process("genshin", "shin", expected)

    def test_multiple_occurrence(self):
        """ Multiple occurrence of pat """
        expected = [(1, 0), (5, 0), (9, 0), (13, 0), (17, 0), (25, 0), (31, 0), (34, 1)]
        self.process("aabxaabcaabraabdaabxghfoaabvdgaabaac", "aab", expected)

    def test_random_small_text_small_pat(self):
        """ Random Case: Small Text, Small Pattern """
        txt = random_string(5000, seed=19)
        pat = random_string(2, seed=20)
        expected = naive_algo(txt, pat)
        self.process(txt, pat, expected)

    def test_random_small_text_medium_pat(self):
        """ Random Case: Small Text, Medium Pattern """
        txt = random_string(5000, seed=21)
        pat = random_string(5, seed=22)
        expected = naive_algo(txt, pat)
        self.process(txt, pat, expected)

    def test_random_small_text_large_pat(self):
        """ Random Case: Small Text, Large Pattern """
        txt = random_string(5000, seed=23)
        pat = random_string(100, seed=24)
        expected = naive_algo(txt, pat)
        self.process(txt, pat, expected)

    def test_random_medium_text_small_pat(self):
        """ Random Case: Medium Text, Small Pattern """
        txt = random_string(100000, seed=25)
        pat = random_string(2, seed=26)
        expected = naive_algo(txt, pat)
        self.process(txt, pat, expected)

    def test_random_medium_text_medium_pat(self):
        """ Random Case: Medium Text, Medium Pattern """
        txt = random_string(100000, seed=27)
        pat = random_string(5, seed=28)
        expected = naive_algo(txt, pat)
        self.process(txt, pat, expected)

    def test_random_medium_text_large_pat(self):
        """ Random Case: Medium Text, Large Pattern """
        txt = random_string(100000, seed=29)
        pat = random_string(5000, seed=30)
        expected = naive_algo(txt, pat)
        self.process(txt, pat, expected)

    def test_random_large_text_small_pat(self):
        """ Random Case: Large Text, Small Pattern """
        txt = random_string(500000, seed=31)
        pat = random_string(2, seed=32)
        expected = naive_algo(txt, pat)
        self.process(txt, pat, expected)

    def test_random_large_text_medium_pat(self):
        """ Random Case: Large Text, Medium Pattern """
        txt = random_string(500000, seed=33)
        pat = random_string(5, seed=34)
        expected = naive_algo(txt, pat)
        self.process(txt, pat, expected)

    def test_random_large_text_large_pat(self):
        """ Random Case: Large Text, Large Pattern """
        txt = random_string(500000, seed=35)
        pat = random_string(10000, seed=36)
        expected = naive_algo(txt, pat)
        self.process(txt, pat, expected)


if __name__ == '__main__':
    unittest.main()
