#!/usr/bin/env python

import os
import mmap

class Chunk:

  def __init__ (self, filename):
    self._filename = filename
    self._bytes = os.stat (self._filename).st_size
    self._frames = self._bytes / 307200
    self._pixels = self._bytes / 4
    self._firstframe = 0
    self._index = -1
    self._firstpixel = -1
    self._lastpixel = -1
    self._map = None

  def mapChunk (self):
    if self._map:
      return True
    try:
      chunk = open (self._filename, "a+b")
    except IOError:
      return False
    try:
      self._map = mmap.mmap (chunk.fileno (), 0)
      # print "Chunk:  _mapped %d" % self._index
      return True
    except IOError:
      return False

  def closeChunk (self):
    if self._map:
      # print "Chunk:  closed %d" % self._index
      self._map.flush ()
      self._map.close ()
      del self._map

  def showChunk (self):
    print "Chunk _index %4d\nFilename %s\nFrames %4d-%4d\nPixels %8d-%8d\n%d Bytes\n---\n" % (
      self._index, self._filename, self._firstframe, (self._firstframe + self._frames - 1),
      self._firstpixel, self._lastpixel, self._bytes)

# vim: tw=0 ts=2 expandtab
# EOF
