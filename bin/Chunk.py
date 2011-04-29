#!/usr/bin/env python

import os
import mmap

class Chunk:

  def __init__ (self, filename):
    self.filename = filename
    self.bytes = os.stat (self.filename).st_size
    self.mapped = False
    self.map = False
    self.frames = self.bytes / 307200
    self.firstframe = 0
    self.index = -1
    self.firstpixel = -1
    self.lastpixel = -1

  def mapChunk (self):
    if self.mapped:
      return True
    try:
      chunk = open (self.filename, "a+b")
    except IOError:
      return False
    try:
      self.map = mmap.mmap (chunk.fileno (), 0)
      self.mappped = True
      # print "Chunk:  mapped %d" % self.index
      return True
    except IOError:
      return False

  def closeChunk (self):
    if self.map:
      # print "Chunk:  closed %d" % self.index
      self.map.flush ()
      self.map.close ()
    self.mapped = False

  def printChunk (self):
    print "Chunk index %4d\nFilename %s\nFrames %4d-%4d\nPixels %8d-%8d\n%d Bytes\n---\n" % (
      self.index, self.filename, self.firstframe, (self.firstframe + self.frames - 1),
      self.firstpixel, self.lastpixel, self.bytes)
# vim: tw=0 ts=2 expandtab
# EOF
