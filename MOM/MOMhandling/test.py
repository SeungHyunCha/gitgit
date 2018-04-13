import os

commit = os.popen('git log --oneline $MY_GIT_TOP/mom/lte/complete/LteRbsNodeComplete.xml')
print commit.readline()
print commit.readline()[1]
prev_commit = commit.readline()
prev_commit = prev_commit.split(' ')[0]
print prev_commit.split(' ')[0]
d_mom = os.popen('git show {}:mom/lte/complete/LteRbsNodeComplete.xml'.format(prev_commit))
#print d_mom.read()
