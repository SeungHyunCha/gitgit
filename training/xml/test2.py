#!/usr/bin/python

from xml.etree.ElementTree import parse, dump

tree = parse("note.xml")
note = tree.getroot()
dump(note)
