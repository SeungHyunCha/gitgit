import xml.etree.ElementTree as ET
import re
from test.test_codeccallbacks import NoEndUnicodeDecodeError

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
                    excepname = MyException(elem)
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
        if mo == "":    
            print str,'\n',"MO\t\t\t",'\n',str
            for mo in self.mos.keys():
                print mo   
        else:
            p = re.compile(mo, re.IGNORECASE)
            mo_list = self.mos.keys()
            for moc in mo_list:
                check = p.search(moc)
                if check:   
                    getMo = self.mos[moc]
#                     print getMo.getTag()
                    if attr == "":
                        getMo.showMoAttrInfo()
                    else:
                        print str,'\n',"Mo\t\t\tAttribute"
                        print getMo.getName()
                        m = re.compile(attr, re.IGNORECASE)
                        attr_list = getMo.getAttrs()
                        for attr_name in sorted(attr_list):
                            check1 = m.search(attr_name)
                            if check1:
                                getAttr = attr_list[attr_name]
                                getAttr.printAttr()

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
    
    def getTag(self):
        return self.obj.tag
    
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
                    if mo_child.tag != 'attribute':
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
        for flag in sorted(self.flags): print flag
        other_list = self.others.keys()
        for key in sorted(other_list): print "%s\t%s" %(key, self.others[key]) 
        print str,'\n',"Attribute:"
        for attr in sorted(self.attrs_obj.keys()): print "\t\t", attr
        print '\n'
        
class Attr:
    def __init__(self, elem):
        self.name = elem.attrib.values()[0]
        self.obj = elem
        self.mo = None
        self.type = None
        self.flags = []
        self.length = {}
        self.range = {}
        self.values = {}
        self.others = {}
        self.__handle()
    
    def getName(self):
        return self.name
    
    def getAttrFlag(self):
        return sorted(self.flags)
    
    def detAttrDatatype(self):
        return self.type.printData()
    
    def __handle(self):
            for attr in self.obj:
                if len(attr._children) == 0:
                    if attr.text == None: 
                        self.flags.append(attr.tag)
                    else: 
                        exec "self.%s = %r" % (attr.tag, attr.text)
                        self.others.update({attr.tag:attr.text})
                else:
                    if attr.tag == 'dataType':
                        self.type = DataType(attr)
                    else:
                        if attr.attrib == {}: 
                            self.type = attr.tag
                            if self.type == 'sequence':
                                for child in attr:
                                    if child.text == None: 
                                        print attr, child.tag
                                    else:
                                        if child._children == []:
                                            self.length.update({child.tag:child.text})
                                        else:
                                            if child.tag == 'long':
                                                self.type = child.tag
                                                for gchild in child:
                                                    if gchild._children == []:
                                                        self.values.update({gchild.tag:gchild.text})
                                                    else:
                                                        for ggchild in gchild:
                                                            self.range.update({ggchild.tag:ggchild.text})
                                            else: 
                                                temp = []
                                                for gchild in child:
                                                    temp.append(gchild.text)
                                                self.values.update({child.tag:temp})
                            else:
                                for child in attr:
                                    if child.attrib == {}:
                                        if child.tag == 'range':
                                            for key in child:
                                                self.range.update({key.tag:key.text})
                                        elif child.tag == 'lengthRange':
                                            for key in child:
                                                self.length.update({key.tag:key.text})
                                        else: 
                                            if child._children == []:
                                                self.values.update({child.tag:child.text})
                                            else:
                                                print 'attr __handle', child.tag, child.text
                                    else: 
                                        print 'attr __handle', child.tag, child.text
                        else:
                            pass
#     def printAttr(self):
#         str = "-" * 100
#         other_list = self.others.keys()
#         print "\t\t\t", self. name
#         print str
# #         print '<flag>',
# #         for flag in sorted(self.flags): print flag,
#         print '\n', 
# #         for key in sorted(other_list): print "%s %s" %(key, self.others[key]) // show attr description
#         if self.type == None: pass
#         else: self.type.printData()
#         print '\n', str
        
class DataType:
    def __init__(self, elem):
        self.elem = elem
        self.flags = []
        self.type = None
        self.length = {}
        self.range = {}
        self.values = {}
        self.__handle()
    
    def getData(self):
        return self.__dict__
    
    def __handle(self):
        temp = {}
        if self.elem.attrib == {}: pass
        else:
            exec "self.%s = %r" % (self.elem.attrib.keys()[0], self.elem.attrib.values()[0]) 
        for dtype in self.elem:
            exec "self.%s = {}" % dtype.tag
            self.type = dtype.tag
            if dtype.attrib == {}:
                for child in dtype:
                    if len(child._children) == 0:
                        if child.attrib == {}: # get min,max values
                            if child.text == None: 
                                if dtype.tag == 'sequence': 
                                    self.type = dtype.tag
                                else: self.flags.append(dtype.tag)
#                                 exec "self.%s = {}" % child.tag
                            else:
                                temp[child.tag] = child.text
                                exec "self.%s.update(%s)" % (dtype.tag, temp)
#                                 print dtype.tag, child.tag, temp
                        else: # Ref elem
                            if child.text == None: 
                                exec "self.%s = %r" % (child.tag, child.attrib.values()[0])
                            else: print 'error', self.elem, dtype.tag
                    else:
                        exec "self.%s = {}" % child.tag
                        for gchild in child:
                            if gchild.text == '\n\t\t\t\t\t\t\t':
                                for ggchild in gchild: # min, max value
                                    temp[ggchild.tag] = ggchild.text
                                    exec "self.%s.update(%s)" % (child.tag, temp)
                            else:
                                temp[gchild.tag] = gchild.text
                                exec "self.%s.update(%s)" % (child.tag, temp)
                            
            else: 
                exec "self.%s = {%r}" % (dtype.tag, dtype.attrib.values()[0]) # Ref elem
                for child in dtype:
                    temp[child.tag] = child.text
                    exec "self.%s.update(%s)" % (dtype.tag, temp)
                    
    def printData(self):
        key_list = self.__dict__
#         print key_list
#         print 'type', self.type
        for val in self.__dict__:
            if val == self.type: 
                values = self.__dict__[val]
                for name in values:
                    self.values.update({name:values[name]})
            else: pass 
                
#         print self.values
        for key in key_list: pass
#                     child = self.__dict__[key]
#                     if key == 'range':
#                         print "\t", key,
#                         print 'min:', child[r'min*'], '^max:', child[r'max*']
#                     elif key == 'enumRef' or 'structRef':
#                         print key, child
# #                         for cchild in child:
# #                             if cchild == 'name': print "\t", key, str(child[cchild])
# #                             else: print "\t\t\t\t\t", cchild, str(child[cchild])    
#                     else:
#                         print "\t", key
#                         for cchild in child:
#                             print "\t", str(cchild), str(child[cchild])    
                    
                        
class Enum(Mo): pass
class Struct(Mo): pass
class MyException(Mo): pass

                       
if __name__ == '__main__':
    name = "LteRbsNodeComplete_Itr27_R10D03.xml"
#     old_mom = """
#     fdsafsa
#     
#     """
    #name = "sample.xml"
    parser = MomParser(name)
#     print 'aaa'
#     parser.mom(mo='Rcs')
#     parser.mom(mo='ReportConfigA1Sec')
#     parser.mom(mo='utrancelltdd')
    parser.mom(mo='utrancelltdd', attr='r')
#     print 'aaa'
#     parser.mom(mo='ReportConfigA1Sec', attr='r')

