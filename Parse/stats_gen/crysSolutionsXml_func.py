# Copyright (C) CSIRO 2012-2013
# $Id: crysSolutionsXml_func.py 138 2013-02-18 23:45:02Z faz014 $

# Functions for crysSolutionsXml script
#
# Original Author: Michelle Ching Wah Chan
#

from xml.dom.minidom import parse
from decimal import Decimal

TRUE=0
FALSE=1
NOT_AVAILABLE=-999

# Look up table of chemicals which are used in C6 reservoirs, but are not recorded in 
# the BDP. Please add a list for each manual look-up chemical with the structure of:
#             chem_tuple = ([0], chemical name), ([1], total occurences),
#                          ([2], units), ([3], concentration mean), 
#                          ([4], concentration standard deviation),
#                          ([5], number of records without a concentration value),
#                          ([6], pH mean), ([7], pH standard deviation),
#                          ([8], number of records without a pH value),
#                          ([9], density value), ([10], molecular weight value)
# Then add the list variable to the LOOK_UP_TABLE list variable. The chemicals in the
# LOOK_UP_TABLE list will then be appended to the end of the XML document by the program.

SODIUM_ACE_ACE_ACID=["SODIUM ACETATE - ACETIC ACID",13601,"M",0.089994,0.141288,2390,4.79118,0.407505,2390,NOT_AVAILABLE,82.02,46,[4.76,-999,-999]]
SODIUM_MAL_MAL_ACID=["SODIUM MALONATE - MALONIC ACID",6090,"M",1.079034,0.643394,245,6.92102,0.349662,254,NOT_AVAILABLE,104.6,-999,[2.83,5.69,-999]]
BIS_TRIS_CHLORIDE=["BIS-TRIS CHLORIDE",7721,"M",0.090257,0.016033,2567,5.913337,0.501148,2567,NOT_AVAILABLE,209.2,50,[6.46,-999,-999]]
DL_MALIC_ACID=["DL-MALIC ACID",683,"M",1.53473,0.723314,97,6.584565,1.198147,97,NOT_AVAILABLE,134.1,41,[3.4,5.1,-999]]
DIAM_HYDRO_PHOS=["DIAMMONIUM HYDROGEN PHOSPHATE",502,"M",0.907834,0.692703,21,8.166667,1.290994,21,NOT_AVAILABLE,132.05,57.5,[2.1,7.2,12.3]]

LOOK_UP_TABLE=[SODIUM_ACE_ACE_ACID,SODIUM_MAL_MAL_ACID,BIS_TRIS_CHLORIDE,DL_MALIC_ACID,DIAM_HYDRO_PHOS]

# Function: Removes empty tuples/array from list
# Parameters: list = List
# Returns: (list, temp)resulting list,
#          (int, nulls) number of empty nodes removed

def strip_nulls(list):
	temp = []
	nulls = 0
	for n in list:
		if n != None:
			temp.append(n)
		else:
			nulls+=1
	return temp,nulls

# Function: Appends a XML element node for a chemical to the
#           parameter document root node
# Parameters: doc = XML document object to append to
#             root = Existing parent node of document to append to
#             chem_tuple = List of current chemical's data
#                          ([0], chemical name), ([1], total occurences),
#                          ([2], units), ([3], concentration mean), 
#                          ([4], concentration standard deviation),
#                          ([5], number of records without a concentration value),
#                          ([6], pH mean), ([7], pH standard deviation),
#                          ([8], number of records without a pH value),
#                          ([9], density value), ([10], molecular weight value)
#                          ([11], solubility value), ([12], pka values list)
#             histo_tuple = List of histogram values of current chemical
#                           ([0], maximum x-axis value), ([1], maximum y-axis value)
#                           ([2], total number of intended coordinates),
#                           ([3], list of coordinates)
# Returns: (void)

def xml_append_chem(doc, root, chem_tuple, histo_tuple):
	conc_occ = chem_tuple[1] - chem_tuple[5]
	ph_occ = chem_tuple[1] - chem_tuple[8]
	
	chem = doc.createElement("chemical")
	chem.setAttribute("name",chem_tuple[0])
	if chem_tuple[9] == NOT_AVAILABLE:
		chem.setAttribute("density","")
	else:
		chem.setAttribute("density",str(chem_tuple[9]))
	if chem_tuple[10] == NOT_AVAILABLE:
		chem.setAttribute("mw","")
	else:
		chem.setAttribute("mw",str(chem_tuple[10]))
	if chem_tuple[11] == NOT_AVAILABLE:
		chem.setAttribute("solubility","")
	else:
		chem.setAttribute("solubility",str(chem_tuple[11]))
	
	if chem_tuple[12]:
		if chem_tuple[12][0] == NOT_AVAILABLE:
			chem.setAttribute("pka1","")
		else:
			chem.setAttribute("pka1",str(chem_tuple[12][0]))
		if chem_tuple[12][1] == NOT_AVAILABLE:
			chem.setAttribute("pka2","")
		else:
			chem.setAttribute("pka2",str(chem_tuple[12][1]))
		if chem_tuple[12][2] == NOT_AVAILABLE:
			chem.setAttribute("pka3","")
		else:
			chem.setAttribute("pka3",str(chem_tuple[12][2]))
	else:
		chem.setAttribute("pka1","")
		chem.setAttribute("pka2","")
		chem.setAttribute("pka3","")
	
	chem.setAttribute("occurence",str(chem_tuple[1]))
	root.appendChild(chem)
	
	if chem_tuple[0].lower() != "unknown":
		conc = doc.createElement("conc")
		conc.setAttribute("units",chem_tuple[2])
		conc.setAttribute("occurence",str(conc_occ))
		chem.appendChild(conc)
		
		conc_mean = doc.createElement("mean")
		conc_mean.setAttribute("value",str(chem_tuple[3]))
		conc.appendChild(conc_mean)
		conc_sd = doc.createElement("sd")
		conc_sd.setAttribute("value",str(chem_tuple[4]))
		conc.appendChild(conc_sd)
		
		ph = doc.createElement("ph")
		ph.setAttribute("occurence",str(ph_occ))
		chem.appendChild(ph)
		
		ph_mean = doc.createElement("mean")
		ph_mean.setAttribute("value",str(chem_tuple[6]))
		ph.appendChild(ph_mean)
		ph_sd = doc.createElement("sd")
		ph_sd.setAttribute("value",str(chem_tuple[7]))
		ph.appendChild(ph_sd)
		
		if histo_tuple[0] >= 0:
			histo = doc.createElement("histogram")
			histo.setAttribute("units",chem_tuple[2])
			histo.setAttribute("maxx",str(histo_tuple[0]))
			histo.setAttribute("maxy",str(histo_tuple[1]))
			chem.appendChild(histo)
		
			for n in histo_tuple[2]:
				coord = doc.createElement("coord")
				coord.setAttribute("x",str(n[0]))
				coord.setAttribute("y",str(n[1]))
				histo.appendChild(coord)
	return

# Function: Creates and returns a list of chemical data from input XML file
# Parameters: file = Filename/path of chemicals XML file
# Returns: (list, xml_chems) list of chemical data tuples each consisting of
#                            ([0], list of names/aliases of chemical),
#                            ([1], density value), ([2], molecular weight)
#                            ([3], solubility value), ([4], pKa values list)

def parse_source_xml(file):
	xml_chems = []
	dom = parse(file)
	data = dom.getElementsByTagName('chemical')
	for n in data:
		names = []
		pkas = []
		
		names.append(str(n.getAttribute('name')))
		density = n.getAttribute('density')
		mw = n.getAttribute('mw')
		solubility = n.getAttribute('solubility')
		pka1 = n.getAttribute('pka1')
		pka2 = n.getAttribute('pka2')
		pka3 = n.getAttribute('pka3')
		
		if density:
			density = float(density)
		else:
			density = NOT_AVAILABLE
		if mw:
			mw = float(mw)
		else:
			mw = NOT_AVAILABLE
		if solubility:
			solubility = float(solubility)
		else:
			solubility = NOT_AVAILABLE
		
		if pka1:
			pka1 = float(pka1)
		else:
			pka1 = NOT_AVAILABLE
		if pka2:
			pka2 = float(pka2)
		else:
			pka2 = NOT_AVAILABLE
		if pka3:
			pka3 = float(pka3)
		else:
			pka3 = NOT_AVAILABLE
		
		pkas.append(pka1)
		pkas.append(pka2)
		pkas.append(pka3)
		pkas = tuple(pkas)
		
		aliases = n.getElementsByTagName('alias')
		for a in aliases:
			names.append(str(a.childNodes[0].nodeValue))
		
		xml_chems.append((names,density,mw,solubility,pkas))
	return xml_chems

# Function: Finds, matches and returns the density and molecule weight
#           of chemical from the list created using function(parse_source_xml)
# Parameters: list = List of chemical tuples
#             chem_name = Current chemical name
# Returns: (Decimal, density), (Decimal, mw) molecular weight

def get_source_xml_chem_data(list, chem_name):
	source_xml_chems = list
	source_row = 0
	source_name = source_xml_chems[source_row][0][0]
	no_match = FALSE
	
	while source_name.lower() != chem_name.lower():
		if source_row == len(source_xml_chems):
			no_match = TRUE
			break
		for a in xrange(len(source_xml_chems[source_row][0])):
			source_name = source_xml_chems[source_row][0][a]
			if source_name.lower() == chem_name.lower():
				break
		source_row+=1
	
	if no_match != TRUE:
		density = source_xml_chems[source_row-1][1]
		mw = source_xml_chems[source_row-1][2]
		solubility = source_xml_chems[source_row-1][3]
		pkas = source_xml_chems[source_row-1][4]
	else:
		density = NOT_AVAILABLE
		mw = NOT_AVAILABLE
		solubility = NOT_AVAILABLE
		pkas = []
		no_match = FALSE
	
	return Decimal(density),Decimal(mw),solubility,pkas
	
	
	
	
# def histo_coords(list):
	# if len(list) < 2:
		# return list[0],1,[(list[0],1)]
	# else:
		# maxy = len(list)
		# maxx = 0
		# minx = 0
		# xcount = 100
		
		# #if prev_name.upper() == "HEPES":
		# #		list = sorted(list)
		# #		print list
		
		# for n in list:
			# if n > maxx:
				# maxx = n
		
		# x_inter = float(maxx) / float(xcount)
		# #x_inter = float(maxx)
		# #xcount = int(maxx)
		
		# #if xcount == 0:
		# #	xcount = 1
		
		# ycoords = [0] * xcount
		# xcoords = [0] * xcount
		
		# for i in xrange(1, (xcount+1)):
			# xcoords[(i-1)] = round((float(i) * x_inter),6)
		
		# for n in list:
			# bucket = int(round((float(n) / float(x_inter)),6) - 1)
			# ycoords[bucket] = ycoords[bucket] + 1
			# #if prev_name.upper() == "HEPES":
			# #	print n, bucket, ycoords[bucket]
		
		# coords = [0] * xcount
		# counter = 0
		
		# while counter < len(xcoords):
			# coords[counter] = xcoords[counter],ycoords[counter]
			# counter+=1
		
		# return maxx,maxy,coords