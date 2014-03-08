# Proof of concept sweeper to find new files and dump them into the database. Seems to work
# pretty well on my local machine. Right now it just outputs the list of newly added files,
# but could be pretty easily extended with MongoDB, I imagine. The strategy is to use system
# time. Only looking at the window between the last sweep and the current sweep eliminates
# potential 'missed' files added during the sweep.

# Note: if this is going to pass files straight into the database, it needs to be able to
# check for compressed files first. We don't want zip files in the database, just documents.

import os
import sys
import time
import math

startTime=long(math.floor(time.time()))

log=open('sweeperLog.log', 'r')		#log file contains start time of last sweep
lastTime=long(log.readline())
log.close()

newPaths = []

for root, directories, files in os.walk('/'):
    for filename in files:
        path = os.path.join(root, filename) 
        if lastTime < os.stat(path).st_ctime < startTime:
            newPaths.append(path)

# Using ctime should work, but it's worth checking. It looks at the last time there was a change
# to the file or its inode information. Dumping the file in the server should 

log=open('sweeperLog.log', 'w')
log.write(str(startTime))

print newPaths
