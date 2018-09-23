# Copyright (C) CSIRO 2012
# $Id: mod_xmlTools.py 104 2012-07-12 06:47:38Z cha68f $

# Module of common XML functions
from xml.dom.minidom import Document

# Function: Initialises an XML document with a root node
# Parameters: root_name = Intended name of document root node
# Returns: (Document, doc), (XML element node, root)

def create_xml(root_name):
	doc = Document()
	root = doc.createElement(root_name)
	doc.appendChild(root)
	return doc,root

# Function: Prints XML document to file
#           (if file already exists, file is overwritten)
# Parameters: doc = Document object
#             doc_name = Intend output filename/path
# Returns: (void)

def print_xml(doc,doc_name):
	try:
		file = open(doc_name, "w")
		file.write(doc.toprettyxml(indent='\t'))
	except IOError:
		print "Error occurred when trying to open and write file."
	else:
		file.close()
	return