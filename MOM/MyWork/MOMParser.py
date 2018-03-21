import xml.etree.ElementTree as ET

class MomParser(object):
    def __init__(self, name):
        self.name = name
        self.ns = {}
        self.root = None
        for event, elem in ET.iterparse(name, events=('start', 'end')):
            if event == 'start' and self.root == None:              
                self.root = elem.tag                                                
            elif event == 'start': 
                if elem.tag == 'class':
                    mo = MO(elem.attrib.values()[0], elem) 
                    mo.handle()
                #elif elem.tag == 'enum': pass
                #elif elem.tag == 'struct': pass
                #elif elem.tag == 'exception': pass
                else: pass
            elif event == 'end':
                if elem.tag == 'class': 
                    for mo_child in elem:  
                        if mo_child.tag == 'attribute':  
                            attr = ATTR(mo_child.attrib.values()[0], mo_child)  
                            attr.handle()
                            attr.mo = elem.attrib.values()[0]
                            mo.attribute.append(attr.name)
                            #print 'Attribute', attr.__dict__
                        else: pass
                    print 'MO', mo.__dict__
                else: pass         
            else: pass

class MO(object):
    def __init__(self, name, elem):
        self.name = name
        self.attribute = []
        self.description = None
        # self.parents = None
        # self.child = None
        self.elem = elem
        
    def handle(self):
        for mo_child in self.elem:
            if len(mo_child._children) == 0 and mo_child.tag != 'attribute':
                if mo_child.text == None: exec("self.%s = 'on'" % mo_child.tag)
                else: exec("self.%s = %r" % (mo_child.tag, mo_child.text))
            else: pass#print 'error_MO_handle', mo_child.attrib
    '''    
    def __getattribute__(self, attr):
        # print "get attr %s" % attr
        return object.__getattribute__(self, attr)
    def __setattr__(self, attr, val):
        # print "set attr %s to %r" % (attr, val)
        return object.__setattr__(self, attr, val)
    '''
    
class ATTR(object):
    def __init__(self, name, elem):
        self.name = name
        self.description = None
        self.mo = None
        self.elem = elem
        self.dataType = None
        
    def handle(self):
        for attribute in self.elem:  
            if len(attribute._children) == 0:  
                if attribute.text == None: exec "self.%s = 'on'" % attribute.tag  
                else: exec "self.%s = %r" % (attribute.tag, attribute.text) 
            else:
                if attribute.tag == 'dataType':
                    temp = attribute._children[0].tag
                    Type = DataType(temp, attribute)
                    Type.handle()               
                    self.dataType = Type.name
                    print 'DataType', Type.__dict__
                else: 'error_ATTR_handle_datatype'   

class DataType(object):
    def __init__(self, name, elem):
        self.name = name
        self.elem = elem
        
    def handle(self):
        for dtype in self.elem:
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
    #name = "LteRbsNodeComplete_Itr27_R10D03.xml"
    name = "sample.xml"
    parser = MomParser(name)
    # print parser.ns    
