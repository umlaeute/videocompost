import time
import os.path
import pickle
import signal
import random
from Compost import Compost
from VCLogger import writelog
from vcconfig import *

"""
Adapt config to your needs.  Use loadConfig () and saveConfig ()
to store data across runs.
"""
config = {}

compost = Compost ()

class BotError (Exception):
  def __init__ (self, msg):
    self.msg = msg

def signalhandler (signum, frame):
  raise BotError ("received signal {0}".format (signum))

def loadConfig ():
  global config
  filename = os.path.join (configdir, "%s.config" % __name__)
  if os.path.isfile (filename):
    infile = open (filename, "r")
    config = pickle.load (infile)
    infile.close ()

def saveConfig ():
  global config
  filename = os.path.join (configdir, "%s.config" % __name__)
  outfile = open (filename, "w")
  pickle.dump (config, outfile)
  outfile.close ()

def runMe ():
  """
  swapping random lines within a frame
  """
  # each image is 320x240 pixels of 4 bytes
  width = 320
  height = 240
  csize = 4
  wsize= width*csize
  size = width*height*csize

  random.seed()
  
  loadConfig ()
  signal.signal (signal.SIGHUP, signalhandler)
  signal.signal (signal.SIGINT, signalhandler)
  writelog ("[{0}]: started".format (__name__))

  try:
    chunk1 = random.randint(0, len (compost._chunks))
    chunk2 = chunk1
    while chunk2 == chunk1:
      chunk2 = random.randint(0, len (compost._chunks))
    compost.mapChunk(chunk1)
    # this try: clause can be deleted I guess
    try:
      frameindex = random.randint(0, len (compost._map) / size)
    except TypeError:
      writelog ("[{0}]: caught exception.  for chunk {1}".format (__name__, chunk1))
    frame = compost._map[frameindex:(frameindex+size)]
    compost.mapChunk(chunk2)
    frameindex = random.randint(0, len (compost._map) / size)
    compost._map[frameindex:(frameindex+size)]=frame
    compost.addEntropy (frameindex)
    saveConfig ()
  except BotError as e:
    writelog ("[{0}]: caught exception {1}.  Exiting".format (__name__, e.msg))
    saveConfig ()
    writelog ("[{0}]: caught exception {1}.  Wrote {2} chunks and {3} bytes to config".format (__name__, e.msg, chunk, byte))
    return 0

  # print "{0} has done one cyle. resetting config".format (__name__)
  saveConfig ()
  return 0
  
if __name__ == "__main__":
  pass

# vim: tw=0 ts=2 expandtab
# EOF
