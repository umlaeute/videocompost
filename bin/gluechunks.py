#!/usr/bin/env python
from chunkList import chunkList
import os.path
import os

cl = chunkList ()
outfilename = "/tmp/video.raw"
if os.path.isfile (outfilename):
    os.remove (outfilename)

outfile = open (outfilename, "w")

for chunk in cl.getList ():
    if os.path.isfile (chunk):
        infile = open (chunk, "r")
        outfile.write (infile.read ())
        infile.close ()

