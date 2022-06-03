import glob
import os
import unittest


class TestMyZip(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        """ Remove All txt and asc files after testing """
        for txt_file in glob.glob(os.path.join(os.getcwd(), '*.txt')):
            os.remove(txt_file)
        for asc_file in glob.glob(os.path.join(os.getcwd(), '*.asc')):
            os.remove(asc_file)

    def process(self, filename, window, lookahead):
        os.system('cmd /c python myzip.py ' + filename + " " + str(window) + " " + str(lookahead))

    def test_sample_1(self):
        """ From Lecture Slides (Huffman Example) """
        self.process("sample1.txt", 5, 5)

    def test_sample_2(self):
        """ From Tutorial (LZ77 Encode) """
        self.process("sample2.asc", 15, 15)

    def test_sample_3(self):
        """ From Tutorial (LZ77 Decode) """
        self.process("sample3.txt", 10, 10)

    def test_sample_4(self):
        """ From Assignment Spec """
        self.process("x.asc", 6, 4)

    def test_empty(self):
        """ Empty File """
        self.process("empty.txt", 10, 10)

    def test_whitespace(self):
        """ File with only whitespace """
        self.process("whitespace.asc", 10, 10)

    def test_single_char(self):
        """ File contains only 1 char """
        self.process("single_char.txt", 10, 10)

    def test_all_same(self):
        """ All chars in file are the same """
        self.process("all_same.asc", 10, 10)

    def test_all_different(self):
        """ All chars in file are different """
        self.process("all_different.txt", 1, 1)

    def test_window_overflow(self):
        """ A match overflows from window to lookahead (From https://www.youtube.com/watch?v=2gr-Qncs_AI) """
        self.process("window_overflow.asc", 3, 5)

    def test_lookahead_overflow(self):
        """ A match overflows from window and past the lookahead """
        self.process("lookahead_overflow.txt", 2, 2)

    def test_ending(self):
        """ When the last triple should be replaced with a char """
        self.process("ending.asc", 3, 3)

    def test_small_random(self):
        """ Small Random Case """
        self.process("small_random.txt", 10, 10)

    def test_medium_random(self):
        """ Medium Random Case """
        self.process("medium_random.asc", 162, 212)

    def test_large_random(self):
        """ Large Random Case """
        self.process("large_random.txt", 244, 455)

    def test_large_unrandom(self):
        """ Largest Not Random Case """
        self.process("large_unrandom.asc", 400, 400)


if __name__ == '__main__':
    unittest.main()
