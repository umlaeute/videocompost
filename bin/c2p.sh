#!/bin/zsh

#
# switch from composter to player
# use at the beginning of exhibition opening time (crontab)
#
user="kompost"
group="kompost"
BASE="/home/$user"

PLAYER="$BASE/bin/playraw.py"
PLAYER_PID="$BASE/run/playraw.pid"
COMPOSTER="$BASE/bin/composter.py"
COMPOSTER_PID="$BASE/run/vc.pid"

# stop composter
kill -1 $(cat $COMPOSTER_PID)

# start player
export DISPLAY=:0
$PLAYER & 2>/dev/null 1>/dev/null

# EOF
