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
randint="${basedir}/bin/RandInt.py"
spaceneeded=1500000

get_next_filename ()
{
  # get the next filename to download
  lines=$(wc -l ${filelist} | awk '{print $1}')
  index=$($randint lines)
  current_file=$(head -n ${lines} ${filelist} | tail -n 1)
  filename=$(basename ${current_file})
}

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

# exit if less than ??? space is available
typeset -i freespace=$(df | egrep rootfs | awk '{print $4}')
if [ ${freespace} -lt ${spaceneeded} ]
then
  # echo "sorry, ${freespace} is less than ${spaceneeded}."
  exit 1
fi

if [ ${1} == "test" ]
then
  get_next_filename
  echo "would download ${current_file}"
  exit 0
fi

# check if it was downloaded already
if [ -f ${completed} ]
then
  found=1
  get_next_filename
  while [ ${found} -eq 1 ]
  do
    egrep -q "${current_file}" ${completed}
    if [ ${?} -eq 0 ]
    then
      remove_filename_from_filelist
      get_next_filename
    else
      found=0
    fi
  done
else
  # echo "${completed} not found"
  exit 1
fi


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
