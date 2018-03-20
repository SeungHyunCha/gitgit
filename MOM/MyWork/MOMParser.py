import xml.etree.ElementTree as ET
  
class MomParser(object):
    def __init__(self, name):
        self.name = name
        self.ns = {}
        self.root = None
        for event, elem in ET.iterparse(name, events=('start','end')):
            #print elem.tag
            if event == 'start' and self.root == None:              
                self.root = elem.tag                                                
            elif event == 'start':
                if elem.tag == 'class': # a class
                    moName = elem.attrib.values()[0] # name of the class
                    mo = MO(moName) # create the obj of 'MO class'
                elif elem.tag == 'enum': pass
                elif elem.tag == 'struct': pass
                elif elem.tag == 'exception': pass
                else: pass
            elif event == 'end':
                if elem.tag == 'class': # a class
                    for mo_child in elem: # child of the class
                        if mo_child.tag == 'attribute': # an attribute
                            attrName = mo_child.attrib.values()[0] # name of the attribute
                            attr = ATTR(attrName) # create the obj of 'ATTR class'
                            for attr_child in mo_child: # child of the attribute 
                                if len(attr_child._children) == 0: # Existence check of child 
                                    if attr_child.text == None: exec "attr.%s = 'on'" % attr_child.tag # 
                                    else: exec "attr.%s = %r" % (attr_child.tag, attr_child.text)
                                else: 
                                    for data_type_child in attr_child:
                                        #print type(attr_child.tag)
                                        #print type(data_type_child.tag)
                                        exec "attr.%s = %r" % (attr_child.tag, data_type_child.tag) 
                                        for range in data_type_child:
                                            print range
                            attr.mo = moName # add name of mo in attr obj
                            mo.attribute.append(attr) # add name of attr in mo obj
                            print 'Attribute', attr.__dict__
                        else: # except attribute
                            if len(mo_child._children) == 0:
                                if mo_child.text == None: exec("mo.%s = 'on'" % mo_child.tag)
                                else: exec("mo.%s = %r" % (mo_child.tag, mo_child.text))
                            else:
                                pass
                    print 'MO', mo.__dict__
                else: pass         
            else: pass
    
class MO(object):
    def __init__(self, name):
        self.name = name
        self.attribute = []
        self.description = None
        #self.parents = None
        #self.child = None
        
    def __getattribute__(self, attr):
        #print "get attr %s" % attr
        return object.__getattribute__(self, attr)
    def __setattr__(self, attr, val):
        #print "set attr %s to %r" % (attr, val)
        return object.__setattr__(self, attr, val)
    '''
    def __len__(self):
        return len(self.name)
    def __getitem__(self, k):
        return self.name[k]
    def __setitem__(self, k, v):
        self.name[k] = v
    '''
    
class ATTR(object):
    def __init__(self, name):
        self.name = name
        self.description = None
        self.mo = None
    def __getattribute__(self, attr):
        #print "get attr %s" % attr
        return object.__getattribute__(self, attr)
    def __setattr__(self, attr, val):
        #print "set attr %s to %r" % (attr, val)
        return object.__setattr__(self, attr, val)
    
if __name__ == '__main__':
    #name = "LteRbsNodeComplete_Itr27_R10D03.xml"
    name = "sample.xml"
    parser = MomParser(name)
    #print parser.ns    
