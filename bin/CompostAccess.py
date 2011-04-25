#!/usr/bin/env python

from ChunkList import ChunkList

pixels_per_frame = 320 * 240
pixel_size = 4

class CompostAccess:

  def __init__ (self):
    self.chunklist = ChunkList ()
    if len (self.chunklist.chunks) > 0:
      self.chunklist.mapChunk (0)

  def mapChunk (self, num):
    return self.chunklist.mapChunk (num)

  def closeChunk (self):
    self.chunklist.closeChunk ()

  def getFrame (self):
    pass

  def setPixelColor (self, pixel, color = [0, 0, 0]):
    return self.chunklist.setPixelColor (pixel, color)

  def getPixelColor (self, pixel):
    return self.chunklist.getPixelColor (pixel)

  def getBytes (self):
    return self.chunklist.bytes

  def getChunkList (self):
    return self.chunklist

  def getMap (self):
    return self.chunklist.chunk.map

  def getFrames (self):
    return self.chunklist.frames

  def getChunks (self):
    return self.chunklist.chunks

if __name__ == "__main__":
  pass

# vim: tw=0 ts=2 expandtab
# EOF
