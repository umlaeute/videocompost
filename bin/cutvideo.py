#!/usr/bin/env python
from chunkList import chunkList

infilename = "video_in.raw"
infile = open (infilename, "r")
chunksize = 20971520         # 20 MB for now
chunk = True
chunknum = 0

cl = chunkList ()

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
    cl.addChunk (outfilename)
    # print "wrote chunk #%2d starting at %d" % (chunknum, chunksize * chunknum)
    chunknum += 1

cl.printList ()
cl.saveList ()
