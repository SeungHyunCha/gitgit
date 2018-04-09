from MOMParser import MomParser
import re 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('mo', type = str, action = 'store', default = '', help = 'mo name')
parser.add_argument('attr', type = str, action = 'store', default = '', help = 'attribute name')
parser.add_argument('-d', dest = 'momd', action = 'store_true', help = 'show mo name')
mom = parser.parse_args()

class ShowMom(MomParser):
    def __init__(self):
        self.mo = mom.mo
        self.attr = mom.attr
        
    def mom(self, mo="", attr=""): # print element
        line = "*" * 200
        print line
        print 'name:"%s"' % self.mim['name'], 'version:"%s"' % self.mim['version'], 'release:"%s"' %self.mim['release'], 'author:"%s"' %self.mim['author'], 'revision:"%s"' %self.mim['revision']
        if mo == "":   
            if attr == "": 
                # show mo, enum, struct, exception
                print line,'\n',"MO".ljust(30),'\n',line
                for mo in self.mos:
                    print mo
                print '\n', line,'\n',"ENUM".ljust(30),'\n',line
                for enum in self.enums:
                    print enum
                   
            else:
                print line,'\n',"MOC".ljust(30), 'Attribute'.ljust(30), 'defaultValue'.ljust(30), 'Flags'.ljust(30), 'Range'.ljust(30)
                print line
                p = re.compile(attr, re.IGNORECASE)
                for attr_name in self.attrs:
                    check = p.search(attr_name)
                    if check:
                        getAttr = self.attrs[attr_name]
#                         print getAttr.getMoName().ljust(30), getAttr.getName().ljust(30), getAttr.getValues(), getAttr.getFlags().ljust(30), getAttr.getRange()
                        print getAttr.getMoName().ljust(30), getAttr.getName().ljust(30), getAttr.getFlags().ljust(40), getAttr.getLength().ljust(20), getAttr.getValues().ljust(20), getAttr.getRange()
                            
                    else:
                        pass
                        
        else:
            p = re.compile(mo, re.IGNORECASE)
            for moc in self.mos:
                check = p.search(moc)
                if check:   
                    getMo = self.mos[moc]
                    if attr == "":
                        getMo.showMoInfo()
                    else:
                        print line,'\n',"MOC".ljust(30), 'Attribute'.ljust(30), 'Flags'.ljust(40), 'length'.ljust(20), 'default'.ljust(20), 'Range'
                        print line
                        m = re.compile(attr, re.IGNORECASE)
                        attr_list = getMo.getAttrs()
                        for attr_name in sorted(attr_list):
                            check1 = m.search(attr_name)
                            if check1:
                                getAttr = attr_list[attr_name]
                                print getAttr.mo.ljust(30), getAttr.getName().ljust(30), getAttr.getFlags().ljust(40), getAttr.getLength().ljust(20), getAttr.getValues().ljust(20), getAttr.getRange()
                            else:
                                pass
                else: pass
if __name__ == '__main__':
    pass