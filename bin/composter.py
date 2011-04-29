#!/usr/bin/env python

import sys
import os
import fcntl
import pickle
import os.path
import time
from BotList import BotList
from vcconfig import *

def mainLoop ():
  """
  """
  run = True
  cycletime = 21600 # 6 hours, 4 cycles a day
  # cycletime = 3600
  # cycletime = 30
  while run:
    botlist = BotList ()
    numbots = len (botlist.bots)
    for b in botlist.getList ():
      try:
        bot = __import__ (b)
        reload (bot)
        bot.runMe (time.time () + (cycletime / numbots))
      except ImportError:
        print "Error importing %s.py" % b
        run = False
  return 0

if __name__ == "__main__":
  sys.exit (mainLoop ())

# vim: tw=0 ts=2 expandtab
# EOF
