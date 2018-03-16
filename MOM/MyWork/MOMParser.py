import xml.etree.ElementTree as ET

class MomParser():
    def __init__(self, name):
        self.name = name
        self.ns = {}
        self.root = None
        for event, elem in ET.iterparse(name, events=('start','end')):
            if event == 'start':              # the start and end mean '<', '>' in XML 
                print event, elem
            else:
                print event, elem
                   
if __name__ == '__main__':
    #name = "LteRbsNodeComplete_Itr27_R10D03.xml"
    name = "sample.xml"
    parser = MomParser(name)
#   print parser.root.__dict__
    #print parser.ns    
