#!/usr/bin/env python

import sys
import os
import fcntl
import pickle
import os.path
import time


class BotList:

  def __init__ (self):
    self.picklefilename = "/tmp/botlist.pck"
    if os.path.isfile (self.picklefilename):
      self.loadList ()
    else:
      self.bots = []

  def saveList (self):
    picklefile = open (self.picklefilename, "w")
    fcntl.flock (picklefile, fcntl.LOCK_EX)
    pickle.dump (self.bots, picklefile)
    fcntl.flock (picklefile, fcntl.LOCK_UN)
    picklefile.close ()

  def loadList (self):
    picklefile = open (self.picklefilename, "r")
    fcntl.flock (picklefile, fcntl.LOCK_EX)
    self.bots = pickle.load (picklefile)
    fcntl.flock (picklefile, fcntl.LOCK_UN)

  def getList (self):
    return self.bots

  def addBot (self, filename):
    newbot = filename [:-3]
    if os.path.isfile (filename):
      for bot in self.bots:
        if bot == newbot:
          return
      self.bots.append (newbot)

  def getNumBots (self):
    return len (self.bots)

def mainLoop ():
  """
  """
  run = True
  while run:
    botlist = BotList ()
    for b in botlist.getList ():
      try:
        bot = __import__ (b)
        bot.runMe (time.time () + 30)
      except ImportError:
        print "Error importing %s.py" % b
        run = False
  return 0

if __name__ == "__main__":
  sys.exit (mainLoop ())

# vim: tw=0 ts=2 expandtab
# EOF
