'''
Created on 2018. 2. 26.

@author: echaseu
'''

class Calculator:
    def setdate(self, first, second):
        self.first = first
        self.second = second
    
    def sum(self, first, second):
        return first+second
    
    def mul(self, first, second):
        return first*second
    
    def sub(self, first, second):
        return first-second      
    
    def div(self, first, second):
        return first/second

a = Calculator()

a.setdate(4,5)

print a.sum(a.first,a.second)
#print a.mul(a.first,a.second)

