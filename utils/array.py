from typing import List

class ArrayUtils:
  @staticmethod
  def join_2d_arrays(array1: List[List[str]], array2: List[List[str]], blank_char:str = "") -> List[List[str]]:
    ret_array = [[]]
    for i, row in enumerate(array1):
      ret_inner_array = []
      for j, item1 in enumerate(row):
        if i >= len(array2) or j >= len(array2[i]):
          ret_inner_array.append(item1)
          continue
        item2 = array2[i][j]
        if item2 == blank_char:
          ret_inner_array.append(array1)
          continue
        ret_inner_array.append(item2)
      ret_array.append(ret_inner_array)

    # Remove the first, empty row of the array 
    ret_array.pop(0)
    return ret_array
