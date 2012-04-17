#!/bin/sh

#
# get the next video from padma.okno.be
# videos are listed in filelist.txt and we always
# take the first video from the list.  When the download
# was successfull, we delete the file from the list.

user="kompost"
group="kompost"
basedir="/home/${user}"
indir="${basedir}/incoming"
downdir="${basedir}/download"
logger="${basedir}/bin/VCLogger.py"
filelist="${basedir}/filelist.txt"
completed="${basdir}/completed.txt"
tmpfilelist="/tmp/tmpfilelist.txt"

remove_filename_from_filelist ()
{
  filename=${1}
  if [ -f ${tmpfilelist} ]
  then
    rm -f ${tmpfilelist}
  fi

  for line in $(cat ${filelist})
  do
    if [ "${line}" == "${filename}" ]
    then
      continue
    fi
    echo ${line} >> ${tmpfilelist}
  done

  mv ${tmpfilelist} ${filelist}
}

# get the next filename to download
current_file=$(head -n 1 ${filelist})
filename=$(basename ${current_file})

# check if it was downloaded already
egrep -q ${current_file} ${completed}
if [ ${?} -eq 0 ]
then
  echo "found ${current_file} in ${completed}"
  exit 1
fi

# download the video to ~/download
scp padma.okno.be:${current_file} ${downdir}/${filename}

# when done, move it to incoming
mv ${downdir}/${filename} ${indir}

# remove the filename from filelist.txt and add it to
# completed.txt
remove_filename_from_filelist ${current_file}
echo ${current_file} >> ${completed}

# vim:  smartindent sw=2
