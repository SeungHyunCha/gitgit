'''
Created on 2018. 2. 27.

@author: echaseu
'''

class Sample:
    count = 0 # class variable
    # initializer self    
    def __init__(self, width, height):
        print self
        # instance variable
        self.width = width 
        self.height = height
        self.__area = width * height # private variable
        #self.__etae = width
        #self._tset = width + height
        self._aset = width + height
        Sample.count += 1
       
    def mul1(self):
        return self.width * self.height
   
    def get_info(self):
        return self.__dict__
#    def get_count(self):
#        return Sample.count 
 

class add_Sample(Sample):
    def add1(self):
        return self.width + self.height

# test  
a = Sample(1, 2)
#print hex(id(a))
#print a.get_count()
b = Sample(3, 4)
#print b.get_count()
#print a.get_count()
print b.get_info()
#c = add_Sample(5,6)

#a_mul = a.mul1()
'''
total_1 = a + b
total_2 = a - b
print a.width
print a.getarea()
print a.height
print 'Multi of the %s is %d' % ('a',a_mul)
print 'Multi of the {0} is {0}'.format('a',a_mul)
print total_1.mul1()
print total_2.mul1()
print a.__cmp__(b)
print c.add1()
print 'Objects are %d' %Sample.count
a.height = 100
'''
#print total_1.mul1()
#print a.mul1()
#print a.__area

'''
    def __add__(self, other):
        obj = Sample(self.width + other.width, self.height + other.height)
        return obj
    def __sub__(self, other):
        obj = Sample(self.width - other.width, self.height - other.height)
        return obj
    def __cmp__(self, other):
        if self.height < other.height:
            return '%s is larger' % 'latter'
        elif self.height == other.height:
            return 'Same value'
        else:
            return '%s is larger' % 'former' 

'''