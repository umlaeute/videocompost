#!/bin/sh

# add videos in incoming to compost

user="vc"
group="vc"
basedir="/home/${user}"
indir="${basedir}/incoming"

cd ${basedir}

# add videos sorted by upload time
for video in $(ls -t ${indir})
do
  infile="${indir}/${video}"

  if [ -f ${infile} ]
  then
    # convert it to .raw format
    ./bin/video2raw.sh ${infile} infile.raw
    
    # cut it to pieces and add it to compost
    ./bin/cutvideo.py
    
    # remove video from incoming
    rm -f ${infile}
  fi
done

# vim: ts=2 tw=0 expandtab
# EOF
