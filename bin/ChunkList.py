#!/usr/bin/env python

from random import randint
import pickle
import fcntl
import os
import mmap
# import os.path
from Chunk import Chunk

class ChunkList:
  """
  keep track of sequence of chunks
  """

  def __init__ (self):
    self.picklefilename = "/tmp/ChunkList.pck"
    if os.path.isfile (self.picklefilename):
      self.filetime = os.stat (self.picklefilename).st_ctime
      self.loadList ()
    else:
      self.chunks = []
    self.chunk = False
    self.frames = 0
    self.bytes = 0
    self.updateChunkList ()

  def renewList (self):
    if os.stat (self.picklefilename).st_ctime > self.filetime:
      print "updating list due to filetime change"
      self.loadList ()
      self.updateChunkList ()
      self.filetime = os.stat (self.picklefilename).st_ctime

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
    self.saveList ()

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
    self.frames = frames

  def mapChunk (self, num):
    self.renewList ()
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
    address = (pixel - self.chunk.firstpixel) * 4
    # print "getPixelColor for pixel %d at local address %d" % (pixel, address)
    color = []
    for i in range (1, 4):
      color.append (ord (self.chunk.map[address+i]))
    return color
      
  def setPixelColor (self, pixel, color):
    c = [0, 0, 0]
    for i in range (0, len (color)):
      if color[i] < 0:
        c[i] = chr (0)
      elif color[i] > 255:
        c[i] = chr (255)
      else:
        c[i] = chr (color[i])
    if not self.chunk:
      if not self.mapPixelChunk (pixel):
        # print "Failed setting color to pixel %d" % pixel
        return False
    elif pixel < self.chunk.firstpixel or pixel > self.chunk.lastpixel:
      self.closeChunk ()
      if not self.mapPixelChunk (pixel):
        # print "Failed setting color to pixel %d" % pixel
        return False
    address = (pixel - self.chunk.firstpixel) * 4
    # print "setPixelColor for pixel %d at local address %d to r=%d g=%d b=%d" % (pixel, address, ord (c[0]), ord (c[1]), ord (c[2]))
    for i in range (1, 4):
      self.chunk.map[address+i] = c[i-1]
    return color

  def deleteList (self):
    print "Deleting all %d chunks" % len (self.chunks)
    for chunk in self.chunks:
      print "===\nremoving chunk"
      chunk.printChunk ()
      try:
        os.remove (chunk.filename)
      except OSError:
        pass
      self.chunks.remove (chunk)
    if len (self.chunks) == 0:
      os.remove (self.picklefilename)
    else:
      print "%d remaining chunks ..." % len (self.chunks)
      self.printList ()
      self.saveList ()
    
  def printList (self):
    for chunk in self.chunks:
      chunk.printChunk ()

if __name__ == "__main__":
  pass

# vim: tw=0 ts=2 expandtab
# EOF
