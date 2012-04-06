#!/usr/bin/env python

import time
import sys
import fcntl
from vcconfig import *

def writelog (line):
  line = line.strip ("\n")
  line = line.strip ()
  logfile = open (logfilename, "a")
  fcntl.flock (logfile, fcntl.LOCK_EX)
  logfile.write ("{0}: {1}\n".format (time.strftime("%a, %d %b %Y %H:%M:%S"), line))
  fcntl.flock (logfile, fcntl.LOCK_UN)
  logfile.close ()
  try:
    if logstderr==True:
      print line
  except NameError:
    pass

if __name__ == "__main__":
  if len (sys.argv) < 2:
    sys.exit (0)
  line = ""
  for i in range (1, len (sys.argv)):
    line = "{0}{1} ".format (line, sys.argv[i])
  writelog (line)

# vim: ts=2 tw=0 expantab
# EOF
