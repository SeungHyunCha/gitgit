#!/usr/bin/python

s = '''
a=1
for k in range(10):
	a = a + 1
print a
'''
code = compile(s, '<string>', 'exec')
exec code
