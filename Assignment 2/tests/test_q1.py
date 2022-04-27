import glob
import os
import unittest
import random


def write_file(filename, data):
    # Important Variables
    text_count = len(data[0])
    pattern_count = len(data[1])
    output_file = open(filename, "w")

    # Write text files
    output_file.write(str(text_count))
    for i in range(len(data[0])):
        # Important Variables
        name = "text" + str(i + 1) + ".txt"
        row = str(i + 1) + " " + name

        # Write Individual String File
        string = str(data[0][i])
        string_file = open(name, "w")
        string_file.write(string)
        string_file.close()

        # Write filename in query file
        output_file.write("\n")
        output_file.write(row)

    # Write pattern files
    output_file.write("\n" + str(pattern_count))
    for i in range(len(data[1])):
        # Important Variables
        name = "pat" + str(i + 1) + ".txt"
        row = str(i + 1) + " " + name

        # Write Individual String File
        string = str(data[1][i])
        string_file = open(name, "w")
        string_file.write(string)
        string_file.close()

        # Write filename in query file
        output_file.write("\n")
        output_file.write(row)

    # Done
    output_file.close()


def read_file(filename):
    # Important Variables
    matches = []
    file = open(filename, "r")
    lines = file.readlines()

    # Read lines
    for line in lines:
        row = line.split()
        matches.append((int(row[0]), int(row[1]), int(row[2])))

    # Done
    file.close()
    return sorted(matches)


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


class TestQ1(unittest.TestCase):
    def process(self, texts, patterns, expected_output, text_index=None, pattern_index=None, seed=None):
        """ Main Testing Process """
        write_file("query.txt", [texts, patterns])
        os.system('cmd /c python gst.py query.txt')
        self.assertEqual(expected_output, read_file("output_gst.txt"), msg="Random Case failed at Text Params " +
                                                                           str(text_index) + ", Pattern Params " +
                                                                           str(pattern_index) + ", Seed " + str(seed))

    @classmethod
    def tearDownClass(cls):
        """ Remove All txt files after testing """
        for txt_file in glob.glob(os.path.join(os.getcwd(), '*.txt')):
            os.remove(txt_file)

    def setUp(self):
        """ Remove All txt files before each test case """
        for txt_file in glob.glob(os.path.join(os.getcwd(), '*.txt')):
            os.remove(txt_file)

    def test_sample_1(self):
        """ Random test I came up (since assignment spec didn't give any sample) """
        expected = sorted([(1, 1, 2), (2, 3, 2)])
        texts = ["hello", "world", "hi"]
        patterns = ["e", "i"]
        self.process(texts, patterns, expected)

    def test_sample_2(self):
        """ From https://edstem.org/au/courses/8237/discussion/802593 """
        expected = sorted([(1, 1, 32),
                           (1, 1, 535),
                           (1, 1, 815),
                           (1, 1, 872),
                           (2, 1, 995),
                           (2, 1, 1107),
                           (2, 2, 21),
                           (2, 2, 589),
                           (2, 2, 743),
                           (2, 2, 959),
                           (2, 2, 1149),
                           (2, 2, 1341),
                           (2, 2, 1486),
                           (3, 1, 1385),
                           (3, 2, 1349),
                           (3, 2, 1494)])
        os.system('cmd /c python gst.py sample.asc')
        self.assertEqual(expected, read_file("output_gst.txt"))

    def test_empty_everything(self):
        """ No texts and patterns """
        expected = []
        texts = []
        patterns = []
        self.process(texts, patterns, expected)

    def test_empty_texts(self):
        """ No texts """
        expected = []
        texts = []
        patterns = ["soihgf80eh", "soef89034gyvrhfu", "q03570824yf24w9efr*)&)*"]
        self.process(texts, patterns, expected)

    def test_empty_patterns(self):
        """ No patterns """
        expected = []
        texts = ["soighorhg", "osehf8w4ygf9rwvfeoerhv", "sdhfuowergfirweogfrro", " ijisdoferigfveruofvhuv "]
        patterns = []
        self.process(texts, patterns, expected)

    def test_single_char_matches(self):
        """ All single char matches """
        expected = sorted([(1, 3, 1), (2, 2, 1)])
        texts = ["@", " ", "\n"]
        patterns = ["\n", " "]
        self.process(texts, patterns, expected)

    def test_single_char_mismatches(self):
        """ All single char mismatches """
        expected = []
        texts = ["\n", ":", "/", "\b"]
        patterns = [")", "!", "`", "*", "q", "1"]
        self.process(texts, patterns, expected)

    def test_single_match(self):
        """ One text and pattern match """
        expected = [(1, 1, 4)]
        texts = ["@#^%@"]
        patterns = ["%"]
        self.process(texts, patterns, expected)

    def test_single_mismatch(self):
        """ One text and pattern mismatch """
        expected = []
        texts = ["@#^%@"]
        patterns = ["p"]
        self.process(texts, patterns, expected)

    def test_pattern_longer(self):
        """ Patterns longer than text """
        expected = []
        texts = ["123", "014", "1"]
        patterns = ["123445", "347623956497"]
        self.process(texts, patterns, expected)

    def test_text_pattern_equal(self):
        """ Text and pattern are exactly equal """
        expected = sorted([(1, 2, 1), (2, 1, 1)])
        texts = ["-+=", "42069"]
        patterns = ["42069", "-+="]
        self.process(texts, patterns, expected)

    def test_text_pattern_equal_length(self):
        """ Text and pattern are equal length but not match """
        expected = []
        texts = ["-+=", "42069"]
        patterns = ["42068", "-+5"]
        self.process(texts, patterns, expected)

    def test_multiple_matches(self):
        """ One pattern has multiple matches """
        expected = sorted([(1, 1, 1), (1, 1, 2), (1, 2, 1), (1, 3, 2)])
        texts = ["000", "007", "300"]
        patterns = ["00", "-"]
        self.process(texts, patterns, expected)

    def test_multiple_patterns_single_text_match(self):
        """ Multiple patterns match with one text """
        expected = sorted([(1, 1, 3), (2, 1, 1), (2, 2, 4)])
        texts = [">.<", "===>", ";_;"]
        patterns = ["<", ">"]
        self.process(texts, patterns, expected)

    def test_no_matches(self):
        """ No matches detected """
        expected = []
        texts = ["vsiuhg89ervhr9egh394hgbo'", "             ", "57h68e5t+n445hj46hjnt4rj+46h8y+5br9hj"]
        patterns = [">.<", ";_;", ":')", '"00', "):"]
        self.process(texts, patterns, expected)

    def test_case_insensitive_match(self):
        """ Test the case insensitive match """
        expected = sorted([(1, 1, 1), (2, 1, 1), (3, 1, 1), (4, 1, 1), (5, 2, 1), (6, 2, 1), (7, 2, 1), (8, 2, 1)])
        texts = ["ab", "cd"]
        patterns = ["AB", "Ab", "aB", "ab", "CD", "Cd", "cD", "cd"]
        self.process(texts, patterns, expected)

    def test_case_insensitive_match_same_char(self):
        """ Test the case insensitive match for same chars """
        expected = sorted([(1, 1, 1),
                           (2, 1, 1),
                           (3, 1, 1),
                           (4, 1, 1),
                           (5, 1, 1),
                           (6, 1, 1),
                           (7, 1, 1),
                           (8, 1, 1),
                           (1, 1, 2),
                           (2, 1, 2),
                           (3, 1, 2),
                           (4, 1, 2),
                           (5, 1, 2),
                           (6, 1, 2),
                           (7, 1, 2),
                           (8, 1, 2),
                           (1, 1, 3),
                           (2, 1, 3),
                           (3, 1, 3),
                           (4, 1, 3),
                           (5, 1, 3),
                           (6, 1, 3),
                           (7, 1, 3),
                           (8, 1, 3),
                           (1, 1, 4),
                           (2, 1, 4),
                           (3, 1, 4),
                           (4, 1, 4),
                           (5, 1, 4),
                           (6, 1, 4),
                           (7, 1, 4),
                           (8, 1, 4)])
        texts = ["aaaAAA"]
        patterns = ["aaa", "aaA", "aAa", "aAA", "Aaa", "AaA", "AAa", "AAA"]
        self.process(texts, patterns, expected)

    def test_case_insensitive_match_multiple_texts(self):
        """ Case insensitive match causes pattern to appear in multiple texts """
        expected = sorted([(1, 1, 1), (2, 1, 1), (4, 1, 1), (5, 1, 1), (6, 1, 1)])
        texts = ["Hello"]
        patterns = ["hello", "HELLO", "world", "HeLLo", "HELLo", "Hello"]
        self.process(texts, patterns, expected)

    def test_case_insensitive_substrings(self):
        """ Case insensitive substrings """
        expected = sorted([(1, 1, 1), (1, 2, 6), (2, 1, 2), (2, 2, 7), (3, 1, 5), (3, 2, 1), (4, 2, 1), (5, 1, 4)])
        texts = ["aabcgt", "GtYYaaAb"]
        patterns = ["AAB", "ab", "gt", "GTY", "C", "00"]
        self.process(texts, patterns, expected)


if __name__ == '__main__':
    unittest.main()
