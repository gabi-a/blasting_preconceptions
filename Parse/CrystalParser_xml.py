#
# Copyright (C) 2008-2014 CSIRO Australia
#

from xml.dom.minidom import Document, parse
import sys




def clean_alias_dict(alias_dict):
  ret_dict = {}
  # check for duplicates, do not add them to file
  global_alias_set = set()
  global_dup_set = set()
  for chem, alias_set in alias_dict.iteritems():
    global_dup_set.update(alias_set.intersection(global_alias_set))
    global_alias_set.update(alias_set)
  for chem, alias_set in alias_dict.iteritems():    
    ret_dict.setdefault(chem,set())
    ret_dict[chem] = alias_set.difference(global_dup_set)
  return ret_dict
      
      
def make_alias_dict_xml_file(filename, dirty_alias_dict, resolved_chemname_set):
  xmldoc = Document()
  alias_dict=clean_alias_dict(dirty_alias_dict)
  chemicals_obj = xmldoc.createElement("chemicals")
  xmldoc.appendChild(chemicals_obj)
  for chem_name, alias_set in alias_dict.iteritems():
    if chem_name in resolved_chemname_set:
      chemical_obj = xmldoc.createElement("chemical")
      chemical_obj.setAttribute("name", chem_name)
      chemicals_obj.appendChild(chemical_obj)
      for alias_name in alias_set:
        alias_obj = xmldoc.createElement("alias")
        alias_txt_obj = xmldoc.createTextNode(alias_name)
        alias_obj.appendChild(alias_txt_obj)
        chemical_obj.appendChild(alias_obj)
  fp=open(filename,'wb')
  fp.write(xmldoc.toprettyxml(indent="  "))
  fp.close()
  

def make_resolved_chem_freq_xml(filename, sort_by_freq, resolved_chems_dict):
  xmldoc = Document()
  chemicals_obj = xmldoc.createElement("chemicals")
  xmldoc.appendChild(chemicals_obj)
  # do resolved list, but only write out if not in non-chem list
  if sort_by_freq:
    sorted_items = sorted(resolved_chems_dict.items(), cmp=lambda x,y: cmp(x[1], y[1]), reverse=True)
    for name, freq in sorted_items:
      chemical_obj = xmldoc.createElement("chemical")
      chemical_obj.setAttribute("name", name)
      chemical_obj.setAttribute("freq", str(freq))
      chemicals_obj.appendChild(chemical_obj)
  else:
    sorted_names = sorted(resolved_chems_dict.keys())
    for name in sorted_names:
      chemical_obj = xmldoc.createElement("chemical")
      chemical_obj.setAttribute("name", name)
      chemical_obj.setAttribute("freq", str(resolved_chems_dict[name]))
      chemicals_obj.appendChild(chemical_obj)
        
  fp=open(filename,'wb')
  fp.write(xmldoc.toprettyxml(indent="  "))
  fp.close()


def make_conditions_xml(filename, cond_dict):

  xmldoc = Document()
  conditions_obj = xmldoc.createElement("conditions")
  xmldoc.appendChild(conditions_obj)
   
  # do cond list, but only write out if not in non-chem list

  for code in cond_dict.keys():
    pdb_obj = xmldoc.createElement("pdb")
    pdb_obj.setAttribute("code", code)
    conditions_obj.appendChild(pdb_obj)
    for solution_type in cond_dict[code].keys():
      soltyp_obj = xmldoc.createElement("solution")
      soltyp_obj.setAttribute("type", solution_type)
      pdb_obj.appendChild(soltyp_obj)
      for conc, units, chem, pH in cond_dict[code][solution_type]:
        condition_obj = xmldoc.createElement("condition")
        condition_obj.setAttribute("conc", str(conc))
        condition_obj.setAttribute("units", units)
        condition_obj.setAttribute("chem", chem)
        condition_obj.setAttribute("pH", str(pH))
        soltyp_obj.appendChild(condition_obj)    

  fp=open(filename,'wb')
  fp.write(xmldoc.toprettyxml(indent="  "))
  fp.close()
        
        
def make_chems_xml(filename, chem_out_set):

  xmldoc = Document()
  chemicals_obj = xmldoc.createElement("chemicals")
  xmldoc.appendChild(chemicals_obj)
  
  # Write out list of chems used
  for chem in list(chem_out_set):
    chemical_obj = xmldoc.createElement("chemical")
    chemical_obj.setAttribute("name", chem)
    chemicals_obj.appendChild(chemical_obj)
      
  fp=open(filename,'wb')
  fp.write(xmldoc.toprettyxml(indent="  "))
  fp.close()
  
def check_xml_alias_file(xml_alias_file, xml_chem_file):
  chem_dom=parse(xml_chem_file)
  
  chemname_set=set()
  chemsobj=chem_dom.getElementsByTagName("chemicals")[0]
  chemobj_list=chemsobj.getElementsByTagName("chemical")
  
  for chemobj in chemobj_list:
    chemname_set.add(chemobj.getAttribute("name"))
  #print "1:", len(chemname_set), str(chemname_set)
  
  al_dom=parse(xml_alias_file)
  alchemname_set=set()
  chemsobj=al_dom.getElementsByTagName("chemicals")[0]
  chemobj_list=chemsobj.getElementsByTagName("chemical")
  for chemobj in chemobj_list:
    chem_name=chemobj.getAttribute("name")
    alchemname_set.add(chem_name)
  #print "2:", len(alchemname_set), str(alchemname_set)
  
  #print "2-1:", str(alchemname_set-chemname_set)
  return chemname_set>=alchemname_set
  

  
  
if __name__== "__main__":
  if len(sys.argv) > 2:
    xml_alias_file=sys.argv[1]
    xml_chem_file=sys.argv[2]
    print "xml_alias_file=", xml_alias_file
    print "xml_chem_file=", xml_chem_file
    print check_xml_alias_file(xml_alias_file, xml_chem_file)
    
