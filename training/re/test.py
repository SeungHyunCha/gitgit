import re

string = 'python'
p = re.compile('pyt')
result = p.match(string)
result1 = p.search(string)

if result:
    print 'match'

if result1:
    print 'search'