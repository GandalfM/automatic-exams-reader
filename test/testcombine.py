from aer.utils.utils import combine

__author__ = 'Bartek'

import unittest


class TestCombine(unittest.TestCase):
    def test_combine_works(self):
        a = lambda x: x + "a"
        b = lambda x: x + "b"
        c = combine(a, b)
        result = c("z")
        self.assertEqual(result, "zab")
