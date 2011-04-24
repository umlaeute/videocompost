#!/usr/bin/env python
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
    # print "Reached the end"
    break
  outfilename = "/tmp/%s.raw" % chunknum
  outfile = open (outfilename, "w")
  outfile.write (chunk)
  outfile.close ()
  chunklist.addChunk (outfilename)
  # print "wrote chunk #%2d starting at %d" % (chunknum, chunksize * chunknum)
  chunknum += 1

chunklist.printList ()
chunklist.saveList ()

# vim: tw=0 ts=2 expandtab
# EOF
