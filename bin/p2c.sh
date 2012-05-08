#!/bin/zsh

#
# switch from player to composter
# use at the end of exhibition opening time (crontab)
#

user="kompost"
group="kompost"
BASE="/home/$user"

PLAYER="$BASE/bin/playraw.py"
PLAYER_PID="$BASE/run/playraw.pid"
COMPOSTER="$BASE/bin/composter.py"
COMPOSTER_PID="$BASE/run/vc.pid"

# stop player
kill -1 $(cat $PLAYER_PID)

# start composter
$COMPOSTER

# EOF
