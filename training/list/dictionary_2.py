#!/usr/bin/python

dic = {'key':'t','key1':'cha', 'key2':[1,2,3]}
dic[10] = 1
dic['key3'] = 'chas'
print dic

#del dic['key1']
#del dic[2]

print dic['key3']

# dic key is possible to use tuple
#dic = {(1,2):'test'}
#print dic[1,2]

#print dic.keys()

# change dic to list 
# Functions of list do not use in dic
c_list = list(dic.keys())
print c_list

print dic.items()
#print dic.clear()

# If error gnerates, get() returns none
print dic.get('key5')
print dic.get('key5', 'X')

print 'key' in dic

