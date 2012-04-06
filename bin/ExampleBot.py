"""

Example for a videocompost bot This will be imported by composter.py
which then will call this module's runMe () method.

Version 0.2 May 7, 2011

Place your code in the runMe () method below.  If you want to leave log
messages, use the writelog () method.  It would be nice to provide the
bot's name in log messages, e.g.:

  writelog ("[{0}]: was here".format (__name__))

Please don't use print statements in your code.  We will remove them
anyhow. Also don't be too chatty with log messages.

Every bot will get a limited amount of time to work on video data.
composter.py keeps track of time and sends signal.SIGHUP to a bot whose
timeout has been reached.  You should use the prepared signal handling
method to save any data you might want to preserve for the next run.

To access video data you have two options:

* pixel access

  There are two methods to access arbitraty pixels in the video:

    compost.getPixelColor (pixel)

  which returns a 3-element list with the pixels RGB values and

    compost.setPixelColor (pixel, color)

  which will set the pixel's color to color;  color must be a 3-element
  list containing the desired RGB values.  To set a the pixel 123456789
  to black you would issue

    compost.setPixelColor (123456789, [0, 0, 0])

  The total number of pixels available is

    compost._pixels

  To run through all the pixels in the video you could thus use a loop
  like

    for pixel in range (0, compost._pixels):
      do something with pixel

* mmap access

  Use the compost module's method mapChunk (num) to map a chunk into
  memory.  To map the third chunk issue

    compost.mapChunk (3)

  The mapped chunk can be accessed via compost._map.  See
  the python documentation [1] for details on mmap objects.

  Video data is in raw format.  We use 4 bytes (32 bits) per pixel.  The
  first byte is actually unused, bytes 2 to 4 are RGB values.

Be gentle to pixels ;)  Your code will be running for more than a year!
Over time, more data will be added to the pool, so there might be data
you have not seen before.

[1]  http://docs.python.org/release/2.6.6/library/mmap.html
"""

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
config["myname"] = __name__
config["counter"] = 0

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
    config = pickle.load (infile)
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
  try:
    """
    your code here
    """
    loadConfig ()
    writelog ("[{0}] counting {1}".format (__name__, config["counter"]))
    config["counter"] += 1
    saveConfig ()

  except BotError as e:
    saveConfig ()
    return 0

  """
  return a number != 0 to indicate an error to composter.py
  """
  return 0
  
if __name__ == "__main__":
  pass

# vim: tw=0 ts=2 expandtab
# EOF
