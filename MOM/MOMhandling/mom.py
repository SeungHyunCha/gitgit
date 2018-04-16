from MOMParser import IterParser
import re 
import argparse
import os
import difflib

class ParsingMom(IterParser):
    def __init__(self, name):
        IterParser.__init__(self, name)
        self.line = "*" * 132
    
    def showMom(self, mo = None, attr = None):
        show_info = ''
        show_info += '%s\nname:%s version:%s release:%s author:%s revision:%s\n' %(self.line, self.mim['name'], self.mim['version'], self.mim['release'], self.mim['author'], self.mim['revision'])
        if mo is None and attr is None:
            show_info += '%s\n%s\n%s\n' %(self.line, "MO".ljust(30), self.line)
            for mo in sorted(self.mos):
                show_info += '%s\n' % mo
            show_info += '%s\n%s\n%s\n' %(self.line, "ENUM".ljust(30), self.line) 
            for enum in sorted(self.enums):
                show_info += '%s\n' % enum
        
            for moc in sorted(self.mos):
                if moc is not None:
                    getMo = self.mos[moc]
                    show_info += '%s\n' % getMo.showMoInfo()
                    show_info += '%s\n%s%s%s%s%s%s\n%s\n' % (self.line, "MOC".ljust(30), 'Attribute'.ljust(30), 'defaultValue'.ljust(20), 'Flags'.ljust(40), 'Length'.ljust(20), 'Range'.ljust(20), self.line)
                    attr_list = getMo.getAttrs()
                    for attr_name in sorted(attr_list):
                        getAttr = attr_list[attr_name]
                        show_info += '%s%s%s%s%s%s\n' % (getAttr.getMoName().ljust(30), getAttr.getName().ljust(30), getAttr.getValues().ljust(20), getAttr.getFlags().ljust(40), getAttr.getLength().ljust(20), getAttr.getRange())
        
        if mo is not None and attr is None:
            p = re.compile(mo, re.IGNORECASE)
            for moc in sorted(self.mos):
                check = p.search(moc)
                if check:   
                    getMo = self.mos[moc]
                    show_info += '%s\n' % getMo.showMoInfo()
        
        if mo is None and attr is not None:
            show_info += '%s\n%s%s%s%s%s%s\n%s\n' % (self.line, "MOC".ljust(30), 'Attribute'.ljust(30), 'defaultValue'.ljust(20), 'Flags'.ljust(40), 'Length'.ljust(20), 'Range'.ljust(20), self.line)
            p = re.compile(attr, re.IGNORECASE)
            for attr_name in sorted(self.attrs):
                check = p.search(attr_name)
                if check:
                    getAttr = self.attrs[attr_name]
                    show_info += '%s%s%s%s%s%s\n' % (getAttr.getMoName().ljust(30), getAttr.getName().ljust(30), getAttr.getValues().ljust(20), getAttr.getFlags().ljust(40), getAttr.getLength().ljust(20), getAttr.getRange())
        
        if mo is not None and attr is not None:
            p = re.compile(mo, re.IGNORECASE)
            for moc in sorted(self.mos):
                check = p.search(moc)
                if check:   
                    getMo = self.mos[moc]
                    show_info += '%s\n%s%s%s%s%s%s\n%s\n' % (self.line, "MOC".ljust(30), 'Attribute'.ljust(30), 'defaultValue'.ljust(20), 'Flags'.ljust(40), 'Length'.ljust(20), 'Range'.ljust(20), self.line)
                    m = re.compile(attr, re.IGNORECASE)
                    attr_list = getMo.getAttrs()
                    for attr_name in sorted(attr_list):
                        check1 = m.search(attr_name)
                        if check1:
                            getAttr = attr_list[attr_name]
                            show_info += '%s%s%s%s%s%s\n' % (getAttr.getMoName().ljust(30), getAttr.getName().ljust(30), getAttr.getValues().ljust(20), getAttr.getFlags().ljust(40), getAttr.getLength().ljust(20), getAttr.getRange())
        return show_info
        
    def showDesc(self, mo = None, attr = None):
        show_info = ''
        show_info += '%s\nname:%s version:%s release:%s author:%s revision:%s\n' %(self.line, self.mim['name'], self.mim['version'], self.mim['release'], self.mim['author'], self.mim['revision'])
        if mo is None and attr is None:
            for moc in sorted(self.mos):
                if moc is not None:
                    getMo = self.mos[moc]
                    show_info += '%s\n%s%s\n' %(self.line,"MO = ", getMo.getName())
                    show_info += '%s%s\n'%("description = ".ljust(10), getMo.getDesc())
            
        if mo is not None and attr is None:
            p = re.compile(mo, re.IGNORECASE)
            for moc in sorted(self.mos):
                check = p.search(moc)
                if check:   
                    getMo = self.mos[moc]
                    show_info += '%s\n%s%s\n' %(self.line,"MO = ", getMo.getName())
                    show_info += '%s%s\n'%("description = ".ljust(10), getMo.getDesc())
                    attr_list = getMo.getAttrs()
                    for attr_name in sorted(attr_list):
                        getAttr = attr_list[attr_name]
                        show_info += '%s\n%s\t%s\n' %(self.line, getAttr.getName(), getAttr.getDesc())
                    
        if mo is None and attr is not None:
            p = re.compile(attr, re.IGNORECASE)
            for attr_name in sorted(self.attrs):
                check = p.search(attr_name)
                if check:
                    getAttr = self.attrs[attr_name]
                    show_info += '%s\n%s%s\t%s%s\n' %(self.line,"MO = ", getAttr.getMoName(),"ATTR = ", getAttr.getName())
                    show_info += '%s%s\n'%("description = ".ljust(10), getAttr.getDesc())
                        
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
                            show_info += '%s\n%s%s\t%s%s\n' %(self.line,"MO = ", getAttr.getMoName(),"ATTR = ", getAttr.getName())
                            show_info += '%s%s\n'%("description = ".ljust(10), getAttr.getDesc())
        return show_info
       
    def showValue(self):
        pass


def diff(prev, cur):
    diff = difflib.ndiff(prev.splitlines(), cur.splitlines())
    diff_info = '\n'.join(list(diff))
    return diff_info

def findPath():
    path_dir = '$MY_GIT_TOP/mom/lte/complete'
    file_list = os.listdir(path_dir)
    for item in file_list:
        if item.find('xml') is not -1:
            return item 

#add argparse operation
def argParse():
    if args.file:
        if args.version == 1:
            cur_mom = open('mom', 'wb')
        if args.version == 2:
            cur_mom = open('mom2', 'wb')
        cur_mom.write(args.file.read())
        cur_mom.close()

    if args.currentMOM:
        if args.version == 1:
            filename = os.popen('cat $MY_GIT_TOP/mom/lte/complete/LteRbsNodeComplete.xml')
            cur_mom = open('mom', 'wb')
        if args.version == 2:
            filename = os.popen('cat $MY_GIT_TOP/mom/lrat/output/Lrat_DWAXE_mp.xml')
            cur_mom = open('mom2', 'wb')
        cur_mom.write(filename.read())
        cur_mom.close()

    if args.diff:
        try:
            if args.version == 1:
                cur_mom = open('mom','rb')
                commit = os.popen('git log --oneline $MY_GIT_TOP/mom/lte/complete/LteRbsNodeComplete.xml')
                prev_commit = commit.readlines()[1]
                prev_commit = prev_commit.split(' ')[0]
                read_prev_mom = os.popen('git show %s:mom/lte/complete/LteRbsNodeComplete.xml' %prev_commit)
            if args.version == 2:
                cur_mom = open('mom2','rb')
                commit = os.popen('git log --oneline $MY_GIT_TOP/mom/lrat/output/Lrat_DWAXE_mp.xml')
                prev_commit = commit.readlines()[1]
                prev_commit = prev_commit.split(' ')[0]
                read_prev_mom = os.popen('git show %s:mom/lrat/output/Lrat_DWAXE_mp.xml' %prev_commit)
            prev_mom = open('prevmom','wb')
            prev_mom.write(read_prev_mom.read())
            prev_mom.close()
            prev_mom = open('prevmom','rb')
            
            if args.mom:
                parser1 = ParsingMom(cur_mom)        
                parser2 = ParsingMom(prev_mom)
                cur_str = parser1.showMom(args.mo, args.attr)
                prev_str = parser2.showMom(args.mo, args.attr)
                diff_file =  diff(prev_str, cur_str)
                print diff_file
                
            if args.description:
                parser1 = ParsingMom(cur_mom)        
                parser2 = ParsingMom(prev_mom)
                cur_str = parser1.showDesc(args.mo, args.attr)
                prev_str = parser2.showDesc(args.mo, args.attr)
                diff_file =  diff(prev_str, cur_str)
                print diff_file

        except Exception as ex: print ex
        
    else:
        if args.mom:
            try: 
                if args.version == 1:
                    cur_mom = open('mom','rb')
                if args.version == 2:
                    cur_mom = open('mom2','rb')
                parser = ParsingMom(cur_mom)
                print parser.showMom(args.mo, args.attr)
            except Exception as ex: print ex 
        
        if args.description:
            try: 
                if args.version == 1:
                    cur_mom = open('mom','rb')
                if args.version == 2:
                    cur_mom = open('mom2','rb')
                parser = ParsingMom(cur_mom)
                print parser.showDesc(args.mo, args.attr) 
            except Exception as ex: print ex 
        
        if args.tree:
            pass
        
# add argparse command line option
parser = argparse.ArgumentParser(description = 'Test MOM handling')
parser.add_argument('-i', dest ='file', action = 'store', type = argparse.FileType('r'), help = 'If you want to show specific MOM version, input filename by using -i option')
parser.add_argument('version', action = 'store', type = int, help = 'Choose G1 or G2 by num')
parser.add_argument('-p', dest ='currentMOM', action = 'store_true', help = 'Load current MOM by using -p option')
parser.add_argument('-mo', dest = 'mo', action = 'store', help = 'Search specific mo using -mo option')
parser.add_argument('-attr', dest = 'attr', action = 'store', help = 'Search specific attr using -attr option')
parser.add_argument('-d', dest ='description', action = 'store_true', help = 'Show only description about specific mo')
parser.add_argument('-diff', dest ='diff', action = 'store_true', help = 'Show difference between current MOM xml and prev MOM xml')
parser.add_argument('-a', dest ='mom', action = 'store_true', help = 'Show all information in MOM')
parser.add_argument('-t', dest ='tree', action = 'store_true', help = 'Show relationship between MOs') 
args = parser.parse_args()  
argParse()

if __name__ == '__main__':
    pass
#     name = "LteRbsNodeComplete_Itr27_R10D03.xml"
#     parser = ShowMom(name)
#     print parser.showMom(mo='nbiot')
#     print parser.showMom(mo='nbiot', attr='cell')
#     print parser.showDesc(mo='nbiot')
#     print parser.showDesc(attr='id$')
#     print parser.showDesc(mo='nbiot', attr='cell')
#     print parser.showMom(attr='id$')
#     print parser.showMom()

