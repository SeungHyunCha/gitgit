'''
Created on 2018. 2. 26.

@author: echaseu
'''

class Calculator:
    count = 0
    def __init__(self, first, second):
        self.first = first
        self.second = second
        Calculator.count += 1
#    def setdate(self, first, second):
#        self.first = first
#        self.second = second    
    def sum1(self):
        return self.first + self.second
    def mul1(self):
        return self.first * self.second
    def sub1(self):
        return self.first - self.second      
    def div1(self):
        if self.second == 0:
            return 0
        else:
            return self.first / self.second

class Morefunc(Calculator):
    def pow1(self):
        return self.first ** self.second
    
a = Calculator(4,5)
b = Morefunc(4,0)

print a.sum1()
print b.sum1()
print b.pow1()
print b.div1()

print Calculator.count
