import unittest
from utils.array import ArrayUtils

class TestUtils(unittest.TestCase):
  def test_array_join(self):
    input1 = [
      ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
      ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
      ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
    ]

    input2 = [
      ['a', 'a', 'a', 'a', 'a', 'a'],
      ['a', 'a', 'a', 'a', 'a', 'a'],
    ]

    output = ArrayUtils.join_2d_arrays(input1, input2)
    
    self.assertEqual(output, [
      ['a', 'a', 'a', 'a', 'a', 'a', 'x', 'x', 'x', 'x'],
      ['a', 'a', 'a', 'a', 'a', 'a', 'x', 'x', 'x', 'x'],
      ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
    ])

