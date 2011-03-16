#!/bin/sh
## usage:
# $0 <infile> <outfile>

#settings are hardcoded here, so we don't need to care
WIDTH=320
HEIGHT=240
FRAMERATE="(fraction)25/1"


INFILE=$1
OUTFILE=$2

echo "converting video ${INFILE} to raw ${OUTFILE}"


if [ -e "${INFILE}" ]; then
 :
else
 echo "no valid input file given: \"${INFILE}\"" 1>&2
 exit 1
fi

if [ "x${OUTFILE}" = "x" ]; then
 echo "no output file given" 1>&2
 exit 1
fi

if [ -e "${OUTFILE}" ]; then
 echo "output file \"${OUTFILE}\" already exists" 1>&2
 exit 1
fi



gst-launch -v filesrc location="${INFILE}" ! \
    decodebin ! \
    ffmpegcolorspace ! \
    "video/x-raw-rgb, bpp=(int)32, endianness=(int)4321, depth=(int)32, red_mask=(int)16711680, green_mask=(int)65280, blue_mask=(int)255, alpha_mask=(int)-16777216" ! \
    videoscale ! \
    "video/x-raw-rgb, width=(int)${WIDTH}, height=(int)${HEIGHT}" !\
    videorate ! \
    "video/x-raw-rgb, framerate=${FRAMERATE}" ! \
    filesink location="${OUTFILE}"
