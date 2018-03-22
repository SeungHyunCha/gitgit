import xml.etree.ElementTree as ET

class MomParser:
    TAG = ('class', 'attribute', 'enum', 'struct', 'exception')
    def __init__(self, name):
        self.name = name
        self.root = None
        self.whole_mo = {}
        self.whole_attr = {}
        self.__run()
        
    def __run(self):
        for event, elem in ET.iterparse(self.name, events=('start', 'end')):
            if event == 'start' and self.root == None:              
                self.root = elem.tag                                                
            elif event == 'start': 
                if elem.tag == 'class':
                    mo = Mo(elem)
                    self.whole_mo[mo.getName()] = mo.addMo()
                elif elem.tag == 'enum': pass
                elif elem.tag == 'struct': pass
                elif elem.tag == 'exception': pass
                else: pass
            elif event == 'end':
                if elem.tag == 'class': 
                    for mo_child in elem:  
                        if mo_child.tag == 'attribute': 
                            attr = Attr(mo_child)  
                            self.whole_attr[attr.getName()] = attr
                            attr.mo = mo.getName()
                            mo.addAttrs(attr)
                        else: pass
                    print mo.__dict__
                else: pass         
            else: pass
    
    def printElem(self, mo="", attribute=""):
        pass

class Mo:
    def __init__(self, elem):
        self.name = elem.attrib.values()[0]
        self.attrs = {}
        # self.parents = None
        # self.child = None
        self.elem = elem
        self.__handle()
    
    def getName(self):
        return self.name
    
    def addMo(self):
        return self.elem
    
    def getTag(self):
        return self.elem.tag
            
    def addAttrs(self, attr):
        self.attrs[attr.getName()] = attr
    
    def getAttrs(self): #get attrs
        return self.attrs
    
    def getAttrsinfo(self, attr):
        for key, value in attr.__dict__.items(): #get infomation of attrs
            self.attrs[key] = value
    
    def __str__(self):
        return 'MOC: ' + self.name
    
    def __handle(self):
        for mo_child in self.elem:
            if len(mo_child._children) == 0 and mo_child.tag != 'attribute':
                if mo_child.text == None: exec("self.%s = 'on'" % mo_child.tag)
                else: exec("self.%s = %r" % (mo_child.tag, mo_child.text))
            else: pass#print 'error_Mo_handle', mo_child.attrib
    
class Attr:
    def __init__(self, elem):
        self.name = elem.attrib.values()[0]
        self.elem = elem
        self.mo = None
        self.types = {}
        self.__handle()
    
    def getName(self):
        return self.name
    
    def getTag(self):
        return self.elem.tag
    
    def __str__(self):
        return 'Attribute: ' + self.name
        
    def __handle(self):
        for attribute in self.elem:  
            if len(attribute._children) == 0:  
                if attribute.text == None: exec "self.%s = 'on'" % attribute.tag
                else: exec "self.%s = %r" % (attribute.tag, attribute.text) 
            else:
                if attribute.tag == 'dataType':
                    Type = DataType(attribute)        
                    for key, value in Type.__dict__.items(): #get dataType
                        self.types[key] = value
                else: 'error_Attr_handle_datatype'   

class DataType:
    def __init__(self, elem):
        self.name = None
        self.elem = elem
        self.__handle()

    def __handle(self):
        for dtype in self.elem:
            self.name = dtype.tag
            if dtype.attrib == {}:  
                for child in dtype:
                    if len(child._children) == 0:
                        if child.attrib == {}:
                            exec "self.%s = %r" % (child.tag, child.text)
                        else:
                            if child.text == None:
                                exec "self.%s = %r" % (child.tag, child.attrib.values()[0])
                            else:
                                print 'error_dataType_handle', child.tag, child.attrib.values()[0], child.text
                    else:
                        exec "self.%s = []" % child.tag
                        for gchild in child:
                            if gchild.text == '\n\t\t\t\t\t\t\t':
                                for ggchild in gchild:
                                    exec "self.%s.append({%r:%r})" % (child.tag, ggchild.tag, ggchild.text)
                            else:
                                exec "self.%s.append({%r:%r})" % (child.tag, gchild.tag, gchild.text)
                            
            else: 
                exec "self.%s = %r" % (dtype.tag, dtype.attrib)
                for child in dtype:
                    exec "self.%s.update({%r:%r})" % (dtype.tag, child.tag, child.text)
                         
if __name__ == '__main__':
    name = "LteRbsNodeComplete_Itr27_R10D03.xml"
    #name = "sample.xml"
    parser = MomParser(name)
    #parser.show();

