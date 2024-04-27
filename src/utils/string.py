"""
Utilities to manipulate strings
"""

import re

class StringUtils:
  @staticmethod
  def split_string_with_capitals(s: str):
    return re.findall('[a-zA-Z][^A-Z]*', s)
 
