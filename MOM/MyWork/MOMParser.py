import xml.etree.ElementTree as ET

class MomParser:
    Tag = ['class', 'enum', 'struct', 'exception']
    
    def __init__(self, name):
        self.name = name
        self.root = None
        self.allmo = {}
        self.allattr = {}
        self.allenum = {}
        self.allstruct = {}
        self.allexception = {}
        self.__run()
        
    def __run(self):
        for event, elem in ET.iterparse(self.name, events=('start', 'end')):
            if event == 'start' and self.root == None:              
                self.root = elem.tag                                                
            elif event == 'start': 
                if elem.tag == 'class':
                    mo = Mo(elem) # create MO
                    self.allmo[mo.getName()] = mo.addMo()
                
                elif elem.tag == 'enum': 
                    en = Enum(elem) # create ENUM
                    self.allenum[en.getName()] = en.addMo()
                
                elif elem.tag == 'struct':
                    st = Struct(elem)
                    self.allstruct[st.getName()] = st.addMo()
                
                elif elem.tag == 'exception': 
                    ex = Exception(elem)
                    self.allexception[ex.getName()] = ex.addMo()
                
                else: '-----Error %s in event' % elem.tag
            
            elif event == 'end':
                for mo_child in elem:  
                    if elem.tag == 'class': 
                        if mo_child.tag == 'attribute': 
                            attr = Attr(mo_child)   # create Attribute  
                            self.allattr[attr.getName()] = attr
                            attr.mo = mo.getName()
                            mo.addAttrs(attr)
                        else: pass
                    
                    elif elem.tag == 'enum':
                        if mo_child.tag == 'enumMember': 
                            attr = Attr(mo_child)  
                            en.addAttrs(attr)
                        else: pass
                        
                    elif elem.tag == 'struct':
                        if mo_child.tag == 'structMember': 
                            attr = Attr(mo_child)  
                            st.addAttrs(attr)
                        else: pass
                    
                    elif elem.tag == 'exception':
                        if mo_child.tag == 'exceptionParameter': 
                            attr = Attr(mo_child)  
                            ex.addAttrs(attr)
                        else: pass
                    else: pass 
            else: pass

    def printElem(self, mo="", attribute=""):
        pass

class Mo:
    def __init__(self, elem):
        self.name = elem.attrib.values()[0]
        self.attrs = {}
        self.elem = elem
        self.handle()
    
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
    
    def getAttrsInfo(self, attr):
        for key, value in attr.__dict__.items(): #get infomation of attrs
            self.attrs[key] = value
    
    def __str__(self):
        return 'MOC: ' + self.name
    
    def handle(self):
        for mo_child in self.elem:
            if len(mo_child._children) == 0 and mo_child.tag != 'attribute' or 'enumMember' or 'structMember':
                if mo_child.text == None: exec("self.%s = 'on'" % mo_child.tag)
                else: exec("self.%s = %r" % (mo_child.tag, mo_child.text))
            else: pass
    
    def getInfo(self):
        if self.name == None:
            print 'getInfo error!\n'
        else:
            info = '\n'
            info += '=' * 100
            
class Attr:
    def __init__(self, elem):
        self.name = elem.attrib.values()[0]
        self.elem = elem
        self.mo = None
        self.dataTypes = {}
        self.__handle()
    
    def getName(self):
        return self.name
    
    def getTag(self):
        return self.elem.tag
    
    def __handle(self):
        if self.elem.tag == 'structMember':
            for attribute in self.elem:
                if len(attribute._children) == 0:
                    if attribute.text == None: exec "self.%s = 'on'" % attribute.tag 
                    else: exec "self.%s = %r" % (attribute.tag, attribute.text) 
                else:
                    Type = DataType(attribute)
                    for key, value in Type.__dict__.items(): #get dataType
                        self.dataTypes[key] = value
        
class DataType:
    def __init__(self, elem):
        #self.name = None
        self.elem = elem
        self.__handle()

    def __handle(self):
        if self.elem.attrib == {}: pass
        else:
            exec "self.%s = %r" % (self.elem.attrib.keys()[0], self.elem.attrib.values()[0]) 
        for dtype in self.elem:
            exec "self.%s = []" % dtype.tag
            if dtype.attrib == {}:
                for child in dtype:
                    if len(child._children) == 0:
                        if child.attrib == {}: # get min,max values
                            temp = {}
                            temp[child.tag] = child.text
                            exec "self.%s.append(%s)" % (dtype.tag, temp)
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
                                    temp = {}
                                    temp[ggchild.tag] = ggchild.text
                                    exec "self.%s.append(%s)" % (child.tag, temp)
                            else:
                                temp = {}
                                temp[gchild.tag] = gchild.text
                                exec "self.%s.append(%s)" % (child.tag, temp)
                            
            else: 
                exec "self.%s.append(%s)" % (dtype.tag, dtype.attrib)
                for child in dtype:
                    temp = {}
                    temp[child.tag] = child.text
                    exec "self.%s.append(%s)" % (dtype.tag, temp)
                    
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

