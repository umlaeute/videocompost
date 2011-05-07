#!/bin/sh

# prepare the directory structure and install binaries

# change user/group if you want
user="vc"
group="vc"

# all files go to ${user}'s home
basedir="/home/${user}"
bindir="/${basedir}/bin"
binaries="addBotToList.py BotList.py Chunk.py cutvideo.py Compost.py composter.py haecksler.sh VCLogger.py playraw.sh video2raw.sh CompostAccess.py gluechunks.py raw2video.sh"
directories="bin config compost incoming log run"

# check if ${user} exists
getent passwd ${user} >/dev/null
if [ $? -ne 0 ]
then
    adduser --disabled-password ${user}
fi

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
    cp bin/${bin} ${bindir}
    echo "done"
done

# echo -n "Installing cronscript as /etc/cron.hourly/videocompost: "
# cp bin/cronscript /etc/cron.hourly/videocompost
# echo "done"

echo -n "creating vcconfig.py: "
cat << EOF > ${bindir}/vcconfig.py
import os
"""
created by install.sh
"""
user = "${user}"
group = "${group}"
basedir = "/home/%s" % user
configdir = os.path.join (basedir, "config")
infilename = os.path.join (basedir, "infile.raw")
compostdir = os.path.join (basedir, "compost")
bindir = os.path.join (basedir, "bin")
logdir = os.path.join (basedir, "log")
logfilename = os.path.join (logdir, "vclog")

if __name__ == "__main__":
  pass
EOF
echo "done"

echo "Finished installation"
exit 0
