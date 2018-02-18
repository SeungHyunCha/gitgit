a = "Life is too short, You need Python"
b = a[0]+a[1]+a[2]+a[-1]
print(b)
print(a[0:4])
print(a[0:19])
print(a[5:])
print(a[19:-7])
print(a[19:-4])

my_test = "pithon"
my_result = my_test[:1] + 'y' + my_test[2:]
print(my_result)

num = 3
str = 'five'
formatting = "I eat %s or %d apples." %(str,num)
print(formatting)

#a = 'hobby'
#b = 'python is best choice'
#print(a.count('b'))
#print(b.find('b'))
#print(b.find('k'))

my_join = "1"
print(my_join.join('abced'))

print(a.replace('Life', 'leg'))
print(a.split())

my_format = 'My name is %s ' % 'chacha'
print(my_format)
my_formatting = 'My name is {}' .format('chacha')
print(my_formatting)

# Docstring
""" Docstring"""
print('test_print')

#print('test_print', end="coding") only possible in python 3.x
