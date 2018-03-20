import xml.etree.ElementTree as ET

class MomParser(object):
    def __init__(self, name):
        self.name = name
        self.ns = {}
        self.root = None
        for event, elem in ET.iterparse(name, events=('start', 'end')):
            # print elem.tag
            if event == 'start' and self.root == None:              
                self.root = elem.tag                                                
            elif event == 'start':
                if elem.tag == 'class':  # a class
                    moName = elem.attrib.values()[0]  # name of the class
                    mo = MO(moName)  # create the obj of MO           
                elif elem.tag == 'enum': pass
                elif elem.tag == 'struct': pass
                elif elem.tag == 'exception': pass
                else: pass
            elif event == 'end':
                if elem.tag == 'class':  # a class
                    for mo_child in elem:  # child of the class
                        if mo_child.tag == 'attribute':  # has an attribute
                            attrName = mo_child.attrib.values()[0]  # name of the attribute
                            attr = ATTR(attrName, mo_child)  # create the obj of attribute
                            
                            attr.mo = moName  # add name of mo in attr obj
                            mo.attribute.append(attr)  # add name of attr in mo obj
                            # print 'Attribute', attr.__dict__
                        else:  # other elements
                            if len(mo_child._children) == 0:
                                if mo_child.text == None: exec("mo.%s = 'on'" % mo_child.tag)
                                else: exec("mo.%s = %r" % (mo_child.tag, mo_child.text))
                            else:
                                pass
                    # print 'MO', mo.__dict__
                else: pass         
            else: pass

class MO(object):
    def __init__(self, name):
        self.name = name
        self.attribute = []
        self.description = None
        # self.parents = None
        # self.child = None
    '''    
    def __getattribute__(self, attr):
        # print "get attr %s" % attr
        return object.__getattribute__(self, attr)
    def __setattr__(self, attr, val):
        # print "set attr %s to %r" % (attr, val)
        return object.__setattr__(self, attr, val)
    '''
    
class ATTR(object):
    def __init__(self, name, child):
        self.name = name
        self.description = None
        self.mo = None
        self.child = child
    
    def handle(self):
        for attr_child in self.child:  # child of the attribute 
            if attr_child._children == []:  # if there is no child 
                # print attr_child, attr_child._children
                if attr_child.text == None: exec "attr.%s = 'on'" % attr_child.tag  # if there is text in child 
                else: exec "attr.%s = %r" % (attr_child.tag, attr_child.text)  # if there is no text in child
            else:  # if there is any child
                for data_type_child in attr_child:
                    # print data_type_child, data_type_child.attrib
                    if data_type_child.attrib == {}:  # dataType
                        exec "attr.%s = %r" % (attr_child.tag, data_type_child.tag) 
                        print attr_child.tag, data_type_child.tag
                        for range in data_type_child:
                            print range
                            if len(range._children) == 0:
                                pass  # print 'nochild', range.tag, range.attrib, range.text
                            else:
                                pass  # print 'child', range.tag, range.attrib, range.text
                                for range_child in range:
                                    pass
                                    # print range.tag, range_child.tag
                                    for child in range_child:
                                        pass
                                        # print child.tag, child.text
                    else: 
                        # print data_type_child.tag, data_type_child.attrib
                        exec "attr.%s = %r" % (data_type_child.tag, data_type_child.attrib)
                        for child in data_type_child:
                            # print child.tag, child.text
                            exec "attr.%s.update({%r:%r})" % (data_type_child.tag, child.tag, child.text)

    '''
    def __getattribute__(self, attr):
        # print "get attr %s" % attr
        return object.__getattribute__(self, attr)

    def __setattr__(self, attr, val):
        # print "set attr %s to %r" % (attr, val)
        return object.__setattr__(self, attr, val)
    '''
                            
if __name__ == '__main__':
    # name = "LteRbsNodeComplete_Itr27_R10D03.xml"
    name = "sample.xml"
    parser = MomParser(name)
    # print parser.ns    
