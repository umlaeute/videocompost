#!/usr/bin/env python

import sys
import os
import fcntl
import pickle
import time
import signal
from BotList import BotList
from vcconfig import *
from VCLogger import writelog
from Compost import Compost

class VCError (Exception):
  pass

class VCTimeout (VCError):
  def __init__ (self, msg):
    self.msg = msg

class VCInterrupt (VCError):
  def __init__ (self, msg):
    self.msg = msg

def alarmhandler (signum, frame):
  raise VCTimeout ("received signal {0}".format (signum))

def interrupthandler (signum, frame):
  raise VCInterrupt ("received signal {0}".format (signum))

def mainLoop ():
  """
  """
  cycletime = 21600 # 6 hours, 4 cycles a day
  # cycletime = 3600
  # cycletime = 30
  signal.signal (signal.SIGTERM, interrupthandler)
  signal.signal (signal.SIGINT, interrupthandler)
  signal.signal (signal.SIGHUP, interrupthandler)
  savedbotfile = os.path.join (rundir, 'savedbot.txt')

  if os.path.isfile (pidfilename):
    writelog ("[composter]:  stale (?) pidfile found.  Exiting.")
    print "[composter]:  stale (?) pidfile found.  Exiting."
    return 1;
  pidfile = open (pidfilename, "w")
  pidfile.write ("{0}".format (os.getpid ()))
  pidfile.close ()
  writelog ("[composter]:  started with pid {0}".format (os.getpid ()))
  while True:
    botlist = BotList ()
    numbots = len (botlist.bots)
    writelog ("[composter]:  started cycle with {0} seconds per bot".format (cycletime / numbots))
    for b in botlist.getList ():
      if os.path.isfile (savedbotfile):
        f = open (savedbotfile, 'r')
        s = f.readline ()
        f.close ()
        if b == s:
          writelog ("[composter]:  continuing with saved bot {0}".format (b))
          os.remove (savedbotfile)
        else:
          continue
      try:
        bot = __import__ (b)
        reload (bot)
        pid = os.fork ()
        if pid == 0:
          return bot.runMe ()
        else:
          signal.signal (signal.SIGALRM, alarmhandler)
          signal.alarm (cycletime / numbots)
          try:
            writelog ("[composter]:  waiting for {0}[.py] with pid {1}".format (b, pid))
            rv = os.waitpid (pid, 0)
            writelog ("[composter]:  {0}[.py] with pid {1} returned {2}".format (b, pid, rv))
          except VCTimeout:
            os.kill (pid, signal.SIGHUP)
            rv = os.waitpid (pid, 0)
            writelog ("[composter]:  {0} with pid {1} returned {2} on SIGHUP after timeout".format (b, pid, rv))
      except ImportError:
        writelog ("[composter]:  Error importing {0}[.py]".format (b))
      except SyntaxError:
        writelog ("[composter]:  Bot {0} has Syntax Error".format (b))
      except VCInterrupt:
        os.kill (pid, signal.SIGHUP)
        rv = os.waitpid (pid, 0)
        # save the running bot
        f = open (savedbotfile, 'w')
        f.write (b)
        f.close ()
        writelog ("[composter]:  Exiting. Saved bot '{0}' for next run.".format (b))
        os.remove (pidfilename)
        return 0

    compost = Compost ()
    compost.dropFrames ()
    writelog ('[composter]:  {0}'.format (compost.stats ()))
    del compost

  writelog ("[composter]:  Loop terminated abnormally.")
  os.remove (pidfilename)
  return 1

if __name__ == "__main__":
  sys.exit (mainLoop ())

# vim: smartindent sw=2 tw=0 ts=2 expandtab
# EOF
