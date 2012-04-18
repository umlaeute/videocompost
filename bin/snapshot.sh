#!/bin/bash

# add videos in incoming to compost

user="kompost"
group="kompost"
basedir="/home/${user}"
logger="${basedir}/bin/VCLogger.py"
lockfile="${basedir}/run/snapshot"
snapshots="${basedir}/snapshots"
rawvideo="${basedir}/video.raw"
oggvideo="${basedir}/video.ogg"
snapshot="${snapshots}/$(date +%Y%M%D).ogv"
current="${snapshots}/snapshot.ogv"

# exit if a lockfile is present
if [ -f ${lockfile} ]
then
  ${logger} "[snapshot]: lockfile present.  exiting."
  exit 0
fi

# create a lockfile
touch ${lockfile}

if ! [ -d ${snapshots} ]
then
  mkdir ${snapshots}
fi

# work in basedir
cd ${basedir}

# glue chunks to get one raw video file
./bin/gluechunks.py

# encode raw video to ogg video
./bin/raw2video.sh ${rawvideo} ${oggvideo}

# move video to snapshots directory
mv ${oggvideo} ${snapshot}

# remove old link snapshot.ogv
rm ${current}

# link video to snapshot.ogv
ln -s ${snapshot} ${current}

# remove lockfile
rm -f ${lockfile}
# vim: ts=2 tw=0 expandtab sw=2
# EOF
