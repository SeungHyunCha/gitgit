import xml.etree.ElementTree as ET

class MomParser():
    def __init__(self, name):
        self.name = name
        self.ns = {}
        self.root = None
        for event, elem in ET.iterparse(name, events=('start','end','start-ns')):
            if event == 'start' and self.root == None:              # the start and end mean '<', '>' in XML 
                self.root = elem.tag                                # tag is the name of element
                #print self.root
                self.ns[self.root] = elem._children                    
                #print self.ns
            elif event == 'start':    
                if elem._children == []:
                    pass
                else:
                    temp = []
                    for tags in elem._children:
                        temp.append(tags.tag)
                    self.ns[elem] = temp 
                if elem.text == None:                               # elem.text is text <element> text </element> in XML
                    pass
                    #print elem.text     
                elif len(elem.attrib) != 0:                             # elem.attrib is <element name /> in XML
                    #self.ns[elem.attrib.keys()] = {'%s'} % elem.attrib.values()
                    print elem.attrib                          
                    for value in elem.attrib:
                        pass
                        #print value    
            else:
                pass

#class Component(MomParser):
#    def 
if __name__ == '__main__':
    #name = "LteRbsNodeComplete_Itr27_R10D03.xml"
    name = "sample.xml"
    parser = MomParser(name)
#   print parser.root.__dict__
    print parser.ns    
