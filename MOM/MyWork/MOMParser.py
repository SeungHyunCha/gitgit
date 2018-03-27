import xml.etree.ElementTree as ET

class MomParser:
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
            elif event == 'start': # create obj for mo, enum, struct, exception
                if elem.tag == 'class':
                    mo = Mo(elem)
                    self.allmo[mo.getName()] = mo.addMo()
                
                elif elem.tag == 'enum': 
                    en = Enum(elem) 
                    self.allenum[en.getName()] = en.addMo()
                
                elif elem.tag == 'struct':
                    st = Struct(elem)
                    self.allstruct[st.getName()] = st.addMo()
                
                elif elem.tag == 'exception': 
                    ex = Exception(elem)
                    self.allexception[ex.getName()] = ex.addMo()

                else: '-----Error %s in event' % elem.tag
            
            elif event == 'end': # add infomation in obj
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
                        
                    elif elem.tag == 'relationship':
                        for attr in elem:
                            for child in attr:
#                                 print child.tag # parent, child
                                for relation in child:
                                    if relation.attrib != {}:
                                        if relation.attrib.values()[0] in self.allmo:
                                            print relation.attrib, relation.attrib.values()[0]
                                            moaddr = self.allmo[relation.attrib.values()[0]]
                                            print moaddr
                                            addvar = Mo(self.allmo[relation.attrib.values()[0]])
#                                             print addvar.__dict__
                                            for card in relation:
                                                pass
                                        else:
                                            print relation, relation.tag, relation.attrib, relation.text
                                '''
                        moname = elem.attrib.values()[0].split('_to_')
                        parent = moname[0]
                        child = moname[1]
                        if parent in self.allmo:
                            a = Mo(self.allmo[parent])
                            for attr in elem:
                                for child in attr:
                                    print child.tag
                                    for relation in child:
#                                         print relation.tag, relation.attrib, relation.text
                                        for card in relation:
                                            pass
#                                             print card.tag, card.text
'''
                    else: pass 
            else: pass

    def printMo(self):
        print self.allmo
    
    def printAttr(self):
        print self.allattr
    
    def printEnum(self):
        print self.allenum
        
    def printStruct(self):
        print self.allstruct
        
    def printException(self):
        print self.allexception
        
    def printElem(self, mo="", attribute=""):
        pass #print 

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
#     parser.printElem()
#     print parser.allattr
#     print parser.printMo()

