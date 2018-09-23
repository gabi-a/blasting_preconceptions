#
# Copyright (C) 2008-2014 CSIRO Australia
#

import csv
from subprocess import *
import sys
from dameraulevenshtein import dameraulevenshtein

#import tre

class CrystalCorrecter():
  # max_dist is the default distance when using 'correct()' procedure
  def __init__(self, correct_words_file, max_dist):
    self.max_dist = max_dist
    self.correct_words_file = correct_words_file
    self.correct_words_str = self.get_wordstr_from_file(correct_words_file)
    self.correct_words_list = self.get_wordlist_from_file(correct_words_file)
    self.debug = False

  #def has_swap(self, good_word, bad_word):
  #  idx=0
  #  #print "good: {0} bad: {1}".format(good_word, bad_word)
  #  if len(good_word)!=len(bad_word):
  #    return False
  #  while idx<len(good_word) and good_word[idx]==bad_word[idx]:
  #    #print repr(idx)
  #    idx+=1
  #  if idx>=len(good_word)-1:
  #    return False
  #  
  #  #print "idx=", repr(idx)
  #  #print "testing: '"+good_word+"'=='"+bad_word[:idx]+"+"+bad_word[idx+1]+"+"+bad_word[idx]+"+"+bad_word[idx+2:]+"' ?"
  #  return good_word==bad_word[:idx]+bad_word[idx+1]+bad_word[idx]+bad_word[idx+2:]
   
  def escape(self, pattern):
    for lit in [',','^','$','.','#','(',')','*','[',']',';','|','-']:
      pattern = pattern.replace(lit,'\\'+lit)
    return pattern
    
  #def run_agrep(self, max_dist, bad_word):
  #  dist = 0
  #  found = False
  #  cand_dict={}
  #  while dist <= max_dist:
  #    cmd = 'SOFTWARE\\agrep337\\agrepw32.exe -%d -n "^%s$" %s'%(dist, bad_word, self.correct_words_file)
  #    #print cmd
  #    popen_obj = Popen(cmd, shell=True, stdout=PIPE)
  #    pipe = popen_obj.stdout
  #    line_list = pipe.readlines()
  #    cand_dict[dist]=[]
  #    for line in line_list:
  #      choice_list=line.split(':')
  #      if len(choice_list)>1 and choice_list[0].isdigit():
  #        candidate=choice_list[1].strip(' \n\r')
  #        cand_dict[dist].append(candidate)
  #    dist+=1
  #  return cand_dict

  #def run_tre(self, max_dist, bad_word):
  #  dist = 0
  #  cand_dict = {}
  #  while dist <= max_dist:
  #    if len(bad_word)==dist:
  #      break
  #    #print "dist=", repr(dist)
  #    fz = tre.Fuzzyness(maxerr = dist)
  #    #print fz
  #    cand_dict[dist] = []
  #    regexp = "\n"+bad_word+"\n"
  #    pt = tre.compile(regexp, tre.EXTENDED)
  #    start=0
  #    m = True
  #    while m!=None:
  #      #print "str=", repr(self.correct_words_str[start:50])
  #      m = pt.search(self.correct_words_str[start:], fz)
  #      #print "m=", repr(m)
  #      #print "regexp=", repr(regexp)
  #      if m!=None:
  #        cand_dict[dist].append(m[0])
  #        start+=m.groups()[0][1]
  #        #print "new start=", repr(start)
  #        #print "m.groups()=", m.groups()
  #        #print "m[0]=", repr(m[0])
  #    dist+=1
  #  return cand_dict
    
  #def tre_choose(self, choice_list, incorrect_word):
  #  fz = tre.Fuzzyness(maxcost=1, inscost=1, delcost=1, subcost=1, maxerr=1, maxins=0, maxdel=1, maxsub=0)

  #  for choice in choice_list:
  #    pt = tre.compile("^"+choice+"$", tre.EXTENDED)
  #    m = pt.search(incorrect_word, fz)
  #    if m!=None:
  #      #print choice, "matched: ", m.groups(), m[0], m.cost, m.numdel, m.numins, m.numsub
  #      return choice
  #  return None

  #def tre_limit(self, list_word, incorrect_word):
  #  fz = tre.Fuzzyness(maxcost=2, inscost=1, delcost=1, subcost=1, maxerr=1, maxins=0, maxdel=1, maxsub=0)
  #  pt = tre.compile("^"+list_word+"$", tre.EXTENDED)
  #  m = pt.search(incorrect_word, fz)
  #  if m!=None:
  #      #print choice, "matched: ", m.groups(), m[0], m.cost, m.numdel, m.numins, m.numsub
  #      return True
  #  return False
    
    
  def run_dl(self, bad_word, max_dist):
    cand_dict = {}
    for corr_word in self.correct_words_list:
       
      dist = dameraulevenshtein(bad_word,corr_word)
      if self.debug:
        print "bad_word=", repr(bad_word), " corr_word=", repr(corr_word), " dist=", repr(dist), " max_dist=", repr(max_dist)
      if dist <= max_dist:
        if self.debug:
          print "!!! Added to cand dist"
        cand_dict.setdefault(dist, [])
        cand_dict[dist].append(corr_word)
    return cand_dict
    
  def get_best_matches(self, bad_chem, max_dist):
    if self.debug:
      print "Get best matches for: ", bad_chem
    esc_bad_chem = self.escape(bad_chem.upper())
    esc_bad_chem = esc_bad_chem.rstrip('\\')
    esc_bad_chem = esc_bad_chem.strip('"')
    # Anything of length less than 5 is usually an acronym, and impossible to correct
    if len(esc_bad_chem)<=4:
      return []
    cand_dict=self.run_dl(esc_bad_chem, max_dist)
    print esc_bad_chem + ": " + repr(cand_dict) + "\n"
    key_list = cand_dict.keys()
    key_list.sort()
    # Return the closest set of matches
    for dist in key_list:
      if len(cand_dict[dist])>0:
        return cand_dict[dist]
    return []  
    
  # This corrects the 'bad_chem' - only returning a match if it is the 
  # only closest possible match. Designed for when there is no human
  # to 'choose' the correct one.
  def correct(self, bad_chem):
    debug_str = ''
    if self.debug:
      print "Correcting: ", bad_chem, " max_dist=", repr(self.max_dist)
    esc_bad_chem = self.escape(bad_chem)
    esc_bad_chem = esc_bad_chem.rstrip('\\')
    esc_bad_chem = esc_bad_chem.strip('"')
    # Anything of length less than 5 is usually an acronym, and impossible to correct
    if len(esc_bad_chem)<=4:
      return None, debug_str
    cand_dict=self.run_dl(esc_bad_chem, self.max_dist)
    debug_str += esc_bad_chem + ": " + repr(cand_dict) + "\n"
    key_list = cand_dict.keys()
    key_list.sort()
    # Only return a match if it the only one that is closest to the 'bad_chem'
    for dist in key_list:
      cand_list_len = len(cand_dict[dist])
      if cand_list_len==1:
        return cand_dict[dist][0], debug_str
      if cand_list_len>1:
        break
    return None, debug_str
    

  #def test_has_swap(self):
  #  print has_swap('about','abuot')
  #  print has_swap('about','about')
  #  print has_swap('about','abouti')
  #  print has_swap('about','baout')
  #  print has_swap('about','abotu')

  def get_wordstr_from_file(self, filename):
    ret_str = '\n'
    fp=open(filename, "rb")
    for row in fp.readlines():
      ret_str += row.replace('\n','').replace('\r','').strip(' "')+'\n'
    fp.close()
    return ret_str

  def get_wordlist_from_file(self, filename):
    ret_list = []
    fp=open(filename, "rb")
    for row in fp.readlines():
      ret_list.append(row.strip('\n\r "'))
    fp.close()
    return ret_list
    
#--------------------------------------------------------------------------------------------

def get_big_alias_file(alias_file):
  alia_dict = {}
  reader = csv.reader(open(alias_file, "rb"))
  for row in reader:
    alia_dict[row[0]] = row[1]
  return alia_dict
      
def make_alias_srch_file(chem_dict, alias_srch_file="alias_srch.txt"):
  fp = file(alias_srch_file, 'w')
  for chem in chem_dict.keys():
    fp.write(chem.strip( )+"\n")
  fp.close()
  return alias_srch_file


  
def make_file_from_chemlist(chem_list, bad_chem_file='bad_chems_new.txt'):
  fp = file(bad_chem_file, 'w')
  for chem in chem_list:
    fp.write(chem+"\n")
  fp.close()
  return bad_chem_file
 
def make_new_alias_file(alias_list, alias_dict):
  fp = file("new_alia.csv", 'a+b')
  writer = csv.writer(fp)
  for temp_name, alias in alias_list:
    writer.writerow([alias, alias_dict[temp_name]])
  fp.close()


    
    
if __name__== "__main__":
    cc = CrystalCorrecter("test_correct_words.txt", max_dist=5)
    bad_chem_list=cc.get_wordlist_from_file('test_bad_words.txt')
    NUM_CORRECTED=0
    NUM_TOTAL=0
    NUM_IMPOSSIBLE=0
    for bad_chem in bad_chem_list:
      correct_chem, debug_str=cc.correct(bad_chem)
      if bad_chem != correct_chem and correct_chem!=None:
        print debug_str
        print "{0} -> {1}".format(bad_chem, correct_chem)
        if correct_chem==None:
          NUM_IMPOSSIBLE+=1
        else:
          NUM_CORRECTED+=1
        NUM_TOTAL+=1
    print "NUM_TOTAL=", repr(NUM_TOTAL)
    print "CORRECTION_RATE=", repr(float(NUM_CORRECTED)/float(NUM_TOTAL))
    print "NUM_CORRECTED=", repr(NUM_CORRECTED)
    print "NUM_IMPOSSIBLE=", repr(NUM_IMPOSSIBLE)
