import unittest

from utils.array import ArrayUtils


class TestArrayUtils(unittest.TestCase):
    def test_join_2d_arrays(self):
        matrix1 = [["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]]
        matrix2 = [["1", "2"], ["3", "4"]]
        expected_result = [["1", "2", "c"], ["3", "4", "f"], ["g", "h", "i"]]

        result = ArrayUtils.join_2d_arrays(matrix1, matrix2, (0, 0))
        self.assertEqual(result, expected_result)

    def test_offset_transparent_characters(self):
        matrix1 = [["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]]
        matrix2 = [["1", "2"], ["3", "4"]]
        expected_result = [["a", "b", "c"], ["d", "e", "2"], ["g", "3", "4"]]
        self.assertEqual(
            ArrayUtils.join_2d_arrays(matrix1, matrix2, (1, 1), "1"), expected_result
        )

    def test_invalid_offset(self):
        matrix1 = [["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]]
        matrix2 = [["1", "2"], ["3", "4"]]
        with self.assertRaises(ValueError):
            ArrayUtils.join_2d_arrays(matrix1, matrix2, (2, 2))
