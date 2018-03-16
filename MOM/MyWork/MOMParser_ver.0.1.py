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
                temp = []
                for tags in elem._children:
                    temp.append(tags.tag)
                self.ns[self.root] = temp                    
                #print self.ns
            elif event == 'start':    
                if elem._children == []:
                    pass
                    if elem.text == None:
                        pass
                        if len(elem.attrib) == 0:
                            pass
                        else:
                            print elem.attrib
                    else:
                        self.ns[elem.tag] = elem.text
                        if len(elem.attrib) == 0:
                            pass
                        else:
                            print elem.attrib
                else:
                    temp = []
                    for tags in elem._children:
                        temp.append(tags.tag)
                    self.ns[elem.tag] = temp 
                    if elem.text == None:
                        pass
                        if len(elem.attrib) == 0:
                            pass
                        else:
                            print elem.attrib
                    else:
                        self.ns[elem.tag] = elem.text
                        if len(elem.attrib) == 0:
                            pass
                        else:
                            print elem.attrib
                if elem.text == None:                               # elem.text is text <element> text </element> in XML
                    pass
                    #print elem.text     
                elif len(elem.attrib) != 0:                             # elem.attrib is <element name /> in XML
                    #self.ns[elem.attrib.keys()] = {'%s'} % elem.attrib.values()
                    #print elem.attrib                          
                    for value in elem.attrib:
                        pass
                        #print value'''
            else:
                pass
'''  
     def comp(self):
        if elem._children == []:
            pass
            if elem.text == None:
                pass
                if len(elem.attrib) == 0:
                    pass
                else:
                    print elem.attrib
            else:
                self.ns[elem.tag] = elem.text
                if len(elem.attrib) == 0:
                    pass
                else:
                    print elem.attrib
        else:
            temp = []
            for tags in elem._children:
                temp.append(tags.tag)
            self.ns[elem.tag] = temp 
            if elem.text == None:
                pass
                if len(elem.attrib) == 0:
                    pass
                else:
                    print elem.attrib
            else:
                self.ns[elem.tag] = elem.text
                if len(elem.attrib) == 0:
                    pass
                else:
                    print elem.attrib
                    '''
                   
if __name__ == '__main__':
    #name = "LteRbsNodeComplete_Itr27_R10D03.xml"
    name = "sample.xml"
    parser = MomParser(name)
#   print parser.root.__dict__
    print parser.ns    
