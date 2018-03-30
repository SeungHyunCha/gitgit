import xml.etree.ElementTree as ET

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
                    self.mos[moname.getName()] = moname
                elif elem.tag == 'enum':
                    enname = Enum(elem)
                elif elem.tag == 'struct':
                    structname = Struct(elem)
                elif elem.tag == 'exception': 
                    excepname = Exception(elem)
                else: pass    

            elif event == 'end': # add infomation in obj
                for attr in elem: 
                    if elem.tag == 'class' and attr.tag == 'attribute':
                        child = Attr(attr)
                        child.mo = moname.getName()
                        self.attrs[child.getName()] = child
                        moname.addAttrs(child)
                        moname.addAttrsInfo(child)
                    
                    elif elem.tag == 'enum' and attr.tag == 'enumMember': 
                        child = Attr(attr)  
                        enname.addAttrs(child)
                        
                    elif elem.tag == 'struct' and attr.tag == 'structMember': 
                        child = Attr(attr)  
                        structname.addAttrs(child)
                    
                    elif elem.tag == 'exception' and attr.tag == 'exceptionParameter': 
                        child = Attr(attr)  
                        excepname.addAttrs(child)
                    else: pass
                    
            else: pass

    def mom(self, mo="", attr=""): # print element
        str = "*" * 100
        mo_list = self.mos.keys()
        if attr == "":
            if mo in mo_list: # check mo
                getMo = self.mos[mo]
                getMo.showMoAttrInfo()
    
            elif mo == "":
                print str,'\n',"MO\t\t\t",'\n',str
                for mo in self.mos.keys():
                    print mo
                    
            else:
                print str,'\n',"MO\t\t\t",'\n',str
                print str, '\n', "Attribute\t\t",'\n',str
        
        else:
            if mo == "":
                if attr in self.attrs:
                    getAttr = self.attrs[attr]
                    getAttr.printAttr()
            else: pass
    
class Mo:
    def __init__(self, elem):
        self.name = elem.attrib.values()[0]
        self.attrs_obj = {}
        self.attrs_info = {}
        self.flags = []
        self.others = {}
        self.obj = elem
        self.handle()
    
    def getName(self):
        return self.name
    
    def addAttrs(self, attr):
        self.attrs_obj[attr.getName()] = attr
    
    def getAttrs(self): #get attrs
        return self.attrs_obj
    
    def addAttrsInfo(self, attr):
#         for key, value in attr.__dict__.items(): #add infomation of attrs
        self.attrs_info[attr.getName()] = attr.__dict__.items()
    
    def getAttrsInfo(self):
        return self.attrs_info
    
    def handle(self):
        for mo_child in self.obj:
            if len(mo_child._children) == 0 and mo_child.tag != 'attribute' or 'enumMember' or 'structMember':
                if mo_child.text == None: 
                    exec("self.%s = {}" % mo_child.tag)
                    self.flags.append(mo_child.tag)
                else: 
                    if mo_child.text == '\n\t\t\t\t': pass
                    else: 
                        exec("self.%s = %r" % (mo_child.tag, mo_child.text))
                        self.others.update({mo_child.tag:mo_child.text})
            else: pass
    
    def showMoAttrInfo(self):
        str = "*" * 100
        print str,'\n',"MO:\t\t", self.name, '\n'
        for flag in self.flags: print flag
        other_list = self.others.keys()
        for key in other_list: print "%s\t%s" %(key, self.others[key]) 
        print str,'\n',"Attribute:"
        for attr in self.attrs_obj.keys(): print "\t\t", attr
        
class Attr:
    def __init__(self, elem):
        self.name = elem.attrib.values()[0]
        self.obj = elem
        self.description = None
        self.mo = None
        self.dataTypes = {}
        self.flags = []
        self.others = {}
        self.__handle()
    
    def getName(self):
        return self.name
    
    def getData(self):
        return self.__dict__
        
    def __handle(self):
            for attr in self.obj:
                if len(attr._children) == 0:
                    if attr.text == None: 
                        exec "self.%s = {}" % attr.tag
                        self.flags.append(attr.tag)
                    else: 
                        exec "self.%s = %r" % (attr.tag, attr.text)
                        self.others.update({attr.tag:attr.text})
                else:
                    Type = DataType(attr)
                    Type.printData()
                    for key, value in Type.__dict__.items(): #get dataType in Attr
                        if key == 'elem': pass
                        else: self.dataTypes[key] = value

    def printAttr(self):
        str = "*" * 100
        print str,'\n',"Mo\t\t\tAttr"
        print str,'\n',self.mo,"\t", self. name
        print str
        for flag in self.flags: print flag
        other_list = self.others.keys()
        for key in other_list: print "%s\t%s" %(key, self.others[key])
        
class DataType:
    def __init__(self, elem):
        self.elem = elem
        self.values = []
        self.__handle()

    def __handle(self):
        if self.elem.attrib == {}: pass
        else:
            exec "self.%s = %r" % (self.elem.attrib.keys()[0], self.elem.attrib.values()[0]) 
#             print self.elem.attrib.keys()[0], self.elem.attrib.values()[0]
        for dtype in self.elem:
            exec "self.%s = {}" % dtype.tag
            if dtype.attrib == {}:
                for child in dtype:
                    if len(child._children) == 0:
                        if child.attrib == {}: # get min,max values
                            if child.text == None: 
                                exec "self.%s = {}" % child.tag
                            else:
                                self.values.append(child.text)
                                temp = {}
                                temp[child.tag] = child.text
                                exec "self.%s.update(%s)" % (dtype.tag, temp)
                        else:
                            if child.text == None: 
                                exec "self.%s = %r" % (child.tag, child.attrib.values()[0])
#                                 print child.tag, child.attrib.values()[0]
                            else: pass
                    else:
                        exec "self.%s = {}" % child.tag
                        for gchild in child:
                            if gchild.text == '\n\t\t\t\t\t\t\t':
                                for ggchild in gchild:
                                    self.values.append(ggchild.text)
                                    temp = {}
                                    temp[ggchild.tag] = ggchild.text
                                    exec "self.%s.update(%s)" % (child.tag, temp)
                            else:
                                self.values.append(gchild.text)
                                temp = {}
                                temp[gchild.tag] = gchild.text
                                exec "self.%s.update(%s)" % (child.tag, temp)
                            
            else: 
                exec "self.%s = %s" % (dtype.tag, dtype.attrib)
                for child in dtype:
                    self.values.append(child.text)
                    temp = {}
                    temp[child.tag] = child.text
                    exec "self.%s.update(%s)" % (dtype.tag, temp)
                    
    def printData(self):
        key_list = self.__dict__.keys()
        for key in key_list:
            if key != 'elem': 
                if self.__dict__[key] == {}:
                    pass#print '*************', key
                else:
                    child = self.__dict__[key]
                    if key == None: pass
                    else:
                        print self.values, key, child
#                         for value in child_list:
#                             print value
                        
                    
                        
class Enum(Mo): pass
class Struct(Mo): pass
class Exception(Mo): pass

                       
if __name__ == '__main__':
    name = "LteRbsNodeComplete_Itr27_R10D03.xml"
    #name = "sample.xml"
    parser = MomParser(name)
#     parser.mom()
    parser.mom(mo='ReportConfigA1Sec')
    parser.mom(attr='a1ThresholdRsrpSec')

