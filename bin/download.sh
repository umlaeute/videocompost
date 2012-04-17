#!/bin/bash
# am I using bashism or does dash really suck?

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
completed="${basedir}/completed.txt"
tmpfilelist="/tmp/tmpfilelist.txt"

# get the next filename to download
current_file=$(head -n 1 ${filelist})
filename=$(basename ${current_file})

echo "retreiving ${current_file}"

# check if it was downloaded already
if [ -f ${completed} ]
then
  egrep -q "${current_file}" ${completed}
  if [ ${?} -eq 0 ]
  then
    echo "found ${current_file} in ${completed}"
    exit 1
  fi
else
  echo "${completed} not found"
  exit 1
fi

remove_filename_from_filelist ()
{
  if [ -f ${tmpfilelist} ]
  then
    rm -f ${tmpfilelist}
  fi

  while read line
  do
    if [ "${line}" == "${current_file}" ]
    then
      continue
    else
      echo ${line} >> ${tmpfilelist}
    fi
  done < ${filelist}

  mv ${tmpfilelist} ${filelist}
}


# download the video to ~/download
scp padma.okno.be:${current_file} ${downdir}/${filename}

# when done, move it to incoming
mv ${downdir}/${filename} ${indir}

# remove the filename from filelist.txt
remove_filename_from_filelist

# add it to completed.txt
echo ${current_file} >> ${completed}

exit 0
# vim:  smartindent sw=2
