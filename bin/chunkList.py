#!/usr/bin/env python

from random import randint
import pickle
import os.path
import fcntl

class chunkList:
    """
    keep track of sequence of chunks
    """

    def __init__ (self):
        self.picklefilename = "/tmp/chunkList.pck"
        if os.path.isfile (self.picklefilename):
            self.loadList ()
        else:
            self.chunks = []

    def addChunk (self, filename):
        if len (self.chunks) > 2:
            index = randint (0, len (self.chunks) - 1)
            self.chunks.insert (index, filename)
        else:
            self.chunks.append (filename)

    def printList (self):
        for i in range (len (self.chunks)):
            print "%3d -> %s" % (i, self.chunks[i])

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
        
if __name__ == "__main__":
    pass
