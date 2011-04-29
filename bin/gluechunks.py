#!/usr/bin/env python
from ChunkList import ChunkList
import os.path
import os

chunklist = ChunkList ()
outfilename = "/tmp/outfile.raw"
if os.path.isfile (outfilename):
  os.remove (outfilename)

outfile = open (outfilename, "w")

for chunk in chunklist.getList ():
  if os.path.isfile (chunk.filename):
    infile = open (chunk.filename, "r")
    outfile.write (infile.read ())
    infile.close ()

# vim: tw=0 ts=2 expandtab
# EOF
