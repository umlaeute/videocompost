"""
python classes used by this bot
"""
import time
import os.path
import pickle
import signal
"""
custom classes to access video compost data
"""
from Compost import Compost
from VCLogger import writelog
from vcconfig import *

"""
Adapt config to your needs.  Use loadConfig () and saveConfig ()
to store data across runs.
"""
config = {}
config['forward2frame'] = 0
config['forward2line'] = 0
config['forward2pixel'] = 0

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

  def __str__ (self):
    return repr (self.msg)

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
  filename = os.path.join (configdir, "{0}.config".format (__name__))
  if os.path.isfile (filename):
    infile = open (filename, "r")
    config = pickle.load (infile)
    infile.close ()

def saveConfig ():
  """
  store config to file
  """
  global config
  filename = os.path.join (configdir, "{0}.config".format (__name__))
  outfile = open (filename, "w")
  pickle.dump (config, outfile)
  outfile.close ()

def runMe ():
  """
  main method called by composter.py
  """
  signal.signal (signal.SIGHUP, signalhandler)
  signal.signal (signal.SIGINT, signalhandler)

  width = 320
  height = 240
  frame_size = width * height
  frame_number = 0
  line_number = 0

  try:

    loadConfig ()

    forwardframe = False
    if config['forward2frame'] > 0:
      forwardframe = True

    forwardline = False
    if config['forward2line'] > 0:
      forwardline = True

    forwardpixel = False
    if config['forward2pixel'] > 0:
      forwardpixel = True

    writelog ("[{0}]:  started".format (__name__))

    for line in range (line_number, height):
      if forwardline:
        if line < config['forward2line']:
          # print 'forwarding line'
          continue
        else:
          # writelog ('[{0}]:  forwarded to line {1}'.format (__name__, config['forward2line']))
          forwardline = False

      for frame in range (frame_number, compost._frames):
        if forwardframe:
          if frame < config['forward2frame']:
            # print 'forwarding frame'
            continue
          else:
            writelog ('[{0}]:  forwarded to frame {1}'.format (__name__, config['forward2frame']))
            forwardframe = False

        start_pixel = frame_size * frame + line * width
        for pixel in range (start_pixel, start_pixel + width):
          if forwardpixel:
            if pixel < config['forward2pixel']:
              # print 'forwarding pixel'
              continue
            else:
              # writelog ('[{0}]:  forwarded to pixel {1}'.format (__name__, config['forward2pixel']))
              forwardpixel = False

          color = compost.getPixelColor (pixel)
          bw = int (color[0] * 0.3 + color[1] * 0.59 + color[2] * 0.11)
          compost.setPixelColor (pixel, [bw, bw, bw])
          # print 'pixel {0} set to {1},{1},{1}'.format (pixel, bw)

      # give the last bw to the prng entropy pool
      compost.addEntropy (bw)
      writelog ('[{0}]:  finished line {1}.'.format (__name__, line))

    # remeber that we are done
    config['forward2frame'] = 0
    config['forward2line'] = 0
    config['forward2pixel'] = 0
    saveConfig ()

  except Exception as e:
    config['forward2frame'] = frame
    config['forward2line'] = line
    config['forward2pixel'] = pixel
    saveConfig ()
    writelog ("[{0}]:  Caught exception ({1}).  Exiting.".format (__name__, e))
    return 0

  return 0
  
if __name__ == "__main__":
  pass

# vim: tw=0 ts=2 expandtab
# EOF
