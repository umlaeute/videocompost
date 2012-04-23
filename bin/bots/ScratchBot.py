"""
leave scratches in the video
"""

"""
python classes used by this bot
"""
import time
import os.path
import pickle
import signal
import random

"""
custom classes to access video compost data
"""
from Compost import Compost
from VCLogger import writelog
from vcconfig import *

"""
Adapt config to your needs.  Use loadConfig () and saveConfig ()
to store data across runs.

not used here!
"""
config = {}
config["name"] = __name__

"""
create an instance of Compost to access video data
"""
compost = Compost ()

class BotError (Exception):
  """
  custom exception
  """
  def __init__ (self, msg):
    self.msg = msg

def signalhandler (signum, frame):
  """
  handler for signals
  """
  raise BotError ("received signal {0}".format (signum))

def loadConfig ():
  """
  load config from file if available
  """
  global config
  filename = os.path.join (configdir, "%s.config" % __name__)
  if os.path.isfile (filename):
    infile = open (filename, "r")
    try:
      config = pickle.load (infile)
    except:
      config["name"] = __name__
      config["chunk"] = 0
    infile.close ()

def saveConfig ():
  """
  store config to file
  """
  global config
  filename = os.path.join (configdir, "%s.config" % __name__)
  outfile = open (filename, "w")
  pickle.dump (config, outfile)
  outfile.close ()

def runMe ():
  """
  main method called by composter.py
  """
  signal.signal (signal.SIGHUP, signalhandler)
  signal.signal (signal.SIGINT, signalhandler)

  frame_size = 76800
  frame_width = 320
  white = 255
  min_length = 5       # shortest scratch
  max_length = 120     # longest scratch
  min_duration = 1     # lasts for 1 frame
  max_duration = 125   # lasts for 125 frames

  writelog ("[{0}]:  starting to make {1} scratches in video".format (
    __name__, len (compost._chunks)))

  # loop over the number of chunks available
  for chunk in range (0, len (compost._chunks)):

    try:
      random.seed ()
      length = random.randint (min_length, max_length)
      duration = random.randint (min_duration, max_duration)
      startpixel = random.randint (0, (compost._pixels - length) - duration)

      for i in range (0, duration):
        startpixel += frame_size * i
        for pixel in range (startpixel, startpixel + length * frame_width, frame_width):
          compost.setPixelColor (pixel, [white, white, white])

      compost.addEntropy (startpixel + (length * duration))

      del length
      del duration
      del startpixel

    except BotError as e:
     return 0

  """
  return a number != 0 to indicate an error to composter.py
  """
  return 0
  
if __name__ == "__main__":
  pass

# vim: tw=0 ts=2 expandtab
# EOF
