import xml.etree.ElementTree as ET
import re

class IterParser:
    def __init__(self, name):
        self.name = name
        self.mos = {}
        self.attrs = {}
        self.enums = {}
        self.emembers = {}
        self.structs = {}
        self.smembers = {}
        self.exceps = {}
        self.expmembers = {}
        self.mim = {}
        self.relations = {}
        self.__run()
        
    def __run(self):
        for event, elem in ET.iterparse(self.name, events=('start', 'end')):
            if event == 'start': # create obj for mo, enum, struct, exception
                if elem.tag == 'class':
                    moname = Mo(elem)
                    self.mos[moname.getName()] = moname
                elif elem.tag == 'enum':
                    enumname = Enum(elem)
                    self.enums[enumname.getName()] = enumname
                elif elem.tag == 'struct':
                    structname = Struct(elem)
                    self.structs[structname.getName()] = structname
                elif elem.tag == 'exception': 
                    excepname = MyException(elem)
                    self.exceps[excepname.getName()] = excepname
                elif elem.tag == 'mim': # mim version
                    self.mim = elem.attrib
                else: 
                    if elem.tag == 'relationship':
                        temp = elem.attrib.values()[0]
                        temp= temp.split('_to_')
                        temp= {temp[0]:temp[1]}
                        self.relations.update(temp)
                        
            elif event == 'end': # add infomation in obj
                if elem.tag == 'class':
                    moname.handle()
                    for attr in elem:
                        if attr.tag == 'attribute': 
                            child = Attr(attr)
                            child.mo = moname.getName()
                            self.attrs[child.getName()] = child
                            moname.addAttrs(child)            
                elif elem.tag == 'enum': 
                    enumname.handle()
                    for attr in elem:
                        if attr.tag == 'enumMember': 
                            child = Attr(attr)
                            child.mo = enumname.getName()  
                            self.emembers[child.getName()] = child
                            enumname.addAttrs(child)
                elif elem.tag == 'struct': 
                    structname.handle()
                    for attr in elem:
                        if attr.tag == 'structMember': 
                            child = Attr(attr) 
                            child.mo = structname.getName() 
                            self.smembers[child.getName()] = child
                            structname.addAttrs(child)
                elif elem.tag == 'exception': 
                    excepname.handle()
                    for attr in elem:
                        if attr.tag == 'exceptionParameter': 
                            child = Attr(attr)  
                            child.mo = excepname.getName()
                            self.expmembers[child.getName()] = child
                            excepname.addAttrs(child)
                else: pass
            else: pass
'''
    def mom(self, mo="", attr=""): # print element
        line = "*" * 200
        print line
        print 'name:"%s"' % self.mim['name'], 'version:"%s"' % self.mim['version'], 'release:"%s"' %self.mim['release'], 'author:"%s"' %self.mim['author'], 'revision:"%s"' %self.mim['revision']
        if mo == "":   
            if attr == "": 
                # show mo, enum, struct, exception
                print line,'\n',"MO".ljust(30),'\n',line
                for mo in self.mos:
                    print mo
                print '\n', line,'\n',"ENUM".ljust(30),'\n',line
                for enum in self.enums:
                    print enum
                   
            else:
                print line,'\n',"MOC".ljust(30), 'Attribute'.ljust(30), 'defaultValue'.ljust(30), 'Flags'.ljust(30), 'Range'.ljust(30)
                print line
                p = re.compile(attr, re.IGNORECASE)
                for attr_name in self.attrs:
                    check = p.search(attr_name)
                    if check:
                        getAttr = self.attrs[attr_name]
#                         print getAttr.getMoName().ljust(30), getAttr.getName().ljust(30), getAttr.getValues(), getAttr.getFlags().ljust(30), getAttr.getRange()
                        print getAttr.getMoName().ljust(30), getAttr.getName().ljust(30), getAttr.getFlags().ljust(40), getAttr.getLength().ljust(20), getAttr.getValues().ljust(20), getAttr.getRange()
                            
                    else:
                        pass
                        
        else:
            p = re.compile(mo, re.IGNORECASE)
            for moc in self.mos:
                check = p.search(moc)
                if check:   
                    getMo = self.mos[moc]
                    if attr == "":
                        getMo.showMoInfo()
                    else:
                        print line,'\n',"MOC".ljust(30), 'Attribute'.ljust(30), 'Flags'.ljust(40), 'length'.ljust(20), 'default'.ljust(20), 'Range'
                        print line
                        m = re.compile(attr, re.IGNORECASE)
                        attr_list = getMo.getAttrs()
                        for attr_name in sorted(attr_list):
                            check1 = m.search(attr_name)
                            if check1:
                                getAttr = attr_list[attr_name]
                                print getAttr.mo.ljust(30), getAttr.getName().ljust(30), getAttr.getFlags().ljust(40), getAttr.getLength().ljust(20), getAttr.getValues().ljust(20), getAttr.getRange()
                            else:
                                pass
                else: pass
'''       
class Mo:
    def __init__(self, elem):
        self.name = elem.attrib.values()[0]
        self.attrs_obj = {}
#         self.attrs_info = {}
        self.flags = []
        self.others = {}
        self.parent = None
        self.child = None
        self.obj = elem
#         self.handle()
    
    def getName(self):
        return self.name
    
    def getDesc(self):
        for desc in self.others: 
            if desc == 'description':
                desc = self.others[desc]
                return desc
    
    def getTag(self):
        return self.obj.tag
    
    def addAttrs(self, attr):
        self.attrs_obj[attr.getName()] = attr
    
    def getAttrs(self): 
        return self.attrs_obj
    
#     def addAttrsInfo(self, attr):
#         self.attrs_info[attr.getName()] = attr.__dict__.items()
    
#     def getAttrsInfo(self):
#         return self.attrs_info
    
    def addParent(self, name):
        self.parent = name
    
    def addChild(self, name):
        self.child, name
    
    def getParent(self):
        return self.parent
    
    def getChild(self):
        return self.child
    
    def handle(self):
        for mo_child in self.obj:
            if len(mo_child._children) == 0 and mo_child.tag != 'attribute' and 'enumMember' and 'structMember' and 'exceptionParameter':
                if mo_child.text == None: 
                    exec "self.%s = {}" % mo_child.tag
                    self.flags.append(mo_child.tag)
                else: 
                    if mo_child.text == '\n\t\t\t\t': pass
                    else: 
                        exec "self.%s = %r" % (mo_child.tag, mo_child.text)
                        self.others.update({mo_child.tag:mo_child.text})
            else: pass
    
    def showMoInfo(self):
        line = "*" * 120
        print line,'\n', "MOC", '\n', line
        print self.name
        for flag in sorted(self.flags): print flag
        for key in sorted(self.others): print "%s\t%s" %(key, self.others[key]) 
        print line,'\n',"Attribute".ljust(30), "Type".ljust(40), 'Flags', '\n', line
        for key, value in sorted(self.attrs_obj.items()): 
            print key.ljust(30), value.getType().ljust(40), value.getFlags()
        
class Attr:
    def __init__(self, elem):
        self.name = elem.attrib.values()[0]
        self.obj = elem
        self.mo = None
        self.types = None
        self.flags = []
        self.length = {}
        self.range = {}
        self.values = {}
        self.others = {}
        self.__handle()
    
    def getName(self):
        return self.name
    
    def getDesc(self):
        for desc in self.others: 
            if desc == 'description':
                desc = self.others[desc]
                return desc
            
    def getMoName(self):
        return self.mo
        
    def getFlags(self):
        temp = sorted(self.flags)
        if temp[0] == []:
            del temp[0]
        temp = ','.join(temp)
        return temp
    
    def getType(self):
        if self.types == {}:
            return 
        else: return str(self.types)
    
    def getLength(self):
        if self.length == {}:
            return ''
        else: 
            leng = []
            for val in sorted(self.length, reverse=True):
                leng.append(int(self.length[val]))
            return str(leng)
         
    def getRange(self):
        if self.range == []:
            return ''
        else:
            return sorted(self.range)
    
    def getValues(self):
        if self.values == {}:
            return ''
        else:
            val = []
            for v in sorted(self.values):
                val.append(self.values[v])
            return str(val)
    
    def getOthers(self):
        return self.others
    
    def getAttrFlag(self):
        return sorted(self.flags)
    
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
#                         self.range = data.getRange()
                        self.range = data.getRanges()
                        self.values = data.getValues()
                        self.types = data.getType()
                else:
                    data = DataType(attr)  
                    self.flags.append(data.getFlags())
                    self.length = data.getLength()
#                     self.range = data.getRange()
                    self.ranges = data.getRanges()
                    self.values = data.getValues()
                    self.types = data.getType()
                    
        if 'visibility' in self.others:
                    self.flags.append('EricssonOnly')
                    
class DataType:
    def __init__(self, attr):
        self.attr = attr
        self.flags = []
        self.types = None
        self.length = {}
        self.range = {}
        self.ranges = []
        self.values = {}
        self.__handle()
    
    def getData(self):
        return self.__dict__
    
    def getFlags(self):
        return self.flags
    
    def getType(self):
        return self.types
    
    def getLength(self):
        return self.length
    
    def getRange(self):
        return self.range
    
    def getRanges(self):
        return self.ranges
    
    def getValues(self):
        return self.values
    
    def __handle(self):
        if self.attr.attrib == {}: 
            self.types = self.attr.tag
            if self.types == 'sequence':
                for child in self.attr:
                    if child.text == None:
                        if child.tag == 'nonUnique':
                            self.flags = child.tag
                        else: 
                            if child.attrib == {}:
                                self.types = child.tag
                            else:
                                temp = {}
                                temp = {child.tag:child.attrib.values()[0]}
                                self.types = temp
                    else:
                        if child._children == []:
                            self.length.update({child.tag:child.text})
                        else:
                            if child.tag == 'long':
                                self.types = child.tag
                                for gchild in child:
                                    if gchild._children == []:
                                        self.values.update({gchild.tag:gchild.text})
                                    else:
                                        for ggchild in gchild:
                                            self.range.update({ggchild.tag:ggchild.text})
                                            self.ranges.append(int(ggchild.text))
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
                                self.ranges.append(int(key.text))
                        elif child.tag == 'lengthRange':
                            for key in child:
                                self.length.update({key.tag:key.text})
                        else: 
                            if child._children == []:
                                self.values.update({child.tag:child.text})
                            else: print 'attr __handle', child.tag, child.text
                    else: print 'attr __handle', child.tag, child.text
        else:
            temp = {}
            temp = {self.attr.tag:self.attr.attrib.values()[0]}
            self.types = temp
            if self.attr._children == []: pass
            else:
                for child in self.attr:
                    self.values = {child.tag:child.text}
                                              
class Enum(Mo): pass
class Struct(Mo): pass
class MyException(Mo): pass
 
def testcase():
    name = "LteRbsNodeComplete_Itr27_R10D03.xml"
#     name = "sample.xml"
    parser = IterParser(name)
    parser.mom()
#     parser.mom()
#     parser.mom(mo='nbiot')
#     parser.mom(mo='nbiot', attr='pm')
#     parser.mom(mo='utrancelltdd', attr='pmradio')
#     parser.mom(attr='id$')
#     parser.mom(attr='^freq')
#     parser.mom(attr='^nbiot')
#     parser.mom(mo='Rcs',attr='t')
#     parser.mom(mo='ReportConfigA1Sec')
#     parser.mom(mo='ReportConfigA1Sec', attr='r')
#     parser.mom(mo='ReportConfigA1Sec', attr='r')

if __name__ == '__main__':
    testcase()