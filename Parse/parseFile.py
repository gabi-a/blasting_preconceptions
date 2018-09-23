#!/bin/env python

# Copyright (C) 2008-2014 CSIRO Australia
#
# This script takes as input a text file of 'REMARK 280' sections from PDB
# entries. (Use 'extract_pdb_ents.sh' to create it) It parses the file and
# and extracts chems, concentrations, units and pH for each PDB entry.
# It prints some statistics about the PDB and its own performance and writes
# out some xml files of results.
#
import csv
import os
import sys
import random

from CrystalParser import CRYSTAL_PARSER
from CrystalParser_alia import non_chem_list
from CrystalParser_xml import make_resolved_chem_freq_xml, make_conditions_xml, make_chems_xml
from CrystalParser_xml import make_alias_dict_xml_file, check_xml_alias_file
from CrystalCorrecter import CrystalCorrecter
      
      
def doFile(fname):
    cond_pdb_dict = {}
    failed_debug=0
    verbose=0
    sort_by_freq=True
    use_chem_classes=False

    # Turn this on and it will process only 'random_sample_size' pdb entries
    # randomly selected from input file
    random_select=False
    random_sample_size=150

    
    sample_code_list=[]
    if random_select:
      # Create a list of pdb entries
      fp=open(fname,"r")
      old_code=None
      code=""     
      code_list=[]
      for line in fp.readlines():
        code=line[3:].split('.')[0]
        colon1_pos=line.find(':')+1
        if colon1_pos<1:
          continue
        if code!=old_code:
          code_list.append(code)
          old_code=code
      fp.close()
      #print "CODE_LIST=", repr(code_list)

      # Pick a selection of pdb entries at random
      if len(code_list)<random_sample_size:
        random_sample_size=len(code_list)
      try:
        sample_code_list=random.sample(code_list, random_sample_size)
      except ValueError, e:
        print repr(e)
        sys.exit(1)
      print "SAMPLE_LIST=", repr(sample_code_list)

    correctedchems_file=os.path.join("input","CORRECTEDCHEMS.txt")
    if not os.path.exists(correctedchems_file):
      print "ERROR - File does not exist: ", correctedchems_file
      sys.exit(1)
    correcter_obj=CrystalCorrecter(correctedchems_file, max_dist=1)
    xc=CRYSTAL_PARSER(verbose, failed_debug, sort_by_freq, use_chem_classes, correcter_obj)
    xc.got_xtal_cond=True
 
    in_cond = False
    conds = ''
    for line in open(fname,"r"):
      if verbose>0:
        print "-->",line
      #code=line[3:7]
      # Look for the pdb code from 4th char to the '.'
      code=line[3:].split('.')[0]
      
      #cond_line=line[23:]
      
      # Look for first colon for start of conditions
      colon1_pos=line.find(':')+1
      if colon1_pos<1:
        continue
        
      remark_pos=line.find('REMARK 280')+10
      
      # Pick either the end of 'REMARK 280' or first colon as the start
      cutoff_pos=max(remark_pos, colon1_pos)

      #stripped_cond=line[23:].rstrip(' \n')
      cond_line=line[cutoff_pos:]
      stripped_cond=line[cutoff_pos:].rstrip(' \n')
      
      # If reached the end of the current entry
      if in_cond and (len(stripped_cond)==0 or old_code!=code):
        if not random_select or random_select and old_code in sample_code_list:
          xc.wellComponentSplit(conds, old_code)
          cond_pdb_dict[old_code]=conds
        in_cond=False
        conds = ''

      # If haven't reached the end then continue concatenating lines
      if in_cond or not in_cond and 'CRYSTALLIZATION CONDITIONS:' in cond_line:
        in_cond = True
        conds += cond_line
        old_code = code
    
    # This parses the last lines in the file
    if in_cond:
      if not random_select or random_select and old_code in sample_code_list:
        xc.wellComponentSplit(conds, old_code)
        cond_pdb_dict[old_code]=conds
      
    # do chem list
    chem_rawhisto_pairs=list(xc.RCHEM_HISTO.iteritems())
    chem_rawhisto_pairs.sort(cmp=lambda x,y: cmp(x[1],y[1]), reverse=True)

    CHEMSP_PASS=CHEMSP_UNKNOWN=CHEMSP_TOTAL=CHEMSP_NON_CHEM=CHEMSP_FAIL=0
    chem_rawname_list = xc.RCHEM_HISTO.keys()
    chem_rawname_list.sort()
    chem_out_set = set()
    
    # Sort chems by descending frequency
    if sort_by_freq:
      chem_rawname_list = []
      for raw_chem, freq in chem_rawhisto_pairs:
        chem_rawname_list.append(raw_chem)

    # make output dir
    if not os.path.exists("output"):
      os.mkdir("output")
   
    # This loop tallies up all the chemicals and the alias lists used to generate them    
    print "Raw chemicals list:"
    for raw_chem in chem_rawname_list:
      print repr(raw_chem), ": ", xc.RCHEM_HISTO[raw_chem],
      res_chem_name=xc.alia.resolve_chem_name(raw_chem)
      if res_chem_name=='Unknown':
        CHEMSP_UNKNOWN+=1
        CHEMSP_FAIL+=1
        print "{Unknown chem}",
      elif res_chem_name in non_chem_list:
        CHEMSP_NON_CHEM += 1
        CHEMSP_FAIL+=1
        print "{Non chem: '"+res_chem_name+"}",
      else:
        print "{Resolved chem: "+res_chem_name+"}",
        CHEMSP_PASS += 1
        chem_out_set.add(res_chem_name)
      CHEMSP_TOTAL += 1

      if xc.RCHEM_HISTO[raw_chem] < 30:
        print repr(xc.RCHEM_CODES[raw_chem])
      else:
        print
       
        
    make_resolved_chem_freq_xml(os.path.join("output","chemfreq_resolved_out.xml"), 
                                                  sort_by_freq, xc.CHEM_HISTO)
    make_conditions_xml(os.path.join("output","cond_resolved_out.xml"),xc.CONDS)
    chem_list_file=os.path.join("output","chem_list.xml")
    make_chems_xml(chem_list_file, chem_out_set)
    chem_alia_file=os.path.join("output","chem_alia.xml")
    make_alias_dict_xml_file(chem_alia_file, xc.chem_alia, chem_out_set)

    print "Checking xml alias file:", check_xml_alias_file(chem_alia_file, chem_list_file)

    CODE_TOTAL=xc.CODE_PASS+xc.CODE_FAIL+xc.CODE_BLANK
    if CODE_TOTAL>0:
      print
      print "--> By PDB code"
      print "total number of pdb codes:  ",CODE_TOTAL
      print "%% passed:      %.2f %%"%(100.0*float(xc.CODE_PASS)/float(CODE_TOTAL))
      print "%% empty:      %.2f %%"%(100.0*float(xc.CODE_BLANK)/float(CODE_TOTAL))
      print "%% failed:      %.2f %%"%(100.0*float(xc.CODE_FAIL)/float(CODE_TOTAL))
      print
      print "failed code list: ", repr(xc.CODE_FAIL_LIST)

    if CHEMSP_TOTAL>0 and CHEMSP_PASS>0:
      print
      print "--> By chem species count:"
      print "Number of chemicals:",CHEMSP_TOTAL
      print "Unknown: ", CHEMSP_UNKNOWN, '/', CHEMSP_TOTAL
      print "Known: ", CHEMSP_PASS, '/', CHEMSP_TOTAL
      print "Non-chem: ", CHEMSP_NON_CHEM, '/', CHEMSP_TOTAL
      print

    if xc.CHEM_TOTAL>0:
      print "--> By chem count:"
      print "Unknown/Total: ", str(xc.CHEM_UNKNOWN), '/', str(xc.CHEM_TOTAL)
      print "%% Known: %.2f %%"%(float(xc.CHEM_PASS)/float(xc.CHEM_TOTAL)*100.0)
      print "%% Unknown: %.2f %%"%(float(xc.CHEM_UNKNOWN)/float(xc.CHEM_TOTAL)*100.0)
      print "%% Non-chem: %.2f %%"%(float(xc.CHEM_NON_CHEM)/float(xc.CHEM_TOTAL)*100.0)
      print

    # Try to estimate conversion success rate
    cnt_tp=0.0
    sum_tp=0.0
    #print repr(xc.TOTAL_PARTS.keys())
    #print repr(xc.CONDS.keys())
    print "--> Conversion Quality Report:"
    for pdb_code, total_parts in xc.TOTAL_PARTS.iteritems():
      num_passed=total_parts-xc.TOTAL_FAILED_PARTS[pdb_code]
      print "PDB: ", pdb_code, " #parts passed/#total: ", str(num_passed),'/',str(total_parts)
      if num_passed>0 and xc.CONDS.get(pdb_code,{}).has_key('reservoir'): 
        print "   Reservoir:" 
        cond_cnt=0
        for cond in xc.CONDS[pdb_code]['reservoir']:
          if cond[3]!=None:
            if cond[0]<0.0001:
              print "     %2d: %8.6f %s %s pH %s"%(cond_cnt,cond[0],cond[1],cond[2],cond[3]) 
            else:
              print "     %2d: %6.4f %s %s pH %s"%(cond_cnt,cond[0],cond[1],cond[2],cond[3]) 
          else:
            if cond[0]<0.0001:
              print "     %2d: %8.6f %s %s"%(cond_cnt,cond[0],cond[1],cond[2]) 
            else:
              print "     %2d: %6.4f %s %s"%(cond_cnt,cond[0],cond[1],cond[2]) 
          cond_cnt+=1
        print
      print "   REMARK280 line: "
      print str(cond_pdb_dict[pdb_code])
      print
      print
      cnt_tp += 1.0
      if total_parts>0:
        sum_tp += float(total_parts-xc.TOTAL_FAILED_PARTS[pdb_code])/float(total_parts)
      print "cnt_tp=", repr(cnt_tp)
      print "sum_tp=", repr(sum_tp)

    if cnt_tp>0.0:
      print "Est. mean conversion = ", str(100.0*sum_tp/cnt_tp), "%"

    print xc.TEMPERATURE
    print xc.CHEMICALS
    print xc.CONCENTRATIONS
    print xc.CONCENTRATION_UPPER_LIMITS
    print xc.CONDS
    print xc.CODE_FAIL_LIST
    print xc.chem_alia
    
    
if __name__== "__main__":
    if len(sys.argv) > 1:
        fname=sys.argv[1]
        print "doFile(", fname, ")"
        doFile(fname)
    else:
      print "Usage: parseFile.py <text file>\n"
      sys.exit(1)


    
