#!/bin/bash

# add videos in incoming to compost

user="kompost"
group="kompost"
basedir="/home/${user}"
indir="${basedir}/incoming"
logger="${basedir}/bin/VCLogger.py"
lockfile="${basedir}/run/haecksler.lock"
rawvideo="${basedir}/infile.raw"

# exit if a lockfile is present
if [ -f ${lockfile} ]
then
  ${logger} "[haecksler]: lockfile present.  exiting."
  exit 0
fi
echo ${BASHPID} > ${lockfile}

# work in basedir
cd ${basedir}

# add videos sorted by upload time
for video in $(ls -t ${indir})
do
  oggvideo="${indir}/${video}"
  
  # remove old rawvideo if there is one
  if [ -f ${rawvideo} ]
  then
    rm -f ${rawvideo}
  fi

  if [ -f ${oggvideo} ]
  then
    # convert it to .raw format
    ${logger} "[haecksler]: importing ${video}"
    ./bin/video2raw.sh ${oggvideo} ${rawvideo}
    
    # cut it to pieces and add it to compost
    ./bin/cutvideo.py
    
    # remove video from incoming
    rm -f ${oggvideo}
    ${logger} "[haecksler]: finished importing ${video}"
  fi
done

rm -f ${lockfile}

# vim: ts=2 tw=0 expandtab
# EOF
