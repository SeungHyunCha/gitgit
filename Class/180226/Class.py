'''
Created on 2018. 2. 26.

@author: echaseu
'''

class Calculator:
    def __init__(self, first, second):
        self.first = first
        self.second = second
#    def setdate(self, first, second):
#        self.first = first
#        self.second = second    
    def sum1(self, first, second):
        return self.first + self.second
    def mul1(self, first, second):
        return self.first * self.second
    def sub1(self, first, second):
        return self.first - self.second      
    def div1(self, first, second):
        if self.second == 0:
            return 0
        else:
            return self.first / self.second

class Morefunc(Calculator):
    def pow1(self):
        return self.first ** self.second
    
a = Calculator(4,5)
b = Morefunc(4,0)
#a.setdate(4,5)

print a.sum1(a.first, a.second)

print b.sum1(b.first, b.second)
#print b.sum1()
print b.pow1()
print b.div1(b.first, b.second)
#print a.sum1()
#print a.mul(a.first,a.second)

