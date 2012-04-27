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

  def __str__ (self):
    return repr (self.msg)

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
  
  signal.signal (signal.SIGHUP, signalhandler)
  signal.signal (signal.SIGINT, signalhandler)
  writelog ("[{0}]: started".format (__name__))

  try:
    chunk1 = random.randint(0, len (compost._chunks) - 1)
    chunk2 = chunk1
    while chunk2 == chunk1:
      chunk2 = random.randint(0, len (compost._chunks) - 1)

    # save frame1 from chunk1
    compost.mapChunk(chunk1)
    frameindex1 = random.randint(0, (len (compost._map) / size) - 1) * size
    frame1 = compost._map[frameindex1:frameindex1 + size]
    
    # save frame2 from chunk2
    compost.mapChunk(chunk2)
    frameindex2 = random.randint(0, (len (compost._map) / size) - 1) * size
    frame2 = compost._map[frameindex2:frameindex2 + size]

    # write frame1 to chunk2 @ frameindex2
    compost._map[frameindex2:frameindex2 + size] = frame1

    # write frame2 to chunk1 @ frameindex1
    compost.mapChunk (chunk1)
    compost._map[frameindex1:frameindex1 + size] = frame2

    compost.addEntropy (frameindex1 + frameindex2)

  except Exception as e:
    writelog ("[{0}]:  Caught exception ({1}).  Exiting".format (__name__, e))
    return 0

  # print "{0} has done one cyle. resetting config".format (__name__)
  return 0
  
if __name__ == "__main__":
  pass

# vim: tw=0 ts=2 expandtab
# EOF
