import xml.etree.ElementTree as ET
  
class MomParser:
    def __init__(self, name):
        self.name = name
        self.ns = {}
        self.weight = 0
        self.root = None
        for event, elem in ET.iterparse(name, events=('start','end')):
            #print elem.tag
            if event == 'start' and self.root == None:              
                self.root = elem.tag                                                 
                #print self.root
            elif event == 'start':
                if elem.tag == 'class':
                    #print elem.attrib.values()[0]
                    moName = elem.attrib.values()[0]
                    mo = MO(moName)         
                    for child in elem:
                        #print child.tag
                        if child.tag == 'description':
                            mo.description = child.text
                        else:
                            pass
                    print mo.__dict__
                     
                elif elem.tag == 'attribute':
                    attrName = elem.attrib.values()[0]
                    attr = ATTR(attrName)
                          
            else:
                pass
            
'''
 temp = []
    for child in elem:
        #print child.tag
        if child.tag == 'description':
            
        else:
            if child.tag == 'attribute':
                
        temp.append(child.tag)
    obj.attribute = temp
'''
class MO:
    def __init__(self, name):
        self.name = name
        self.attribute = None
        self.description = None
        self.parents = None
        self.child = None
    
    def __repr__(self):
        return 
    
class ATTR:
    def __init__(self, name):
        self.name = name
        self.attribute = None
        self.description = None
        self.mo = None

if __name__ == '__main__':
    #name = "LteRbsNodeComplete_Itr27_R10D03.xml"
    name = "sample.xml"
    parser = MomParser(name)
    #print parser.ns    
