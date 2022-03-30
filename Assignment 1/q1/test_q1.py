import os
import unittest
import random


def read_file(filename):
    data = []
    file = open(filename, "r")
    lines = file.readlines()
    for line in lines:
        data.append(int(line.strip()))
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


def naive_pattern_match(txt, pat):
    matches = []
    if pat != "":
        for i in range(len(txt) - len(pat) + 1):
            match = True
            for j in range(len(pat)):
                if txt[i + j] != pat[j]:
                    match = False
                    break
            if match:
                matches.append(i + 1)
    return matches


class TestQ1(unittest.TestCase):
    def process(self, text, pattern, expected_output):
        write_file("text.txt", text)
        write_file("pattern.txt", pattern)
        os.system('cmd /c python modified_BoyerMoore.py text.txt pattern.txt')
        self.assertEqual(expected_output, read_file("output_modified_BoyerMoore.txt"))

    @classmethod
    def tearDownClass(cls):
        os.remove("text.txt")
        os.remove("pattern.txt")
        os.remove("output_modified_BoyerMoore.txt")

    def setUp(self):
        if os.path.exists("output_modified_BoyerMoore.txt"):
            os.remove("output_modified_BoyerMoore.txt")

    def test_given(self):
        """ Given from prac sheet """
        expected = [1, 5, 9]
        text = "abcdabcdabcd"
        pattern = "abc"
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

    def test_single_char_match(self):
        """ Everything (txt, pat) is single char match """
        expected = [1]
        self.process("r", "r", expected)

    def test_single_char_mismatch(self):
        """ Everything (txt, pat) is single char mismatch """
        expected = []
        self.process("z", "u", expected)

    def test_same_length_match(self):
        """ Everything (txt, pat) is same length and equal"""
        expected = [1]
        self.process("hello world", "hello world", expected)

    def test_same_length_mismatch(self):
        """ Everything (txt, pat) is same length but not equal"""
        expected = []
        self.process("Some Random Text", "Some Random Test", expected)

    def test_single_char_pattern_match(self):
        """ Pattern is single char match """
        expected = [4, 7]
        self.process("zsdhgrhogb", "h", expected)

    def test_single_char_pattern_mismatch(self):
        """ Pattern is single char mismatch """
        expected = []
        self.process("grgtdhrgreg", "a", expected)

    def test_pat_longer(self):
        """ Pattern is longer than Text """
        expected = []
        self.process("gg", "ggergetbtebhtrbhr", expected)

    def test_bad_character(self):
        """ Test Bad Character Rule (For BM) """
        expected = []
        self.process("abaaca", "abc", expected)

    def test_single_pattern_always_present(self):
        """ When single char pattern is in every index """
        expected = [1, 2, 3, 4, 5, 6, 7, 8]
        self.process("eeeeeeee", "e", expected)

    def test_overlapping_pattern(self):
        """ When pattern match overlaps """
        expected = [1, 2, 3, 4]
        self.process("zzzzzz", "zzz", expected)

    def test_long_pattern_always_present(self):
        """ When multiple char pattern is in every index """
        expected = [1, 3, 5, 7, 9]
        self.process("abababababab", "aba", expected)

    def test_all_rules_give_one(self):
        """ When all rules give shift by 1 """
        expected = []
        self.process("aaaaaa", "bb", expected)

    def test_single_occurrence(self):
        """ One occurrence of pat """
        expected = [4]
        self.process("genshin", "shin", expected)

    def test_multiple_occurrence(self):
        """ Multiple occurrence of pat """
        expected = [1, 5, 9, 13, 17, 25, 31]
        self.process("aabxaabcaabraabdaabxghfoaabvdgaabaac", "aab", expected)

    def test_bc_order(self):
        """ Tests if bc rule followed """
        expected = []
        txt = "___________________________XMATCH_"
        pat = "X_X_ZMATCH_____YMATCH______YMATCH"
        self.process(txt, pat, expected)

    def test_gs_order(self):
        """ Tests if gs rule followed """
        expected = []
        txt = "__________________________XMATCH_"
        pat = "__ZMATCH_____YMATCH____X__YMATCH"
        self.process(txt, pat, expected)

    def test_new_shift(self):
        """ Tests if assignment-specific rule followed """
        expected = []
        txt = "________________________________XMATCH_"
        pat = "XMATCH__ZMATCH_____YMATCH____X__YMATCH"
        self.process(txt, pat, expected)

    def test_new_shift_double(self):
        """ Tests if assignment-specific rule followed when two cases present (pick rightmost) """
        expected = []
        txt = "________________XMATCH_"
        pat = "XMATCH__XMATCH__YMATCH"
        self.process(txt, pat, expected)

    def test_new_shift_bc(self):
        """ Tests if bc rule followed when assignment-specific rule case is not present """
        expected = []
        txt = "____ZMATCH__XMATCH_"
        pat = "X___ZMATCH__YMATCH"
        self.process(txt, pat, expected)

    def test_new_shift_gs(self):
        """ Tests if gs rule followed when assignment-specific rule case is not present """
        expected = []
        txt = "________X__XMATCH_"
        pat = "ZMATCH__X__YMATCH"
        self.process(txt, pat, expected)

    def test_new_shift_mp(self):
        """ Tests if mp rule followed when assignment-specific rule case is not present """
        expected = []
        txt = "_______XMATCH_"
        pat = "TCH____YMATCH"
        self.process(txt, pat, expected)

    def test_new_shift_prioritise(self):
        """ Tests if new shift prioritised over other rules """
        expected = []
        txt = "________________________________XMATCH_"
        pat = "ZMATCH__YMATCH___X__XMATCH______YMATCH"
        self.process(txt, pat, expected)

    def test_mp_order(self):
        """ Tests if mp rule followed """
        expected = []
        txt = "______________________________________XMATCH_"
        pat = "TCH______________________YMATCH____X__YMATCH"
        self.process(txt, pat, expected)

    def test_galil_special(self):
        """ Tests if Galil's optimisation followed for special rule """
        expected = [25]
        txt = "________________________________XMATCH__________________YMATCH"
        pat = "________XMATCH__________________YMATCH"
        self.process(txt, pat, expected)

    def test_galil_gs(self):
        """ Tests if Galil's optimisation followed for gs """
        expected = []
        txt = "________________________________XMATCH__________________YMATCH"
        pat = "________ZMATCH______X___________YMATCH"
        self.process(txt, pat, expected)

    def test_galil_mp(self):
        """ Tests if Galil's optimisation followed for mp """
        expected = [25]
        txt = "_____________________XMATCH_____YMATCH___X___YMATCH"
        pat = "TCH_____YMATCH___X___YMATCH"
        self.process(txt, pat, expected)

    def test_bc_gs_equal(self):
        """ Tests bc and gs shift equal """
        expected = [12]
        txt = "_____________________XMATCH_____YMATCH"
        pat = "__________XMATCH_____YMATCH"
        self.process(txt, pat, expected)

    def test_kmp_order(self):
        """ Test if KMP shift followed """
        expected = []
        txt = "MATCHZ________________MATCHX__"
        pat = "MATCHZ________________MATCHY_"
        self.process(txt, pat, expected)

    def test_random_small_text_small_pat(self):
        """ Random Case: Small Text, Small Pattern """
        txt = random_string(5000, seed=1)
        pat = random_string(1, seed=2)
        expected = naive_pattern_match(txt, pat)
        self.process(txt, pat, expected)

    def test_random_small_text_medium_pat(self):
        """ Random Case: Small Text, Medium Pattern """
        txt = random_string(5000, seed=3)
        pat = random_string(5, seed=4)
        expected = naive_pattern_match(txt, pat)
        self.process(txt, pat, expected)

    def test_random_small_text_large_pat(self):
        """ Random Case: Small Text, Large Pattern """
        txt = random_string(5000, seed=5)
        pat = random_string(100, seed=6)
        expected = naive_pattern_match(txt, pat)
        self.process(txt, pat, expected)

    def test_random_medium_text_small_pat(self):
        """ Random Case: Medium Text, Small Pattern """
        txt = random_string(100000, seed=7)
        pat = random_string(1, seed=8)
        expected = naive_pattern_match(txt, pat)
        self.process(txt, pat, expected)

    def test_random_medium_text_medium_pat(self):
        """ Random Case: Medium Text, Medium Pattern """
        txt = random_string(100000, seed=9)
        pat = random_string(5, seed=10)
        expected = naive_pattern_match(txt, pat)
        self.process(txt, pat, expected)

    def test_random_medium_text_large_pat(self):
        """ Random Case: Medium Text, Large Pattern """
        txt = random_string(100000, seed=11)
        pat = random_string(5000, seed=12)
        expected = naive_pattern_match(txt, pat)
        self.process(txt, pat, expected)

    def test_random_large_text_small_pat(self):
        """ Random Case: Large Text, Small Pattern """
        txt = random_string(500000, seed=13)
        pat = random_string(1, seed=14)
        expected = naive_pattern_match(txt, pat)
        self.process(txt, pat, expected)

    def test_random_large_text_medium_pat(self):
        """ Random Case: Large Text, Medium Pattern """
        txt = random_string(500000, seed=15)
        pat = random_string(5, seed=16)
        expected = naive_pattern_match(txt, pat)
        self.process(txt, pat, expected)

    def test_random_large_text_large_pat(self):
        """ Random Case: Large Text, Large Pattern """
        txt = random_string(500000, seed=17)
        pat = random_string(10000, seed=18)
        expected = naive_pattern_match(txt, pat)
        self.process(txt, pat, expected)


if __name__ == '__main__':
    unittest.main()
