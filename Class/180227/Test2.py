'''
Created on 2018. 2. 27.

@author: echaseu
'''

print globals()
test_num = 20
print globals()
#print hex(id(test_num))
'''
class A:
    pass

a = A()
print globals()
print hex(id(a))
print hex(id(A))
'''
class A:
    def func(self):
        self.__dict__ = {'a':1, 'b':2, 'c':3}
        return self.__dict__
a = A()
print globals()
print a.func()
