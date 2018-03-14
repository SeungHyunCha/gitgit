import xml.etree.ElementTree as ET
#nsmap = {}
class MomParser():
    def __init__(self, mom):
        self.mom = mom
        for event, elem in ET.iterparse(mom, events=('start','end','start-ns')):
            print event, elem

if __name__ == '__main__':
#   mom = "LteRbsNodeComplete_Itr27_R10D03.xml"
    mom = "sample.xml"
    parser = MomParser(mom)
    
    
