#!/usr/bin/env python

from random import randint
import pickle
import fcntl
import os
import mmap
import os.path
from Chunk import Chunk

class ChunkList:
  """
  keep track of sequence of chunks
  """

  def __init__ (self):
    self.picklefilename = "/tmp/ChunkList.pck"
    self.ppf = 320 * 240          # pixels per frame
    self.ps = 4                   # pixel size
    self.fs = self.ppf * self.ps  # frame size
    if os.path.isfile (self.picklefilename):
      self.loadList ()
    else:
      self.chunks = []
    self.chunk = False
    self.updateChunkList ()

  def addChunk (self, filename):
    if not os.path.isfile (filename):
      return
    chunk = Chunk (filename)
    if len (self.chunks) > 2:
      index = randint (0, len (self.chunks) - 1)
      self.chunks.insert (index, chunk)
    else:
      self.chunks.append (chunk)
    self.updateChunkList ()

  def printList (self):
    for i in range (len (self.chunks)):
      self.chunks[i].printChunk ()

  def getList (self):
    return self.chunks
            
  def saveList (self):
    picklefile = open (self.picklefilename, "w")
    fcntl.flock (picklefile, fcntl.LOCK_EX)
    pickle.dump (self.chunks, picklefile)
    fcntl.flock (picklefile, fcntl.LOCK_UN)
    picklefile.close ()

  def loadList (self):
    picklefile = open (self.picklefilename, "r")
    fcntl.flock (picklefile, fcntl.LOCK_EX)
    self.chunks = pickle.load (picklefile)
    fcntl.flock (picklefile, fcntl.LOCK_UN)

  def updateChunkList (self):
    self.bytes = 0
    frames = 0
    for i in range (0, len (self.chunks)):
      self.bytes += self.chunks[i].bytes
      if i is not 0:
        frames += self.chunks[i - 1].frames
      self.chunks[i].firstframe = frames
      self.chunks[i].index = i
      self.chunks[i].firstpixel = frames * 76800
      self.chunks[i].lastpixel = ((frames + self.chunks[i].frames - 1) * 76800) + 76799

  def mapChunk (self, num):
    if num >= len (self.chunks):
      return False
    if self.chunk:
      if self.chunk.index is not num:
        self.closeChunk ()
      else:
        return True
    if self.chunks[num].mapChunk ():
      self.chunk = self.chunks[num]
      return True
    return False

  def mapPixelChunk (self, pixel):
    for i in range (0, len (self.chunks)):
      if self.chunks[i].firstpixel <= pixel and self.chunks[i].lastpixel >= pixel:
        return self.mapChunk (i)
    # print "Failed mapping chunk for pixel %d" % pixel
    return False
    
  def closeChunk (self):
    if self.chunk:
      self.chunk.closeChunk ()
    self.chunk = False

  def getPixelColor (self, pixel):
    if not self.chunk:
      if not self.mapPixelChunk (pixel):
        return False
    elif pixel < self.chunk.firstpixel or pixel > self.chunk.lastpixel:
      self.closeChunk ()
      if not self.mapPixelChunk (pixel):
        return False
    color = []
    for i in range (3):
      color.append (ord (self.chunk.map[pixel - self.chunk.firstpixel + i + 1]))
    return color
      
  def setPixelColor (self, pixel, color):
    for i in range (0, len (color)):
      if color[i] < 0:
        color[i] = 0
      if color[i] > 255:
        color[i] = 255
      try:
        color[i] = chr (color[i])
      except TypeError:
        pass
    if not self.chunk:
      if not self.mapPixelChunk (pixel):
        # print "Failed setting color to pixel %d" % pixel
        return False
    elif pixel < self.chunk.firstpixel or pixel > self.chunk.lastpixel:
      self.closeChunk ()
      if not self.mapPixelChunk (pixel):
        # print "Failed setting color to pixel %d" % pixel
        return False
    for i in range (3):
      self.chunk.map[pixel - self.chunk.firstpixel + i + 1] = color[i]
    return color
    
if __name__ == "__main__":
  pass

# vim: tw=0 ts=2 expandtab
# EOF
