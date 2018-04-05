#!/usr/bin/python
import copy

list = [0,1,2,3,['a','b']]
other = list
other[0] = 10

del list[4][1]

# The append does not add many values, just express only one value. 
list.append([5,6,7])

# The insert is possible to insert anywhere.
list.insert(0, 100)

# pop can remove last one  
list.pop()

# Compared with append, the extend can add many values.
list.extend(['a','b','c'])

# python 2.7 does not support .copy()
#new_list = list.copy()
new_list = copy.copy(list)
newd_list = copy.deepcopy(list)
#print new_list
print newd_list

#copy vs deepcopy in case of nested list
"""
a = [1,2,3]
b = [4,a,5]

c = copy.copy(b)
a[0] = 100

print c
"""



