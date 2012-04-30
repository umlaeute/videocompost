#!/usr/bin/env python

import os
import mmap
import random
from VCLogger import writelog

class Chunk:

  def __init__ (self, filename):
    self._filename = filename
    self._bytes = os.stat (self._filename).st_size
    self._frames = self._bytes / (320 * 240 * 4)
    self._pixels = self._bytes / 4
    self._index = -1
    self._firstframe = 0
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
      return True
    except IOError:
      return False

  def closeChunk (self):
    if self._map:
      self._map.flush ()
      self._map.close ()
      self._map = None

  def updateChunk (self):
    self._bytes = os.stat (self._filename).st_size
    self._frames = self._bytes / (320 * 240 * 4)
    self._pixels = self._bytes / 4

  def showChunk (self):
    print "Chunk _index %4d\nFilename %s\nFrames %4d-%4d (%2d)\nPixels %8d-%8d\n%d Bytes\n---\n" % (
      self._index, self._filename, self._firstframe, (self._firstframe + self._frames - 1),
      self._frames, self._firstpixel, self._lastpixel, self._bytes)

  def dropLastNFrames (self):
    """
    Drops a random number of frames from Chunk if there are more than
    min_size frames left in Chunk.
    Returns the number of dropped frames.
    """
    min_size = 5
    dropNumFrames = 0
    if self._frames > min_size:
      intervalMin = 1
      intervalMax = self._frames / 10 + 1
      random.seed ()
      dropNumFrames = random.randint (intervalMin, intervalMax)
      self._map.resize ((self._frames - dropNumFrames) * 320 * 240 * 4)
      self.updateChunk ()
    else:
      writelog ('[Chunk]:  frame {0} reached minimum size {1}'.format (self._index, min_size))
    self.closeChunk ()
    return dropNumFrames

# vim: tw=0 ts=2 expandtab
# EOF
