import xml.etree.ElementTree as ET
import re

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
        str = "*" * 200
        if mo == "":    
            print str,'\n',"MO".ljust(30),'\n',str
            for mo in self.mos.keys():
                print mo   
            if attr != "":
                pass
        else:
            p = re.compile(mo, re.IGNORECASE)
            mo_list = self.mos.keys()
            for moc in mo_list:
                check = p.search(moc)
                if check:   
                    getMo = self.mos[moc]
#                     print getMo.getTag()
                    if attr == "":
                        getMo.showMoInfo()
                    else:
                        print str,'\n',"MOC".ljust(30), 'Attribute'.ljust(30), 'defaultValue'.ljust(30), 'Flags'.ljust(30), 'Range'.ljust(30)
                        m = re.compile(attr, re.IGNORECASE)
                        attr_list = getMo.getAttrs()
                        for attr_name in sorted(attr_list):
                            check1 = m.search(attr_name)
                            if check1:
                                getAttr = attr_list[attr_name]
                                print getAttr.mo.ljust(30), getAttr.getName().ljust(30), getAttr.getValues(), getAttr.getFlags().ljust(30), getAttr.getRange()
                            else:
                                pass
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
    
    def getTag(self):
        return self.obj.tag
    
    def addAttrs(self, attr):
        self.attrs_obj[attr.getName()] = attr
    
    def getAttrs(self): #get attrs
        return self.attrs_obj
    
    def addAttrsInfo(self, attr):
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
    
    def showMoInfo(self):
        str = "*" * 100
        print str,'\n', "MO", '\n', str 
        print self.name
        for flag in sorted(self.flags): print flag
        other_list = self.others.keys()
        for key in sorted(other_list): print "%s\t%s" %(key, self.others[key]) 
        print str,'\n',"Attribute".ljust(30), "Type".ljust(35), 'Flags', '\n', str
        for key, value in sorted(self.attrs_obj.items()): 
            print key.ljust(30), value.getType(), ''.ljust(29), value.getFlags()
        
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
    
    def getFlags(self):
        self.flags.pop()
        str = ','.join(self.flags)
        return str
    
    def getType(self):
        return self.type
    
    def getLength(self):
        return self.length
    
    def getRange(self):
        return self.range
    
    def getValues(self):
        return self.values
    
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
                    for child in attr:
                        data = DataType(child)
                        self.flags.append(data.getFlags())
                        self.length = data.getLength()
                        self.range = data.getRange()
                        self.values = data.getValues()
                        self.type = data.getType()
                else:
                    data = DataType(attr)  
#                 print data.getData()   
                
        
class DataType:
    def __init__(self, attr):
        self.attr = attr
        self.flags = []
        self.type = None
        self.length = {}
        self.range = {}
        self.values = {}
        self.__handle()
    
    def getData(self):
        return self.__dict__
    
    def getFlags(self):
        return self.flags
    
    def getType(self):
        return self.type
    
    def getLength(self):
        return self.length
    
    def getRange(self):
        return self.range
    
    def getValues(self):
        return self.values
    
    def __handle(self):
        if self.attr.attrib == {}: 
            self.type = self.attr.tag
            if self.type == 'sequence':
                for child in self.attr:
                    if child.text == None:
                        if child.tag == 'nonUnique':
                            self.flags = child.tag
                        else: 
                            if child.attrib == {}:
                                self.type = child.tag
                            else:
                                temp = {}
                                temp = {child.tag:child.attrib.values()[0]}
                                self.type = temp
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
                for child in self.attr:
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
            temp = {}
            temp = {self.attr.tag:self.attr.attrib.values()[0]}
            self.type = temp
            if self.attr._children == []: pass
            else:
                for child in self.attr:
                    self.values = {child.tag:child.text}
                                              
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
#     parser.mom()
    parser.mom(mo='Rcs')
#     parser.mom(mo='Rcs',attr='t')
#     parser.mom(mo='ReportConfigA1Sec')
#     parser.mom(mo='utrancelltdd')
#     parser.mom(mo='utrancelltdd', attr='pmradio')
#     parser.mom(mo='ReportConfigA1Sec', attr='r')

