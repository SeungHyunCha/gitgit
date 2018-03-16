import xml.etree.ElementTree as ET

class MomParser():
    def __init__(self, name):
        self.name = name
        self.ns = {}
        self.root = None
        for event, elem in ET.iterparse(name, events=('start','end')):
            if event == 'start':              
                # 'start' and 'end' mean '<', '>' in XML 
                # elem.text is text <element> text </element> in XML
                # tag is the name of element
                # elem.attrib is <element name /> in XML
                # elem._children is child of this element
                print elem.tag
                print elem.attrib
                print elem._children
                print elem.text
            else:
                pass
                #print event, elem
                   
if __name__ == '__main__':
    #name = "LteRbsNodeComplete_Itr27_R10D03.xml"
    name = "sample.xml"
    parser = MomParser(name)
#   print parser.root.__dict__
    #print parser.ns    
