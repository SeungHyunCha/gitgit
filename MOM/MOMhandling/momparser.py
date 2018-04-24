import xml.etree.ElementTree as ET
import re, argparse, os, difflib
from cStringIO import StringIO
# Gen1
Gen1 = 1
Gen1_MOM = 'cat $MY_GIT_TOP/mom/lte/complete/LteRbsNodeComplete.xml'
Gen1_commit = 'git log --oneline $MY_GIT_TOP/mom/lte/complete/LteRbsNodeComplete.xml'
Gen1_prevMOM = 'git show %s:mom/lte/complete/LteRbsNodeComplete.xml'
# Gen2
Gen2 = 2
Gen2_MOM = 'cat $MY_GIT_TOP/mom/lrat/output/Lrat_DWAXE_mp.xml'
Gen2_commit = 'git log --oneline $MY_GIT_TOP/mom/lrat/output/Lrat_DWAXE_mp.xml'
Gen2_prevMOM = 'git show %s:mom/lrat/output/Lrat_DWAXE_mp.xml'
#etc
prev = '-'
modified = '?'
new = '+'
red = u"\u001b[31m %s \u001b[0m\n"
yellow = u"\u001b[33m %s \u001b[0m\n"
green = u"\u001b[32m %s \u001b[0m\n"
root = 'ManagedElement'
ref_to_By = 'reservedBy'
hidden = 'EricssonOnly'

class IterParser:
    def __init__(self, name):
        self.name = name
        self.mos = {}
        self.attrs = {}
        self.enums = {}
        self.emembers = {}
        self.structs = {}
        self.smembers = {}
        self.exceps = {}
        self.expmembers = {}
        self.mim = {}
        self.count = 0
        self.relations = {}
        self.__run()

    def __run(self):
        for event, elem in ET.iterparse(self.name, events=('start', 'end')):
            if event == 'start':
                if elem.tag == 'class':
                    mo_class = Mo(elem)
                    self.mos[mo_class.getName()] = mo_class
                elif elem.tag == 'enum':
                    mo_class = Mo(elem)
                    self.enums[mo_class.getName()] = mo_class
                elif elem.tag == 'struct':
                    mo_class = Mo(elem)
                    self.structs[mo_class.getName()] = mo_class
                elif elem.tag == 'exception':
                    mo_class = Mo(elem)
                    self.exceps[mo_class.getName()] = mo_class
                elif elem.tag == 'relationship':
                    relation_name = Relation(elem)
                    self.relations[relation_name.getName()] = relation_name
                else: pass

            if event == 'end':
                if elem.tag == 'class':
                    mo_class.handle()
                    for attr in elem:
                        if attr.tag == 'attribute':
                            child = Attr(attr)
                            child.mo = mo_class.getName()
                            self.attrs[child.getName()] = child
                            mo_class.addAttrs(child)
                        else: pass
                elif elem.tag == 'enum':
                    mo_class.handle()
                    for attr in elem:
                        if attr.tag == 'enumMember':
                            child = Attr(attr)
                            child.mo = mo_class.getName()
                            self.emembers[child.getName()] = child
                            mo_class.addAttrs(child)
                        else: pass
                elif elem.tag == 'struct':
                    mo_class.handle()
                    for attr in elem:
                        if attr.tag == 'structMember':
                            child = Attr(attr)
                            child.mo = mo_class.getName()
                            self.smembers[child.getName()] = child
                            mo_class.addAttrs(child)
                        else: pass
                elif elem.tag == 'exception':
                    mo_class.handle()
                    for attr in elem:
                        if attr.tag == 'exceptionParameter':
                            child = Attr(attr)
                            child.mo = mo_class.getName()
                            self.expmembers[child.getName()] = child
                            mo_class.addAttrs(child)
                        else: pass
                elif elem.tag == 'mim': # Add MIM version
                    if self.count == 0:
                        self.mim = elem.attrib
                        self.count = 1
                    else: pass
                elif elem.tag == 'relationship':
                    relation_name.handle()
                else: pass

class Mo:
    def __init__(self, elem):
        self.name = elem.attrib.values()[0]
        self.attrs_obj = {}
        self.flags = []
        self.others = {}
        self.obj = elem

    def getName(self):
        return self.name

    def getDesc(self):
        try:
            desc = self.others['description']
            return desc
        except: pass

    def getFlags(self):
        temp = sorted(self.flags)
        try:
            if temp[0] == []: del temp[0]
        except: pass
        temp = ','.join(temp)
        return str(temp)

    def addAttrs(self, attr):
        self.attrs_obj[attr.getName()] = attr

    def getAttrs(self):
        return self.attrs_obj

    def handle(self):
        # To add flags and others
        for mo_child in self.obj:
            if len(mo_child._children) == 0 and mo_child.tag != 'attribute' and 'enumMember' and 'structMember' and 'exceptionParameter':
                if mo_child.text == None:
                    self.flags.append(mo_child.tag)
                else:
                    if mo_child.text == '\n\t\t\t\t': pass
                    else:
                        self.others.update({mo_child.tag:mo_child.text})
            else:
                if mo_child.tag == 'action':
                    pass

    def showMoInfo(self):
        show_info = ''
        line = "*" * 132
        show_info += '%s\nMOC\n%s\n' %(line, line)
        show_info += '%s\n' % self.name
        if self.getFlags():
            show_info += '%s\n' % self.getFlags()
        if self.getDesc():
            show_info += 'description\t%s\n' % self.getDesc()
        show_info += '%s\n%s%s%s\n%s\n' %(line, "Attribute".ljust(30), "Type".ljust(40), 'Flags', line)
        for key, value in sorted(self.attrs_obj.items()):
            show_info += key.ljust(30) + value.getType().ljust(40) + value.getFlags() + '\n'
        return show_info

class Attr:
    def __init__(self, elem):
        self.name = elem.attrib.values()[0]
        self.obj = elem
        self.flags = []
        self.length = {}
        self.range = {}
        self.values = {}
        self.others = {}
        self.__handle()

    def getName(self):
        return self.name

    def getDesc(self):
        try:
            desc = self.others['description']
            return desc
        except: pass

    def getMoName(self):
        return self.mo

    def getFlags(self):
        temp = sorted(self.flags)
        try:
            if temp[0] == []:
                del temp[0]
        except: pass
        temp = ','.join(temp)
        return str(temp)

    def getType(self):
        if self.types == {}: return ''
        else: return str(self.types)

    def getLength(self):
        if self.length == {}: return ''
        else:
            leng = []
            for val in sorted(self.length, reverse=True):
                leng.append(int(self.length[val]))
            return str(leng)

    def getRange(self):
        if self.range == []: return ''
        else:
            return sorted(self.range)

    def getValues(self):
        if self.values == {}: return ''
        else:
            val = []
            for v in sorted(self.values):
                val.append(self.values[v])
            return str(val)

    def getDefault(self):
        for key in self.values:
            if key == 'defaultValue':
                return str(self.values['defaultValue'])
            else: pass
        return ''

    def getUnit(self):
        for key in self.values:
            if key == 'unit':
                return str(self.values['unit'])
            else: pass
        return ''

    def getMulti(self):
        for key in self.values:
            if key == 'multiplicationFactor':
                return str(self.values['multiplicationFactor'])
            else: pass
        return ''

    def __handle(self):
        for attr in self.obj:
            if len(attr._children) == 0:
                if attr.text == None:
                    self.flags.append(attr.tag)
                else:
                    exec "self.%s = %r" % (attr.tag, attr.text)
                    self.others.update({attr.tag:attr.text})
            else:
                if attr.tag == 'dataType':
                    for child in attr:
                        data = DataType(child)
                        self.flags.append(data.getFlags())
                        self.length = data.getLength()
                        self.range = data.getRanges()
                        self.values = data.getValues()
                        self.types = data.getType()
                else:
                    data = DataType(attr)
                    self.flags.append(data.getFlags())
                    self.length = data.getLength()
                    self.ranges = data.getRanges()
                    self.values = data.getValues()
                    self.types = data.getType()

        if 'visibility' in self.others:
            self.flags.append(hidden)

class DataType:
    def __init__(self, attr):
        self.attr = attr
        self.flags = []
        self.types = None
        self.length = {}
        self.stringlength = {}
        self.ranges = []
        self.values = {}
        self.__handle()

    def getFlags(self):
        return self.flags

    def getType(self):
        return self.types

    def getLength(self):
        return self.length

    def getRanges(self):
        return self.ranges

    def getValues(self):
        return self.values

    def __handle(self):
        if self.attr.attrib == {}:
            self.types = self.attr.tag
            if self.types == 'sequence':
                for child in self.attr:
                    if child.text == None:
                        if child.tag == 'nonUnique':
                            self.flags = child.tag
                        else:
                            if child.attrib == {}:
                                self.types = 'seq(%s)' % child.tag
                            else:
                                temp = {}
                                temp = {child.tag:child.attrib.values()[0]}
                                self.types = 'seq(%s)' % temp
                    else:
                        if child._children == []:
                            self.length.update({child.tag:child.text})
                        else:
                            if child.tag == 'long':
                                self.types = 'seq(%s)' % child.tag
                                for gchild in child:
                                    if gchild._children == []:
                                        self.values.update({gchild.tag:gchild.text})
                                    else:
                                        for ggchild in gchild:
                                            self.ranges.append(int(ggchild.text))
                            else:
                                temp = []
                                for gchild in child:
                                    temp.append(gchild.text)
                                self.values.update({child.tag:temp})
            else:
                for child in self.attr:
                    if child.attrib == {}:
                        if child.tag == 'range':
                            for key in child:
                                self.ranges.append(int(key.text))
                        elif child.tag == 'lengthRange':
                            for key in child:
                                self.length.update({key.tag:key.text})
                        else:
                            if child._children == []:
                                self.values.update({child.tag:child.text})
                            else:
                                if child.tag == 'stringLength':
                                    self.stringlength.update({child.tag:child.text})
                                print child, child.tag, child.text
                                for gchild in child:
                                    print gchild
                    else: pass
        else:
            temp = {}
            temp = {self.attr.tag:self.attr.attrib.values()[0]}
            self.types = temp
            if self.attr._children == []: pass
            else:
                for child in self.attr:
                    self.values = {child.tag:child.text}

class Relation:
    def __init__(self, elem):
        self.obj = elem
        self.name = elem.attrib.values()[0]
        self.type = None
        self.parent = None
        self.child = None
        self.to_cardi = None
        self.from_cardi = None
        self.from_class = None
        self.to_class = None
        self.from_attr = None
        self.to_attr = None
        self.to_flags = None

    def getName(self):
        return self.name

    def getParentName(self):
        return self.parent

    def getChildName(self):
        return self.child

    def getCaldi(self):
        return self.to_cardi

    def handle(self):
        for attr in self.obj:
            if attr.tag == 'containment':
                self.type = attr.tag
                for child in attr:
                    if child.tag == 'parent':
                        for gchild in child:
                            self.parent = gchild.attrib.values()[0]
                    elif child.tag == 'child':
                        for gchild in child:
                            if gchild.tag == 'cardinality':
                                cardi = []
                                for ggchild in gchild:
                                    cardi.append(int(ggchild.text))
                                self.to_cardi = '%s' % list(set(cardi))
                            else:
                                self.child = gchild.attrib.values()[0]
                    else: pass
            elif attr.tag == 'biDirectionalAssociation':
                self.type = attr.tag
                for child in attr:
                    str = child.attrib.values()[0]
                    if str[-3:] != 'Ref':
                        self.to_attr = str
                        for gchild in child:
                            if gchild.tag == 'hasClass':
                                self.to_class = gchild.attrib.values()[0]
                            else:
                                cardi = []
                                for ggchild in child:
                                    cardi.append(ggchild.text)
                                self.to_cardi = '%s' % cardi
                    else:
                        self.from_attr = str
                        for gchild in child:
                            if gchild.tag == 'hasClass':
                                self.from_class = gchild.attrib.values()[0]
                            else:
                                cardi = []
                                for ggchild in child:
                                    cardi.append(ggchild.text)
                                self.from_cardi = '%s' % cardi

class ParsingMom(IterParser):
    def __init__(self, name):
        IterParser.__init__(self, name)
        self.root = root
        self.line = "*" * 132
        self.sortMO = sorted(self.mos.keys())

    def showMom(self, mo = None, attr = None):
        show_info = ''
        show_info += '%s\nname:%s version:%s release:%s author:%s revision:%s\n' %(self.line, self.mim['name'], self.mim['version'], self.mim['release'], self.mim['author'], self.mim['revision'])
        if mo is None and attr is None:
            show_info += '%s\n%s\n%s\n' %(self.line, "MO".ljust(30), self.line)
            for mo in self.sortMO:
                show_info += '%s\n' % mo
            show_info += '%s\n%s\n%s\n' %(self.line, "ENUM".ljust(30), self.line)
#             for enum in sorted(self.enums):
#                 show_info += '%s\n' % enum
            for moc in self.sortMO:
                getMo = self.mos[moc]
                show_info += '%s\n' % getMo.showMoInfo()
                show_info += '%s\n%s%s%s%s%s%s\n%s\n' % (self.line, "MOC".ljust(30), 'Attribute'.ljust(30), 'defaultValue'.ljust(20), 'Flags'.ljust(40), 'Length'.ljust(20), 'Range'.ljust(20), self.line)
                attr_list = getMo.getAttrs()
                for attr_name in sorted(attr_list):
                    getAttr = attr_list[attr_name]
                    show_info += '%s%s%s%s%s%s\n' % (getAttr.getMoName().ljust(30), getAttr.getName().ljust(30), getAttr.getDefault().ljust(20), getAttr.getFlags().ljust(40), getAttr.getLength().ljust(20), getAttr.getRange())

        if mo is not None and attr is None:
            p = re.compile(mo, re.IGNORECASE)
            for moc in self.sortMO:
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
                    show_info += '%s%s%s%s%s%s\n' % (getAttr.getMoName().ljust(30), getAttr.getName().ljust(30), getAttr.getDefault().ljust(20), getAttr.getFlags().ljust(40), getAttr.getLength().ljust(20), getAttr.getRange())

        if mo is not None and attr is not None:
            p = re.compile(mo, re.IGNORECASE)
            for moc in self.sortMO:
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
                            show_info += '%s%s%s%s%s%s\n' % (getAttr.getMoName().ljust(30), getAttr.getName().ljust(30), getAttr.getDefault().ljust(20), getAttr.getFlags().ljust(40), getAttr.getLength().ljust(20), getAttr.getRange())
        return show_info

    def showDesc(self, mo = None, attr = None):
        show_info = ''
        show_info += '%s\nname:%s version:%s release:%s author:%s revision:%s\n' %(self.line, self.mim['name'], self.mim['version'], self.mim['release'], self.mim['author'], self.mim['revision'])
        if mo is None and attr is None:
            for moc in self.sortMO:
                getMo = self.mos[moc]
                show_info += '%s\n%s%s\n' %(self.line,"MO = ", getMo.getName())
                show_info += '%s%s\n'%("description = ".ljust(10), getMo.getDesc())

        if mo is not None and attr is None:
            p = re.compile(mo, re.IGNORECASE)
            for moc in self.sortMO:
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
            for moc in self.sortMO:
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

    def findParentTree(self, child, tree_list):
        for key, value in self.relations.items():
            if key[-10:] == ref_to_By: pass
            elif child == value.getChildName():
                parent = value.getParentName()
                cardi = value.getCaldi()
                child_cardi = child + cardi
                tree_list.insert(0, child_cardi)
                if parent == root:
                    tree_list.insert(0, root + '[1]')
                    return tree_list
                else: return self.findParentTree(parent, tree_list)
            else: pass

    def findChild(self, parent):
        child_dic = {}
        for key, value in self.relations.items():
            if parent == value.getParentName():
                child = value.getChildName()
                cardi = value.getCaldi()
                child_cardi = child + cardi
                child_dic.update({child:child_cardi})
            else: pass
        return child_dic

    def checkSys(self, tree_list):
        if tree_list[-1][-3:] == '[1]':
            return '(systemCreated)'
        else: return ''

    def treeStruct(self, tree_list, show_info, mo):
        child_list = self.findChild(mo)
        if child_list != {}:
            for child in child_list:
                tree_list.append(child_list[child])
                show_info += '%s%s\n' % (tree_list, self.checkSys(tree_list))
                check_child = self.findChild(child)
                if check_child != {}:
                    for gchild in check_child:
                        tree_list.append(check_child[gchild])
                        show_info += '%s%s\n' % (tree_list, self.checkSys(tree_list))
                        check2_child = self.findChild(gchild)
                        if check2_child != {}:
                            for ggchild in check2_child:
                                tree_list.append(check2_child[ggchild])
                                show_info += '%s%s\n' % (tree_list, self.checkSys(tree_list))
                                check3_child = self.findChild(ggchild)
                                if check3_child != {}:
                                    for gggchild in check3_child:
                                        tree_list.append(check3_child[gggchild])
                                        show_info += '%s%s\n' % (tree_list, self.checkSys(tree_list))
                                        tree_list.pop()
                                tree_list.pop()
                        tree_list.pop()
                tree_list.pop()
            return show_info
        else: return ''

    def relation(self, mo = None):
        show_info = ''
        if mo == None:
            tree_list = []
            tree_list.append(root + '[1]')
            show_info += '%s\n' % self.treeStruct(tree_list, show_info, root)
        else:
            p = re.compile(mo, re.IGNORECASE)
            for key, value in self.relations.items():
                if key[-10:] == ref_to_By: pass
                else:
                    parent_mo = value.getParentName()
                    child_mo = value.getChildName()
                    cardi = value.getCaldi()
                    child_cardi = child_mo + cardi
                    check = p.search(child_mo)
                    if check:
                        tree_list = []
                        tree_list.append(child_cardi)
                        tree_list = self.findParentTree(parent_mo, tree_list)
                        show_info += '%s%s\n' % (tree_list, self.checkSys(tree_list))
                        show_info += '%s\n' % self.treeStruct(tree_list, show_info, child_mo)
        return show_info

def diff(prev, cur):
    diff = difflib.ndiff(prev.splitlines(), cur.splitlines())
    diffstr = ''
    for line in list(diff):
        if line.split(' ')[0] == prev:
            diffstr += red % line
        elif line.split(' ')[0] == modified:
            diffstr += yellow % line
        elif line.split(' ')[0] == new:
            diffstr += green % line
        else:
            pass
            # if you want to add previous mom, please turn on this sentence
            #diffstr += '%s\n' % line
    return diffstr

def argParse():
    if args.diff:
        if not args.file:
            file = os.popen(Gen1_MOM)
        commit = os.popen(Gen1_commit)
        prev_commit = commit.readlines()[1]
        prev_commit = prev_commit.split(' ')[0]
        read_prev_mom = os.popen(Gen1_prevMOM % prev_commit)
        prev_mom = open('prevmom','wb')
        prev_mom.write(read_prev_mom.read())
        prev_mom.close()
        prev_mom = open('prevmom','rb')
        if args.mom:
            parser1 = ParsingMom(prev_mom)
            parser2 = ParsingMom(cur_mom)
            prev_str = parser1.showMom(args.mo, args.attr)
            cur_str = parser2.showMom(args.mo, args.attr)
            diff_file =  diff(prev_str, cur_str)
            print diff_file
        elif args.description:
            parser1 = ParsingMom(prev_mom)
            parser2 = ParsingMom(cur_mom)
            prev_str = parser1.showDesc(args.mo, args.attr)
            cur_str = parser2.showDesc(args.mo, args.attr)
            diff_file =  diff(prev_str, cur_str)
            print diff_file
    else:
        if not args.file:
            file = os.popen(Gen1_MOM)
        if args.mom:
            parser = ParsingMom(StringIO(file.read()))
            print parser.showMom(args.mo, args.attr)

        if args.description:
            parser = ParsingMom(cur_mom)
            print parser.showDesc(args.mo, args.attr)

        if args.tree:
            parser = ParsingMom(cur_mom)
            print parser.relation(args.mo)

parser = argparse.ArgumentParser(description = 'Test MOM handling')
parser.add_argument('-i', dest ='file', action = 'store', type = argparse.FileType('r'), help = 'If you want to show specific MOM version, input filename by using -i option')
parser.add_argument(dest = 'mo', action = 'store', help = 'Search specific mo using -mo option')
parser.add_argument(dest = 'attr', action = 'store', help = 'Search specific attr using -attr option')
parser.add_argument('-d', dest ='description', action = 'store_true', help = 'Show only description about specific mo')
parser.add_argument('-diff', dest ='diff', action = 'store_true', help = 'Show difference between current MOM xml and prev MOM xml')
parser.add_argument('-a', dest ='mom', action = 'store_true', help = 'Show all information in MOM')
parser.add_argument('-t', dest ='tree', action = 'store_true', help = 'Show relationship between MOs')
args = parser.parse_args()
argParse()
