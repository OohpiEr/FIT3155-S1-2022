import glob
import os
import unittest


class TestMyUnzip(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        """ Remove All txt and asc files after testing """
        for txt_file in glob.glob(os.path.join(os.getcwd(), '*.txt')):
            os.remove(txt_file)
        for asc_file in glob.glob(os.path.join(os.getcwd(), '*.asc')):
            os.remove(asc_file)

    def process(self, filename):
        os.system('cmd /c python myunzip.py outputs/' + filename + ".bin")
        expected = open("inputs/" + filename, encoding="utf-8").read()
        actual = open(filename, encoding="utf-8").read()
        self.assertEqual(expected, actual, msg="Decoded file is not equal to original")

    def test_sample_1(self):
        """ From Lecture Slides (Huffman Example) """
        self.process("sample1.txt")

    def test_sample_2(self):
        """ From Tutorial (LZ77 Encode) """
        self.process("sample2.asc")

    def test_sample_3(self):
        """ From Tutorial (LZ77 Decode) """
        self.process("sample3.txt")

    def test_sample_4(self):
        """ From Assignment Spec """
        self.process("x.asc")

    def test_empty(self):
        """ Empty File """
        self.process("empty.txt")

    def test_whitespace(self):
        """ File with only whitespace """
        self.process("whitespace.asc")

    def test_single_char(self):
        """ File contains only 1 char """
        self.process("single_char.txt")

    def test_all_same(self):
        """ All chars in file are the same """
        self.process("all_same.asc")

    def test_all_different(self):
        """ All chars in file are different """
        self.process("all_different.txt")

    def test_window_overflow(self):
        """ A match overflows from window to lookahead (From https://www.youtube.com/watch?v=2gr-Qncs_AI) """
        self.process("window_overflow.asc")

    def test_lookahead_overflow(self):
        """ A match overflows from window and past the lookahead """
        self.process("lookahead_overflow.txt")

    def test_ending(self):
        """ When the last triple should be replaced with a char """
        self.process("ending.asc")

    def test_small_random(self):
        """ Small Random Case """
        self.process("small_random.txt")

    def test_medium_random(self):
        """ Medium Random Case """
        self.process("medium_random.asc")

    def test_large_random(self):
        """ Large Random Case """
        self.process("large_random.txt")

    def test_large_unrandom(self):
        """ Largest Not Random Case (Renamed to test if that affects decoding) """
        os.system('cmd /c python myunzip.py outputs/renamed.bin')
        expected = open("inputs/large_unrandom.asc", encoding="utf-8").read()
        actual = open("large_unrandom.asc", encoding="utf-8").read()
        self.assertEqual(expected, actual, msg="Decoded file is not equal to original")


if __name__ == '__main__':
    unittest.main()
