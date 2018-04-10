from MOMParser import IterParser
import re 
import argparse

class ShowMom(IterParser):
    def __init__(self, name):
        IterParser.__init__(self, name)
        self.line = "*" * 200
#         self.mo = mom.mo
#         self.attr = mom.attr
    
    def showMim(self):
        print self.line
        print 'name:"%s"' % self.mim['name'], 'version:"%s"' % self.mim['version'], 'release:"%s"' %self.mim['release'], 'author:"%s"' %self.mim['author'], 'revision:"%s"' %self.mim['revision']
        
    def showMom(self, mo = None, attr = None):
        if mo is None and attr is None:
            print self.line,'\n',"MO".ljust(30),'\n', self.line
            for mo in sorted(self.mos):
                print mo
            print '\n', self.line,'\n',"ENUM".ljust(30),'\n', self.line
            for enum in sorted(self.enums):
                print enum
            for moc in sorted(self.mos):
                if moc is not None:
                    getMo = self.mos[moc]
                    getMo.showMoInfo()
                    print self.line,'\n',"MOC".ljust(30), 'Attribute'.ljust(30), 'defaultValue'.ljust(30), 'Flags'.ljust(30), 'Range'.ljust(30)
                    print self.line
                    attr_list = getMo.getAttrs()
                    for attr_name in sorted(attr_list):
                        getAttr = attr_list[attr_name]
                        print getAttr.mo.ljust(30), getAttr.getName().ljust(30), getAttr.getFlags().ljust(40), getAttr.getLength().ljust(20), getAttr.getValues().ljust(20), getAttr.getRange()
        
        if mo is not None and attr is None:
            p = re.compile(mo, re.IGNORECASE)
            for moc in sorted(self.mos):
                check = p.search(moc)
                if check:   
                    getMo = self.mos[moc]
                    getMo.showMoInfo()
        
        if mo is None and attr is not None:
            print self.line,'\n',"MOC".ljust(30), 'Attribute'.ljust(30), 'defaultValue'.ljust(30), 'Flags'.ljust(30), 'Range'.ljust(30)
            print self.line
            p = re.compile(attr, re.IGNORECASE)
            for attr_name in sorted(self.attrs):
                check = p.search(attr_name)
                if check:
                    getAttr = self.attrs[attr_name]
                    print getAttr.getMoName().ljust(30), getAttr.getName().ljust(30), getAttr.getFlags().ljust(40), getAttr.getLength().ljust(20), getAttr.getValues().ljust(20), getAttr.getRange()
        
        if mo is not None and attr is not None:
            p = re.compile(mo, re.IGNORECASE)
            for moc in sorted(self.mos):
                check = p.search(moc)
                if check:   
                    getMo = self.mos[moc]
                    print self.line,'\n',"MOC".ljust(30), 'Attribute'.ljust(30), 'Flags'.ljust(40), 'length'.ljust(20), 'default'.ljust(20), 'Range'
                    print self.line
                    m = re.compile(attr, re.IGNORECASE)
                    attr_list = getMo.getAttrs()
                    for attr_name in sorted(attr_list):
                        check1 = m.search(attr_name)
                        if check1:
                            getAttr = attr_list[attr_name]
                            print getAttr.mo.ljust(30), getAttr.getName().ljust(30), getAttr.getFlags().ljust(40), getAttr.getLength().ljust(20), getAttr.getValues().ljust(20), getAttr.getRange()
        
    def showDesc(self, mo = None, attr = None):
        if mo is None and attr is None:
            for moc in sorted(self.mos):
                if moc is not None:
                    getMo = self.mos[moc]
                    print self.line,'\n',"MO =", getMo.getName()
                    print "description =".ljust(10), getMo.getDesc()


            
        if mo is not None and attr is None:
            p = re.compile(mo, re.IGNORECASE)
            for moc in sorted(self.mos):
                check = p.search(moc)
                if check:   
                    getMo = self.mos[moc]
                    print self.line,'\n',"MO =", getMo.getName()
                    print "description =".ljust(10), getMo.getDesc()
                    
        if mo is None and attr is not None:
            p = re.compile(attr, re.IGNORECASE)
            for attr_name in sorted(self.attrs):
                check = p.search(attr_name)
                if check:
                    getAttr = self.attrs[attr_name]
                    print self.line,'\n',"MO =", getAttr.getMoName(), "ATTR =", getAttr.getName()
                    print "description =".ljust(10), getAttr.getDesc()
                
        if mo is not None and attr is not None:
            p = re.compile(mo, re.IGNORECASE)
            for moc in sorted(self.mos):
                check = p.search(moc)
                if check:   
                    getMo = self.mos[moc]
                    m = re.compile(attr, re.IGNORECASE)
                    attr_list = getMo.getAttrs()
                    for attr_name in sorted(attr_list):
                        check1 = m.search(attr_name)
                        if check1:
                            getAttr = attr_list[attr_name]
                            print self.line,'\n',"MO =", getAttr.getMoName(), "ATTR =", getAttr.getName()
                            print "description =".ljust(10), getAttr.getDesc()
            
    def showValue(self):
        pass

def argParse():
	if args.file:
		f = open('mom', 'wb')
		f.write(args.file.read())
		f.close()
	
	if args.all:
		fopen = open('mom','rb')
		parser = ShowMom(fopen)
		parser.showMim()
		parser.showMom()

	if args.description:
		fopen = open('mom','rb')
		parser = ShowMom(fopen)
		parser.showMim()
		parser.showDesc(args.mo, args.attr) 

	if args.test:
		fopen = open('mom','rb')
		parser = ShowMom(fopen)
		parser.showMim()
		parser.showMom(args.mo, args.attr) 
	

parser = argparse.ArgumentParser(description = 'mom handling')
parser.add_argument('-i', dest ='file', action = 'store', type = argparse.FileType('r'), help = 'input file in -i option')
parser.add_argument('-mo', dest = 'mo', action = 'store', help = 'add mo name')
parser.add_argument('-attr', dest = 'attr', action = 'store', help = 'add attribute name')
parser.add_argument('-d', dest ='description', action = 'store_true')
parser.add_argument('-a', dest ='all', action = 'store_true')
parser.add_argument('-t', dest ='test', action = 'store_true')
args = parser.parse_args()  

argParse()

'''   
if __name__ == '__main__':
    name = "LteRbsNodeComplete_Itr27_R10D03.xml"
    parser = ShowMom(name)
    parser.showMim()
#     parser.showMom(mo='nbiot', attr='id$')
    parser.showDesc(mo = 'cellre',attr='id$')
	'''
