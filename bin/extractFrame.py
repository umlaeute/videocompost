#!/usr/bin/env python
"""
dumps one frame from the specified chunk file to 'frame.ppm'
input is expected as ARGB with 255 bits per channel (the
internal format used by videocomposter)
"""

import mmap
import sys
import os

def extractFrame (chunkfilename, frame_num):
  if not os.path.isfile (chunkfilename):
    print 'File {0} not found'.format (chunkfilename)
    return 1
  width = 320
  height = 240
  bytes_per_pixel = 4
  framesize = width * height * bytes_per_pixel

  chunkfile = open (chunkfilename, 'rb')
  chunkmap = mmap.mmap (chunkfile.fileno (), 0, mmap.MAP_PRIVATE, mmap.PROT_READ)
  frames = len (chunkmap) / framesize

  if frames <= frame_num:
    print 'Taking last frame instead of frame {0} of a total of {1}'.format (
      frame_num, frames)
    frame_num = frames - 1

  outfilename = 'frame.ppm'
  print 'Extracting frame {0} (total={1}) from {2} and writing to {3}.'.format (
    frame_num, frames, chunkfilename, outfilename)

  framefile = open (outfilename, 'wb')
  framefile.write ('P6\n{0} {1}\n255\n'.format (width, height))

  # goto first pixel
  chunkmap.seek (framesize * frame_num)
  for i in range (0, framesize / bytes_per_pixel):
    chunkmap.read_byte ()
    framefile.write (chunkmap.read (3))

  framefile.close ()
  chunkmap.close ()
  return 0

if __name__ == "__main__":
  if len (sys.argv) < 2:
    print 'usage: extractFrame.py path_to_chunk [frame_num]'
    print
    print 'frame_num starts at 0'
    sys.exit (1)
  if len (sys.argv) > 2:
    frame_num = int (sys.argv[2])
  else:
    frame_num = 0
  sys.exit (extractFrame (sys.argv[1], frame_num))

# vim: tw=0 sw=2 smartindent
