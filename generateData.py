import sys
import subprocess

if len(sys.argv) < 2:
    print 'Lacking arguments'

startNo = 1
noOfFiles = int(sys.argv[1])

if len(sys.argv) > 2:
    startNo = int(sys.argv[2])

allFiles = []

print 'CXXFLAGS = -Wall -Wextra -std=c++11'
print 'CC = g++'
print ''
print 'all: program'

for i in range(noOfFiles):
    fName = 'main{0}.cpp'.format(i + startNo)
    oName = 'main{0}.o'.format(i + startNo)
    exName = 'main{0}'.format(i + startNo)
    cmd = 'python generator.py > ./generated/{0}'.format(fName)
    subprocess.call(cmd, shell=True)
    allFiles.append(exName)
    print '{0}: {1}'.format(exName, oName)
    print '{0}: {1}'.format(oName, fName)
print 'OBJS = {0}'.format(' '.join(allFiles))
print 'program: $(OBJS)'
print 'clean:'
print "\trm -f *.o $(OBJS)"