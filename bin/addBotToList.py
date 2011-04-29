#!/usr/bin/env python

import sys
from composter import BotList
botlist = BotList ()
if len (sys.argv) != 2:
  sys.exit (1)
botlist.addBot (sys.argv[1])
botlist.saveList ()

# vim: tw=0 ts=2 expandtab
# EOF
