"""

Example for a videocompost bot This will be imported by composter.py
which then will call this module's runMe () method.

Version 0.3 May 12, 2012

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

  where 'pixel' is the index of the pixel yout want, ranging from 0 to
  compost._pixels.  It returns a 3-element list with the pixels RGB values and

    compost.setPixelColor (pixel, color)

  which will set the pixel's color to color;  color must be a 3-element
  list containing the desired RGB values.  To set the pixel 123456789 to
  black you would issue

    compost.setPixelColor (123456789, [0, 0, 0])

  The total number of pixels available is

    compost._pixels

  To run through all the pixels in the video you could thus use a loop
  like

    for pixel in range (0, compost._pixels):
      do something with pixel

* mmap access

  Use the compost module's method mapChunk (num) to map a chunk into
  memory.  To map the third chunk you would call

    compost.mapChunk (3)

  The mapped chunk can be accessed via compost._map.  See
  the python documentation [1] for details on mmap objects.

  Video data is in raw format.  We use 4 bytes (32 bits) per pixel.  The
  first byte is actually unused, bytes 2 to 4 are RGB values.

Be gentle to pixels ;)  Your code will be running for more than a year!
Over time, more data will be added to the pool, so there might be data
you have not seen before.

When saving the state of your bot for the next run, keep in mind that
frames/pixels might disappear!  After each completed cycle, a random number of
frames will be deleted from about 10% of all chunks in compost.

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

  try:
    loadConfig ()
    writelog ("[{0}]:  started".format (__name__))
    saveConfig ()
    """
    Your code should go here.  Some examples illustrate how
    things can work.

    Example loop over all pixels, saving the current pixels
    color:
    """

    for pixel in range (0, compost._pixles):
      color = compost.getPixelColor (pixel)

    """
    Example on how to use the memory mapping way of accessing data.
    We just save the three color channels of the first pixel from chunk
    number 4:
    """

    compost.mapChunk (4)
    red = ord (compost._map[1])
    green = ord (compost._map[2])
    blue = ord (compost._map[3])

    """
    make use of the addEntropy method every once a while to
    help feed the machine's entropy pool.  Like here we feed it 
    the product of the three color channels from above
    """

    compost.addEntropy (red * green * blue)

  except Exception as e:
    saveConfig ()
    writelog ("[{0}]:  Caught exception ({1}).  Exiting.".format (__name__, e))
    return 0

  return 0
  
if __name__ == "__main__":
  pass

# vim: tw=0 ts=2 expandtab
# EOF
