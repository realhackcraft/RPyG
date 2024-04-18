from classes.map import List


def join_arrays(array1: List[List[str]], array2: List[List[str]], blank_char:str = "") -> List[List[str]]:
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

  # Remove the first row, which is empty
  ret_array

  return ret_array


# Example usage
input1 = [
    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
]

input2 = [
    ['a', 'a', 'a', 'a', 'a', 'a'],
    ['a', 'a', 'a', 'a', 'a', 'a'],
]

output = join_arrays(input1, input2, "")

# Print the output
for row in output:
    print(' '.join(row))


