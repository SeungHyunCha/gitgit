import xml.etree.ElementTree as ET
from collections import defaultdict

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
        self.count = 0
        self.relations = []
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
                    if self.count == 0:
                        self.mim = elem.attrib
                        self.count = 1
                    else: pass
                    
                else: 
                    if elem.tag == 'relationship':
                        relationname = Tree(elem)
#                         self.relations[] = relationname
                        temp = elem.attrib.values()[0]
                        temp= temp.split('_to_')
                        temp= (temp[0],temp[1])
                        self.relations.append(temp)
                        
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

class Mo:
    def __init__(self, elem):
        self.name = elem.attrib.values()[0]
        self.attrs_obj = {}
        self.flags = [] # systemcreated
        self.others = {} # description, etc
        self.parent = None
        self.child = None
        self.obj = elem
#         self.handle()
    
    def getName(self):
        return self.name
    
    def getDesc(self):
        try:
            desc = self.others['description']
            return desc
        except: pass
    
    def getFlags(self):
        temp = sorted(self.flags)
        try: 
            if temp[0] == []:
                del temp[0]
        except: pass
        temp = ','.join(temp)
        return str(temp)
    
    def addAttrs(self, attr):
        self.attrs_obj[attr.getName()] = attr
    
    def getAttrs(self): 
        return self.attrs_obj
    
    def handle(self):
        # To handle MOC except attribute, enumMember, structMember and exceptionParameter
        for mo_child in self.obj:
            if len(mo_child._children) == 0 and mo_child.tag != 'attribute' and 'enumMember' and 'structMember' and 'exceptionParameter':
                if mo_child.text == None: 
                    self.flags.append(mo_child.tag)
                else:
                    if mo_child.text == '\n\t\t\t\t': pass
                    else: 
                        self.others.update({mo_child.tag:mo_child.text})
            else: 
                if mo_child.tag == 'action':
                    pass
#                     print 'action', mo_child.text, mo_child.attrib
    
    def showMoInfo(self):
        show_info = ''
        line = "*" * 132
        show_info += '%s\nMOC\n%s\n' %(line, line)
        show_info += '%s\n' % self.name
        if self.getFlags():
            show_info += '%s\n' % self.getFlags()
        if self.getDesc():
            show_info += 'description\t%s\n' % self.getDesc()
        show_info += '%s\n%s%s%s\n%s\n' %(line, "Attribute".ljust(30), "Type".ljust(40), 'Flags', line)
        for key, value in sorted(self.attrs_obj.items()): 
            show_info += key.ljust(30) + value.getType().ljust(40) + value.getFlags() + '\n'
        return show_info
    
class Attr:
    def __init__(self, elem):
        self.name = elem.attrib.values()[0]
        self.obj = elem
        self.mo = None
        self.types = None
        self.flags = [] # readonly, restricted, mandatory, nonPersistent...(etc)
        self.length = {}
        self.range = {}
        self.values = {} # default, multi, unit....(etc)
        self.others = {} # description, dependancies...(etc)
        self.__handle()
    
    def getName(self):
        return self.name
    
    def getDesc(self):
        try:
            desc = self.others.__dict__['description']
            return desc
        except: pass
        
    def getMoName(self):
        return self.mo
        
    def getFlags(self):
        temp = sorted(self.flags)
        try: 
            if temp[0] == []:
                del temp[0]
        except: pass
        temp = ','.join(temp)
        return str(temp)
    
    def getType(self):
        if self.types == {}: return ''
        else: return str(self.types)
    
    def getLength(self):
        if self.length == {}: return ''
        else: 
            leng = []
            for val in sorted(self.length, reverse=True):
                leng.append(int(self.length[val]))
            return str(leng)
         
    def getRange(self):
        if self.range == []: return ''
        else:
            return sorted(self.range)
    
    def getValues(self):
        if self.values == {}: return ''
        else:
            val = []
            for v in sorted(self.values):
                val.append(self.values[v])
            return str(val)
    
    def getDefault(self):
        for key in self.values:
            if key == 'defaultValue':
                return str(self.values['defaultValue'])
            else: pass
        return ''
                
    def getUnit(self):
        for key in self.values:
            if key == 'unit':
                return str(self.values['unit'])
            else: pass
        return ''

    def getMulti(self):
        for key in self.values:
            if key == 'multiplicationFactor':
                return str(self.values['multiplicationFactor'])
            else: pass
        return ''
    
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
                        self.range = data.getRanges()
                        self.values = data.getValues()
                        self.types = data.getType()
                else:
                    data = DataType(attr)  
                    self.flags.append(data.getFlags())
                    self.length = data.getLength()
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
    
    def getFlags(self):
        return self.flags
    
    def getType(self):
        return self.types
    
    def getLength(self):
        return self.length
    
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
                                self.types = 'seq(%s)' % child.tag
                            else:
                                temp = {}
                                temp = {child.tag:child.attrib.values()[0]}
                                self.types = 'seq(%s)' % temp
                                
                    else:
                        if child._children == []:
                            self.length.update({child.tag:child.text})
                        else:
                            if child.tag == 'long':
                                self.types = 'seq(%s)' % child.tag
                                for gchild in child:
                                    if gchild._children == []:
                                        self.values.update({gchild.tag:gchild.text})
                                    else:
                                        for ggchild in gchild:
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
                                self.ranges.append(int(key.text))
                                
                        elif child.tag == 'lengthRange':
                            for key in child:
                                self.length.update({key.tag:key.text})
                                
                        else: 
                            if child._children == []:
                                self.values.update({child.tag:child.text})
                            else: 
                                if child.tag == 'stringLength':
                                    self.stringlength.update({child.tag:child.text})
                                print child, child.tag, child.text
                                for gchild in child:
                                    print gchild
                    else: pass
                    
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

class Tree:
    def __init__(self, elem):
        self.obj = elem
        self.temp_name = elem.attrib.values()[0]
        self.cardi = None
        self.relation = None
        self.__getRelation()
        self.__getCardi()
    
    def __getRelation(self):
        temp = self.temp_name.split('_to_')
        temp = (temp[0],temp[1])
        self.relation = temp
    
    def __test(self):
        pass
    
    def __getCardi(self):
        for child in self.obj:
            for gchild in child:
                for ggchild in gchild:
                    if ggchild.tag == 'cardinality':
                        pass#print 'ggchild', ggchild

def test(d):
    del_list = []
    for parent_mo, list_child in d.items():
#         if parent_mo[-3:] is not 'ref':
        for child_mo in list_child:
            for check in d.keys():
                if child_mo == check:
#             if child_mo in d.keys():
                    d[parent_mo].remove(child_mo)
                    d[parent_mo].append((child_mo, d[child_mo]))
                    del_list.append(child_mo)      
    return del_list
          
def testcase():
    name = "LteRbsNodeComplete_Itr27_R10D03.xml"
    parser = IterParser(name)
    d = defaultdict(list)
    for key, value in parser.relations:
        d[key].append(value)
    print d
    del_list = test(d)
    try:
        for del1 in del_list:
            del d[del1]
    except:
        pass
    
    print d

if __name__ == '__main__':
    testcase()