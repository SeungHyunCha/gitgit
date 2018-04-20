import xml.etree.ElementTree as ET
from define import *

class IterParser:
    def __init__(self, name):
        # all of information in dictionary {name:object}
        self.name = name
        self.mos = {}       # all of MO classes
        self.attrs = {}     # all of attributes
        self.enums = {}     # all of enums
        self.emembers = {}  # all of enum members
        self.structs = {}   # all of structs
        self.smembers = {}  # all of struct members
        self.exceps = {}    # all of exceptions
        self.expmembers = {}# all of exception parameters
        self.mim = {}       # information of MIM
        self.count = 0
        self.relations = {} # all of relationships
        self.__run()
        
    def __run(self):
        for event, elem in ET.iterparse(self.name, events=('start', 'end')):
            # Create object
            if event == 'start': 
                if elem.tag == 'class':
                    mo_class = Mo(elem)
                    self.mos[mo_class.getName()] = mo_class
                elif elem.tag == 'enum':
                    mo_class = Mo(elem)
                    self.enums[mo_class.getName()] = mo_class
                elif elem.tag == 'struct':
                    mo_class = Mo(elem)
                    self.structs[mo_class.getName()] = mo_class
                elif elem.tag == 'exception': 
                    mo_class = Mo(elem)
                    self.exceps[mo_class.getName()] = mo_class
                elif elem.tag == 'relationship':
                    relation_name = Relation(elem)
                    self.relations[relation_name.getName()] = relation_name
                else: pass
                
            # Parse and add an information in created object            
            elif event == 'end': 
                if elem.tag == 'class':
                    mo_class.handle()                            
                    for attr in elem:
                        if attr.tag == 'attribute': 
                            child = Attr(attr)
                            child.mo = mo_class.getName()
                            self.attrs[child.getName()] = child
                            mo_class.addAttrs(child)       
                        else: pass     
                elif elem.tag == 'enum': 
                    mo_class.handle()
                    for attr in elem:
                        if attr.tag == 'enumMember': 
                            child = Attr(attr)
                            child.mo = mo_class.getName()  
                            self.emembers[child.getName()] = child
                            mo_class.addAttrs(child)
                        else: pass
                elif elem.tag == 'struct': 
                    mo_class.handle()
                    for attr in elem:
                        if attr.tag == 'structMember': 
                            child = Attr(attr) 
                            child.mo = mo_class.getName() 
                            self.smembers[child.getName()] = child
                            mo_class.addAttrs(child)
                        else: pass
                elif elem.tag == 'exception': 
                    mo_class.handle()
                    for attr in elem:
                        if attr.tag == 'exceptionParameter': 
                            child = Attr(attr)  
                            child.mo = mo_class.getName()
                            self.expmembers[child.getName()] = child
                            mo_class.addAttrs(child)
                        else: pass
                elif elem.tag == 'mim': # Add MIM version
                    if self.count == 0:
                        self.mim = elem.attrib
                        self.count = 1
                    else: pass
                elif elem.tag == 'relationship':
                    relation_name.handle()
                else: pass

class Mo:
    def __init__(self, elem):
        self.name = elem.attrib.values()[0]
        self.attrs_obj = {} # attribute in MOC
        self.flags = [] # systemcreated, and so on
        self.others = {} # description, and so on
        self.obj = elem
    
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
            if temp[0] == []: del temp[0]
        except: pass
        temp = ','.join(temp)
        return str(temp)
    
    def addAttrs(self, attr):
        self.attrs_obj[attr.getName()] = attr
    
    def getAttrs(self): 
        return self.attrs_obj
    
    def handle(self):
        # To add flags and others
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
                    pass#print 'action', mo_child.text, mo_child.attrib

    # Show information using only -mo option
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
        self.flags = [] # readonly, restricted, mandatory, nonPersistent, and so on
        self.length = {} # length 
        self.range = {} # range
        self.values = {} # default, multi, unit, and so on
        self.others = {} # description, dependancies, and so on
        self.__handle()
    
    def getName(self):
        return self.name
    
    def getDesc(self):
        try:
            desc = self.others['description']
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
    # handle flags, others, and dataType
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
            self.flags.append(hidden)
                    
class DataType:
    def __init__(self, attr):
        self.attr = attr
        self.flags = []
        self.types = None
        self.length = {}
        self.stringlength = {}
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

class Relation:
    def __init__(self, elem):
        self.obj = elem
        self.name = elem.attrib.values()[0]
        self.type = None
        self.parent = None
        self.child = None
        self.to_cardi = None
        self.from_cardi = None
        self.from_class = None
        self.to_class = None
        self.from_attr = None
        self.to_attr = None
        self.to_flags = None
        
    def getName(self):
        return self.name    
        
    def getParentName(self):
        return self.parent
    
    def getChildName(self):
        return self.child
    
    def getCaldi(self):
        return self.to_cardi
    
    def handle(self):
        for attr in self.obj:
            if attr.tag == 'containment':
                self.type = attr.tag
                for child in attr:
                    if child.tag == 'parent':
                        for gchild in child:
                            self.parent = gchild.attrib.values()[0]
                    elif child.tag == 'child':
                        for gchild in child:
                            if gchild.tag == 'cardinality':
                                cardi = []
                                for ggchild in gchild:
                                    cardi.append(int(ggchild.text)) 
                                self.to_cardi = '%s' % list(set(cardi))
                            else:
                                self.child = gchild.attrib.values()[0]
                    else: pass
            elif attr.tag == 'biDirectionalAssociation':
                self.type = attr.tag
                for child in attr:
                    str = child.attrib.values()[0]
                    if str[-3:] != 'Ref':
                        self.to_attr = str # reservedBy
                        for gchild in child:
                            if gchild.tag == 'hasClass':
                                self.to_class = gchild.attrib.values()[0]
                            else:
                                cardi = []
                                for ggchild in child:
                                    cardi.append(ggchild.text)
                                self.to_cardi = '%s' % cardi
                    else:
                        self.from_attr = str # ref
                        for gchild in child:
                            if gchild.tag == 'hasClass':
                                self.from_class = gchild.attrib.values()[0]
                            else:
                                cardi = []
                                for ggchild in child:
                                    cardi.append(ggchild.text)
                                self.from_cardi = '%s' % cardi
        
def testcase():
    name = "LteRbsNodeComplete_Itr27_R10D03.xml"
#     name = "Lrat_DWAXE_mp_Itr27_R10E02.xml"
    parser = IterParser(name)
#     d = combinedTree(parser.relations)
#     a = getsubtree(d, 'ManagedElement')
    
if __name__ == '__main__':
    testcase()