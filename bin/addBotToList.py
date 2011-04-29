#!/usr/bin/env python

import sys
import os.path
from composter import BotList
from vcconfig import *

botlist = BotList ()
if len (sys.argv) != 2:
  sys.exit (1)
botscript = os.path.basename (sys.argv[1])
if not os.path.isfile (os.path.join (bindir, botscript)):
  sys.exit (1)
botlist.addBot (botscript)
botlist.saveList ()

# vim: tw=0 ts=2 expandtab
# EOF
