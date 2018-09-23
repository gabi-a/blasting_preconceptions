# Copyright (C) CSIRO 2012-2013
# $Id: crysSolutionsXml.py 138 2013-02-18 23:45:02Z faz014 $

# Creates and outputs a XML file based on the combined data collected
# from the PDB's Chemicals and CrystalSOLUTIONs databases.
#
# Original Author: Michelle Ching Wah Chan
#
import psycopg2
import mod_maths
import mod_unitConverter
import mod_xmlTools
import mod_dynamicKneecap
import crysSolutionsXml_func

IN_DB="host=138.194.245.200 dbname=crystaldb user=tom"  #Details to connect to database
DB_QUERY="SELECT Chemicals.Name, Crystal_SOLUTIONs.CONCENTRATION, Crystal_SOLUTIONs.PH, Crystal_SOLUTIONs.UNITS FROM Chemicals INNER JOIN Crystal_SOLUTIONs ON Chemicals.Chemical_id=Crystal_SOLUTIONs.Chemical_id ORDER BY Chemicals.Name"
IN_SOURCE_XML="Chemicals_18Dec12.xml"                   #Source XML file used to collect the density, molecular weight,
                                                        #pKa values and solubility of chemicals
OUT_XML_FILENAME="chemicals.xml"                        #Intended name/path of this script's output XML file
NOT_AVAILABLE=-999
NOT_SET = -2
TRUE = 0
FALSE = 1

def main():
	conn = psycopg2.connect(IN_DB)
	cur = conn.cursor()
	
	cur.execute(DB_QUERY)
	db_result = cur.fetchall()
	
	# Locate and create list of chemicals stored using multiple measurement units
	multi_unit_tracker = []
	curr_chem = db_result[0][0]
	curr_unit = db_result[0][3]
	multi_unit_found = FALSE
	
	for chem in db_result:
		if chem[0] == curr_chem:
			if (chem[3] != curr_unit) and (multi_unit_found == FALSE):
				multi_unit_tracker.append(chem[0])
				multi_unit_found = TRUE
		else:
			curr_chem = chem[0]
			curr_unit = chem[3]
			multi_unit_found = FALSE
	
	curr_chem = []
	conc = []
	ph = []
	histogram = []
	coords = []
	
	row = 0
	prev_name = db_result[row][0]
	density = NOT_SET
	mw = NOT_SET
	solubility = NOT_SET # NEW
	pkas = NOT_SET # NEW
	set_wv_unit = FALSE
	invalid_unit = FALSE
	
	doc,doc_root = mod_xmlTools.create_xml("chemicals")   #Initialise XML document
	source_xml_chems = crysSolutionsXml_func.parse_source_xml(IN_SOURCE_XML)
	
	while row < len(db_result):
		curr_name = db_result[row][0]
		
		# Find the density and molecular weight value of current chemical.
		# If density was not stored in source XML file, default density to 1.
		# If both density and molecular weight were not stored, then set invalid_unit
		# variable to TRUE to indicate concentration values of this chemical cannot
		# be converted.
		if (density == NOT_SET) and (mw == NOT_SET) and (solubility == NOT_SET) and (pkas == NOT_SET):
			density,mw,solubility,pkas = crysSolutionsXml_func.get_source_xml_chem_data(source_xml_chems, curr_name)
			if density == NOT_AVAILABLE:
				if mw == NOT_AVAILABLE:
					invalid_unit = TRUE
				else:
					density = 1
			#if mw == NOT_AVAILABLE:
			#	print curr_name
			#print curr_name, density, mw
		
		if curr_name == prev_name:
			# Create lists of recorded concentration and pH values used for current chemical
			curr_conc = db_result[row][1]
			
			# If chemical has been stored using multiple units, convert all values to W/V.
			# If this chemical has record/s using invalid units, variable invalid_unit is
			# set to TRUE to indicate that a histogram cannot be created for this chemical.
			if (curr_name in multi_unit_tracker) and (invalid_unit == FALSE):
				if mod_unitConverter.get_unit_type(db_result[row][3],density) != NOT_AVAILABLE:
					curr_conc = mod_unitConverter.convert_unit_to_wv(db_result[row][3],db_result[row][1],density,mw)
					if set_wv_unit == FALSE:
						set_wv_unit = TRUE
				# Going ahead with printing histograms for chemicals with invalid unit records
				# by ignoring these records. Uncomment these following 2 lines to disable
				# printing the histograms for these chemicals.
				# else:
					# invalid_unit = TRUE
			
			if (solubility == NOT_AVAILABLE) or (curr_conc <= solubility):
				conc.append(curr_conc)
				ph.append(db_result[row][2])
			
			prev_name = curr_name
			row+=1
		else:
			# Create the chemical data and histogram tuples for current chemical
			total = len(conc)
			
			conc,conc_nulls = crysSolutionsXml_func.strip_nulls(conc)
			ph,ph_nulls = crysSolutionsXml_func.strip_nulls(ph)
			
			conc_mean = mod_maths.calc_mean(conc)
			conc_sd = mod_maths.calc_sd(conc,conc_mean)
			ph_mean = mod_maths.calc_mean(ph)
			ph_sd = mod_maths.calc_sd(ph,ph_mean)
			
			if set_wv_unit == TRUE:
				units = "W/V"
			else:
				units = db_result[row-1][3]
			
			if len(conc) < 1:
				print "VALID CONC LIST NA",
				print prev_name
				histogram.append(NOT_AVAILABLE)
				invalid_unit = TRUE
			else:
				if (max(conc) == 0) or (invalid_unit == TRUE):
					print "HISTO NA",
					print prev_name
					histogram.append(NOT_AVAILABLE)
					invalid_unit = TRUE
			
			if (invalid_unit == FALSE) and (prev_name.lower() != "unknown"):
			
				#DYNAMIC KNEECAP
				maxx,maxy,coords = mod_dynamicKneecap.get_capped_list(conc)
				
				#RAW FREQUENCY HISTOGRAM
				# maxx,maxy,coords = crysSolutionsXml_func.histo_coords(conc)
				
				histogram.append(maxx)
				histogram.append(maxy)
				histogram.append(coords)
			
			curr_chem.append(prev_name)
			curr_chem.append(total)
			curr_chem.append(units)
			curr_chem.append(round(conc_mean,6))
			curr_chem.append(round(conc_sd,6))
			curr_chem.append(conc_nulls)
			curr_chem.append(round(ph_mean,6))
			curr_chem.append(round(ph_sd,6))
			curr_chem.append(ph_nulls)
			curr_chem.append(round(density,6))
			curr_chem.append(round(mw,6))
			curr_chem.append(solubility)
			curr_chem.append(pkas)
			
			
			# Append current chemical data to XML document
			crysSolutionsXml_func.xml_append_chem(doc, doc_root, curr_chem, histogram)
			
			# Reset variables
			conc[:] = []
			ph[:] = []
			curr_chem[:] = []
			coords[:] = []
			histogram[:] = []
			pkas = NOT_SET
			density = NOT_SET
			mw = NOT_SET
			solubility = NOT_SET
			set_wv_unit = FALSE
			invalid_unit = FALSE
			prev_name = curr_name
	
	# Append all chemicals from look-up table to XML document
	for chem in crysSolutionsXml_func.LOOK_UP_TABLE:
		crysSolutionsXml_func.xml_append_chem(doc, doc_root, chem, [NOT_AVAILABLE])
	
	mod_xmlTools.print_xml(doc,OUT_XML_FILENAME)   #Output XML document to file
	
	cur.close()
	conn.close()

if __name__ == '__main__':
	main()