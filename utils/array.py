from typing import List, Tuple

class ArrayUtils:
  @staticmethod
  def join_2d_arrays(matrix1: List[List[str]], matrix2: List[List[str]], offsets: Tuple[int, int]=(0,0)) -> List[List[str]]:
    # Get the dimensions of the matrices
    rows1, cols1 = len(matrix1), len(matrix1[0])
    rows2, cols2 = len(matrix2), len(matrix2[0])

    # Ensure that the dimensions of the matrices are compatible for overlaying
    if rows2 + offsets[1] > rows1 or cols2 + offsets[0] > cols1:
        raise ValueError("Matrix 2 dimensions with offsets are larger than Matrix 1 dimensions.")

    # Create a new list to hold the overlaid matrix
    overlaid_matrix = [row[:] for row in matrix1]  # Copy Matrix 1

    # Overlay Matrix 2 on top of Matrix 1 with offsets
    for i in range(rows2):
        for j in range(cols2):
            overlaid_matrix[i + offsets[1]][j + offsets[0]] = matrix2[i][j]

    return overlaid_matrix 
