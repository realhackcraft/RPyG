"""
Utilities related to math
"""
from math import atan2, sqrt
from typing import Tuple


class Math:
  @staticmethod
  def diff(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> Tuple[int, int]:
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]

    return (dx, dy)


  @staticmethod
  def distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    dx, dy = Math.diff(pos1, pos2) 

    return sqrt(dx**2+dy**2) # sqrt x^2 + y^2

  @staticmethod
  def angle(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    dx, dy = Math.diff(pos1, pos2) 

    return atan2(dy, dx)
