#
# Copyright (C) 2008-2014 CSIRO Australia
#

import re
import string 
import math
import os
import sys
import csv

from CrystalParser_alia import CRYSTAL_PARSER_ALIA

class CRYSTAL_PARSER_BASE:

  def __init__(self, verbose, failed_debug, use_chem_classes, correcter_obj):
    self.re_dict={}
    self.matchgroups=[]
    
    # Initialise with the internal dictionary, full dictionary will be loaded later on 
    self.chem_alia = {}    
    self.GEN_ALIAS_DICT=True
    self.ILLEGAL_NUMBER_RE=re.compile("[:~,;%]")
    self.ILLEGAL_CHAR_RE=re.compile("[:]")
    self.WV_VV_REGEXP=r'%?\s*[\[\(]?\s*[WV]\s*[/\\]?\s*[WV]/?\s*[\]\)]?'
    self.WV_REGEXP1=r'%?\s*[\[\(]?\s*W\s*[/\\]?\s*[WV]/?\s*[\]\)]?'
    self.WV_REGEXP2=r'%?\s*[\[\(]?\s*V\s*[/\\]?\s*W/?\s*[\]\)]?'
    self.VV_REGEXP=r'%?\s*[\[\(]?\s*V\s*[/\\]?\s*V/?\s*[\]\)]?'
    self.UNITS_REGEXP=self.WV_VV_REGEXP+r'|%|UM\b|MM\b|M\b|MG/ML\b|G/ML\b|G/L\b|MG\b|UG\b|G\b|UG/ML\b'
    
    # Debug flags
    self.verbose=verbose
    self.phdebug=0
    self.failed_debug=failed_debug
    self.debug_temp=0
    
    self.alia=CRYSTAL_PARSER_ALIA(verbose, use_chem_classes, correcter_obj)

    # Load dictionary of pKas
    self.pka_dict = {}
    """ select name, pka1, pka2, pka3 from chemicals
        where pka1 is not null
    """
    pkaFile=os.path.join('input','chem+pka.csv')
    if not os.path.exists(pkaFile):
      print "Cannot find csv file: {0}".format(pkaFile)
      sys.exit(1)
    pkaCsvReader = csv.reader(open(pkaFile))
    for chem, pka1, pka2, pka3 in pkaCsvReader:
      chemu = chem.upper()
      # Correct some flaws in CT's alia:
      # Can't have both TRIS and TRIS CHLORIDE
      if chemu=='TRIS':
        chemu='TRIS CHLORIDE'
      # Can't have both SODIUM CITRATE and SODIUM CITRATE - CITRIC ACID
      if chemu=='SODIUM CITRATE':
        chemu='SODIUM CITRATE - CITRIC ACID'
      try:
        self.pka_dict[chemu] = [float(pka1)] 
        if pka2 not in [None,'']:
          self.pka_dict[chemu] += [float(pka2)]
        if pka3 not in [None,'']:
          self.pka_dict[chemu] += [float(pka3)]
      except ValueError:
        print "ERROR: Bad pKa in ", repr(pkaFile)

    # Load dictionary of default units
    self.default_units_dict={}
    """ select name, units_type from chemicals
        where chemical_id not in (select chemical_id from proteins)
        and units_type is not null
    """
    unitsFile=os.path.join('input','chem+units.csv')
    if not os.path.exists(unitsFile):
      print "Cannot find csv file: {0}".format(unitsFile)
      sys.exit(1)
    unitsCsvReader = csv.reader(open(unitsFile))
    for chem, units in unitsCsvReader:
      chemu = chem.upper()
      unitsu = units.upper()
      # Correct some flaws in CT's alia:
      # Can't have both TRIS and TRIS CHLORIDE
      if chemu=='TRIS':
        chemu='TRIS CHLORIDE'
      # Can't have both SODIUM CITRATE and SODIUM CITRATE - CITRIC ACID
      if chemu=='SODIUM CITRATE':
        chemu='SODIUM CITRATE - CITRIC ACID'
      self.default_units_dict[chemu]=unitsu
        
  # This function returns True if 'chem' is a buffer at around float 'pH'
  def is_buffer(self, chem, pH):
    PKA_RANGE = 1.0
    for pka in self.pka_dict.get(chem,[]):
      if pka-PKA_RANGE < pH and pka+PKA_RANGE > pH:
        return True
    return False

  # This function returns True if 'chem' is a possible buffer
  def is_potential_buffer(self, conc, uoms, chem):
    return conc<0.2 and uoms=='M' and self.pka_dict.has_key(chem)

  # Sometimes units are given as '%' or 'V/V', but it is 
  # obvious from the chemical (which is a solid at room temperature)
  # that they should be 'W/V'.
  # This routine fixes that problem.
  def resolve_units(self, chem, units):
    default_units=self.default_units_dict.get(chem,'Unknown')
    if units=='V/V' and default_units=='W/V':
      return 'W/V'
    return units

  # Function to clean up any strings
  # Used at first input point to convert to upper case and remove any undesirable chars
  # Could be expanded to remove/convert non-ASCII chars ...  
  def init_strclean(self, strng):
    return strng.upper().replace('_',' ').strip()
  
    
  def re_compile(self,restr):
      if not self.re_dict.has_key(restr):
          self.re_dict[restr]=re.compile(restr)
      return self.re_dict[restr]

  def re_search(self,str,restr, debug=False):
    if debug:
      print "re_search(",repr(str),",",repr(restr),")"
    R=self.re_compile(restr)
    m=R.search(str)
    if debug:
      print "Ret:", repr(m)
    return m

  def re_substitute(self,str,restr,substitution, count=0, debug=False):
    if debug:
      print "re_substitute(str=", repr(str), "restr=", repr(restr), "substitution=", repr(substitution), "count=", repr(count),")"
    R=self.re_compile(restr)
    if self.GEN_ALIAS_DICT:
      if substitution!='' and not substitution.isspace():
        match_obj=R.search(str, count)
        if match_obj!=None and match_obj.group(0)!=substitution:
          # try to see if either an alias can be built from substitution plus a word to the left
          # or a word to the right.
          found_it=False
          left_idx=str[:match_obj.start(0)].rfind(' ')
          if left_idx<0:
            left_idx=0
          right_idx=str[match_obj.end(0):].find(' ')
          if right_idx<0:
            right_idx=len(str)
          left_chem=str[left_idx:match_obj.start(0)]
          if left_chem!='' and not left_chem.isspace():
            chem=left_chem+match_obj.expand(substitution)
            if self.alia.has_alias(chem):
              resolved_chem=self.alia.resolve_chem_name(chem)
              if resolved_chem!=left_chem+match_obj.group(0):
                self.chem_alia.setdefault(resolved_chem, set())
                self.chem_alia[resolved_chem].add(left_chem+match_obj.group(0))
                found_it=True
          if not found_it:
            right_chem=str[match_obj.end(0):right_idx]
            if right_chem!='' and not right_chem.isspace():
              chem=match_obj.expand(substitution)+right_chem
              if self.alia.has_alias(chem):
                resolved_chem=self.alia.resolve_chem_name(chem)
                if resolved_chem!=match_obj.group(0)+right_chem:
                  self.chem_alia.setdefault(resolved_chem, set())
                  self.chem_alia[resolved_chem].add(match_obj.group(0)+right_chem)
                  found_it=True
          if not found_it and self.alia.has_alias(substitution):
            resolved_chem=self.alia.resolve_chem_name(substitution)
            if resolved_chem!=match_obj.group(0):
              self.chem_alia.setdefault(resolved_chem, set())
              self.chem_alia[resolved_chem].add(match_obj.group(0))
    str=R.sub(substitution,str,count)
    if debug:
      print "Ret:", repr(str)
    return str

  def re_match_groups(self,str,restr):
    m=self.re_search(str,restr)
    self.matchgroups=[]
    if m is not None:
        self.matchgroups=list(m.groups())
        self.matchgroups.insert(0,restr)
        return True
    return False

  def re_substitute_groups(self,str,restr,substitution):
    R=self.re_compile(restr)
    m=R.search(str)
    if self.GEN_ALIAS_DICT:
      if substitution!='' and not substitution.isspace():
        if m!=None and m.group(0)!=substitution and self.alia.has_alias(substitution):
          #print "*", repr(m.group(0)), "->", repr(substitution)
          self.chem_alia.setdefault(substitution, set())
          self.chem_alia[substitution].add(m.group(0))

    str=R.sub(substitution,str)
    self.matchgroups=[]
    if m is not None:
        self.matchgroups=list(m.groups())
        self.matchgroups.insert(0,restr)
    return str

  def remove_unmatched_brackets(self,str):
    # Removes brackets if there is single left or right, but not if they aren't in the
    # reverse order
    for lb, rb in [('{','}'),('(',')'),('[',']')]:
      lb_pos = str.find(lb)
      rb_pos = str.rfind(rb)
      if lb_pos>=0 and rb_pos<0:
        lb = "\\"+lb
        str = self.re_substitute(str, lb, '')
      elif lb_pos<0 and rb_pos>=0:
        rb = "\\" + rb
        str = self.re_substitute(str, rb, '')
    return str
   
  def trim_string(self,str):
    str = self.re_substitute(str, r'[_\W\s]+$', '')
    str = self.re_substitute(str, r'^[_\W\s]+', '')
    str = self.re_substitute(str, r'^\s+', '')
    str = self.re_substitute(str, r'\s+', ' ')
    return (str)
    
  def is_rubbish(self, str):
    return self.re_search(str, r'^[A-Z]$') or \
             self.re_search(str, r'^[-0-9.]+$') or \
             self.re_search(str, r'^\W+$') or str==''

  def list_cmp(self, list1, list2):
    if len(list1)!=len(list2):
      return False
    for i in range(len(list1)):
      if list1[i]!=list2[i]:
        return False
    return True
  
  def strip_down(self, name):
    for delim in ['\n','\r','\t',' ']:
      name = name.replace(delim,'~')
    name_list = name.split('~')
    ret_list = []
    for elem in name_list:
      if elem!='':
        ret_list.append(elem)
    return ret_list

  def parser_strip_illegals(self, regex,str):
    str=regex.sub(" ",str)
    return str

  def parser_get_integer(self, str):
    i=0
    str=string.strip(self.parser_strip_illegals(self.ILLEGAL_NUMBER_RE,str))
    if str=="NULL" or str=="" or str=="NONE":
      return None
    if str[-1]=="-":
      str=str[:-1]
    try:
      i=string.atoi(str)
    except:
      i=None
    return i

  def parser_get_float(self, str):
    f=0.0
    str=string.strip(self.parser_strip_illegals(self.ILLEGAL_NUMBER_RE,str))
    if str=="NULL" or str=="" or str=="NONE":
      return None
    try:
      f=string.atof(str)
    except:
      f=None
    if not isinstance(f, float) or math.isnan(f) or math.isinf(f):
      f=None
    return f

  def parser_standardise_conc_units(self, conc_float, units_str):
    #print "parser_standardise_conc_units(", repr(conc_float), ',', units_str
    if conc_float==None or units_str==None:
      return (conc_float, units_str)
    if units_str=="MM":
      return (conc_float/1000.0, "M")
    if units_str=="UM":
      return (conc_float/1000000.0, "M")
    if re.match(self.WV_REGEXP1, units_str)!=None or re.match(self.WV_REGEXP2, units_str)!=None:
      return (conc_float, "W/V")
    if units_str=="%" or re.match(self.VV_REGEXP, units_str)!=None:
      return (conc_float, "V/V")
    # Assuming w/v = g/ml verify!
    if units_str=="G/ML":
      return (conc_float, "W/V")
    if units_str=="MG/ML" or units_str=="MG":
      return (conc_float/1000.0, "W/V")
    if units_str=="UG/ML" or units_str=="UG":
      return (conc_float/10000000.0, "W/V")
    # Assuming G is G/L
    if units_str=="G" or units_str=="G/L":
      return (conc_float/1000.0, "W/V")
    return (conc_float, units_str)
    
