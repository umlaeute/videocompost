import time
import os.path
import pickle
import signal
from random import randint
from Compost import Compost
from VCLogger import writelog
from vcconfig import *

"""
Adapt config to your needs.  Use loadConfig () and saveConfig ()
to store data across runs.
"""
config = {}
config["chunk"] = 0
config["byte"] = 2

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
  slowly removing green and black values
  """
  loadConfig ()
  signal.signal (signal.SIGHUP, signalhandler)
  signal.signal (signal.SIGINT, signalhandler)
  writelog ("[{0}]: starting to work on chunk {1} at byte {2}".format (
    __name__, config["chunk"], config["byte"]))
  try:
    for chunk in range (config["chunk"], len (compost._chunks)):
      compost.mapChunk (chunk)
      for byte in range (config["byte"], len (compost._map), 4):
        green = ord (compost._map[byte])
        blue = ord (compost._map[byte+1])
        if green > 0:
          compost._map[byte] = chr (green - 1)
          compost.addEntropy (green - 1)
        if blue > 0:
          compost._map[byte+1] = chr (blue - 1)
          compost.addEntropy (blue - 1)
      config["chunk"] = chunk
      config["byte"] = 2
      saveConfig ()
  except BotError as e:
    config["chunk"] = chunk
    config["byte"] = byte
    saveConfig ()
    writelog ("[{0}]: caught exception {1}.  Saving chunk {2} at byte {3} for next run".format (
      __name__, e.msg, chunk, byte))
    return 0

  config["chunk"] = 0
  config["byte"] = 2
  saveConfig ()
  return 0
  
if __name__ == "__main__":
  pass

# vim: tw=0 ts=2 expandtab
# EOF
