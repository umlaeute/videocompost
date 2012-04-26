#!/usr/bin/env python

import random
import pickle
import fcntl
import os
import mmap
import sys
import time
from Chunk import Chunk
from VCLogger import writelog
from vcconfig import *

class Compost:
  """
  keep track of sequence of _chunks
  """

  def __init__ (self):
    self._filename = os.path.join (configdir, "Compost.pck")
    self._compost_lock_name = os.path.join (rundir, "Compost.lock")
    if os.path.isfile (self._filename):
      self._filetime = os.stat (self._filename).st_ctime
      self.load ()
    else:
      self._chunks = []
    self._chunk = None
    self._map = None
    self._frames = 0
    self._bytes = 0
    self._pixels = 0
    self._entropy = 0
    self.update ()

  def renew (self):
    if os.stat (self._filename).st_ctime > self._filetime:
      # print "updating list due to _filetime change"
      self.load ()
      self.update ()
      self._filetime = os.stat (self._filename).st_ctime

  def addChunk (self, filename):
    if not os.path.isfile (filename):
      return
    chunk = Chunk (filename)
    if len (self._chunks) > 1:
      random.seed ()
      self._chunks.insert (random.randint (0, len (self._chunks)), chunk)
    else:
      self._chunks.append (chunk)
    self.update ()
    self.save ()

  def save (self):
    picklefile = open (self._filename, 'w')
    fcntl.lockf (picklefile, fcntl.LOCK_EX)
    pickle.dump (self._chunks, picklefile)
    picklefile.flush ()
    os.fsync (picklefile.fileno ())
    fcntl.lockf (picklefile, fcntl.LOCK_UN)
    picklefile.close ()

  def load (self):
    picklefile = open (self._filename, 'r+')
    fcntl.lockf (picklefile, fcntl.LOCK_EX)
    picklefile.flush ()
    self._chunks = pickle.load (picklefile)
    fcntl.lockf (picklefile, fcntl.LOCK_UN)
    picklefile.close ()

  def lockCompost (self):
    while os.path.isfile (self._compost_lock_name):
      time.sleep (1)
    self._compost_lock_file = open (self._compost_lock_name, "a")
    self._compost_lock_file.write ("locked")
    self._compost_lock_file.close ()

  def unlockCompost (self):
    if os.path.isfile (self._compost_lock_name):
      os.unlink (self._compost_lock_name)

  def update (self):
    self._bytes = 0
    self._pixels = 0
    _frames = 0
    for i in range (0, len (self._chunks)):
      self._chunks[i].updateChunk ()
      self._bytes += self._chunks[i]._bytes
      self._pixels += self._chunks[i]._pixels
      if i is not 0:
        _frames += self._chunks[i-1]._frames
      self._chunks[i]._firstframe = _frames
      self._chunks[i]._index = i
      self._chunks[i]._firstpixel = _frames * 76800
      self._chunks[i]._lastpixel = ((_frames + self._chunks[i]._frames - 1) * 76800) + 76799
    self._frames = _frames

  def mapChunk (self, num):
    self.renew ()
    if 0 > num or num >= len (self._chunks):
      return None
    if self._chunk and self._chunk._index is num:
      return self._map
    self.closeChunk ()
    if self._chunks[num].mapChunk ():
      self._chunk = self._chunks[num]
      self._map = self._chunk._map
      self.dumpEntropy ()
      return self._map
    return None

  def closeChunk (self):
    if self._chunk:
      self._chunk.closeChunk ()
    self._chunk = None
    self._map = None

  def mapPixelChunk (self, pixel):
    for i in range (0, len (self._chunks)):
      if self._chunks[i]._firstpixel <= pixel and self._chunks[i]._lastpixel >= pixel:
        return self.mapChunk (i)
    return False
    
  def getPixelColor (self, pixel):
    if not self.mapPixelChunk (pixel):
      return None
    address = (pixel - self._chunk._firstpixel) * 4
    color = []
    for i in range (1, 4):
      color.append (ord (self._map[address+i]))
    return color
      
  def setPixelColor (self, pixel, color = [0, 0, 0]):
    c = [0, 0, 0]
    for i in range (0, len (color)):
      if color[i] < 0:
        c[i] = chr (0)
      elif color[i] > 255:
        c[i] = chr (255)
      else:
        c[i] = chr (color[i])
    if not self.mapPixelChunk (pixel):
      return None
    address = (pixel - self._chunk._firstpixel) * 4
    for i in range (1, 4):
      self._map[address+i] = c[i-1]
      self.addEntropy (ord (c[i-1]))
    return color

  def addEntropy (self, entropy):
    self._entropy += entropy

  def dumpEntropy (self):
    while self._entropy > (self._map.size () + 512):
      self._entropy -= (self._map.size () + 512)
    randdev = open ("/dev/urandom", "w")
    self._map.seek (self._entropy)
    randdev.write (self._map.read (512))
    self._map.seek (0)
    # writelog ("[Compost]:  wrote 512 bytes from chunk {0} starting at {1} to /dev/urandom".format (self._chunk._index, self._entropy))
    randdev.close ()
    self._entropy = 0

  def delete (self):
    print "Deleting all %d _chunks" % len (self._chunks)
    for chunk in self._chunks:
      print "===\nremoving _chunk"
      chunk.showChunk ()
      try:
        os.remove (chunk._filename)
      except OSError:
        pass
      # self._chunks.remove (_chunk)
    os.remove (self._filename)

  def deleteChunk (num):
    pass

  def show (self):
    for chunk in self._chunks:
      chunk.showChunk ()
    print 'totals\nframes: {0}\nbytes: {1}\npixels: {2}'.format (self._frames, self._bytes, self._pixels)

  def dropFrames (self):
    for index in range (random.randint (0, 9), len (self._chunks), random.randint (6, 12)):
      self.mapChunk (index)
      self._chunk.dropLastFrame ()
    self.update ()
    self.save ()

  def runTime (self):
    seconds = self._frames / 25
    hours = seconds / 3600
    seconds = seconds - (3600 * hours)
    minutes = seconds / 60
    seconds = seconds - (60 * minutes)
    return '{0:02d}:{1:02d}:{2:02d}'.format (hours, minutes, seconds)

  def stats (self):
    return 'Compost stats: chunks={0}, bytes={1}, frames={2}, pixels={3}, duration(hh:mm:ss)={4}'.format (
      len (self._chunks), self._bytes, self._frames, self._pixels, self.runTime ())

def runcmd (cmd, compost):
  if cmd == "show":
    compost.show ()
    return 0
  if cmd == "stats":
    print compost.stats ()
    return 0
  if cmd == "delete":
    compost.delete ()
    return 0
  if cmd == "":
    return 0
  print ">> Unknown command '{0}'".format (cmd)
  return 0

def cmdline ():
  print "VideoCompost command line interface.  Type ctrl-d to exit."
  print "loading compost ..."

  compost = Compost ()

  while True:
    try:
      cmd = raw_input ("<< ")
      runcmd (cmd, compost)
    except EOFError:
      print "Exiting ..."
      return 0

if __name__ == "__main__":
  sys.exit (cmdline ())

# vim: tw=0 ts=2 expandtab
# EOF
