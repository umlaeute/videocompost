#!/usr/bin/env python

from ChunkList import ChunkList

pixels_per_frame = 320 * 240
pixel_size = 4

class CompostAccess:

  def __init__ (self):
    self.chunklist = ChunkList ()
    self.chunklist.mapChunk (0)
    self.bytes = self.chunklist.bytes
    self.chunks = self.chunklist.chunks

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


if __name__ == "__main__":
  pass

# vim: tw=0 ts=2 expandtab
# EOF
