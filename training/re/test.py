import re

string = 'python'
p = re.compile('yt')
result = p.search(string)
if result:
    print 'search!!'
    
p = re.compile('on$')
result = p.search(string)
if result:
    print 'search!!'

p = re.compile('ona$')
result = p.search(string)
if result:
    print 'search!!'
else: print 'fail!!'