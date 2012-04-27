"""
BlueShift - reduce red and green channels for certain regions, leave
blue channel untouched.
"""

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
config['continue'] = False

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

def setValues ():
  height = random.randint (32, 80)
  width = random.randint (24, 60)
  duration = random.randint (15, 90)
  start = random.randint (0, compost._pixels - duration * height * width)
  return height, width, duration, start

def runMe ():
  """
  slowly removing red and green values for a small region
  """
  signal.signal (signal.SIGHUP, signalhandler)
  signal.signal (signal.SIGINT, signalhandler)

  loadConfig ()

  writelog ("[{0}]:  Started.  Continue set to {1}.".format (__name__, config['continue']))

  width = 320
  height = 240
  framesize = width * height
 
  # check if we have to finish a previously worked region
  if config['continue']:
    region_width = config['region_width']
    region_height = config['region_height']
    start_pixel = config['start_pixel']
    duration = config['duration']
  else:
    region_height, region_width, duration, start_pixel = setValues ()

  try:
    # this bot runs indefinitely (until signal is received)
    while True:
      # loop for duration frames
      for frame in range (0, duration):
        # loop over lines
        for line in range (start_pixel, start_pixel + width * region_height, width):
          # loop over pixels in a line
          for index in range (0, region_width):
            pixel = duration + line + index
            color = compost.getPixelColor (pixel)
            # check if we have color.  frames get removed so we could be
            # where there is nothing left ...
            if color:
              color[0] = color[0] / 10
              color[1] = color[1] / 10
              compost.setPixelColor (pixel, color)

      # set new values for next loop
      region_height, region_width, duration, start_pixel = setValues ()

  except Exception as e:
    config['region_height'] = region_height
    config['region_width'] = region_width
    config['start_pixel'] = start_pixel
    config['duration'] = duration
    config['continue'] = True
    saveConfig ()
    writelog ("[{0}]:  Caught excption ({1}).  Saving values for next run".format (
      __name__, e))
    return 0

  return 0
  
if __name__ == "__main__":
  pass

# vim: tw=0 sw=2 smartindent expandtab
# EOF
