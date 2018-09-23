#
# Copyright (C) 2008-2014 CSIRO Australia
#

from CrystalParser_base import CRYSTAL_PARSER_BASE
from CrystalParser_names import MPD_REGEXP_LIST
#
# At the moment looks for cryo conditions in 'line'
# but could be generalised at a later date to look for other things
#

class CRYSTAL_PARSER_USECLASSIFIER(CRYSTAL_PARSER_BASE):
  def __init__(self, verbose, failed_debug):
    # NB: Do not need correcter obj or chem classes, since we are only using 're_search()'
    # 'verbose' and 'failed_debug' are set in the base class 
    CRYSTAL_PARSER_BASE.__init__(self, verbose, failed_debug, use_chem_classes=False, correcter_obj=None)
    
  # Input: line = line to be classified
  # Returns: match_obj, 'cryoprotect'
  # or None, None if no cryo conditions found
  def classify(self, line):
    if self.verbose>0:
      print "classify(line=",repr(line),")"
    line=line.replace("\n"," ")  
    CRYO_CHEM=r'\s*('
    for mpd_regexp in MPD_REGEXP_LIST:
      CRYO_CHEM+=mpd_regexp+'|'
    CRYO_CHEM+='SODIUM FORMATE|MPD|GLYCEROL|PEG\s*\d+00|ETHYLENE\s*GLYCOL)\s*'
    CRYO_UNITS=r'\s*[0-9.]+\s*('+self.UNITS_REGEXP+r')\s*'
    CRYO_REGEXP_LIST=[
     CRYO_UNITS+CRYO_CHEM+r'\s*WAS.*FOR\s+CRYOPROTECTION.*',
     r',\s+'+CRYO_UNITS+CRYO_CHEM+r' CRYO-PROTECTANT', 
     r'\.\s*[A-Z].*WAS\s*USED\s*FOR\s*CRYOPROTECTION\s*\.',
     CRYO_UNITS+CRYO_CHEM+r'\s*(WERE)?\s+USED\s*AS\s*CRYOPROTECTANT',
     r'CRYOPROTECTION\s+CONDITIONS:'+CRYO_UNITS+CRYO_CHEM,
     CRYO_UNITS+CRYO_CHEM+r'(WAS USED)?\s*(AS)?\s*A?\s*CRYOPRO?T?ECTING\s*AGENT',
     CRYO_UNITS+CRYO_CHEM+r'WAS\s*THEN\s*ADDED\s*AS\s*CRYO',
     CRYO_UNITS+CRYO_CHEM+r'(ADDED)?\s*AS\s*(THE|A)?\s*CRYO\-? ?PRO?T?ECTANT',
     r'CRYO\s?PROTECTION WAS'+CRYO_UNITS+CRYO_CHEM,
     r'CRYOCOOLED\s*(WITH|IN|USING)'+CRYO_UNITS+CRYO_CHEM,
     CRYO_UNITS+CRYO_CHEM+r'(ADDED|USED)\s*FOR CRYOPROTECTION',
     CRYO_UNITS+CRYO_CHEM+r'\s+FOR\s*CRYOPROECTION',
     r'CONCENTRATION OF'+CRYO_CHEM+'WAS\s*INCREASED\s*TO\s*\d+\% FOR\s*CRYOPROTECTION',
     r'FOR\s*CRYOPROTECTION\s*THE\s*CONCENTRATION\s*OF '+CRYO_CHEM+' WAS\s*ADJUSTED\s*TO '+CRYO_UNITS,
     r'(CRYO)?PROTECTED\s*(IN|WITH)\s*(UNBUFFERED)?'+CRYO_UNITS+CRYO_CHEM,
     r'CRYOSOLUTION:.*$',
     r'CRYO\s*SOLUTION\s*CONTAINING.*$',
     r'CRYO-BUFFER\s*CONTAINING.*$', 
     r'CRYO-(CONDITION|BUFFER)\s*:.*$',
     r'CRYO\s*PROTECTANT:.*$',
     r'WITH\s*A\s*CRYOPROTECTANT OF\s+.*$',
     r'A\s*CRYOGENIC\s*SOLUTION\s*CONTAINING.*$',
     r'SOAKED\s*IN .* FOR\s*\d+\s*HOURS\s*BEFORE\s*BEING\s*FLASH\s*FROZEN',
     r'FLASH\s*\-?\s*FROZEN\s*WITH A\s*CRYOPROTECTANT OF\s+.*$',
     r'FLASH\s*COOLED\s*IN\s*\d.*$',
     r'THE\s*CRYSTALS\s*WERE\s*CRYO-PROTECTED\s*IN\s+.*$',
     r'THE*\sCRYSTAL\s*WAS\s*CRYOCOOLED\s*WITH.*$',
     r'CRYOPROTECTANT\s*SOLUTION:.*$',
     r'THE\s*CRYSTAL\s*WAS\s*CRYOPROTECTED\s*IN\s*THE\s*RESERVOIR\s*SOLUTION\s*SUPPLEMENTED\s*BY'+CRYO_UNITS+CRYO_CHEM,
     r'CRYO-PROTECTANT SOLUTION OF.*$',
     CRYO_UNITS+CRYO_CHEM+r'(WAS\s*THEN\s*ADDED)?\s*AS\s*CRYO',
     CRYO_UNITS+CRYO_CHEM+r'(ADDED)?\s*AS\s*(THE|A)?\s*CRYO\-? ?PRO?T?ECTANT',
     r'CRYO\s?PROTECTION WAS.*$',
     r'\.?[0-9]+\s*\%\s*(GLYCEROL|PEG\s*[0-9]*)\s*WAS.*FOR\s+CRYOPROTECTION.*',
     r'[0-9]+\s*\%\s*\(V/V\)\s*GLYCEROL\s*(WERE)?\s+USED\s*AS\s*CRYOPROTECTANT',
     r'CRYOPROTECTION\s+CONDITIONS:?.*$',
     r'FOR\s*CRYOPROTECTION\s*[^\.].*$',
     r'\.\s*CRYOPROTECTANT\s+.*$',
     r'CRYO-SOLUTION\s*CONTAINING\s+.*$',
     CRYO_UNITS+CRYO_CHEM+r'(WAS\s*USED)?\s*(AS)?\s*A?\s*CRYOPRO?T?ECTING\s*AGENT',
     r'CRYOPROTECTANT \(MOTHER\s*LIQUOR\s*WITH.*$',
     r'AND.*(ADDED)?\s*AS\s*CRYO\-?(PROTECTANT)?',
     r'; CRYO(PROTECTANT)?\s*\-?\s+.*$',
     r',\s+[^,]*\s+CRYO-PROTECTANT',
     r',\s+CRYOPROTECTANT'+CRYO_UNITS+CRYO_CHEM,
     r'AND\s+CRYOPROTECTANT'+CRYO_UNITS+CRYO_CHEM,
     r'FLASH\s*FROZEN\s*IN.*$',
     r'CRYSTALS\s*WERE\s*THEN\s*TRANSFERR?ED TO .* BEFORE\s*FLASH\s*COOLING',
     r'FLASH\s*FROZEN\s*WITH\s*A\s*CRYOPROTECTANT\s*OF.*$',
     r'SOAKED\s*IN\s*RESERVOIR\s*SOLUTION\s*SUPPLEMENTED\s*WITH.*PRIOR\s*TO\s*CRYOCOOLING',
     r'FLASH\s*FROZEN\s*BY\s*TRANSFERR?ING\s*INTO.*$',
    ]
    for regexp in CRYO_REGEXP_LIST:
      cryo_match=self.re_search(line, regexp)
      if cryo_match!=None and self.verbose>9:
        print "match=", repr(cryo_match)
        print "self.re_search: line=", repr(line) 
        print '   regexp=', repr(regexp)
      if cryo_match!=None:
        return cryo_match, 'cryoprotect'
    return None, None
    
