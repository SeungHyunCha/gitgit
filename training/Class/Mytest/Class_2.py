'''
Created on 2018. 2. 26.

@author: echaseu
'''

class Data:
    def __init__(self, data):
        tmp = data.split(',')
        self.name = tmp[0]
        self.age = tmp[1]
        self.grade = tmp[2]
    def print_age(self):
        return self.age
        
class Print(Data):
    def print_out(self):
        return 'The age of %s is %s.' %(self.name, self.age)
        
    
data = Data('echaseu,28,B')

print data.name
print data.age
print data.grade
print data.print_age()

data = Print('echaseu,28,B')
print data.print_out()


