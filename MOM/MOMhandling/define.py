# Gen1
Gen1 = 1
Gen1_MOM = 'cat $MY_GIT_TOP/mom/lte/complete/LteRbsNodeComplete.xml'
Gen1_commit = 'git log --oneline $MY_GIT_TOP/mom/lte/complete/LteRbsNodeComplete.xml'
Gen1_prevMOM = 'git show %s:mom/lte/complete/LteRbsNodeComplete.xml'

# Gen2
Gen2 = 2
Gen2_MOM = 'cat $MY_GIT_TOP/mom/lrat/output/Lrat_DWAXE_mp.xml'
Gen2_commit = 'git log --oneline $MY_GIT_TOP/mom/lrat/output/Lrat_DWAXE_mp.xml'
Gen2_prevMOM = 'git show %s:mom/lrat/output/Lrat_DWAXE_mp.xml'

#etc
prev = '-'
modified = '?'
new = '+'
red = u"\u001b[31m %s \u001b[0m\n"
yellow = u"\u001b[32m %s \u001b[0m\n"
green = u"\u001b[33m %s \u001b[0m\n"
root = 'ManagedElement'