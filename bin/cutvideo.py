#!/usr/bin/env python

import hashlib
import time
from ChunkList import ChunkList

infilename = "/tmp/infile.raw"
infile = open (infilename, "r")
# pixels_per_frame * bytes_per_pixel * frames
chunksize = 320 * 240 * 4 * 68
chunk = True
chunknum = 0

chunklist = ChunkList ()

while True:
  infile.seek (chunksize * chunknum)
  chunk = infile.read (chunksize)
  if not chunk:
    print "Done"
    break
  hash = hashlib.md5 (str (time.time ()))
  outfilename = "/tmp/%s.raw" % hash.hexdigest ()
  outfile = open (outfilename, "w")
  outfile.write (chunk)
  outfile.close ()
  chunklist.addChunk (outfilename)
  print "wrote chunk #%4d with name %s" % (chunknum, outfilename)
  chunknum += 1

chunklist.printList ()
chunklist.saveList ()

# vim: tw=0 ts=2 expandtab
# EOF
