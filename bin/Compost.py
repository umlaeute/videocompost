#!/usr/bin/env python

from random import randint
import pickle
import fcntl
import os
import mmap
import sys
from Chunk import Chunk
from vcconfig import *

class Compost:
  """
  keep track of sequence of _chunks
  """

  def __init__ (self):
    self._filename = os.path.join (configdir, "Compost.pck")
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
      index = randint (0, len (self._chunks))
      self._chunks.insert (index, chunk)
    else:
      self._chunks.append (chunk)
    self.update ()
    self.save ()

  def save (self):
    picklefile = open (self._filename, "w")
    fcntl.flock (picklefile, fcntl.LOCK_EX)
    pickle.dump (self._chunks, picklefile)
    fcntl.flock (picklefile, fcntl.LOCK_UN)
    picklefile.close ()

  def load (self):
    picklefile = open (self._filename, "r")
    fcntl.flock (picklefile, fcntl.LOCK_EX)
    self._chunks = pickle.load (picklefile)
    fcntl.flock (picklefile, fcntl.LOCK_UN)

  def update (self):
    self._bytes = 0
    self._pixels = 0
    _frames = 0
    for i in range (0, len (self._chunks)):
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
    # print "Failed mapping _chunk for pixel %d" % pixel
    return False
    
  def getPixelColor (self, pixel):
    if not self._chunk:
      if not self.mapPixelChunk (pixel):
        return False
    elif pixel < self._chunk._firstpixel or pixel > self._chunk._lastpixel:
      self.closeChunk ()
      if not self.mapPixelChunk (pixel):
        return False
    address = (pixel - self._chunk._firstpixel) * 4
    # print "getPixelColor for pixel %d at local address %d" % (pixel, address)
    color = []
    for i in range (1, 4):
      color.append (ord (self._chunk._map[address+i]))
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
    if not self._chunk:
      if not self.mapPixelChunk (pixel):
        # print "Failed setting color to pixel %d" % pixel
        return None
    elif pixel < self._chunk._firstpixel or pixel > self._chunk._lastpixel:
      self.closeChunk ()
      if not self.mapPixelChunk (pixel):
        # print "Failed setting color to pixel %d" % pixel
        return None
    address = (pixel - self._chunk._firstpixel) * 4
    # print "setPixelColor for pixel %d at local address %d to r=%d g=%d b=%d" % (pixel, address, ord (c[0]), ord (c[1]), ord (c[2]))
    for i in range (1, 4):
      self._map[address+i] = c[i-1]
    return color

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

def runcmd (cmd):
  compost = Compost ()

  if cmd == "show":
    compost.show ()
    return 0
  if cmd == "delete":
    compost.delete ()
    return 0
  print ">> Unknown command '{0}'".format (cmd)
  return 0

def cmdline ():
  print "VideoCompost command line interface.  Type ctrl-d to exit."
  while True:
    try:
      cmd = raw_input ("<< ")
      runcmd (cmd)
    except EOFError:
      print "Exiting ..."
      return 0

if __name__ == "__main__":
  sys.exit (cmdline ())

# vim: tw=0 ts=2 expandtab
# EOF
