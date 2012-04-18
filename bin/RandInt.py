#!/usr/bin/env python

import sys
from random import randint

"""
return a random integer between 1 and sys.argv[1]
"""

if __name__ == "__main__":
  if len (sys.argv) < 2:
    sys.exit (0)
  try:
    maxint = int (sys.argv[1])
  except ValueError:
    sys.exit (1)
  print randint (1, maxint)

# vim: ts=2 tw=0 expandtab sw=2
# EOF
