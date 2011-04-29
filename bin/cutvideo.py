#!/usr/bin/env python

"""
  takes the file 'infile.raw' (expected in /usr/local/vc)
  and cuts it into chunks of a defined size, adding the chunks
  to chunklist and storing them in /usr/local/vc/chunks/.
"""

import hashlib
import time
import sys
import os
from ChunkList import ChunkList
from vcconfig import *

if os.path.isfile (infilename):
  infile = open (infilename, "r")
else:
  print "%s not found" % infilename
  sys.exit (1)

# pixels_per_frame * bytes_per_pixel * frames
# will be changed to aprox. 2GB
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
  chunkfilename = os.path.join (chunkdir, "%s.raw" % hash.hexdigest ())
  chunkfile = open (chunkfilename, "w")
  chunkfile.write (chunk)
  chunkfile.close ()
  chunklist.addChunk (chunkfilename)
  print "wrote chunk #%4d with name %s" % (chunknum, chunkfilename)
  chunknum += 1

os.remove (infilename)
chunklist.saveList ()
chunklist.printList ()

# vim: tw=0 ts=2 expandtab
# EOF
