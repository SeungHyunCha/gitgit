import xml.etree.ElementTree as ET
#nsmap = {}
class MomParser():
    def __init__(self, mom):
        self.mom = mom
        
    def parse(self):
        for event, elem in ET.iterparse(self.mom, events=('start','end')):
            print event, elem

if __name__ == '__main__':
#   mom = "LteRbsNodeComplete_Itr27_R10D03.xml"
    mom = "sample.xml"
    par = MomParser(mom)
    par.parse()
    
    
