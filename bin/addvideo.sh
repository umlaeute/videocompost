#!/bin/sh

# add one video from incoming to compost

user="vc"
group="vc"
basedir="/home/${user}"
indir="${basedir}/incoming"

cd ${basedir}

# find the oldest video in incoming
for video in $(ls -t ${indir})
do
    continue
done
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
