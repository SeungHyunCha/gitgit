import xml.etree.ElementTree as ET
from __builtin__ import str
from _ast import Str

class MomParser:
    def __init__(self, name):
        self.name = name
        self.mos = {}
        self.attrs = {}
        self.__run()
        
    def __run(self):
        for event, elem in ET.iterparse(self.name, events=('start', 'end')):
            if event == 'start': # create obj for mo, enum, struct, exception
                if elem.tag == 'class':
                    moname = Mo(elem)
                    self.mos[moname.getName()] = elem
            elif event == 'end': # add infomation in obj
                for attr in elem: 
                    if elem.tag == 'class' and attr.tag == 'attribute':
                        child = Attr(attr)
                        child.mo = moname.getName()
                        moname.addAttrs(child)
                        moname.addAttrsInfo(child)
            else: pass

    def printMo(self, mo=""):
        str = "-" * 100
        print str + "print MO" + str
        str = "*" * 100
        mo_list = self.mos.keys()
        if mo in mo_list:
            temp = Mo(self.mos[mo])
            print str
            print "mo\t\t", "attribute\t\t"
            print str
            print temp.getName()
            print str
            print temp.getAttrs()
        elif mo == "":
            for key in mo_list:
                temp = Mo(self.mos[key])
                print str
                print temp.getName()

class Mo:
    def __init__(self, elem):
        self.name = elem.attrib.values()[0]
        self.attrs_obj = {}
        self.attrs_info = {}
        self.obj = elem
        self.handle()
    
    def getName(self):
        return self.name
    
    def getMo(self):
        return self.obj
            
    def addAttrs(self, attr):
        self.attrs_obj[attr.getName()] = attr
    
    def getAttrs(self): #get attrs
        return self.attrs_obj
    
    def addAttrsInfo(self, attr):
        for key, value in attr.__dict__.items(): #get infomation of attrs
            self.attrs_info[key] = value
    
    def getAttrsInfo(self):
        return self.attrs_info
    
    def __str__(self):
        return self.name
    
    def handle(self):
        for mo_child in self.obj:
            if len(mo_child._children) == 0 and mo_child.tag != 'attribute' or 'enumMember' or 'structMember':
                if mo_child.text == None: exec("self.%s = {}" % mo_child.tag)
                else: 
                    if mo_child.text == '\n\t\t\t\t': pass
                    else: exec("self.%s = %r" % (mo_child.tag, mo_child.text))
            else: pass
            
class Attr:
    def __init__(self, elem):
        self.name = elem.attrib.values()[0]
        self.obj = elem
        self.mo = None
        self.dataTypes = {}
        self.__handle()
    
    def getName(self):
        return self.name
    
    def __handle(self):
            for attr in self.obj:
                if len(attr._children) == 0:
                    if attr.text == None: exec "self.%s = {}" % attr.tag
                    else: exec "self.%s = %r" % (attr.tag, attr.text)
                else:
                    Type = DataType(attr)
                    for key, value in Type.__dict__.items(): #get dataType in Attr
                        if key == 'elem': pass
                        else: self.dataTypes[key] = value
#                     print self.dataTypes
        
class DataType:
    def __init__(self, elem):
        self.elem = elem
        self.__handle()

    def __handle(self):
        if self.elem.attrib == {}: pass
        else:
            exec "self.%s = %r" % (self.elem.attrib.keys()[0], self.elem.attrib.values()[0]) 
        for dtype in self.elem:
            exec "self.%s = {}" % dtype.tag
            if dtype.attrib == {}:
                for child in dtype:
                    if len(child._children) == 0:
                        if child.attrib == {}: # get min,max values
                            if child.text == None: exec "self.%s = {}" % child.tag
                            else:
                                temp = {}
                                temp[child.tag] = child.text
                                exec "self.%s.update(%s)" % (dtype.tag, temp)
                        else:
                            if child.text == None: exec "self.%s = %r" % (child.tag, child.attrib.values()[0])
                            else: pass
                    else:
                        exec "self.%s = {}" % child.tag
                        for gchild in child:
                            if gchild.text == '\n\t\t\t\t\t\t\t':
                                for ggchild in gchild:
                                    temp = {}
                                    temp[ggchild.tag] = ggchild.text
                                    exec "self.%s.update(%s)" % (child.tag, temp)
                            else:
                                temp = {}
                                temp[gchild.tag] = gchild.text
                                exec "self.%s.update(%s)" % (child.tag, temp)
                            
            else: 
                exec "self.%s = %s" % (dtype.tag, dtype.attrib)
                for child in dtype:
                    temp = {}
                    temp[child.tag] = child.text
                    exec "self.%s.update(%s)" % (dtype.tag, temp)
                    
class Enum(Mo):
    pass
class Struct(Mo):
    pass
class Exception(Mo):
    pass

                       
if __name__ == '__main__':
    name = "LteRbsNodeComplete_Itr27_R10D03.xml"
    #name = "sample.xml"
    parser = MomParser(name)
#     parser.printElem()
#     print parser.allattr
    print parser.printMo('MceFunction')

