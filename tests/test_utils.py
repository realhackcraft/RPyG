import unittest
from utils.array import ArrayUtils

class TestUtils(unittest.TestCase):
  def test_array_join(self):
    back = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']

    input1 = [
      back,
      back,
      back,
      back,
    ]
    
    a = ['a', 'a', 'a', 'a', 'a', 'a']
    b = ['b', 'b', 'b', 'b', 'b', 'b']
    c = ['c', 'c', 'c', 'c', 'c', 'c']
    x = ['x', 'x', 'x', 'x']

    input2 = [
      a,
      b,
      c
    ]

    output1 = [
      back,
      a + x,
      b + x,
      c + x,
    ]

    
    output2 = [
      a + x,
      b + x,
      c + x,
      back,
    ]

    result = ArrayUtils.join_2d_arrays(input1, input2)
    result2 = ArrayUtils.join_2d_arrays(input1, input2, (0, 1))
    
    print()

    for i in result:
      for j in i:
        print(j, end=" ")
      print()
    print()
    for i in result2:
      for j in i:
        print(j, end=" ")
      print()

    
    self.assertEqual(ArrayUtils.join_2d_arrays(input1, input2), output1)
    self.assertEqual(result2, output2)

