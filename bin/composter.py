#!/usr/bin/env python

import sys
import os
import fcntl
import pickle
import time
from BotList import BotList
from vcconfig import *
from Logger import writelog

def keepRunning ():
  # FIXME:  check what we read from runfile
  if os.path.isfile (runfilename):
    runfile = open (runfilename, "r")
    run = int (runfile.read ())
    runfile.close ()
    return run
  return True

def mainLoop ():
  """
  """
  # run = True
  cycletime = 21600 # 6 hours, 4 cycles a day
  # cycletime = 3600
  # cycletime = 30
  writelog ("[composter]: started with cycletime {0} seconds".format (cycletime))
  # FIXME:  call keepRunning more often
  while keepRunning ():
    botlist = BotList ()
    numbots = len (botlist.bots)
    for b in botlist.getList ():
      try:
        bot = __import__ (b)
        reload (bot)
        writelog ("[composter]: running {0}[.py]".format (b))
        # FIXME:  redirect output from bot to logfile or dev/null
        bot.runMe (time.time () + (cycletime / numbots))
      except ImportError:
        writelog ("[composter]: Error importing {0}[.py]".format (b))
  writelog ("[composter]: Exiting ...")
  return 0

if __name__ == "__main__":
  sys.exit (mainLoop ())

# vim: tw=0 ts=2 expandtab
# EOF
