#!/bin/sh

# prepare the directory structure and install binaries

user="vc"
group="vc"
basedir="/home/${user}"
bindir="/${basedir}/bin"
binaries="addBotToList.py Chunk.py cutvideo.py ChunkList.py composter.py playraw.sh video2raw.sh CompostAccess.py gluechunks.py raw2video.sh vcconfig.py"
directories="bin chunks config incoming"

# FIXME: we should check if user/group exist and create them if not

echo -n "Creating ${basedir}: "
if [ -d ${basedir} ]
then
    echo "exists"
else
    mkdir ${basedir}
    chown ${user}:${group} ${basedir}
    echo "done"
fi

for dir in ${directories}
do
    echo -n "Creating ${basedir}/${dir}: "
    if [ -d ${basedir}/${dir} ]
    then
        echo "exists"
    else
        mkdir ${basedir}/${dir}
        chown ${user}:${group} ${basedir}/${dir}
        echo "done"
    fi
done

for bin in ${binaries}
do
    echo -n "Installing ${bin}: "
    cp "bin/${bin}" ${bindir}
    echo "done"
done

echo "Finished installation"
exit 0
