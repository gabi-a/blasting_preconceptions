#!/bin/env python

#
# Copyright (C) 2008-2014 CSIRO Australia
#
import re,string


from CrystalParser_names import CRYSTAL_PARSER_NAMES
from CrystalParser_UseClassifier import CRYSTAL_PARSER_USECLASSIFIER
from CrystalParser_alia import non_chem_list

bad_word_list=['-SET-UP', '24-PLATES', 'A', 'ABOUT', 'ABOVE', 'ABSENCE', 'ACTIVATOR',
'ADDUCT', 'AEROBIC', 'AEROBICALLY', 'AGAINST', 'ALSO', 'AMOUNT',
'AMOUNTS', 'AN', 'ANALOG', 'AND', 'ANOTHER', 'ANTIPAIN',
'APPEAR', 'APPEARED', 'AQUEOUS', 'ARGON', 'ASSEMBLED', 'ATOM',
'ATTACHED', 'AURORA', 'BACK-EXTRACTION', 'BASED', 'BECAME', 'BEEN',
'BEST', 'BETWEEN', 'BIFFFER', 'BIND', 'BOUND', 'BUBBLED',
'BUFFFER', 'BUFFRE', 'BUT', 'CAN', 'CAPILLARY', 'CAPPILARY',
'CARRIED', 'CARTESIAN', 'CATALYTIC', 'CATIONS', 'CATIOS', 'CENTRE',
'CENTRFUGATE', 'CENTRIFUGAL', 'CENTRIFUGATE', 'CHAMBER', 'CHELATING', 'CHILL',
'CHIP', 'CLEAR', 'CLUSTER', 'CO-BOUND', 'CO-COMPLEX', 'COAT',
'COCRYSTALLISATION', 'COCRYSTALLIZATION', 'COFACTOR', 'COMPLEMENTARY', 'COMPLEMENTED', 'COMPLETE',
'COMPLETELY', 'COMPLEX', 'COMPLEXED', 'COMPLEXES', 'COMPONENTS', 'COMPOSED',
'COMPOSITION', 'COMPRISING', 'CONCENTRATED', 'CONCENTRATION', 'CONJUGATE', 'CONSISTS',
'CONSTANT', 'CONSULTED', 'CONTACT', 'CONTAING', 'CONTAINS', 'CONTROL',
'CORE', 'COVER', 'CORRESPONDING', 'COVALENTLY', 'COVERED', 'COVERSLIPS', 'CREATE',
'CRO-PROTECTANT', 'CRUSHED', 'CRYO', 'CRYOBUFFER', 'CRYOCOOLING', 'CRYOPROTECTANT',
'CRYOPROTECTING', 'CUBIC', 'CYLINDER', 'CYOPROTECTANT', 'DATA', 'DAY',
'DDIDITIVE', 'DECAHYDRATE', 'DEHYDRATE', 'DEHYDRATION', 'DEIONIZED', 'DELIVERED', 'DERIVATIVE', 'DERIVATIZED',
'DESCRIBED', 'DESIGNED', 'DEVICES', 'DIFFRACTION', 'DIHYDRATE', 'DILUTION', 'DIRECT', 'DIRECTLY',
'DISHES', 'DISCUSSION', 'DISOLVED', 'DISSOLVE', 'DISTINCT', 'DIVALENT', 'DOES',
'DOMAIN', 'DOUBLE', 'DRAMATICALLY', 'DRUG', 'DUE', 'DUNKING',
'EIGHT', 'ELONGATED', 'ENRICHED', 'ENVIRONMENT', 'EQILIBRATED', 'EQUILBRIATED',
'EQUIMOLAR', 'EQUIVALENT', 'EQULIBRATED', 'EUQAL', 'EXCEPTION', 'EXCHANGE', 'EXCHANGED',
'EXPRESSED', 'EXPRESSION', 'EXTRACT', 'FACT', 'FACTOR', 'FIFTH',
'FILL', 'FILLED', 'FILLING', 'FILTER', 'FILTERED', 'FLUSHED',
'FOCUS', 'FOLLOWING', 'FORMED', 'FRACTIONS', 'FRAGMENT', 'FREE',
'FURTHER', 'FUSION', 'GEL-TUBE', 'GENERALLY', 'GIVE', 'GLASS',
'GLYCOLSYLATED', 'GRADE', 'GREW', 'GRID', 'GROW', 'GROWTH',
'HAD', 'HALF', 'HANGIGN', 'HANGMAN', 'HARVESTED', 'HARVESTING',
'HAS', 'HAVE', 'HEPTAHYDRATE', 'HEXAHYDRATE', 'HIGHER', 'HOURS', 'HUMAN', r'I\.E\.',
'IE', 'IML-I', 'IMMEDIATELY', 'IMMERSION', 'IMPORTANT', 'IMPROVED',
'INCLUBATE', 'INCLUDED', 'INCLUDES', 'INCREASE', 'INCREASED', 'INCREASING',
'INCREMENTS', 'INCUBATE', 'INCUBATION', 'INSTEAD', 'INTEREST', 'INTERFACE',
'INTRODUCED', 'KEPT', 'LABELED', 'LACKING', 'LARGE', 'LARGEST',
'LASER-INDUCED', 'LATTER', 'LAYERED', 'LEAST', 'LEFT', 'LENS',
'LET', 'LINEAR', 'LINKAGE', 'LIPIDIC', 'LISING', 'LIZING',
'LONGER', 'LOOP', 'LOOPS', 'LOW', 'LOWERING', 'MAGIC',
'MAKE', 'MANY', 'MEDIA', 'MEMBANE', 'MEMBRANE', 'MICOBATCH',
'MICRO', 'MICROCRYSTALS', 'MICROFLUIDIC', 'MICROSOMES', 'MINUTES', 'MOLARITY',
'MOLECULE', 'MONOHYDRATE', r'MONTHS?', 'MORE', 'MORPHEUS', 'MORPHOLOGIES',
'MOST', 'MOTHER', 'MOUNTING', 'MOVE', 'MUCH', 'MULTIPLE',
'MUTANT', 'N-LOBE', 'NEAT', 'NON-BIREFRINGENT', 'NON-CHELATING', 'NUCLEATION',
'NUMBER', 'OBTAIN', 'OCCURRED', 'OCTAHYDRATE', 'OCTAMER', 'OIL', 'ONE',
'OPTIC', 'OPTIMUM', 'ORIGINAL', 'OUT', 'OVERLAYED', 'OXIDISED',
'OXIDIZED', 'PAPER', 'PART', 'PARTICLE', 'PARTICULAR', 'PARTS',
'PASSED', 'PERFORM', 'PENTAHYDRATE', 'PERFORMED', 'PHASE', 'PHASING', 'PLACED',
r'PLATES?', 'PLEASE', 'POINT', 'POWDER', 'PRECEPITANT',
'PRECIPITATORS', 'PRECIPTANT', 'PREINCUBATED', 'PRESENCE', 'PRIMARY', 'PRIOR',
'PRIORLY', 'PRODUCE', 'PRODUCED', 'PRODUCT', 'PROTECTANT', 'PROTECTING',
'PROTECTION', 'PUFFER', 'PURIFICATION', 'PURIFIED', 'PURPLE', 'QUALITY',
'QUICK', 'RACEMIC', 'RANGE', 'RATHER', 'REACH', 'REACTION', 'REACTOR',
'RECOMBINANT', 'REDLIGHT', 'REDUCED', 'REDUCTION', 'REDUCTANT', 'REDUCTIVELY', 'REERVOIR',
'REFINEMENT', 'REFOLDED', 'REMOVE', 'REMOVED', 'REPLACED', 'REQUIRED',
'RESERVE', 'RESERVIOR', 'RESERVOUR', 'RESEVIOR', 'RESEVOIR', 'RESIDUES',
'RESULTS', 'RINSED', 'ROD-LIKE', r'RODS?', 'ROUTINELY', 'SANDWICH',
'SANDWITCH', 'SCALED', 'SCINTILLATION', 'SEALED', 'SECONDS', r'SEEDS?',
'SEED-DNA', 'SEGMENT', 'SEPARATION', 'SERIALL?Y?', 'SET',
'SETTING-UP', 'SHORT', 'SHOW', 'SIGMA', 'SILICONIZED', 'SIMILAR',
'SINGLE', 'SITING', 'SIZE', 'SLIGHT', 'SLIDES', 'SLIP', 'SOAKING',
'SOCKING', 'SOLUBILITY', 'SOLUBILIZED', 'SOURCE', 'SPACE', 'SPHERICAL',
'SPONGE', 'SPONTANEOUS', 'SQUARE-LIKE', 'STABILISING', 'STABILIZATION', 'STABILIZING',
'STATE', r'STEPS?', 'STEPWISE', 'STOICHIOMETRIC', 'STORAGE',
'STRUCTURE', 'STUDIES', 'SUBMITTED', 'SUBSEQUENT', 'SUCH', 'SUITE',
'SUPERNATANT', 'SUPERSATURATION', 'SUSPENDED', 'SUSPENSION', 'SYNTHETIC', 'SYSTEM',
'TAG', 'TARGET', 'TERMINAL', 'TETRAHYDRATE', 'THAN', 'THAT',  'THEIR', 'THEM',
'THIN', 'THREE', 'THREE-FOLD', 'THREEFOLD', 'THROUGH', 'TILANDER',
r'TIMES?', 'TISSUE', 'TRACE', 'TRACKING', 'TRAPPED',
'TREATED', 'TRIALS', 'TRIANGLE', 'TRIANGULAR', 'TRIHYDRATE', 'TROUT', 'TUBE',
'TWO', 'TWOFOLD', 'TYPE', 'TYPICALLY', 'ULTRAFREE', 'UNDER',
'UNDERWENT', 'UNEXPECTEDLY', 'UNIFORMLY', 'UNTIL', 'UP', 'USUALLY', 'VALUES',
'VARIED', 'VARYING', 'VERIFY', 'VESICLES', 'VISCOUS', 'VITRIFICATION',
'WARD', 'WASHED', 'WEIGHT', 'WHERE', 'WISE', 'WILD', 'WILD-TYPE',
'XTAL', r'YIELDS?', 'YIELDED', 'HYDRATE' ]



class CRYSTAL_PARSER(CRYSTAL_PARSER_NAMES):
  def __init__(self, verbose, failed_debug, sort_by_freq, use_chem_classes, correcter_obj):
    CRYSTAL_PARSER_NAMES.__init__(self, verbose, failed_debug, use_chem_classes, correcter_obj)
    self.got_xtal_cond=True
    self.xtal_cond=""
    self.CHEMICALS = [] # Name as corrected and found in PDB then standardised
    self.RAW_CHEMICALS = [] # Name as corrected and found in PDB
    self.CONCENTRATIONS = []
    self.CONCENTRATION_UPPER_LIMITS = []
    self.UOMS=[]
    self.TEMPERATURE=0
    self.pH=[]
    self.pH_UPPER=[]

    self.CODE_PASS=0
    self.CODE_BLANK=0
    self.CODE_FAIL=0
    self.CODE_FAIL_LIST=[]
    self.CONDS={}
    self.CHEM_HISTO={}
    self.RCHEM_HISTO={}
    self.RCHEM_CODES={}
    self.CHEM_TOTAL=0
    self.CHEM_NON_CHEM=0
    self.CHEM_PASS=0
    self.CHEM_FAIL=0
    self.CHEM_UNKNOWN=0
    self.CHEM_UNKNOWN_DICT = {}

    # When parsing, some parts of the line can be parsed, some parts cannot
    # This tries to estimate which pdb entries could be parsed fully and which
    # could be parsed partially
    self.TOTAL_PARTS = {}
    self.TOTAL_FAILED_PARTS = {}
    
    # IF we are told the final ph it is put in here, key is pdb id
    self.final_ph = {}

    # Global variables
    self.sort_by_freq=sort_by_freq

  def parse_conditions(self,pdb):
    
    if not self.got_xtal_cond:
      print "Not got cond"
      return False, False

    line=self.xtal_cond
    pdb=string.lower(pdb)

    pH=''
    comps = []
    CONC=[]
    comp_cnt = 0
    index = 0
    self.CHEMICALS = []
    CHEMICALS = []
    self.RAW_CHEMICALS = []
    self.CONCENTRATIONS = []
    self.CONCENTRATION_UPPER_LIMITS = []
    self.UOMS=[]
    self.TEMPERATURE=0
    self.pH=[]
    PH = []
    self.pH_UPPER=[]
    PH_UPPER = []

    # These are used to tally which parts could be parsed fully and which
    # could be parsed partially
    self.NUM_PARTS=0
    self.NUM_FAILED_PARTS=0

    if (self.verbose > 1):
      print 'Parsing> ' + repr(line)
              
    line = self.re_substitute(line, r'\<', '')
    line = self.re_substitute(line, r'\>', '')
    line = self.re_substitute(line, r'\|', '')


# fixing up general items, standardizing...
    line = self.re_substitute(line, r'MILLI\s*MOLAR', r'MM')
    line = self.re_substitute(line, r'MMOLAR', r'MM')
    line = self.re_substitute(line, r'MMOL\/L', r'MM')
    line = self.re_substitute(line, r'MICRO\s*MOLAR', r'UM')
    line = self.re_substitute(line, r'\(MICRO\)\s*L', r'UL')
    line = self.re_substitute(line, r'\bMICROM\b', r'UM')
    line = self.re_substitute(line, r'\bMICROMOLES\s*(PER|/)\s*LITER', r'UM')
    line = self.re_substitute(line, r'\bMIROMOLAR\b', r'UM')
    line = self.re_substitute(line, r'AT A MOLAR RATIO OF 1:\d+','')
    line = self.re_substitute(line, r'\bMOLAR\s+(?!RATIO)', r'M ')
    line = self.re_substitute(line, r'MOL\/L', r'M')
    # FIXME: Multiply #drops x size?
    line = self.re_substitute(line, r'\d\+(\d+)\s+(MI[CK]ROLITR?ER?|UL)\s+DROPS', r'\1 UL')
    line = self.re_substitute(line, r'(\d+\.?\d*)\s*(MI[CK]R?O\s*LITR?ER?S?|MULS?)', r'\1 UL')
    line = self.re_substitute(line, r'(\d+\.?\d*)\s*MI[CK]RO\s*LITR?ER?S?', r'\1 UL')
    line = self.re_substitute(line, r'(\d+\.?\d*)\s*MICRO\-?L\b', r'\1 UL')
    line = self.re_substitute(line, r'MILLI\s*LITR?ER?S?', r'ML')
    line = self.re_substitute(line, r'MICOLITER', r'UL')
    line = self.re_substitute(line, r'\%PEG', r'% PEG')
    line = self.re_substitute(line, r'\%MPD', r'% MPD')
    line = self.re_substitute(line, r'O\.(\d+)\s*M', r'0.\1 M')
    line = self.re_substitute(line, r'\bENZYME', r'PROTEIN')
    
    # Remove waters of hydration
    line = self.re_substitute(line, r'\*?\d\(H2O\)', '')
    line = self.re_substitute(line, r'\.\s*\d+\s*H2O', '')
    line = self.re_substitute(line, r'\*?\-?[2-9]?H2[O0]\b', '')
    line = self.re_substitute(line, r'\(OH2\)\d', '')
    # standardize ranges
    line = self.re_substitute(line, r'(\.\.\.)', r'-')
    line = self.re_substitute(line, r'([0-9.]+)\s*[-~]\s*([0-9.]+)\s*', r'\1-\2 ')
    line = self.re_substitute(line, r'([0-9]+)\s*\%\s+TO\s+([0-9]+)\s*\%\s*', r'\1%-\2% ')
    line = self.re_substitute(line, r'\(?([0-9.]+)\s*%?\s*\-([0-9.]+)\s*%\)?', r'\1%-\2%')
    line = self.re_substitute(line, r'([0-9.]+)\s+TO\s+([0-9.]+)\s*', r'\1-\2 ')
    line = self.re_substitute(line, r'BETWEEN\s+([0-9.]+)\s+AND\s+([0-9.]+)\s*', r'\1-\2 ')
    line = self.re_substitute(line, r'([A-Z]),([0-9\.]+%)', r'\1 \2 ')
    line = self.re_substitute(line, r'\s+', r' ')

    if self.verbose>1:
      print "parse:1", line
    line = self.re_substitute(line, r'T=', r'AT ') # fix temperature lines
    line = self.re_substitute(line, r'[@]', r'AT ') # fix temperature/pH lines
    line = self.re_substitute(line, r'=', '') #ignore =
    line = self.re_substitute(line, r'WT/V', r'W/V')
    line = self.re_substitute(line, r'\(M/V\)', r'W/V')
    line = self.re_substitute(line, r'W\.V', r'W/V')
    line = self.re_substitute(line, r'WT\./VOL\.', r'W/V')
    line = self.re_substitute(line, r'WEIGHT\s*/\s*VOLUME', r'W/V')
    line = self.re_substitute(line, r'W/V\s*\(\%\)', r'% W/V')
    line = self.re_substitute(line, r'\(W/V\)\%', r'W/V')
    line = self.re_substitute(line, r'W/\s*V\s*\%', r'% W/V')
    line = self.re_substitute(line, r'\(W/\s*V\)\s*\%', r'% W/V')
    
    line = self.re_substitute(line, r'\%\s*W/\s*V', r'% W/V')
    line = self.re_substitute(line, r'\%\s*\(W/\s*V\)', r'% W/V')
    
    line = self.re_substitute(line, r'\%V/\s*V', r'% V/V')
    line = self.re_substitute(line, r'\%\(V/\s*V\)', r'% V/V')
    
    line = self.re_substitute(line, r'\%W/\s*W', r'% W/W')
    line = self.re_substitute(line, r'\%\(W/\s*W\)', r'% W/W')
    
    line = self.re_substitute(line, r'W/VOL', r'W/V')
    line = self.re_substitute(line, r'\(BY WEIGHT\)', r'W/V')
    line = self.re_substitute(line, r'\(W:W\)', r'W/W')
    line = self.re_substitute(line, r'\(W:V\)', r'W/V')
    line = self.re_substitute(line, r'\(W\s*TO\s*V\)', r'W/V')
    line = self.re_substitute(line, r'\(V[:,]V\)', r'V/V')
    line = self.re_substitute(line, r'VOL\s*/\s*VOL', r'V/V')
    line = self.re_substitute(line, r'ML/ML', r'V/V')
    line = self.re_substitute(line, r'\%V\s+', r'% V/V ')
    line = self.re_substitute(line, r'\(BY VOLUME\)', r'V/V')
    line = self.re_substitute(line, r'\(BY VOL\.\)', r'V/V')
    line = self.re_substitute(line, r'(AVERAGE )?MOLECULAR WEIGHT', '')
    line = self.re_substitute(line, r'RATIO PROTEIN:DNA', '')

    line = self.re_substitute(line, r'(\S+)\s+WAS\s+CONCENTRATED\s+TO\s+([-0-9.]+\s*[%UMGL/]+)', r'\2 \1')
    line = self.re_substitute(line, r';', r',')
    line = self.re_substitute(line, r'PERCENT', r'%')
    line = self.re_substitute(line, r'\bDEGRESS?\b', r'DEGREES')
    line = self.re_substitute(line, r'\bAT\s+PH', r'PH')
    line = self.re_substitute(line, r'([0-9.][MUGL%/]*) TO ([0-9.])', r'\1-\2')
    line = self.re_substitute(line, r'PH:', r'PH ')
    line = self.re_substitute(line, r'PH\s+RANGE', r'PH ')
    line = self.re_substitute(line, r'UP TO', '')
    line = self.re_substitute(line, r'PHOSPHATE\s+BUFFERED\s+SALINE', r'PBS')
    line = self.re_substitute(line, r'\bAMM?\.\s+(SULPH\.|SULF\.|SULPHATE|SULFATE?)', r'AMMONIUM SULFATE')
    line = self.re_substitute(line, r'\bTRIS\.\s*H?CL', r'TRIS CHLORIDE')
    line = self.re_substitute(line, r'\bAS BUFFER\b', '')
    line = self.re_substitute(line, r'LUCIFERASE', r'PROTEIN')
    line = self.re_substitute(line, r'CENTRIFUGED AT \d+\s*G FOR \d+\s*(MN|MINUTES)', '')
    line = self.re_substitute(line, r'\s+', r' ')
    # Do this here because the '(15/ 4' etc. is mistaken for number+units by the parser
    line = self.re_substitute(line, r'\(15/\s+4\s+EO/OH\)', r'(15/4 EO/OH)')
    line = self.re_substitute(line, r'\(5/\s+4\s+PO/OH\)', r'(5/4 PO/OH)')

    if self.verbose>1:
      print "parse:2", line
    
    if self.phdebug>0:
      print "pH:1", line
    
    # Final pH
    if self.re_match_groups(line, 'FINAL\s+(MEASURED)?\s+PH\s*(IS|WAS|=)?\s*(\d+\.?\d+?)'):    
      try:
        self.final_ph[pdb] = float(self.matchgroups[3])
        if self.phdebug>0:
          print "Final ph is:", self.final_ph[pdb]
      except ValueError, TypeError:
        pass
      else:
        line = self.re_substitute(line,'FINAL\s+(MEASURED)?\s+PH\s*(IS|WAS|=)?\s*\d+\.?\d+?', '')
        
    elif self.re_match_groups(line, 'PH\s*\d+\.?\d*\s*,?\s+PH\s*(\d+\.?\d*)\s*\-\s*(\d+\.?\d*)'):
      try:
        print self.matchgroups[2]
        self.final_ph[pdb] = float(self.matchgroups[2])
        if self.phdebug>0:
          print "Final ph is:", self.final_ph[pdb]
      except ValueError, TypeError:
        pass
      else:
        line = self.re_substitute(line,'(PH\s*\d+\.?\d*\s*),?\s+PH\s*\d+\.?\d*\s*\-\s*(\d+\.?\d*)', r'\1')
     
    # If there's a PH by itself, with temperature or something else before it, remove it
    line = self.re_substitute(line, r'TEMPERATURE\s+(\d+[KC]),\s+PH\s*\d+\.\d+', r'TEMPERATURE \1')
    line = self.re_substitute(line, r'VAPOR\s+DIFFUSION\s*,?\s+PH\s*\d+\.\d+,?', '')
    line = self.re_substitute(line, r'(NANODROP|HANGING\s*DROP|MICRO\s*BATCH),\s+PH\s*\d+\.\d+,?\s+', '')
    
    # Remove 'PH N/A' "PH NONE" etc.
    line = self.re_substitute(line, r'\bPH\s+(N/\s*A|NONE)', '')
    line = self.re_substitute(line, r'\bPH\s+NOT\s+APPLICABLE', '')


    
    if self.phdebug>0:
      print "pH:2", line
    # Remove trailing PH if there are two 'PH' strings
    line = self.re_substitute(line, r'\bPH\s+(PH\s*\d+\.?\d*)', r'\1')
    
    # Remove ph range if another follows
    line = self.re_substitute(line, r'\bPH\s+\d+\.\d+\-\d+\.\d+\s*,?\s+(PH\s+\d+\.\d+)', r'\1')
    
    if self.phdebug>0:
      print "pH:3", line
    # Remove a pH if as the same ph value twice, first is in a range,
    # second at end
    if self.re_match_groups(line,r'\bPH\s*(\d+\.\d+)\s*\-\s*(\d+\.\d+).*\s+PH\s*(\d+\.\d+)\s*$'):  
      try:
        ph1=float(self.matchgroups[1])
        ph2=float(self.matchgroups[2])
        ph3=float(self.matchgroups[3])
      except ValueError:
        pass
      else:
        if ph1==ph3 or ph2==ph3 or (ph1+ph2)/2.0==ph3:
          line = self.re_substitute(line, r'PH\s*\d+\.\d+\s*$', '')
          if self.phdebug>0:
            print "pH:4", line

    # Remove a pH when has 3 phs, 3rd one at end
    elif self.re_match_groups(line,r'\bPH\s*(\d+\.\d+).*\s+PH\s*(\d+\.\d+).*\s+PH\s*(\d+\.\d+)\s*$'):
      try:
        ph1=float(self.matchgroups[1])
        ph2=float(self.matchgroups[2])
        ph3=float(self.matchgroups[3])
      except ValueError:
        pass
      else:
        if ph1==ph3 or ph2==ph3:
          line = self.re_substitute(line, r'PH\s*\d+\.\d+\s*$', '')
          if self.phdebug>0:
            print "pH:5", line
          
    # Remove a pH when has the same ph value twice, 2nd one at the end
    elif self.re_match_groups(line,r'\bPH\s*(\d+\.?\d*),?[^\-].*\s+PH\s*(\d+\.\d+)\s*$'):
      try:
        ph1=float(self.matchgroups[1])
        ph2=float(self.matchgroups[2])
      except ValueError:
        pass
      else:
        if ph1==ph2:
          line = self.re_substitute(line, r'PH\s*\d+\.\d+\s*$', '')
          if self.phdebug>0:
            print "pH:6", line
    
    if self.phdebug>0:      
      print "pH:7", line      

    if self.verbose>1:
      print "parse:3", line
      
    #  Temperature specific fixes
    if self.re_search(pdb, r'1aa0|1zxt'):
        line = self.re_substitute(line, r'(AT)?\s*22OC', r'AT 22C')
    if self.re_search(pdb, r'1ab9'):
        line = self.re_substitute(line, r'AT 310K', r'AT 293K')
    if self.re_search(pdb, r'1b4w|1dss'):
        line = self.re_substitute(line, r'ROOM TEMPERATURE OF\s+17DEG(\.|REES)\s*C', r'AT 17C')
    if self.re_search(pdb, r'1bw8'):
        line = self.re_substitute(line, r'16DEGREES', r'AT 16C')
    if self.re_search(pdb, r'1dss|1jia'):
        line = self.re_substitute(line, r'ROOM TEMPERATURE', '')
    if self.re_search(pdb, r'1e[36]w|1e3s'):
        line = self.re_substitute(line, r'18 C$', r'AT 18 C')
    if self.re_search(pdb, r'2ecp'):
        line = self.re_substitute(line, r'18C', r'AT 18C')
    if self.re_search(pdb, r'1f38|1ngw'):
        line = self.re_substitute(line, r'.*', r'AT 25 C') #Fix from author, paper
    if self.re_search(pdb, r'2gm[emp]'):
        line = self.re_substitute(line, r'TEMPERATURE 373K', r'AT 0 C')  # probably not correct, but closer...
    if self.re_search(pdb, r'1ise'):
        line = self.re_substitute(line, r'277K', r'287K')
    if self.re_search(pdb, r'1iuk|1iy[hi]|1kqo|1nwk'):
        line = self.re_substitute(line, r'.*', r'AT 20 C') #Fix from papers- or common sense...
    if self.re_search(pdb, r'1iik'):
        line = self.re_substitute(line, r'TEMPERATURE 298\.0K', '') #double dip...
    if self.re_search(pdb, r'1j07|1n5[mr]|1n6c|1ng[xyz]|1q7y|1q8[126]'):
        line = self.re_substitute(line, r'.*', r'AT 4 C') #Fix from papers- or common sense...
    if self.re_search(pdb, r'1jn4'):
        line = self.re_substitute(line, r'.*AT 189K', r'AT 16 C') #a guess...
    if self.re_search(pdb, r'1ki[2m]'):
        line = self.re_substitute(line, r'AT 25O', r'AT 25 ') #a guess...
    if self.re_search(pdb, r'1kl9|1nfz|1nv5'):
        line = self.re_substitute(line, r'.*', r'AT 22 C') #Fix from papers or author
    if self.re_search(pdb, r'1le9|1ox[0h]|1r3o'):
        line = self.re_substitute(line, r'.*', r'AT 18 C') #Fix from papers
    if self.re_search(pdb, r'1n2v'):
        line = self.re_substitute(line, r'.*395K', r'AT 22 C') #a guess...
    if self.re_search(pdb, r'1oh[cde]'):
        line = self.re_substitute(line, r'20 OC', r'293K')
    if self.re_search(pdb, r'1p2f'):
        line = self.re_substitute(line, r'.*', r'AT 37 C') #Fix from paper
    if self.re_search(pdb, r'1v7t'):
        line = self.re_substitute(line, r'.*', r'AT 40 C') #Fix from paper
    if self.re_search(pdb, r'1l2[ij]'):
        line = self.re_substitute(line, r'292-294', r', AT 293')
        line = self.re_substitute(line, r'294-296', r', AT 295')
    if self.re_search(pdb, r'1lzw'):
        line = self.re_substitute(line, r'TEMPERATURE 100K', r'AT 293K') #Fix from paper...
    if self.re_search(pdb, r'1m2[ov]'):
        line = self.re_substitute(line, r'AT 27[03]K', r'AT 22 C') #Fix from papers or author
    if self.re_search(pdb, r'1mq[23]'):
        line = self.re_substitute(line, r'AT 18 DEGREES \(C\)', '')
    if self.re_search(pdb, r'1n57'):
        line = self.re_substitute(line, r'273K', r'287K') # fix from paper
    if self.re_search(pdb, r'1n9e|1s5[mn]'):
        line = self.re_substitute(line, r'TEMPERATURE\s+398K', r'AT 298K')
    if self.re_search(pdb, r'1nkz'):
        line = self.re_substitute(line, r'TEMPERATURE 16K', r'AT 289K')
    if self.re_search(pdb, r'1nqn|1nyi|1p74|1q7f'):
        line = self.re_substitute(line, r'TEMPERATURE\s+20\.?0?K', r'AT 293K')
    if self.re_search(pdb, r'1ovg|1p9n|1pf3|1s2[dgil]|1s3f|1suz'):
        line = self.re_substitute(line, r'TEMPERATURE\s+22K', r'AT 295K')
    if self.re_search(pdb, r'1pxf'):
        line = self.re_substitute(line, r'TEMPERATURE 17K', r'AT 290K')
    if self.re_search(pdb, r'1pv2'):
        line = self.re_substitute(line, r'TEMPERATURE 22K,', '')
    if self.re_search(pdb, r'1pzd|1ni2'):
        line = self.re_substitute(line, r'TEMPERATURE 18K', r'AT 291K')
    if self.re_search(pdb, r'1q1l'):
        line = self.re_substitute(line, r'TEMPERATURE 100K', r'AT 298K') #fix from author...
    if self.re_search(pdb, r'1r6w'):
        line = self.re_substitute(line, r'\-80 C', r'293K')
    if self.re_search(pdb, r'1r85'):
        line = self.re_substitute(line, r'TEMPERATURE 193K', r'AT 293K')
    if self.re_search(pdb, r'1rj8'):
        line = self.re_substitute(line, r'TEMPERATURE 19K', r'AT 292K')
    if self.re_search(pdb, r'1rts'):
      line = self.re_substitute(line, r'AT 4 OC', r'AT 4C')
    if self.re_search(pdb, r'1sx8'):
        line = self.re_substitute(line, r'TEMPERATURE 100K', r'TEMPERATURE 17C') # Correction from author
    if self.re_search(pdb, r'1tkk'):
        line = self.re_substitute(line, r'STORED AT \-80 C', '')
    if self.re_search(pdb, r'1wa[012]'):
         line = self.re_substitute(line, r'21OC', r'21C')
    if self.re_search(pdb, r'2apg'):
        line = self.re_substitute(line, r'TEMPERATURE\s*100K', r'AT 293K') # presumably the same as the complexes...
    if self.re_search(pdb, r'3fyg'):
      line = self.re_substitute(line, r'40', r'AT 4C') # just a guess
    if self.re_search(pdb, r'[567]msf'):
      line = self.re_substitute(line, r'30(0|O)\s+OR\s+37(0|O)\s*C', r'AT 30C') # just a guess
    if self.re_search(pdb, r'2b6t'):
      line = self.re_substitute(line, r'TEMPERATURE 293, TEMPERATURE 20K', r'AT 293K') 
    if self.re_search(pdb, r'2gv[dz]'):
      line = self.re_substitute(line, r'TEMPERATURE\s+589K', r'AT 289K')  # just a guess
    if self.re_search(pdb, r'3lrq'):
      line = self.re_substitute(line, r'\(\+\-\)\-2\-METHYL\-2,4\-PENTANEDIOL', r'2-METHYL-2,4-PENTANEDIOL')
    if self.re_search(pdb, r'3hvn'):
      line = self.re_substitute(line, r'1,2,3-HEPTANETRIOL ISOMER H', r'1,2,3-HEPTANETRIOL')

    if self.verbose>1:
      print "parse:4", line
      
    #get temperature and  handle ROOM TEMPERATURE, too
    temp = ''
    line = self.re_substitute(line, r'AT ROOM TEMPERATURE\s*\((\d+)\s*K\s*\)', r' AT \1 K')
    line = self.re_substitute(line, r'(\(CELSIUS\)|CELCIUS|CENTIGRADE|\(C\))',r'C')
    line = self.re_substitute(line, r'KELVIN',r'K')
    line = self.re_substitute(line, r'\bDEG(\.|\b|REE\b)', r' DEGREES ')
    line = self.re_substitute(line, r' DEG C[^A-Z]', r' DEGREES C')
    line = self.re_substitute(line, r'(\d+)DEG\.? C(\b|[^A-Z])', r'\1 DEGREES C')
    line = self.re_substitute(line, r'(\d+)DEG\.?C', r'\1 DEGREES C')
    line = self.re_substitute(line, r'(AT)? ROOM\s*-?\s*TEMPERATURE',r' AT 22 C')
    line = self.re_substitute(line, r'(AT)? ROOM\s*-?TEMP\b',r' AT 22 C')
    line = self.re_substitute(line, r' \(?AT\s+RT\)?',r' AT 22 C')
    line = self.re_substitute(line, r'\bRT\.?\b',r'AT 22 C')
    line = self.re_substitute(line, r'(AT|TEMPERATURE)?\s*([-0-9.]+)\s*DEG(\.|REES?)?\s*CELSIUS', r' AT \2 C')
    line = self.re_substitute(line, r'([-0-9.]+)\s*CELSIUS', r' AT \1 C')
    line = self.re_substitute(line, r'\b(AT)?\s*TEMPERATURES?\s*([0-9.]+)\s*KK?\b', r' AT \2 K')
#    line = self.re_substitute(line, r'\b(AT)?\s*TEMPERATURES?\s*([0-9.]+)\.?\s*KK?\b', r' AT \2 K')
    line = self.re_substitute(line, r'\b(AT)?\s*TEMPERATURES?\s*(BETWEEN)?\s*([0-9.]+)-([0-9.]+)', r' AT \4')
    line = self.re_substitute(line, r'\bAT\s*([0-9]+)\.\w+K', r' AT \1 K')
    line = self.re_substitute(line, r'\bTEMP(ERATURE)?(:|S)?', r'AT ')

    if self.verbose>1:
      print "parse:5", line
      
    if self.re_search(line, r'AT\s+[-0-9.O]+\s*[C|K]'):
      if self.debug_temp>0:
        print "temp:1", "line=", line, "temp=", temp
      if self.re_search(line, r'AT\s+([-0-9.O]+\s*[CK])'):
        if self.debug_temp>0:
          print "temp:2", "line=", line, "temp=", temp
        line=self.re_substitute_groups(line, r'AT\s+([-0-9.O]+\s*[CK])', '')
        temp = self.matchgroups[1]
        if self.debug_temp>0:
          print "temp:3", "line=", line, "temp=", temp
    elif self.re_search(line, r'DEGREES'):
      line = self.re_substitute(line, r'CELSIUS', r'C')
      if self.re_search(line, r'AT\s*([-0-9.O]+\s+)DEGREES\s+([CK])'):
        line = self.re_substitute_groups(line, r'AT\s*([-0-9.O]+\s+)DEGREES\s+([CK])', '')
        temp = self.matchgroups[1] + self.matchgroups[2]
        if self.debug_temp>0:
          print "temp:4", "line=", line, "temp=", temp
      elif self.re_search(line, r'AT\s*(\d+\.\d\s+)DEGREES\s+([CK])'):
        line = self.re_substitute_groups(line, r'AT\s*(\d+\.\d\s+)DEGREES\s+([CK])', '')
        temp = self.matchgroups[1] + self.matchgroups[2]
        if self.debug_temp>0:
          print "temp:5", "line=", line, "temp=", temp
      elif self.re_search(line, r'([-0-9.O]+\s+)DEGREES\s+([CK])'):    
        line = self.re_substitute_groups(line, r'([-0-9.O]+\s+)DEGREES\s+([CK])', '')
        temp = self.matchgroups[1] + self.matchgroups[2]
        if self.debug_temp>0:
          print "temp:6", "line=", line, "temp=", temp     
      elif self.re_search(line, r'AT ([-0-9.O]+\s+)DEGREES'):
        line=self.re_substitute_groups(line, r'AT ([-0-9.O]+\s+)DEGREES', '')
        temp = self.matchgroups[1] + 'C'
        if self.debug_temp:
          print "temp:7", "line=", line, "temp=", temp
      elif self.re_search(line, r'([-0-9.O]+\s+)DEGREES'):
        line=self.re_substitute_groups(line, r'([-0-9.O]+\s+)DEGREES', '')
        temp = self.matchgroups[1] + 'C'
        if self.debug_temp>0:
          print "temp:8", "line=", line, "temp=", temp
    elif self.re_search(line, r'\b([0-9.O]+\-[0-9.O]+)\s*C\b'):
      line=self.re_substitute_groups(line, r'\b([0-9.O]+\-[0-9.O]+)\s*C\b', '')
      temp = self.matchgroups[1]
      if self.debug_temp>0:
        print "temp:9", "line=", line, "temp=", temp
    elif self.re_search(line, r'\b\+?([0-9.O]+)\s*C\b'):
      line=self.re_substitute_groups(line, r'\b\+?([0-9.O]+)\s*C\b', '')
      temp = self.matchgroups[1]
      if self.debug_temp>0:
        print "temp:10", "line=", line, "temp=", temp
    elif self.re_search(line, r'(2[0-9][0-9]\-2[0-9][0-9]\s*K\b)'):
      line=self.re_substitute_groups(line, r'(2[0-9][0-9]\-2[0-9][0-9]\s*K\b)', '')
      temp = self.matchgroups[1]
      if self.debug_temp>0:
        print "temp:11", "line=", line, "temp=", temp
    elif self.re_search(line, r'(\s+T\s+2[0-9][0-9]\s*K\.?\b)'):
      line=self.re_substitute_groups(line, r'T\s+(2[0-9][0-9]\s*K\.?\b)', '')
      temp = self.matchgroups[1]
      if self.debug_temp>0:
        print "temp:14", "line=", line, "temp=", temp
    elif self.re_search(line, r'(2[0-9][0-9]\s*K\.?\b)'):
      line=self.re_substitute_groups(line, r'(2[0-9][0-9]\s*K\.?\b)', '')
      temp = self.matchgroups[1]
      if self.debug_temp>0:
        print "temp:12", "line=", line, "temp=", temp
    elif self.re_search(line, r',\s*\+?[0-9][0-9]\s*C(,|\s+|$)'):
      line=self.re_substitute_groups(line, r'([0-9][0-9]\s*C\s*)', '')
      temp = self.matchgroups[1]
      if self.debug_temp>0:
        print "temp:13", "line=", line, "temp=", temp
    # Sometimes a 'O' is used in place of '0'
    temp = self.re_substitute(temp, r'([-0-9.]+)O', r'\g<1>0')
    if self.verbose > 1:
        print "Got temp: ", temp
 
    if temp != "":
      if self.re_search(temp, r'K'):
        temp=self.re_substitute(temp, r'K', '')
        if (self.re_match_groups(temp,r'^([ 0-9.]+)(.*)$')):
          temp=self.matchgroups[1]
          self.TEMPERATURE = self.parser_get_integer(temp)
          if self.TEMPERATURE != None and self.TEMPERATURE > 272:
            self.TEMPERATURE=self.TEMPERATURE - 273
          elif self.TEMPERATURE > 99:
            self.TEMPERATURE = None
      else:
        temp = self.re_substitute(temp, r'C', '')
        if (self.re_match_groups(temp,r'^([ 0-9.]*)(.*)$')):
          temp=self.matchgroups[1]
          self.TEMPERATURE=self.parser_get_integer(temp)

    # Sometimes there are two temperatures. Remove them.
    line = self.re_substitute(line, r'\b[0-9]{1,3}\s*(DEGREES)?\s*C\b', '')
    # Gets PEG3.35K etc.
    #line = self.re_substitute(line, r'[^G]\s*[0-9]{1,3}\s*K', '')

    # FIXME currently unparsable files - note that 2a48 can be fixed, but I need the reference paper...
    # some of these are just not published yet...
    if self.re_search(pdb, r'3ka7|2o1i|3pi[op]|1a78|1a8d|1ae8|1afe|1aq[pu]|1axb|1ay7|1ayn|1b13|1b2j|1b8c|1bdw|1bgg|1bhc|5bir|1c1m|1c4d|1c57|1doj|1dzk|1e4i|1equ|1eu[qy]|1ev[36]|1fm[qs]|1gan|2gar|1g9n|1gx[89]|1h29|1h4l|1h7[pr]|1hka|1hkn|1hn[wxz]|1i5d|1k06|1k08|1kti|1lrv|1n4f|1n73|1nzz|1onk|1p39|1qex|1qml|1qow|1rzk|1s5[tvw]|1uyq|1vhb|1vrh|1ydv|1zb[89]|1ze[ghi]|2a48|2pw[12]|2idl'):
      return False, False
      
    if self.verbose>1:
      print "parse:6", line
      
    #specific error fixes
    # NOT in these pdb records!
    if not self.re_search(pdb, r'1adq'):
      line = self.re_substitute(line, r'DROPS?\s+CONSISTED.*', '')
    if not self.re_search(pdb, r'1aq6|1awf|1bwf|1gl[jl]|1n7[uv]|1psz|1qhr|1qj[167]|[1234]sli|1sll|1ukr'):
      line = self.re_substitute(line, r'MACRO ?SEED(ING|ED).*', '')
    if not self.re_search(pdb, r'1uy[no]'):
      line = self.re_substitute(line, r'^.+\s+CRYSTALLI[ZS]ED\s+(FROM|IN|WITH)', '')
    # IN these specific files
    if self.re_search(pdb, r'1ak9|1aq1|1bj1|1bli|1c4o|1ci4|1us[cf]'):       # this one out of order on purpose...
        line = self.re_substitute(line, r'AGAINST.*', '')
    if self.re_search(pdb, r'1bwf|1gl[jlo]'):       # this one out of order on purpose...
        line = self.re_substitute(line, r'SEEDS.*', '')
    if self.re_search(pdb, r'13pk|1a50|1a5s|1aq1|1b2[01xz]|1b3[589]|1c25|1c5[wxyz]|1cw[rst]|1du[cn]|1e[36]w|1e3s|1e1h|1e7[dl]|4eca|2emd|1eml|1en7|1f1e|1f7t|1gwc|1jcn|1gl2|1i0z|1i10|1m6y|[234]mat|1n2x|1olx|1qoj|1qtn|1sgf|1sqs|1tt4|5upj|1uru|2wsy|1zl[xy]'):
        line = self.re_substitute(line, r'.* WELL\s*(SOLUTIONS?|BUFFER)?(:|-)?', '')
        line = self.re_substitute(line, r'MCDONALD.*', '')
    if self.re_search(pdb, r'12e8|1abs|1acc|2ewe|2aim|1amk|1bzs|2cav|1deq|1duh|1e5k|1ga0|1guu|1gv2|1h0o|1hfk|1hj[jl]|1j7g|1lti|1nkr|1ofc|1q8[yz]|1q97|1rcx|1som|1uru|1us[45]|1v0[stuvwy]|1vif|1w30|1xgs'):
        #if self.re_search(pdb, r'4wbc|12e8|1abs|1acc|2ewe|2aim|1amk|1bzs|2cav|1deq|1duh|1e5k|1ga0|1guu|1gv2|1h0o|1hfk|1hj[jl]|1j7g|1lti|1nkr|1ofc|1q8[yz]|1q97|1rcx|1som|1uru|1us[45]|1v0[stuvwy]|1vif|1w30|1xgs'):
        line = self.re_substitute(line, r'CRYSTALS?\s+.*', '')
    if self.re_search(pdb, r'1914|1a6t|1akz|1al7|3fct|1qhv|1qmo|1up[7abc]'):
      line = self.re_substitute(line, r'WITH .*', '')
    if self.re_search(pdb, r'22[356]l'):
        line = self.re_substitute(line, r'OXIDIZED.*', '')
    if self.re_search(pdb, r'23[012]l|1k3f|1tls|1tsn'):
        line = self.re_substitute(line, r'THIS.*', '')
        line = self.re_substitute(line, r'.* SOLUTION', '')
    if self.re_search(pdb, r'[23]5c8'):
        line = self.re_substitute(line, r'FAB:LIGAND .*', '')
    if self.re_search(pdb, r'46[46]d'):
        line = self.re_substitute(line, r' \% \(V/V\) MPD AGAINST 0.5 ML ', r'-')
    if self.re_search(pdb, r'465d'):
        line = self.re_substitute(line, r'MPD EQUILIBRATED AGAINST 1 ML OF A SOLUTION OF', r'-')
    if self.re_search(pdb, r'46[89]d|47[01]d|1a04|1a71|1ad5|1amu|1at[56]|1bu1|1bw[df]|[456]cox|1cx2|1dze|1etj|2hck|1g6x|1glo|1gyq|1hkc|1nl4|3pgh|1qlq|3rsp|1tkk|1tol|1us[7uv]|1xg[mnos]|2j1n'):
        line = self.re_substitute(line, r'.*(WELLS?|SOLUTION|BUFFER|LIQUOR)\s+CONTAINING', '')
    if self.re_search(pdb, r'1a94|1a8[ko]|1ak4|1aq0|1aum|1b4x|1bg9|1bj[15t]|1bli|1c4o|5cev|1cjc|1cy5|1dbf|1dd6|1dl5|2dub|1dz[4689]|1e26|5eaa|1fn[jk]|1ft2|1fuy|1fvm|1g98|1gk[cd]|1h6e|1ibc|1nub|1o76|1o8[34]|1oko|1pau|1qf8|1qo[pq]|2req|4rsk|1sl[mn]|1tio|1umn|1uoj|1uw5|1uz[pq]'):
        line = self.re_substitute(line, r'.* RESERVO[IU]R?\s+(BUFFER|SOLUTION):?', '')
        line = self.re_substitute(line, r'GEOMETRY.*', '')
    if self.re_search(pdb, r'1a02'):
        line = self.re_substitute(line, r'\(10 MM\)\.', '')
    if self.re_search(pdb, r'1a09|1a1a|1a8i|1aq1|1ckn|1d0[7v]|1dd7|1duh|1e0[vx]|1e1[vx]|1f7[np]|1gz8|1h0[vw]|1hkv|1k9[yz]|1ka[01]|1eoe|1qi2|2hcy|2or[opqrst]|3znb|7taa'):
        line = self.re_substitute(line, r'(THE|THESE)?\s*\(?CRYSTALS?\s+(WERE|WAS)?\s*SOAKED.*', '')
    if self.re_search(pdb, r'1a0a|1aa5|1bl4|[12]mpr|1qbp|1upt|1zme|1zpd'):
        line = self.re_substitute(line, r'RESERVOIR-?.*', '')
        line = self.re_substitute(line, r'VAPOR DIFFUSION METHOD\: DROP-', '')
    if self.re_search(pdb, r'1a0d|1ak4|1dc1|1e3[gk]|1icf|1qqw|1us7|20gs'):
        line = self.re_substitute(line, r'(INITIAL)?\s+DROPS?\s+(WERE|WAS) .*', '')
    if self.re_search(pdb, r'1a0[st]|1dlf'):
        line = self.re_substitute(line, r'THE CONCENTRATION OF.*', '')
    if self.re_search(pdb, r'2qyq'):
        line = self.re_substitute(line, r'COMPLEX FORMED BY SOAKING IN:', '')
    if self.re_search(pdb, r'1a19|1a9u|1qm[hi]'):
        line = self.re_substitute(line, r'PROTEIN CONC.*', '')
    if self.re_search(pdb, r'1a1[5q]|1gqy|1h70|1hht|1hi[01]|4eca|[56]upj'):
        line = self.re_substitute(line, r'.*WE[LE]L\s+SOLUTION\s*(OF)?:?', '')
    if self.re_search(pdb, r'1a3j'):
        line = self.re_substitute(line, r'\(DISSOLVED IN 5% V/V AQUEOUS ACETIC ACID\)', '')
    if self.re_search(pdb, r'5a3h|1b4w|1e3d|1gzx|1oq4|1xk5'):
        line = self.re_substitute(line, r'\bAND .*', '')
    if self.re_search(pdb, r'1a3q|3bc2|1bio|1bkh|1c0m|1c1a|1cit|1fdp|1hfd|1mcz'):
        line = self.re_substitute(line, r'(THE)?\s*DROPS?\s+CONTAINED.*', '')
    if self.re_search(pdb, r'1a2[tu]|1a3[tuv]|5nuc'):
        line = self.re_substitute(line, r'PROTEIN.*', r'2MG/ML PROTEIN, 21% MPD')
    if self.re_search(pdb, r'1a4v'):
        line = self.re_substitute(line, r'CRYSTALLIZATION TRAYS.*', '')
        line = self.re_substitute(line, r'2\.0 M AMM\.', r'2.0M AMMONIUM')
    if self.re_search(pdb, r'1a4x'):
        line = self.re_substitute(line, r'HEXAGONAL SETTING.*', '')
    if self.re_search(pdb, r'1a4y|1bp1|1esj|1iao|1ouw|1s0y'):
        line = self.re_substitute(line, r'0\.(\d+) AMMONIUM', r'0.\1M AMMONIUM')
        line = self.re_substitute(line, r'0\.1 NA', r'0.1M NA')
        line = self.re_substitute(line, r'0\.1 TRIS', r'0.1M TRIS')
        line = self.re_substitute(line, r'(\d) IMIDAZOLE', r'\1M IMIDAZOLE')
    if self.re_search(pdb, r'[23]a3h'):
        line = self.re_substitute(line, r'THIS STRUCTURE WAS.*', '')
    if self.re_search(pdb, r'1a7[29]|1az[pq]|1fy[2e]|1igt|3tat'):
        line = self.re_substitute(line, r'EQUILIBRATED.*', '')
    if self.re_search(pdb, r'1a7x|[23]amv|1b3n|1bke|1e5k|1e8[3-6]|1f0l|1fsg|1h4[cde]|1hj[jl]|1qa[st]|2sk[cde]|1w9x|1wa[012]'):
        line = self.re_substitute(line, r'.*CONSISTING\s+OF', '')
    if self.re_search(pdb, r'1a8d|2bls'):
        line = self.re_substitute(line, r'LARGER?\s+CRYSTALS.*', '')
    if self.re_search(pdb, r'1a8e|1bp5|1fsg|1qk5|1toh'):
        line = self.re_substitute(line, r'CRYSTALS?\s*(WERE|WAS)?\s*GROWN.*', '')
    if self.re_search(pdb, r'1a8u'):
        line = self.re_substitute(line, r'SMALL.*', '')
    if self.re_search(pdb, r'1a9m'):
        line = self.re_substitute(line, r'THE PROTEIN.*', r'10% DIMETHYLSULFOXIDE, 30 MM B-MERCAPTOETHANOL, 4% ISOPROPANOL, 42% AMMONIUM SULFATE, PH 6.8')
    if self.re_search(pdb, r'1a9u|1bl6|1g2w|1l9v|1p38'):
        line = self.re_substitute(line, r'(PROTEIN )?BUFFER.*', '')
    if self.re_search(pdb, r'1aa0'):
        line = self.re_substitute(line, r'AS WELL SOLUTION.*', '')
    if self.re_search(pdb, r'1ab9|1bli|1bt[123]|1bug|1el[xyz]|1vhr|2v0c'):
        line = self.re_substitute(line, r'(DROP WAS)?\s+EQUILI?BRI?ATED\s+AGAINST.*', '')
    if self.re_search(pdb, r'2acy|1e3[xz]|1e4[03]|1fl0|1nuf|1kw[tuvwxyz]|1kx0|1tiw'):
        line = self.re_substitute(line, r'OR 4000', '')
        line = self.re_substitute(line, r'OR 5000', '')
        line = self.re_substitute(line, r'OR 6000', '')
        line = self.re_substitute(line, r'OR 20K', '')
        line = self.re_substitute(line, r'OR 3500', '')
        line = self.re_substitute(line, r'OR PEG 3350', '')
        line = self.re_substitute(line, r'PROTEIN SOLUTION:.* 10MM CACL2,', '')
    if self.re_search(pdb, r'1ad[28]|1ae[237]|1aik|1bf4|1c8c|1e1c|1ejg|1fno|1h3n|1npl|1ob[bh]'):
        line = self.re_substitute(line, r'.*EQUILI?BRI?ATED? AGAINST', '')
    if self.re_search(pdb, r'1aei'):
        line = self.re_substitute(line, r'65 W/V PEG 6000', r'65% W/V PEG 6000')
    if self.re_search(pdb, r'1af4|1aux|1be[68]|1bf[ku]|1e1t|1e2[24]|1ha1'):
        line = self.re_substitute(line, r'THEN.*', '')
    if self.re_search(pdb, r'1ag1'):
        line = self.re_substitute(line, r'2 MOPS BUFFER, PH 7\.0 FOLLOWED.*', r'2M MOPS BUFFER, PH 7.0')
    if self.re_search(pdb, r'1agj'):
        line = self.re_substitute(line, r'PEG.*', r'18% PEG, 1% DMSO')
    if self.re_search(pdb, r'1ah[034]|1eko|1el3|1ocx'):
      line = self.re_substitute(line, r'.*DROP', '')
    if self.re_search(pdb, r'1ah5|1dzb|2fhi|1hk7|1nwo|1o7d|1qou|1vhr|1w75'):
        line = self.re_substitute(line, r'.*WITH', '')
    if self.re_search(pdb, r'1ahw'):
        line = self.re_substitute(line, r'AT AN.*', '')
    if self.re_search(pdb, r'1ai8'):
        line = self.re_substitute(line, r'PEG 8000 0\.05', r'PEG 8000, 0.05M')
    if self.re_search(pdb, r'1ai9|1aoe'):
        line = self.re_substitute(line, r'C\. ALBICANS DHFR', r'PROTEIN')
        line = self.re_substitute(line, r'WAS MIXED .* PART OF', '')
    if self.re_search(pdb, r'1ail'):
        line = self.re_substitute(line, r'MERCURY DERIVATIVE.*', '')
    if self.re_search(pdb, r'1air|1u9a'):
        line = self.re_substitute(line, r'SYMMETRY.*', '')
    if self.re_search(pdb, r'1aj[ko]|1atg|1bv1|1dxj|1h1[234]|3rsd'):
        line = self.re_substitute(line, r'.*EQUAL (VOLUME|AMOUNT) OF', '')
        line = self.re_substitute(line, r'MIXING EQUAL VOLUMES', '')
    if self.re_search(pdb, r'1aj[vx]|1j85'):
        line = self.re_substitute(line, r'.*CRYSTALLIZATION (BUFFER|CONDITIONS?)', '')
    if self.re_search(pdb, r'1ak0'):
        line = self.re_substitute(line, r'PEG 6000 12 \- 20\%', r'12-20% PEG 6000,')
    if self.re_search(pdb, r'1ak1'):
        line = self.re_substitute(line, r'.*CRYSTALS IN:', '')
    if self.re_search(pdb, r'1akd'):
        line = self.re_substitute(line, r'IN THE PRESENCE OF EXCESS.*', '')
    if self.re_search(pdb, r'1al0|1cd3'):
        line = self.re_substitute(line, r'\(OF SATURATION\)', '')
    if self.re_search(pdb, r'1al8'):
        line = self.re_substitute(line, r'JF 5969 IS .*', '')
    if self.re_search(pdb, r'1amz|2igd'):
        line = self.re_substitute(line, r'CELL.*', '')
    if self.re_search(pdb, r'1an1'):
        line = self.re_substitute(line, r'27 MONTHS FOR GROWTH\.', '')
    if self.re_search(pdb, r'1ao5'):
        line = self.re_substitute(line, r'57 MG/ML', r'57 MG/ML PROTEIN')
    #if self.re_search(pdb, r'1aoj|1od[ijkl]|1uv7'):
    #    line = self.re_substitute(line, r'CRYSTALLI[ZS]ATION.*', '')
    #    line = self.re_substitute(line, r'USED\.', '')
    if self.re_search(pdb, r'1aq1|1e1v|1eeh|1efv|1g6q|1g9m|1gc1|1gjv|1gk[xz]|1gmj|1gz8|1h0[vw]|1jqf|1o6v|[23]req'):
        line = self.re_substitute(line, r'.* RESER?VOIR:?', '')
        line = self.re_substitute(line, r'EQUAL .*', '')
    if self.re_search(pdb, r'1aq8|1as[678]|1ekg'):
        line = self.re_substitute(line, r'0\.1\s+SODIUM', r'0.1M SODIUM') # 1aq8 fix from paper
    if self.re_search(pdb, r'1aqd'):
        line = self.re_substitute(line, r'HLA-DR1 / PEPTIDE COMPLEX', r'PROTEIN')
    if self.re_search(pdb, r'1ava'):
        line = self.re_substitute(line, r'MES.*', r'10MM MES PH 6.5, 5MM CACL2, 3-10% PEG 6000')
    if self.re_search(pdb, r'1avc'):
        line = self.re_substitute(line, r'SODIUM.*', r'1.2M SODIUM ACETATE, 0.1M POTASSIUM CACODYLATE PH 6.5, 6.2MM CALCIUM CHLORIDE')
    if self.re_search(pdb, r'1awb'):
        line = self.re_substitute(line, r'0\.1M SODIUM.*', '')
    if self.re_search(pdb, r'1axw|1ci7|1gce|1ts[lm]|1zyr|2hcy|2or[opqrst]'):
        line = self.re_substitute(line, r'.* OVER', '')
    if self.re_search(pdb, r'1ay6|1ba8|1bb0|1ca8'):
      line = self.re_substitute(line, r'SOD\.\s+PHOSPHATE', r'SODIUM PHOSPHATE')
    if self.re_search(pdb, r'1azd'):
      line = self.re_substitute(line, r'.*\(11-15', r'11-15')
    if self.re_search(pdb, r'1azs'):
      line = self.re_substitute(line, r'AND 100 MM', r'AND 100 MM MES ')
    if self.re_search(pdb, r'1azt'):
      line = self.re_substitute(line, r'OR NAH2PO4.*', '')
    if self.re_search(pdb, r'1azx|1bvs|1ohh'):
        line = self.re_substitute(line, r'.* AND', '')
    if self.re_search(pdb, r'7ahl|1b08|1b24|1bo[hi]|6cro|1e4[wx]|1fbm|4thn|5gds|1gpw|1gzw|1h0c|1h1b|1h6z|1h8f|1hdh|1hw7|[1-4]jdw|1kgs|1ki[234678m]|1lk9|1o9u|1psz|1qm[jn]|1ux1|1w6[m-q]'):
        line = self.re_substitute(line, r'.* PRECIPITANT:?', '')
        line = self.re_substitute(line, r'.* PRECIPITATE SOLUTION:', '')
        line = self.re_substitute(line, r'.* PRECIPITATING (BUFFER|SOLUTION):?', '')
        line = self.re_substitute(line, r'POTASSIUM\s+THIOC[IY]N?ANATE \(KSCN\)', r'POTASSIUM THIOCYANATE')
        line = self.re_substitute(line, r'THE EXCHANGE.*', '')
    if self.re_search(pdb, r'1b08|1bh[oq]|1dzo|1fcg|1gu9|1idn|1jck|1lw1|1qo1'):
      line = self.re_substitute(line, r'.*LIQUOR', '')
      line = self.re_substitute(line, r'MIXED.*', '')
    if self.re_search(pdb, r'1b0e|1bpl|1h3e|1h4[gh]|1nt0|1ojs|1ok7|1q7r|1qqw|1uv7|462d'):
        line = self.re_substitute(line, r'.*RESERVOIR:', '') 
    if self.re_search(pdb, r'1ar2|1b0w|1ffh'):
        line = self.re_substitute(line, r'.* USING', '')
    if self.re_search(pdb, r'1b0p'):
        line = self.re_substitute(line, r'PEG.*', r'11% PEG 6000, 100MM MGCL2, 100MM CACODYLATE PH 6.0')
    if self.re_search(pdb, r'1b0y'):
        line = self.re_substitute(line, r'40 MM TRI 180 MM KCL', r'40 MM TRIS, 180 MM KCL')   # fix from paper
    if self.re_search(pdb, r'1b13|1b2j|1b2o|1be7'):
        line = self.re_substitute(line, r'IN SODIUM ACETATE BUFFER \(\s*50 MM\)', r'50MM SODIUM ACETATE')
    if self.re_search(pdb, r'1b1x|1bjr'):
        line = self.re_substitute(line, r'MICRODIALY[SZ]ED.*', r'10% V/V ETHANOL')  # fix from paper
    if self.re_search(pdb, r'1b2[01x]'):
        line = self.re_substitute(line, r'PH 7\.5 1-2 MM ZNSO4 0\.15-0\.30 M \(NH4\)\s+2SO4', r'PH 7.5, 1-2 MM ZNSO4, 0.15-0.30 M AMMONIUM SULFATE,')
    if self.re_search(pdb, r'1b2p|1do[02]|1e8c|1elj|1fd[yz]|1gwa|1gyj|1hia|1id[qu]|1pue|1q90|1rhi'):
        line = self.re_substitute(line, r'DROP:.*', '')
    if self.re_search(pdb, r'1b2k|1bq2'):
        line = self.re_substitute(line, r'.*WELL (S )?CONTAINING', '')
    if self.re_search(pdb, r'1b4s'):
        line = self.re_substitute(line, r'21\%\s*PEG\s+400', '')
    if self.re_search(pdb, r'1b4x|5eaa'):
        line = self.re_substitute(line, r'POTASSIUM[,.]\s+PHOSPHATE', r'POTASSIUM PHOSPHATE')
    if self.re_search(pdb, r'1b5f'):
        line = self.re_substitute(line, r'LYOPH.*', r'12MG/ML PROTEIN, 40% PEG 4000, 0.1M SODIUM CITRATE, 0.2M AMMONIUM ACETATE')
    if self.re_search(pdb, r'1b68|1c7[st]|1e19|1e6f|1f7r|1gqb|1gy9|1ked|1nks|[46]r1r|1uuo|1wb[78]|2f6l'):
        line = self.re_substitute(line, r'PROTEIN\s+(SOLN:|SOLUTION).*', '')
    if self.re_search(pdb, r'1b6c|1dc0|1dg6|1qhl|1g96'):
        line = self.re_substitute(line, r'(IN)?\s*DROP.*', '')
    if self.re_search(pdb, r'1b6v|1f99'):
        line = self.re_substitute(line, r'.*BUFFER\s+(WHICH)?\s*CONTAINED', '')
    if self.re_search(pdb, r'1b8e'):
        line = self.re_substitute(line, r'METHOD IN PRESENCE OF AMMONIUM SULPHATE 2.5 M', r'2.5M AMMONIUM SULFATE')
    #if self.re_search(pdb, r'1b8f|1eb4|1gk[23j]'):
    #    line = self.re_substitute(line, r'20 \%.*', '')
    #if self.re_search(pdb, r'1gkm'):
    #    line = self.re_substitute(line, r'25 \%.*', '')
    if self.re_search(pdb, r'1b9c'):
        line = self.re_substitute(line, r'23\% MG/ ML\s+PROTEINA', r'23 MG/ML PROTEIN A')
    if self.re_search(pdb, r'1ba3'):
        line = self.re_substitute(line, r'.*\+', '')
    if self.re_search(pdb, r'1bb[67]|1bgx'):
        line = self.re_substitute(line, r'COMPLEX WAS MADE.*', '')
    if self.re_search(pdb, r'1bbz'):
        line = self.re_substitute(line, r'DTT/EDTA', r'DTT, 1MM EDTA')
    if self.re_search(pdb, r'1bd9|1beh'):
        line = self.re_substitute(line, r'4000/6000/8000', r'6000')
    if self.re_search(pdb, r'1bdl'):
        line = self.re_substitute(line, r'SAMPLE:.*', '')
    if self.re_search(pdb, r'1beb'):
        line = self.re_substitute(line, r'.* FROM', '')
    if self.re_search(pdb, r'1ben|1bj5|1bke|1cg2|1h4[cde]|1nmt'):
        line = self.re_substitute(line, r'CRYSTALS\s+(GROWN?|GREW).*', '')
    if self.re_search(pdb, r'1bfd'):
        line = self.re_substitute(line, r'CRYSTALS.*', r'22% V/V PEG 400, 0.15M CACL2, 0.5% V/V MPD, 0.1M TRIS PH 8.5')
    if self.re_search(pdb, r'1bg0'):
        line = self.re_substitute(line, r'CONCENTRATION', '')
    if self.re_search(pdb, r'1bga'):
        line = self.re_substitute(line, r'PH .*', r'PH 8.3, 14MG/ML PROTEIN')
    if self.re_search(pdb, r'1bh9'):
        line = self.re_substitute(line, r'1 MM PCMBS \(SOAK\)', '')
    if self.re_search(pdb, r'1bi5|1bq6|1cgk|1chw'):
        line = self.re_substitute(line, r'.*WHICH CONTAINED', '') 
        line = self.re_substitute(line, r'IN THE PRESENCE.*', '') 
    if self.re_search(pdb, r'1bj0'):
        line = self.re_substitute(line, r'MG2\+.*', '')
    if self.re_search(pdb, r'1bji'):
        line = self.re_substitute(line, r'THE GLAXO.*', '')

    if self.verbose>1:
      print "parse:7", line
        
    # getting rid of parenthesis
    if self.re_search(pdb, r'1bk0|1blz|1hb[1-4]|3lkf|1qiq|1qj[ef]|483d'):
        line = self.re_substitute(line, r'\(', '')
        line = self.re_substitute(line, r'\)', '')
    if self.re_search(pdb, r'1bl3'):
        line = self.re_substitute(line, r'\[PROTEIN.*', r'0.13MM PROTEIN')
    if self.re_search(pdb, r'1xc6|1xqn'):
        line = self.re_substitute(line, r'\([A-Z 0-9,]+\)', '')
    if self.re_search(pdb, r'1bkm|1dcy|1skj|2anl'):
        line = self.re_substitute(line, r'(AN )?INHIBITOR.*', '')
    if self.re_search(pdb, r'1bkr|1dcn'):
        line = self.re_substitute(line, r'PEG8K 30% \(W/V\)', r'30% (W/V) PEG 8000')
        line = self.re_substitute(line, r'PEG 2K MME 18-20 \%', r'18-20% PEG 2000 MME')
    if self.re_search(pdb, r'1bkx'):
        line = self.re_substitute(line, r'.* CRYSTALLIZATION WELL SOLUTION', '')
        line = self.re_substitute(line, r'BICINE BUFFER \(100.*', r'100MM BICINE PH 8.0')
    if self.re_search(pdb, r'1bkz|1dd7|1t5r|1xdt|2jcr'):
        line = self.re_substitute(line, r'.*CONTAINING', '')
    if self.re_search(pdb, r'3hh3|3hh4|3hh5|3hh6'):
        line = self.re_substitute(line, r'\(VAPOR\-DIFFUSION FOR COMPLEX PREPARATION\)','')
    if self.re_search(pdb, r'2x5q'):
        line = self.re_substitute(line, r'ETHYLENE GLYCOL.DERIVATIVE CRYSTALS FOR SAD\s*PHASING WERE OBTAINED BY SOAKING THE CRYSTALS IN', '') 
    if self.re_search(pdb, r'3bls|1g0r'):
        line = self.re_substitute(line, r'COCRYSTALLI(ZED|SATION).*', '')
    if self.re_search(pdb, r'3gnx'):
        line = self.re_substitute(line, r'CRYSTALLINE SUSPENSION', r'PROTEIN')
    if self.re_search(pdb, r'1bm[2b]'):
        line = self.re_substitute(line, r'IN PRESENCE OF.*', '')
    if self.re_search(pdb, r'1bn[134mnqtuvw]'):
        line = self.re_substitute(line, r'FULL-GROWN.*', '')
    if self.re_search(pdb, r'1boi'):
        line = self.re_substitute(line, r'ACET MM SODIUM', r'ACETATE, 1MM SODIUM') # fix from paper
    if self.re_search(pdb, r'1box'):
        line = self.re_substitute(line, r'12,5 \% PEG 6000 RESERVOIR: 25 \% PEG 6000', r'12.5-25% PEG 6000')
    if self.re_search(pdb, r'1bpl'):
        line = self.re_substitute(line, r'CALCIUM REMOVAL.*', '')
    if self.re_search(pdb, r'1bq[ad]'):
        line = self.re_substitute(line, r'AS,0\.2 2-METHYLMORPHOLINE, PH 7\.5', r'AMMONIUM SULFATE, 0.2 M MES, PH 7.5,')
    if self.re_search(pdb, r'1brw'):
        line = self.re_substitute(line, r'PSEUDOURIDINE AT 10X PROTEIN CONCENTRATION', '')
    if self.re_search(pdb, r'1bs2'):
        line = self.re_substitute(line, r'AMMONIUM SULFATE 2\.45 M', r'2.45M AMMONIUM SULFATE')
    if self.re_search(pdb, r'1bv4'):
        line = self.re_substitute(line, r'02\%,', r'02%')
    if self.re_search(pdb, r'1bvn'):
        line = self.re_substitute(line, r'HARVESTED.*', '')
    if self.re_search(pdb, r'1bvw|1gz1'):
        line = self.re_substitute(line, r'\%\.', r'%')
    if self.re_search(pdb, r'1bw8|1exm|1ha3|1hes|1qtq'):
        line = self.re_substitute(line, r'MOLAR RATIO.*', '')
    if self.re_search(pdb, r'1bwf|1gl[jl]'):
      line = self.re_substitute(line, r'.* MACRO\s*SEED(ING|ED)', '')
    if self.re_search(pdb, r'1bx6'):
        line = self.re_substitute(line, r'THE.*', r'0.2MM PROTEIN, 0.5MM BALANOL, 15% MPD, 10% PEG 200, 100MM TRIS PH 7.5')
    if self.re_search(pdb, r'1byt'):
        line = self.re_substitute(line, r'PHOSPHATE-CITRATE BUFFER 0\.05M', r'50MM CITRATE PHOSPHATE')
    if self.re_search(pdb, r'1bz4|1ea8|1h7i|1or2'):
        line = self.re_substitute(line, r'NOTE.*', '')
    if self.re_search(pdb, r'1bzs'):
        line = self.re_substitute(line, r'WITH THREEFOLD EXCESS INHIBITOR IN DMF\s+ADDED\.', '')
    if self.re_search(pdb, r'1c1[vw]|[34]eng'):
        line = self.re_substitute(line, r'(A )?CO-CRYSTAL.*', '')
    if self.re_search(pdb, r'1c1x'):
        line = self.re_substitute(line, r'10 MM L-3- PHENYLLACTATE', r', 10 MM L-3-PHENYLLACTATE,')
    if self.re_search(pdb, r'1ci6'): # temp appears twice
        line = self.re_substitute(line, r'AT 15 DEGREES C', '')
    if self.re_search(pdb, r'1c2[e-k]'):
        line = self.re_substitute(line, r'BATCH.*', r'1.51M MGSO4, 1MM ZN(II), 5% DMSO, 0.59MM PROTEIN')
    if self.re_search(pdb, r'1c3g'):
        line = self.re_substitute(line, r'PEG.*', r'20% PEG 3350')
    if self.re_search(pdb, r'1c6v'):
        line = self.re_substitute(line, r'PEG6K 8\%', r'8% PEG 6000')
    if self.re_search(pdb, r'1c6[xz]|1g2v|1g3l|1g5p|1gtw|1gu4|1id[qu]|1o6e|4ovw|1qhu|1ute'):
        line = self.re_substitute(line, r'PROTEIN-?.*', '')
    if self.re_search(pdb, r'1c7i'):
        line = self.re_substitute(line, r'TRIS', r'TRIS PH 7.5,') #fix from paper
    if self.re_search(pdb, r'1c7j'):
        line = self.re_substitute(line, r'175 LISO4', r'PH 8.4, 175MM LISO4') #fix from paper
    if self.re_search(pdb, r'1c8o'):
        line = self.re_substitute(line, r'SODIUM.*', r'1.6M SODIUM POTASSIUM PHOSPHATE')
# getting rid of errant commas...
    if self.re_search(pdb, r'1c7[qr]|1ni3|1npe|1o6l|1ode|1psw|1rka|1rv1|1s68|1so[36]|1vzj|2ben'):
        line = self.re_substitute(line, r',', '')
    if self.re_search(pdb, r'1cb8'):
        line = self.re_substitute(line, r'PEG-MME 2K 17\% AMMONIUM ACETATE 80MM', r'17% PEG-MME 2K, 80MM AMMONIUM ACETATE')
    if self.re_search(pdb, r'2c9w'):
        line = self.re_substitute(line, r'300\s*NL.*', '')
    if self.re_search(pdb, r'2c1[5689]'):
        line = self.re_substitute(line, r'ABOVE.*', '')
    if self.re_search(pdb, r'1c1[n-t]|1c2[lm]|1c5[p-v]'):
        line = self.re_substitute(line, r'TRYPSIN\-BENZAMIDINE, P3\(1\) 2 1\s*(CRYSTALS )?WERE GROWN BY VAPOR DIFFUSION, AS DESCRIBED FOR\s*P2\(1\) 2\(1\) 2\(1\) \(LARGE CELL\) \(MANGEL, ET AL\.,\s*BIOCHEMISTRY 29, 8351-8357\s*, 1990\)', '')
    if self.re_search(pdb, r'2cbl'):
        line = self.re_substitute(line, r'1:5.*', '')
    if self.re_search(pdb, r'2cb[uv]'):
        line = self.re_substitute(line, r'25.*', '')
    if self.re_search(pdb, r'1cd1'):
        line = self.re_substitute(line, r'[0-9.]+\s+UL PROTEIN.*', '')
    if self.re_search(pdb, r'4cev'):
        line = self.re_substitute(line, r'10 MM MOPSM.*', '')
    if self.re_search(pdb, r'5cev'):
        line = self.re_substitute(line, r'L-\s+LYSINE', r'L-LYSINE')
    if self.re_search(pdb, r'1cic'):
        line = self.re_substitute(line, r'10MGM', r'10MG')
    if self.re_search(pdb, r'1cii'):
        line = self.re_substitute(line, r'STARTING WITH.*', '')
    if self.re_search(pdb, r'1cip'):
        line = self.re_substitute(line, r'H 6\.0', r'PH 6.0')
    if self.re_search(pdb, r'1cj0'):
        line = self.re_substitute(line, r'20MM K2HPO4, KH2PO4', r'20MM POTASSIUM PHOSPHATE')
        line = self.re_substitute(line, r'OR SODIUM HEPES', '')
    if self.re_search(pdb, r'1cjc|1e1l|1olt'):
        line = self.re_substitute(line, r'.* RESER?VOIR:', '')
    if self.re_search(pdb, r'1cm0'):
        line = self.re_substitute(line, r'WITH 2 M EXCESS COFACTOR', '')
    if self.re_search(pdb, r'1cm[14]|1jyo|1lfo'):
        line = self.re_substitute(line, r'STOCK:?.*', '')
        line = self.re_substitute(line, r'\(PEG\s*6000\)', '')
    if self.re_search(pdb, r'1cn0'):
        line = self.re_substitute(line, r'1\.0M\(NH4\)2SO4', r'1.0M AMMONIUM SULFATE')
    if self.re_search(pdb, r'1cp2|1fxo|1ogw'):
        line = self.re_substitute(line, r'STORED.*', '')
        line = self.re_substitute(line, r'PROTEIN', '')
    if self.re_search(pdb, r'1cr7'):
        line = self.re_substitute(line, r'PURE .*', r'4-5MG/ML PROTEIN, 0.05M SODIUM ACETATE PH 4.6, 0.2M NACL, 1.5MM LACTOSE 0.05% SODIUM AZIDE, 12% PEG 8000')
    if self.re_search(pdb, r'6cro'):
        line = self.re_substitute(line, r'ALLOWED .*', '')
    if self.re_search(pdb, r'1cq4'):
        line = self.re_substitute(line, r'.*OF BUFFER', '')
        line = self.re_substitute(line, r'WHICH.*', '')
    if self.re_search(pdb, r'1ct1'):
        line = self.re_substitute(line, r'.*PH 7\.5', '')  #fix from paper
    if self.re_search(pdb, r'1cv8'):
        line = self.re_substitute(line, r'6\.0 5MM E\-64', r'6.0')
    if self.re_search(pdb, r'1cx2'):
        line = self.re_substitute(line, r'10-240', r'10-240MM')
    if self.re_search(pdb, r'1d0s'):
        line = self.re_substitute(line, r'5,\s+6', r'5,6')
    if self.re_search(pdb, r'1d1l'):
        line = self.re_substitute(line, r'INCLUDING .*', '')
    if self.re_search(pdb, r'1d4a'):
        line = self.re_substitute(line, r'200 MM NAACETATE\s*12-24 MICROM FAD', r',200 MM SODIUM ACETATE, 12-24 UM FAD,')
    if self.re_search(pdb, r'1d6m'):
        line = self.re_substitute(line, r'NA, POTASSIUM', r'SODIUM POTASSIUM')
    if self.re_search(pdb, r'1daz|1ebk'):
        line = self.re_substitute(line, r'CITRATE.*', r'0.05M CITRATE PHOSPHATE, 10MM DTT, 10% DMSO, 25-50% AMMONIUM SULFATE, 2-5MG/ML PROTEIN')
    if self.re_search(pdb, r'1dd6|1got|1tbg'):
      line = self.re_substitute(line, r'MIXTURE.*', '')
    if self.re_search(pdb, r'1dfg'):
        line = self.re_substitute(line, r'1,2-DIHYDRO-1-HYDROXY-2-.*', r'BENZODIAZABORINE')
    if self.re_search(pdb, r'1dfh'):
        line = self.re_substitute(line, r'1,2-DIHYDRO-1-HYDROXY-2-.*', r'THIENODIAZABORINE')
    if self.re_search(pdb, r'1dfx'):
        line = self.re_substitute(line, r'CACL2 0\.2 M', r'0.2M CACL2')
    if self.re_search(pdb, r'1dke'):
        line = self.re_substitute(line, r'1MM IHP', r'1MM INOSITOL HEXAPHOSPHATE')
    if self.re_search(pdb, r'1dmu'):
        line = self.re_substitute(line, r'\d:\d.*', '')
    if self.re_search(pdb, r'1dq[45]'):
        line = self.re_substitute(line, r'UNLOCKED.*', '')
    if self.re_search(pdb, r'1dsz'):
        line = self.re_substitute(line, r'RXR AND RAR.*', '')
    if self.re_search(pdb, r'1dw6'):
        line = self.re_substitute(line, r'CITRATE.*', r'0.05M CITRATE PHOSPHATE, 10MM DTT, 10% DMSO, 25-50% AMMONIUM SULFATE, 2-5MG/ML PROTEIN')
    if self.re_search(pdb, r'1dw[9k]'):
        line = self.re_substitute(line, r'MICROSEEDING.*', '')
        line = self.re_substitute(line, r'TRIC', r'TRIS')
    if self.re_search(pdb, r'1dua'):
        line = self.re_substitute(line, r'PEG 8000 \(23\-26\%\), AMMONIUM  SULPHATE 0\.2 M', r'23-26% PEG 8000, 0.2M AMMONIUM SULPHATE')
    if self.re_search(pdb, r'1dun'):
        line = self.re_substitute(line, r'GROWTH.*', '')
    if self.re_search(pdb, r'1dxp|1dy[89]'):
        line = self.re_substitute(line, r'.* WEEKS', '')
        line = self.re_substitute(line, r'THE TERNARY COMPLEX.*', '')
    if self.re_search(pdb, r'1dy5'):
        line = self.re_substitute(line, r'CONC.*', r'10MG/ML PROTEIN')
    if self.re_search(pdb, r'1dze'):
        line = self.re_substitute(line, r'INCUBATION.*', '')
    if self.re_search(pdb, r'1dz[4689]|1o76'):
        line = self.re_substitute(line, r'SAME BUFFER AS PROTEIN\)', '')
    if self.re_search(pdb, r'1dz[gh]|1e03'):
        line = self.re_substitute(line, r'1:1 MIX OF INHIBITORY: LATENT ANTITHROMBIN-III', r'PROTEIN')
    if self.re_search(pdb, r'1bio|1c0m|1c1a|2cav|1cc0|1e2[vwz]|1e94|1hdi|1hfd|1hk9'):
        line = self.re_substitute(line, r'.*RESERVOIR\s+(SOLUTIONS?)?\s*CONTAINED:?', '')
        line = self.re_substitute(line, r'CRYSTALLIZATION WERE.*', '')
        line = self.re_substitute(line, r'0\.4 MG/ML RESORUFIN-LABELLED CASEIN', '')  #1e94 fix from paper...
    if self.re_search(pdb, r'1e0b'):
        line = self.re_substitute(line, r'TIME.*', '')
    if self.re_search(pdb, r'1e15'):
        line = self.re_substitute(line, r'M\(NH4\)2SO4,\s+CITRATE', r'M (NH4)2SO4, 50MM CITRATE') # fix from papers
    if self.re_search(pdb, r'1e1a'):
        line = self.re_substitute(line, r'\d+\s+DAYS? .*', '')
    if self.re_search(pdb, r'1e1[vx]|1oju'):
        line = self.re_substitute(line, r'.*MIXED WITH', '')
        line = self.re_substitute(line, r'EQUAL VOLUMES.*', '')
    if self.re_search(pdb, r'1e26'):
        line = self.re_substitute(line, r'SET UP.*', '')
        line = self.re_substitute(line, r'100MM\,', r'100MM KCL,')
    if self.re_search(pdb, r'1e2y'):
        line = self.re_substitute(line, r'PH HANGING.*', r'PH 7.5, 10% (V/V) GLYCEROL, 100MM DTT, 0.25% (V/V) DMSO') #fix from paper
    if self.re_search(pdb, r'1e30'):
        line = self.re_substitute(line, r'PROTEIN.*', r'7MG/ML PROTEIN')
    if self.re_search(pdb, r'1e39|1qjd'):
        line = self.re_substitute(line, r'10MM FUM', r'10MM FUMARATE')
    if self.re_search(pdb, r'1e42'):
        line = self.re_substitute(line, r'5MM HEPES.*', '')
    if self.re_search(pdb, r'1e4[fg]'):
        line = self.re_substitute(line, r'MES,', r'MES, PH')
    if self.re_search(pdb, r'1e5d'):
        line = self.re_substitute(line, r'VAPOUR.*', r'10MG/ML PROTEIN, 10% PEG 6K, 0.1M TRIS-MALEATE, PH 6.0')
    if self.re_search(pdb, r'1e5j|1e7y|1efp|1h5v|1m6p|1oc[57]|1oem'):
        line = self.re_substitute(line, r'(THE)?\s*PROTEIN (WAS|AT).*', '')
    if self.re_search(pdb, r'1e5[hi]'):
        line = self.re_substitute(line, r'GLYCEROL\s+([-0-9]+)\s*\%\s*(\([WV]/[WV]\))?,', r'\1% GLYCEROL')
    if self.re_search(pdb, r'1e5p'):
        line = self.re_substitute(line, r'PEG 8K 28\%', r'28% PEG 8K')
        line = self.re_substitute(line, r'\[P\]2\.65MG.*', '')
    if self.re_search(pdb, r'1e6[01]'):
        line = self.re_substitute(line, r'5\s*-\s*2', r'5, 2')
    if self.re_search(pdb, r'1e6e'):
        line = self.re_substitute(line, r'0\.5MM COMPLEX IN 100MMTRIS-HCL', r'100MM TRIS CHLORIDE')
    if self.re_search(pdb, r'1e6[nprz]|1gpf'):
        line = self.re_substitute(line, r'HEPES', r'100MM HEPES') # a guess from author of another paper...
    if self.re_search(pdb, r'1e6u|1e7[sr]'):
        line = self.re_substitute(line, r'TRIS BUFFER 21C', r'TRIS')
    if self.re_search(pdb, r'1e7d'):
        line = self.re_substitute(line, r'C\.A\.', '')
    if self.re_search(pdb, r'1e9x|1ea1'):
        line = self.re_substitute(line, r'4-.*', '')
    if self.re_search(pdb, r'2ebo'):
        line = self.re_substitute(line, r'2 CACL2', r'2M CACL2')
    if self.re_search(pdb, r'1ec5'):
        line = self.re_substitute(line, r'CRYSTALS.*', r'2M AMMONIUM SULFATE')
    if self.re_search(pdb, r'1eg9'):
        line = self.re_substitute(line, r'AMMONIUM.*', r'2M AMMONIUM SULFATE, 0.1M MES, 2-3% DIOXANE')
    if self.re_search(pdb, r'1ega'):
        line = self.re_substitute(line, r'.*', r'8MG/ML PROTEIN, 0.1M TRIS PH 8.0, 0.8M LITHIUM SULFATE, 0.8M NACL')
    if self.re_search(pdb, r'1egz'):
        line = self.re_substitute(line, r'VAPOR.*', r'28% PEG 4000, 20MM TRIS PH 8.0, 20MM MGSO4')
    if self.re_search(pdb, r'1ej0'):
        line = self.re_substitute(line, r'19 AMMONIUM', r'19M AMMONIUM')
    if self.re_search(pdb, r'1ejo'):
        line = self.re_substitute(line, r'PEG.*', r'16% PEG 4000, 0.2M LICL, 50MM TRIS')
    if self.re_search(pdb, r'1ek4|1mo[9k]|1nh[uv]'):
      line = self.re_substitute(line, r'PH\s+6\.5', '')
      line = self.re_substitute(line, r'PH\s+7\.50?', '')
    if self.re_search(pdb, r'1elv'):
        line = self.re_substitute(line, r'.*', r'34% PEG 4000, 100MM AMMONIUM SULFATE')
    if self.re_search(pdb, r'1emt'):
        line = self.re_substitute(line, r'FAB', r'PROTEIN')
    if self.re_search(pdb, r'1env'):
        line = self.re_substitute(line, r'SPACE GROUP R32 IN HEXAGONAL SETTING', '')
    if self.re_search(pdb, r'1eq2'):
        line = self.re_substitute(line, r'20NM\s+SPERMIDINE', r'0.02MM SPERMIDINE')
    if self.re_search(pdb, r'1es2'):
        line = self.re_substitute(line, r'.*', r'0.1M TRIS, 22% PEG 6000, 0.4M NACL')
    if self.re_search(pdb, r'1es3'):
        line = self.re_substitute(line, r'.*', r'0.1M MES, 25% PEG 6000, 0.5M NACL')
    if self.re_search(pdb, r'1es4'):
        line = self.re_substitute(line, r'.*', r'0.1M TRIS, 30% PEG 6000, 0.4M NACL')
    if self.re_search(pdb, r'1es5'):
        line = self.re_substitute(line, r'.*', r'0.1M TRIS, 21-30% PEG 6000, 0.4M NACL')
    if self.re_search(pdb, r'1esi'):
        line = self.re_substitute(line, r'.*', r'0.1M TRIS, 27-33% PEG 6000, 0.4M NACL')
    if self.re_search(pdb, r'1esu'):
        line = self.re_substitute(line, r'.*', r'0.1M IMIDAZOLE PH 7.0, 43-48% AMMONIUM SULFATE')
    if self.re_search(pdb, r'1euh|1p5e|1qi6'):
        line = self.re_substitute(line, r'HEPES\s+(0\.1\s*M|100MM)', r'0.1M HEPES')
    if self.re_search(pdb, r'1ev9'):
        line = self.re_substitute(line, r'3-CYCLOHEXYLAMINO-1-\s*PROPANE SULFONIC ACID \(CAPS\)', r'CAPS')
    if self.re_search(pdb, r'1evu'):
        line = self.re_substitute(line, r'\bTO .*', '')
    if self.re_search(pdb, r'1ewd'):
        line = self.re_substitute(line, r'.*', r'43% AMMONIUM SULFATE, 5MM EDTA, 100MM TRIETHYLAMINE')
    if self.re_search(pdb, r'1ewe'):
        line = self.re_substitute(line, r'.*', r'43% AMMONIUM SULFATE, 5MM EDTA')
    if self.re_search(pdb, r'1ezj'):
        line = self.re_substitute(line, r'.*', r'16% PEG 3K, 200MM NACL, 10MM CACL2, 5MM ETHYLMERCURYTHIOSALICILIC ACID, 100MM TRIS CHLORIDE')
    if self.re_search(pdb, r'1ezz|1gpj'):
        line = self.re_substitute(line, r'.*BUFFER:', '')
    if self.re_search(pdb, r'1f51'):
        line = self.re_substitute(line, r'AND ALF3', '')
    if self.re_search(pdb, r'1fdw'):
      line = self.re_substitute(line, r'.*', r'30% PEG 4K, 100MM HEPES PH 7.0, 100MM MGCL2, 0.5MM ESTRADIOL, 2-4% PROPANEDIOL')
    if self.re_search(pdb, r'1fej|1ff[0fi]|1fg[68c]'):
      line = self.re_substitute(line, r'.*', r'2-5 MG/ML PROTEIN, 0.05M CITRATE PHOSPHATE PH 5.0-6.5, 10MM DTT, 10% DMSO, 25-50% AMMONIUM SULFATE')
    if self.re_search(pdb, r'1ff3'):
      line = self.re_substitute(line, r'CACODYLATE BUFFER 0\.1 M', r'0.1M CACODYLATE BUFFER')
    if self.re_search(pdb, r'1fgn'):
      line = self.re_substitute(line, r'.*', r'17.5% PEG 10K PH 8.5')
    if self.re_search(pdb, r'1fgs'):
      line = self.re_substitute(line, r'5 NM MGATP', r'5MM MAGNESIUM ATP') # fix from paper
    if self.re_search(pdb, r'1fh7'):
      line = self.re_substitute(line, r'.*', r'15% PEG 4K, 0.1M SODIUM ACETATE') 
    if self.re_search(pdb, r'1fhi'):
      line = self.re_substitute(line, r'.*EQUAL VOLUME.* OF', '') 
    if self.re_search(pdb, r'1fhj'):
      line = self.re_substitute(line, r'.*', r'30% PEG 1500') 
    if self.re_search(pdb, r'1fif'):
      line = self.re_substitute(line, r'GOLYETHYLENE GLYCOL 8,\s*000', r'PEG 8000')
    if self.re_search(pdb, r'1fir'):
      line = self.re_substitute(line, r'PH 5\.6$', '')
    if self.re_search(pdb, r'1fiu'):
      line = self.re_substitute(line, r'.*', r'100MM MES, 200MM MGCL2, 25% MPD')
    if self.re_search(pdb, r'1fo0'):
      line = self.re_substitute(line, r'.*', r'10% PEG 6000, 0.1M HEPES PH 7.0, 0.25M MAGNESIUM ACETATE, 0.25M NACL')
    if self.re_search(pdb, r'1fx7'):
      line = self.re_substitute(line, r'~0\.1 MM 21 BP DUPLEX\s+DNA OLIGOMER', r'0.1 MM DNA DUPLEX')
    if self.re_search(pdb, r'1fx8'):
      line = self.re_substitute(line, r'GLPF AT 15-20 MG/ML', r'15-20 MG/ML PROTEIN')
    if self.re_search(pdb, r'1fxm'):
      line = self.re_substitute(line, r'.*', r'12-25% PEG 6000, 20 MG/ML PROTEIN')
    if self.re_search(pdb, r'1fxp|1hr0|1vl4|1vrb|1yd9|1ygt|1z90|1zpw|1zup|2a6b|2aj7|2amy|2apj|2avn|2cve'):
        line = self.re_substitute(line, r'VAPOU?R.*', '') # fix - duplication
    if self.re_search(pdb, r'1fxu'):
      line = self.re_substitute(line, r'.*', r'11-16% PEG 4000, 0.04M TRIS CHLORIDE, 0.08M MGCL2')
    if self.re_search(pdb, r'1fyv'):
      line = self.re_substitute(line, r'1\.2M NAH2PO4/\s+K2HPO4', r'1.2M SODIUM POTASSIUM PHOSPHATE,')
    if self.re_search(pdb, r'[45]gal'):
      line = self.re_substitute(line, r'GALECTIN-7.*', '')
    if self.re_search(pdb, r'1g17'):
      line = self.re_substitute(line, r'POLY.*', r'25% PEG 4K, 200MM MGCL2, 30% ETHYLENE GLYCOL, 100MM SODIUM HEPES PH 7.7') 
    if self.re_search(pdb, r'1g1l|1g23'):
      line = self.re_substitute(line, r'4.*', '') 
    if self.re_search(pdb, r'1g1s'):
      line = self.re_substitute(line, r'MN NACL', r'MM NACL') 
    if self.re_search(pdb, r'1g2a'):
      line = self.re_substitute(line, r'.*5 \+', '') 
    if self.re_search(pdb, r'1g33'):
      line = self.re_substitute(line, r'.*', r'3M AMMONIUM SULFATE, 30MM CALCIUM CHLORIDE') 
    if self.re_search(pdb, r'1g3x'):
      line = self.re_substitute(line, r'DUPLEX', r'DNA DUPLEX') # fix from paper
    if self.re_search(pdb, r'1g6x|1qlq'):
      line = self.re_substitute(line, r'THE HANGING .*', '') 
    if self.re_search(pdb, r'1g7u'):
      line = self.re_substitute(line, r'MES.*', r'10% V/V PEG 400, 25% GLYCEROL, 61MM MES PH 6.1') 
    if self.re_search(pdb, r'1gjw'):
      line = self.re_substitute(line, r'.*', r'0.35-0.40M AMMONIUM PHOSPHATE PH 4.8, 50MM MALTOSE, 18 MG/ML PROTEIN') 
    if self.re_search(pdb, r'1gk1'):
      line = self.re_substitute(line, r'PH 7\.0/9\.0', r'PH 7.0-9.0')
    if self.re_search(pdb, r'1gk[kl]'):
      line = self.re_substitute(line, r'.*', r'100MM HEPES PH 7.5, 1M SODIUM ACETATE, 50MM CADMIUM ACETATE, 5% GLYCEROL')
    if self.re_search(pdb, r'1gkp'):
      line = self.re_substitute(line, r'1\.65 MM', r'1.65 M') # fix from paper
    if self.re_search(pdb, r'1gnu'):
        line = self.re_substitute(line, r'PEGMONO', r'PEG MME 2000, 10MM NICKEL CHLORIDE')   # fix from paper
    if self.re_search(pdb, r'1gp[56]'):
      line = self.re_substitute(line, r'\(IN MEOH.* MEOH\)', '')
    if self.re_search(pdb, r'1gpj|1xca'):
        line = self.re_substitute(line, r'SALT', '')
    if self.re_search(pdb, r'1gpq'):
      line = self.re_substitute(line, r'CHES BUFFER 0\.1M', r'0.1M CHES BUFFER')
    if self.re_search(pdb, r'1gqa'):
      line = self.re_substitute(line, r'.*', r'12 MG/ML PROTEIN, 25MM SODIUM ACETATE PH 4.5, 15% PEG 8000')
    if self.re_search(pdb, r'1gqe'):
      line = self.re_substitute(line, r'PEG.*', r'28-34% PEG MME 2K')

    if self.verbose>1:
      print "parse:8", line
    
    #  putting the word protein in where there was only a concentration before...
    if self.re_search(pdb, r'1gq[ijkl]|1gv0|1gyg|1h0u|1hlq|[12]knt|1o6s|1of7|32c2'):
      line = self.re_substitute(line, r'([-0-9.]+)\s*MGS?[/ ]ML(-1)?', r'\1 MG/ML PROTEIN')
    if  self.re_search(pdb, r'1gqn'):
      line = self.re_substitute(line, r'PRECIPITANT TO BUFFER RATIO 4:6\-3 :7', '')
    if self.re_search(pdb, r'1gqw|1hm5'):
        line = self.re_substitute(line, r'PROTEIN\s+(IN)?\s*SOLUTION.*', '')
    if self.re_search(pdb, r'1gr0'):
        line = self.re_substitute(line, r'.*', r'6.2-6.7% W/V PEG 4000, 50MM SODIUM CACODYLATE PH 7.0, 100MM CALCIUM ACETATE')
    if self.re_search(pdb, r'1gt6'):
        line = self.re_substitute(line, r'10.*', r'10-20 MG/ML PROTEIN, 10MM TRIS PH 8.0')
    if self.re_search(pdb, r'1gu5'):
        line = self.re_substitute(line, r'PROTEIN-DNA COMPLEX .*', '')
    if self.re_search(pdb, r'1guj'):
        line = self.re_substitute(line, r'HUMAN INSULIN IN SULPHURIC ACID PH 2\.1 RESERVOIR SOL: SULPHURIC ACID', '')
    if self.re_search(pdb, r'1guy'):
        line = self.re_substitute(line, r'5.*', r'5-15% PEG 400, 100 MM SODIUM ACETATE, PH 4.6, 40MM CADMIUM ACETATE') # fix from paper- duplication
    if self.re_search(pdb, r'1gv0|1ljy'):
        line = self.re_substitute(line, r'MMTRIS', r'MM TRIS')
        line = self.re_substitute(line, r'MMHEPES', r'MM HEPES')
    if self.re_search(pdb, r'1gvh'):
        line = self.re_substitute(line, r'.*', r'0.1M SODIUM ACETATE PH 5.1, 21-26% PEG 3350, 0.2M NACL')
    if self.re_search(pdb, r'1gvz'):
        line = self.re_substitute(line, r'NA-CACODYLATE', r'M SODIUM CACODYLATE')
    if self.re_search(pdb, r'1gx1'):
      line = self.re_substitute(line, r'MONOETHYL ETHER', r' PH 4.4-5.0') #fix from paper
    if self.re_search(pdb, r'1gxa'):
        line = self.re_substitute(line, r'.*', r'1.25M SODIUM CITRATE, 0.1M HEPES PH 7.3')
    if self.re_search(pdb, r'1gxr'):
      line = self.re_substitute(line, r'.*22\% PEG8000, 100MM, NACACODYLATE, 100MM CAACETATE\)', r'22% PEG 8000, 100MM SODIUM CACODYLATE, 100MM CALCIUM ACETATE')
    if self.re_search(pdb, r'1gy7'):
        line = self.re_substitute(line, r'1\.6M AMMONIUM SULPHATE\(DROP\) .*', '')
    if self.re_search(pdb, r'1gz7'):
        line = self.re_substitute(line, r'SODIUM ACETATE 0\.1M', r'0.1M SODIUM ACETATE')
    if self.re_search(pdb, r'1gz8|1h0[vw]'):
        line = self.re_substitute(line, r'.*MIXED WITH WELL BUFFER', '')
    if self.re_search(pdb, r'1gzf'):
        line = self.re_substitute(line, r'ADDED WITH .*', r',20MM NAD')
    if self.re_search(pdb, r'1gzu'):
        line = self.re_substitute(line, r'100 M M TRIS', r'100 MM TRIS')
    if self.re_search(pdb, r'1gzx'):
        line = self.re_substitute(line, r'75-90 MG/ML', r'75-90 MG/ML PROTEIN')
    if self.re_search(pdb, r'1h14'):
        line = self.re_substitute(line, r'SUCCESS.*', '') 
    if self.re_search(pdb, r'1h1o'):
        line = self.re_substitute(line, r'MES.*30\%', r'0.1M MES PH 6.5, 25-30% PEG MME, 1MM ASCORBATE,') # even the paper doesn't say which PEG MME! 
    if self.re_search(pdb, r'1h27'):
        line = self.re_substitute(line, r'PROTEIN.*', r'10MG/ML PROTEIN') 
    if self.re_search(pdb, r'1h2h'):
        line = self.re_substitute(line, r'KDIH\.PHOSPHATE', r'POTASSIUM PHOSPHATE')  # fix from paper...
        line = self.re_substitute(line, r'2\% ETHYLENE GLYCOL', r'1MM EDTA') # fix from paper...
    if self.re_search(pdb, r'1h4[78]'):
        line = self.re_substitute(line, r'10.*', r'0.2M AMMONIUM SULFATE, 0.1M SODIUM ACETATE PH 5.6, 25% PEG 4000') #fix from crystallization paper
    if self.re_search(pdb, r'1h4m'):
        line = self.re_substitute(line, r'NATIVE.*', '')
    if self.re_search(pdb, r'1h4r|1jk4'):
        line = self.re_substitute(line, r'(A)? \d:\d\s*(MOLAR)?\s+RATIO.*', '')
    if self.re_search(pdb, r'1h58'):
        line = self.re_substitute(line, r'THE FERROUS STATE.*', '')
    if self.re_search(pdb, r'1h5x|1h8[yz]'):
        line = self.re_substitute(line, r'PROTEIN.*', r'12-15MG/ML PROTEIN') 
    if self.re_search(pdb, r'1h6m'):
        line = self.re_substitute(line, r'.*', r'200MM SODIUM ACETATE PH 4.5, 4.0% W/V NACL')
    if self.re_search(pdb, r'1h6w'):
        line = self.re_substitute(line, r'\,2-METHYLPROPANE-2-OL \(TERTIARY BUTANOL\)', r' TERT-BUTANOL')
    if self.re_search(pdb, r'1h87'):
        line = self.re_substitute(line, r'.*', r'0.8M NACL, 50MM SODIUM ACETATE PH 4.5, 100MM GD-HP-DO3A, 40MG/ML PROTEIN')
    if self.re_search(pdb, r'1h89|1oby'):
        line = self.re_substitute(line, r'0\.05 MGSO4', r'0.005M MGSO4') # fix from paper
        line = self.re_substitute(line, r'2 MGSO4', r'2M MGSO4') 
    if self.re_search(pdb, r'1h8k'):
        line = self.re_substitute(line, r'/AC\. ACETIC', '')
    if self.re_search(pdb, r'1h91|1joi'):
        line = self.re_substitute(line, r'DROPS? MADE.*', '')
    if self.re_search(pdb, r'1h96'):
        line = self.re_substitute(line, r'.*COMPOSED OF', '')
    if self.re_search(pdb, r'1h9w'):
        line = self.re_substitute(line, r'AND MNCL2', r'10MM MNCL2')
    if self.re_search(pdb, r'1hb6'):
        line = self.re_substitute(line, r'5MMCDCL2', r'5MM CDCL2')
    if self.re_search(pdb, r'1hcu'):
        line = self.re_substitute(line, r'.*WELL CONTAINS', '')
    if self.re_search(pdb, r'1hdk'):
        line = self.re_substitute(line, r'.*', r'100MM TRIS ACETATE PH 7.0')
    if self.re_search(pdb, r'1hdo'):
        line = self.re_substitute(line, r'NADP.*', r'2.5MM NADP')
    if self.re_search(pdb, r'[12]hdd'):
        line = self.re_substitute(line, r'DROP STARTS AT.*', '')
    if self.re_search(pdb, r'1he[2-5]'):
        line = self.re_substitute(line, r'NADP\s+ADDED.*', r'2.5MM NADP')
    if self.re_search(pdb, r'1hfw|1hg[01]'):
        line = self.re_substitute(line, r'CROSSLINKING.*', '')
    if self.re_search(pdb, r'1hiz'):
        line = self.re_substitute(line, r'R.*', r'0.75-1.5M AMMONIUM SULFATE, 8% (W/V) MPD, 5-6 MG/ML PROTEIN')
    if self.re_search(pdb, r'1hkb'):
        line = self.re_substitute(line, r'AND PRESUMABLE.*', '')
    if self.re_search(pdb, r'1hkc'):
        line = self.re_substitute(line, r'PROTEIN SAMPLES.*', '')
    if self.re_search(pdb, r'1hke'):
        line = self.re_substitute(line, r'IMIDAZOLE\/MALATE 0\.2M', r',0.2M IMIDAZOLE MALATE,')
    if self.re_search(pdb, r'1hl8'):
        line = self.re_substitute(line, r'JEFFAMINE.*600', r'JEFFAMINE M-600,')
    if self.re_search(pdb, r'1hql'):
        line = self.re_substitute(line, r'5 EQU\.\s+SUGAR', '')
    if self.re_search(pdb, r'1hu3'):
      line = self.re_substitute(line, r'ACETATE \(4\.6\)', r'ACETATE PH 4.6')
    if self.re_search(pdb, r'1hu[jk]'):
      line = self.re_substitute(line, r'.*', r'10MG/ML PROTEIN, 0.1M MES PH 6.5, 16-25% MPD')
    if self.re_search(pdb, r'1i5[89ab]'):
        line = self.re_substitute(line, r'PEG.*', r'33-36% PEG 8000, 0.8M AMMONIUM ACETATE, 0.085M SODIUM ACETATE PH 4.5')
    if self.re_search(pdb, r'1i5c'):
        line = self.re_substitute(line, r'PEG.*', r'33-36% PEG 8000, 0.8M AMMONIUM ACETATE, 0.085M SODIUM ACETATE PH 5.0')
    if self.re_search(pdb, r'1i5d'):
        line = self.re_substitute(line, r'SODIUM.*', r'0.1M SODIUM ACETATE, 1.9M AMMONIUM SULFATE, PH 4.7')
    if self.re_search(pdb, r'1i5z|1i6x'):
        line = self.re_substitute(line, r'(CAMP|20\:1 CAMP\:CRP)', '')
    if self.re_search(pdb, r'1i6i'):
        line = self.re_substitute(line, r'20MM AMPPCP.*', '')
        line = self.re_substitute(line, r'COLLECTING X\-RAY DATA', '')
    if self.re_search(pdb, r'1iau|1rzj'):
        line = self.re_substitute(line, r'.*RESERVOIR OF', '')
    if self.re_search(pdb, r'1ic1'):
        line = self.re_substitute(line, r'NA CACODYLATE', r'10MM SODIUM CACODYLATE') # correction from paper
    if self.re_search(pdb, r'1ihb|1ofc|1w25|2cia'):
        line = self.re_substitute(line, r'.*RESERVOIRE?', '')
        line = self.re_substitute(line, r'WITHIN.*', '')
    if self.re_search(pdb, r'1ijw|1jj[68]|1jk[opqr]'):
        line = self.re_substitute(line, r'CONCENTRATION\s+OF\s+PEG400.*', '')
    if self.re_search(pdb, r'1ik7'):
        line = self.re_substitute(line, r'TRIS', r'0.1M TRIS PH 8.0') # correction from paper
    if self.re_search(pdb, r'1ise'):
        line = self.re_substitute(line, r'PEG.*', r'PH 6.5, 10% PEG MME 350, 12% PEG 400, 1.8MM DECYL-B-D-MALTOPYRANOSIDE') # correction from paper
    if self.re_search(pdb, r'1j4b'):
        line = self.re_substitute(line, r'.*', r'100MM CACODYLATE PH 6.5, 18% PEG 8000, 200MM CALCIUM ACETATE')
    if self.re_search(pdb, r'1j6z'):
        line = self.re_substitute(line, r'PEG.*', r'22% PEG MME 2000, 200MM CALCIUM ACETATE, 10MM TRIS PH 7')
    if self.re_search(pdb, r'1j72'):
        line = self.re_substitute(line, r'0 AMMONIUM', r'0M AMMONIUM')
    if self.re_search(pdb, r'1j9m'):
        line = self.re_substitute(line, r'.*', r'100MM TRIS, 30% PEG 6K, 0.4M NACL')
    if self.re_search(pdb, r'1ja3'):
        line = self.re_substitute(line, r'.*', r'100MM CHESS, 12% PEG 8000, 0.2M NACL')
    if self.re_search(pdb, r'1ji[sty]'):
        line = self.re_substitute(line, r'NA\-ACETATE', r'40MM NA-ACETATE')
    if self.re_search(pdb, r'1jj[013]'):
        line = self.re_substitute(line, r'NA\-ACETATE', r'40MM NA-ACETATE')
    if self.re_search(pdb, r'1jj8'):
        line = self.re_substitute(line, r'.* SOLUTION CONTAINS', '')
    if self.re_search(pdb, r'1jma'):
        line = self.re_substitute(line, r'TRIS-HCL 100MM', r'100MM TRIS CHLORIDE')
    if self.re_search(pdb, r'1jml'):
        line = self.re_substitute(line, r'CACODYLATE', r'50MM CACODYLATE, PH 6.5') # correction from paper
    if self.re_search(pdb, r'1jn1|1nt0|1pn1'):
        line = self.re_substitute(line, r'1 MES', r'1M MES')
    if self.re_search(pdb, r'1joc'):
        line = self.re_substitute(line, r'INS\(1,3\)P2', r'INOSITOL 1,3-DIPHOSPHATE')
    if self.re_search(pdb, r'1joe'):
        line = self.re_substitute(line, r'METHOD.*', r'25% PEG 4000, 0.2M MAGNESIUM CHLORIDE, 0.1M TRIS PH 8.5')
    if self.re_search(pdb, r'1joi|3std'):
        line = self.re_substitute(line, r'(\d) TRIS', r'\1M TRIS')
    if self.re_search(pdb, r'1jot'):
        line = self.re_substitute(line, r'0\.2', r'0.2M')
    if self.re_search(pdb, r'1jqu'):
        line = self.re_substitute(line, r'PIPES', r'0.1M PIPES') # correction from paper
    if self.re_search(pdb, r'1jsf'): # FIXME: Check 3M concentration using paper
        line = self.re_substitute(line, r'SOLUTION\s*WITH PH 4\.5 ACETATE BUFFER AND', r', 3M ACETATE PH4.5,')
    if self.re_search(pdb, r'1jsq'):
        line = self.re_substitute(line, r'A-DDM', r'DODECYL-ALPHA-D-MALTOSIDE, 20MM TRIS, 100-200MM CITRATE PH 4.8-5.4') # correction from paper
    if self.re_search(pdb, r'1jsv'):
        line = self.re_substitute(line, r'BETA', r'0.1% BETA') # correction from paper
    if self.re_search(pdb, r'1jy5'):
        line = self.re_substitute(line, r'NACL.*', r'0.2M NACL, 0.1M ACETATE PH 4.6, 30% MPD') # correction from paper
    if self.re_search(pdb, r'1k6y'):
      line = self.re_substitute(line, r'NAH2PO4/1\.0', r'NAH2PO4, 1.0M')
    if self.re_search(pdb, r'1k9[ij]|[12357]r1r|1rts|2tsr'):
        line = self.re_substitute(line, r'PROTEIN SOLUTION CONTAIN.*', '')
        line = self.re_substitute(line, r'CA AC2\.', r'CALCIUM ACETATE')
    if self.re_search(pdb, r'1k9p'):
      line = self.re_substitute(line, r'EGTA.*', r'2MM EGTA')
    if self.re_search(pdb, r'1kao'):
      line = self.re_substitute(line, r'.*', r'25% PEG 6K, 100MM TRIS PH 8, 100MM MAGNESIUM CHLORIDE')
    if self.re_search(pdb, r'1kc7'): #|1lci'):
        line = self.re_substitute(line, r'SOLUTION:? .*', '')
    if self.re_search(pdb, r'1kd7'):
        line = self.re_substitute(line, r'.* ACETATESOLUTION OF', '')
    if self.re_search(pdb, r'1kek'):
      line = self.re_substitute(line, r'.*', r'10-15% PEG 6K')
    if self.re_search(pdb, r'1kez'):
        line = self.re_substitute(line, r'HEPES 7\.5', r'100MM HEPES PH 7.5, 2MM DTT') # correction from paper
    if self.re_search(pdb, r'1ki[234678m]'):
        line = self.re_substitute(line, r'\bDT\.\)?', r' DEOXYTHYMIDINE')
        line = self.re_substitute(line, r'EXCHANGE.*', '')
    if self.re_search(pdb, r'1kj3'):
      line = self.re_substitute(line, r'N2HPO4', r'NA2HPO4')
    if self.re_search(pdb, r'1kr3|1l9y'):
        line = self.re_substitute(line, r'10MICROM', r'10 UM')
    if self.re_search(pdb, r'1ku1'):
        line = self.re_substitute(line, r'OR SODIUM CITRATE', '')
    if self.re_search(pdb, r'2ptw|2ptx|2pty|2ptz|2pu0|2pu1'):
        line = self.re_substitute(line, r'OR ZNCL2', '')
    if self.re_search(pdb, r'1ku9'):
        line = self.re_substitute(line, r'TRIS', r'0.1M TRIS') # correction from paper
    if self.re_search(pdb, r'1kvl'):
        line = self.re_substitute(line, r'THE\s+CRYSTAL\s+WAS.*', '')
    if self.re_search(pdb, r'1kw2'):
        line = self.re_substitute(line, r'.*', r'28% PEG 200, 0.1M SODIUM ACETATE')
    if self.re_search(pdb, r'1kxp'):
        line = self.re_substitute(line, r'.*', r'12% PEG 8K, 200MM MAGNESIUM ACETATE, 100MM SODIUM CACODYLATE, 20% GLYCEROL')
    if self.re_search(pdb, r'1kxq'):
        line = self.re_substitute(line, r'.*', r'0.8M PHOSPHATE')
    if self.re_search(pdb, r'1kxt'):
        line = self.re_substitute(line, r'.*', r'15% PEG 20000, 0.2M IMIDAZOLE MALATE')
    if self.re_search(pdb, r'1kxv'):
        line = self.re_substitute(line, r'.*', r'32% PEG 4K, 0.1M SODIUM CITRATE, 0.2M AMMONIUM ACETATE')
    if self.re_search(pdb, r'1l2s'):
        line = self.re_substitute(line, r'\(STC\)', '')
    if self.re_search(pdb, r'1l5t'):
        line = self.re_substitute(line, r'CONCENTRATED SOLUTION OF THE\s+PROTEIN \(50-80 MG ML-1\)', r'50 MG/ML PROTEIN')
    if self.re_search(pdb, r'1l6y'):
      line = self.re_substitute(line, r'PEG 3350', r'1-6% PEG 3350') # fix from paper
    if self.re_search(pdb, r'1l9l'):
        line = self.re_substitute(line, r'WITH\s+SODIUM\s+HYDROXIDE', '')
    if self.re_search(pdb, r'1lci'):
      line = self.re_substitute(line, r'LUCIFERASE', r'PROTEIN')
    if self.re_search(pdb, r'3lck'):
      line = self.re_substitute(line, r'AS A WELL SOLUTION\.', '')
    if self.re_search(pdb, r'1ld[afi]'):
        line = self.re_substitute(line, r'GLPF AT 15-20 MG/ML', r'15-20 MG/ML PROTEIN')
        line = self.re_substitute(line, r'35 MM,', r'35 MM')
        line = self.re_substitute(line, r', MGCL2', r'300MM MGCL2') #Fix from paper...
        line = self.re_substitute(line, r'MMDTT', r'MM DTT')
    if self.re_search(pdb, r'1ld[oq]'):
        line = self.re_substitute(line, r'1 IMMIDAZOLE', r'1M IMMIDAZOLE')
        line = self.re_substitute(line, r'0,1M', r'0.1M')
    if self.re_search(pdb, r'1lf8'):
      line = self.re_substitute(line, r'CAPS ', r'CAPS PH')
    if self.re_search(pdb, r'1li[57]'):
        line = self.re_substitute(line, r'CACODYLATE', '')
        line = self.re_substitute(line, r'BUFFER', r'CACODYLATE')
    if self.re_search(pdb, r'1lj9'):
      line = self.re_substitute(line, r'PEG 3350, 22\%,', r'22% PEG 3350')
    if self.re_search(pdb, r'1lkf'):
      line = self.re_substitute(line, r'\bOR .*', '')
    if self.re_search(pdb, r'1ll1'):
      line = self.re_substitute(line, r'PH IN THE DROP NEAR', r'PH')
    if self.re_search(pdb, r'1lpi'):
      line = self.re_substitute(line, r'THE.*', r'20MG/ML PROTEIN')
    if self.re_search(pdb, r'1lt3|1lt4'):
      line = self.re_substitute(line, r'USING THE 3 LAYER CAPPILARY METHOD', '')
    if self.re_search(pdb, r'1lu2'):
        line = self.re_substitute(line, r'BLOOD GROUP A', '')
    if self.re_search(pdb, r'1lwd|1m6z|1m70|1r0v|1rke|1st[04]'):
      line = self.re_substitute(line, r'PH 7\.70', '')
      line = self.re_substitute(line, r'PH 6\.6', '')
      line = self.re_substitute(line, r'PH 8\.0', '')
      line = self.re_substitute(line, r'PH 5\.0', '')
    if self.re_search(pdb, r'1lx[6c]'):
        line = self.re_substitute(line, r'2M\(NH4\)2SO4', r'2M AMMONIUM SULFATE')
    if self.re_search(pdb, r'1lzw'):
        line = self.re_substitute(line, r'PH 5\.6', r'0.1M SODIUM CITRATE PH 5.6') #Fix from paper...
    if self.re_search(pdb, r'1m06'):
        line = self.re_substitute(line, r'MM-M', r'MM M')
    if self.re_search(pdb, r'1m5t|1mav|1mb[03]'):
        line = self.re_substitute(line, r'MES.*', r'32% PEG MME 550, 40MM MES PH 6.0, 5MM DTT, 2MG/ML PROTEIN')
    if self.re_search(pdb, r'1m80'):
        line = self.re_substitute(line, r'FOR THE.*', '')
    if self.re_search(pdb, r'1ml0'):
        line = self.re_substitute(line, r'200MM,', r',200MM')
    if self.re_search(pdb, r'1mq[56]'):
        line = self.re_substitute(line, r'.*', r'12-17MG/ML PROTEIN, 21% PEG 1500, 10MM CACL2')
    if self.re_search(pdb, r'1mr7'):
        line = self.re_substitute(line, r'.*', r'2.7M SODIUM FORMATE')
    if self.re_search(pdb, r'1mvt'):
        line = self.re_substitute(line, r'PHOSPHATE', r'0.1M PHOSPHATE') # correction from paper
    if self.re_search(pdb, r'1my7'):
        line = self.re_substitute(line, r'0\.L M SODIUM HEPES', r'0.1 M SODIUM HEPES')
    if self.re_search(pdb, r'1n1c'):
        line = self.re_substitute(line, r'AMMONIUM.*', r'1.6M AMMONIUM SULFATE, 100MM MES PH 6.4') # correction from paper
    if self.re_search(pdb, r'1n57'):
        line = self.re_substitute(line, r'PEG 3350', r'25% PEG 3350') # fix from paper
    if self.re_search(pdb, r'1n16'):
        line = self.re_substitute(line, r'NICKEL, CHLORIDE', r'NICKEL CHLORIDE')
    if self.re_search(pdb, r'1n8n|1n9k'):
        line = self.re_substitute(line, r'APHA 6MG/ML', r'6MG/ML PROTEIN')
    if self.re_search(pdb, r'2ncd'):
        line = self.re_substitute(line, r'.*RESERVOIR WAS', '')
    if self.re_search(pdb, r'1ncj'):
        line = self.re_substitute(line, r'REMARK\s+280', '')
        line = self.re_substitute(line, r'UO2 ACETATE', r'URANYL ACETATE')
    if self.re_search(pdb, r'1ni2'):
        line = self.re_substitute(line, r'10.*', r'10-15% PEG MME 2000, 15% GLYCEROL, 10% ISOPROPANOL, 0.1M SODIUM HEPES PH 8.1') # correction from paper
    if self.re_search(pdb, r'2nll|2trh'):
        line = self.re_substitute(line, r'\\', '')
    if self.re_search(pdb, r'1m9p|1nej'):
        line = self.re_substitute(line, r'CHLORIDE ANION TRACES', '')
    if self.re_search(pdb, r'1njs'):
        line = self.re_substitute(line, r'HEPES 6\.7-7\.0', r'HEPES, PH 6.7-7.0')
    if self.re_search(pdb, r'1nko'):
        line = self.re_substitute(line, r'PEG 4000 20\%, NACL 0\.2 M', r'20% PEG 4000, 0.2M NACL')
    if self.re_search(pdb, r'1nlr'):
        line = self.re_substitute(line, r'ACETATE BUFFER METHOD', '')
    if self.re_search(pdb, r'1nmc'):
        line = self.re_substitute(line, r'.*', r'1.3M POTASSIUM PHOSPHATE PH 6.8')
    if self.re_search(pdb, r'1nm[xyz]|1nn[0135]'):
        line = self.re_substitute(line, r'5%\s*(STERILE)?\s*FILTERED DEAD SEA WATER,', '')
        line = self.re_substitute(line, r'^PEG 3350', r'15-20% PEG 3350')
    if self.re_search(pdb, r'1nov'):
        line = self.re_substitute(line, r'.*', r'0.24-0.28M SODIUM CITRATE PH 6.0, 0.1% BETA OCTYLGLUCOPYRANOSIDE, 7MG/ML VIRUS')
    if self.re_search(pdb, r'1nuc'):
        line = self.re_substitute(line, r'PROTEIN.*', r'2MG/ML PROTEIN, 21% MPD,')
    if self.re_search(pdb, r'1nvg'):
        line = self.re_substitute(line, r'PH\s+NULL', '')
    if self.re_search(pdb, r'1nwp'):
        line = self.re_substitute(line, r'BY MIXING.*', r'30-36% PEG 8000, 5MM TRIS PH 6.5-7.5, 100MM SODIUM CHLORIDE, 180MM ZINC ACETATE')
    if self.re_search(pdb, r'1nza'):
        line = self.re_substitute(line, r'NA ACETATE 1\.65M, MES 0\.1M', r'1.65M NA ACETATE, 0.1M MES')
    if self.re_search(pdb, r'1o0u|1o1x|1o6a|3kh8|3ksm'):
        line = self.re_substitute(line, r'\(\+/?\-\)-2-\s*METHYL?-2,4-\s*PENTANEDIOL', r'MPD')
    if self.re_search(pdb, r'1o13'):
        line = self.re_substitute(line, r'PHOSPHATE-CITRATE 40\%\(V/V\) PEG\s+-600', r'CITRATE PHOSPHATE, 40% (V/V) PEG 600')
    if self.re_search(pdb, r'1o20'):
        line = self.re_substitute(line, r'5000\(30\%\), 0.06M TRIS\s+CL\(1M\), 0.04M TRIS_BASE\(1M\)', r'5000, 0.05M TRIS CHLORIDE,')
    if self.re_search(pdb, r'1o3u'):
        line = self.re_substitute(line, r'IMIDAZOLE', r'100MM IMIDAZOLE')
    if self.re_search(pdb, r'1o3w'):
        line = self.re_substitute(line, r'\bAND .*', r'PH 7.2,')
    if self.re_search(pdb, r'1o4w'):
        line = self.re_substitute(line, r'MES', r'100MM MES')
    if self.re_search(pdb, r'1o50'):
        line = self.re_substitute(line, r'CRYSTAL\s+2.*', '')
    if self.re_search(pdb, r'1o5e'):
        line = self.re_substitute(line, r'SOAK.*', r'PH 6.5')
    if self.re_search(pdb, r'1o5z'):
        line = self.re_substitute(line, r'W/V/\s+PEG 3350', r'W/V PEG 3350')
    if self.re_search(pdb, r'1o6k'):
        line = self.re_substitute(line, r'PROTEIN\s+20 PEG 4K', r'PROTEIN, 20% PEG 4000')
    if self.re_search(pdb, r'1o6t|1q7r'):
        line = self.re_substitute(line, r'.* RESEVOIR\:', '')
        line = self.re_substitute(line, r'CRYSTALS GREW.*', '')
    if self.re_search(pdb, r'1o7e'):
        line = self.re_substitute(line, r'AMMONIUM.*', r'1.5M AMMONIUM SULFATE, 0.1M SODIUM CACODYLATE PH 6.5')
    if self.re_search(pdb, r'1o7[ghmnpw]'):
        line = self.re_substitute(line, r'.*', r'2M AMMONIUM SULFATE, 0.1M MES, 2-3% DIOXANE')
    if self.re_search(pdb, r'1o82'):
        line = self.re_substitute(line, r'SODIUM.*', r'M SODIUM ACETATE PH 4.5, 12% W/V PEG 4000, 10MG/ML PROTEIN') # a guess
    if self.re_search(pdb, r'1o9r'):
        line = self.re_substitute(line, r'HEP.*', r'16%-24% V/V ETHYLENE GLYCOL, 0.1M HEPES PH 7.0-7.8')
    if self.re_search(pdb, r'1oa[79]'):
        line = self.re_substitute(line, r'PEG 4000 15\% W/V', r'15% W/V PEG 4000')
    if self.re_search(pdb, r'1oab'):
        line = self.re_substitute(line, r'TRIS.*', r'10MM TRIS PH 7.5-9.0, 20% PEG 3400, 5% GLYCEROL, 13-17MG/ML PROTEIN')
    if self.re_search(pdb, r'1oah'):
        line = self.re_substitute(line, r'CACL2.*', r'0.2M CACL2, 0.1M HEPES PH 7.5, 80MM 3-(DECYL-METHYLAMMONIUM)PROPANE-1-SULFONATE, 10MG/ML PROTEIN')
    if self.re_search(pdb, r'1ob0|1c8c|1sih|1sii|2o1i'):
        line = self.re_substitute(line, r'EQUILIBRATED\s+AGAINST.*', '')
        line = self.re_substitute(line, r'.* RESERVOIR\s+SOLUTION', '')
    if self.re_search(pdb, r'1ob3'):
        line = self.re_substitute(line, r'PEG .*', r'8-16% PEG 8K, 2-8% ISOPROPANOL')
    if self.re_search(pdb, r'1ob9'):
        line = self.re_substitute(line, r'PASSED THROUGH .*', '')
    if self.re_search(pdb, r'1obg'):
        line = self.re_substitute(line, r'ASP\. ASID', r'ASPARTIC ACID')
        line = self.re_substitute(line, r'\b5\b', r'23MG/ML PROTEIN') #from literature
    if self.re_search(pdb, r'1ocb'):
        line = self.re_substitute(line, r'.*SUBSTRATE', '')
    if self.re_search(pdb, r'1oc[su]|1dm3|2pth|1oi4|1gzg'):
        line = self.re_substitute(line, r'PH\s*7,5', r'PH 7.5') # comma replacement
        line = self.re_substitute(line, r'0,1 M', r'0.1 M')
        line = self.re_substitute(line, r'0,2M', r'0.2M')
        line = self.re_substitute(line, r'9,5', r'9.5')
    if self.re_search(pdb, r'1ocq'):
        line = self.re_substitute(line, r'.*', r'10MG/ML PROTEIN, 1.3M AMMONIUM SULFATE')
    if self.re_search(pdb, r'1ocx'):
        line = self.re_substitute(line, r'ADDITION.*', '')
    if self.re_search(pdb, r'1od[mn]'):
        line = self.re_substitute(line, r'\(', '')
    if self.re_search(pdb, r'1odo'):
        line = self.re_substitute(line, r'0 5', r'0.5')
    if self.re_search(pdb, r'1oer'):
        line = self.re_substitute(line, r'A 65 .*', '')
    if self.re_search(pdb, r'1of5'):
        line = self.re_substitute(line, r'PEG 3000 20\%', r', 20% PEG 3000')
    if self.re_search(pdb, r'1of[pq]'):
        line = self.re_substitute(line, r'TRIS PH 7\.5-9\.0 10 MM', r'10MM TRIS PH 7.5-9.0')
    if self.re_search(pdb, r'1ofz'):
        line = self.re_substitute(line, r'PLUS.*', r'10MG/ML PROTEIN, 137UG/ML L-FUCOSE')
    if self.re_search(pdb, r'1og6'):
        line = self.re_substitute(line, r'.*', r'0.2M IMIDAZOLE MALATE PH 7.0, 0.1M AMMONIUM SULFATE, 16% PEG')
    if self.re_search(pdb, r'1ogw'):
        line = self.re_substitute(line, r'.*UBIQUITIN\s+AND\s+5\s+MUL', r'20MG/ML PROTEIN,')
    if self.re_search(pdb, r'1oh9'):
        line = self.re_substitute(line, r'SODIUM.*', r'0.1M SODIUM ACETATE PH 4.6, 0.25-0.4M AMMONIUM CITRATE')
    if self.re_search(pdb, r'1oh[ab]'):
        line = self.re_substitute(line, r'SODIUM.*', r'0.1M SODIUM ACETATE PH 4.6, 0.15-0.3M AMMONIUM SULFATE')
    if self.re_search(pdb, r'1oi1'):
        line = self.re_substitute(line, r'PEG200.*', '')
    if self.re_search(pdb, r'1ojj'):
        line = self.re_substitute(line, r'280 ', '')
    if self.re_search(pdb, r'1ojr'):
        line = self.re_substitute(line, r'AND.*', r'35% (V/V) DIOXANE')
    if self.re_search(pdb, r'1ojt'):
        line = self.re_substitute(line, r'PRISM.*', '')
    if self.re_search(pdb, r'1okz'):
        line = self.re_substitute(line, r'0\.25 UL COBALTOUS', r'0.02M COBALT')  #fix from paper
    if self.re_search(pdb, r'1olx'):
        line = self.re_substitute(line, r'SERIALLY\s+DILUTED.*', '')
    if self.re_search(pdb, r'1omo'):
        line = self.re_substitute(line, r'MPD \(\~20\%\)', r'20% MPD')
    if self.re_search(pdb, r'1ooe'):
        line = self.re_substitute(line, r'10\s*MM\s+HEPES.*', '')
    if self.re_search(pdb, r'1opc'):
        line = self.re_substitute(line, r'POLYETHYLENEGLYCOL-MONOMETHYLETHER \(PMME\)', r'PEG MME')
    if self.re_search(pdb, r'1oql'):
        line = self.re_substitute(line, r'GLYCINE', r'0.1M GLYCINE')  #fix from paper
    if self.re_search(pdb, r'1or[23]'):
        line = self.re_substitute(line, r'\bNO.*', '')
    if self.re_search(pdb, r'1oth'):
        line = self.re_substitute(line, r'.*', r'2% PEG 400, 2M AMMONIUM SULFATE, 0.1M SODIUM HEPES PH 7.5') #correction from paper
    if self.re_search(pdb, r'1ot[vw]'):
        line = self.re_substitute(line, r'1.*', r'1.2M AMMONIUM SULFATE, 0.1M SODIUM MES PH 6.0') #correction from paper
    if self.re_search(pdb, r'1ovn'):
        line = self.re_substitute(line, r'MIXING.*', r'0.1M MES PH 6.1, 0.1M CSCL, 2MM CACL2, 16% (V/V) PEG 300,')
    if self.re_search(pdb, r'1ov8'):
        line = self.re_substitute(line, r'HEPES', r'0.1M HEPES')
    if self.re_search(pdb, r'1ovu'):
        line = self.re_substitute(line, r'CO.*', r'30MM COBALT ACETATE, 100MM TRIS PH 7.5, 43% PEG 400')
    if self.re_search(pdb, r'1oxm'):
        line = self.re_substitute(line, r'PEG.*', r'14% W/V PEG 6000, 0.1M HEPES PH 7.0, 15 MG/ML PROTEIN') #correction from paper
    if self.re_search(pdb, r'1p0z|1pgv|1spv|3ubp'):
        line = self.re_substitute(line, r'PROTEIN SOLUTION:.*', '')
    if self.re_search(pdb, r'1p8d'):
        line = self.re_substitute(line, r'PEG3350-8000', r'PEG 3350')
    if self.re_search(pdb, r'1pd2|1a52|1af9|1e42'):
        line = self.re_substitute(line, r'PROTEIN\s*(SOLUTION|STOCK):?.*', '')
    if self.re_search(pdb, r'1pe0'):
        line = self.re_substitute(line, r'100 MM BIS-TRIS\(7\.0\)', r'100 MM BIS TRIS PH 7.0')
    if self.re_search(pdb, r'1pew'):
        line = self.re_substitute(line, r'AMM\.', r'AMMONIUM')
    if self.re_search(pdb, r'3pgh|[456]cox'):
        line = self.re_substitute(line, r'(\d) MGCL2', r'\1MM MGCL2')
    if self.re_search(pdb, r'1pj6'):
        line = self.re_substitute(line, r'(\d) MGCL2', r'\1M MGCL2')
    if self.re_search(pdb, r'1psr'):
        line = self.re_substitute(line, r'.*', r'20-30% PEG MME 2000, 50-300MM AMMONIUM SULFATE, 100MM SODIUM ACETATE PH 4.6-7.5')
    if self.re_search(pdb, r'1pt3|1s7j'):
        line = self.re_substitute(line, r'PH 7\.50', '')
    if self.re_search(pdb, r'1pu2'):
        line = self.re_substitute(line, r'0\.1 TRIS.*', '') #correction from paper
    if self.re_search(pdb, r'1pug'):
        line = self.re_substitute(line, r'MSODIUM', r'M SODIUM')
    if self.re_search(pdb, r'1pv2'):
        line = self.re_substitute(line, r'PH 7\.5\.5G', r'PH 7.5')
    if self.re_search(pdb, r'1pvl'):
        line = self.re_substitute(line, r'TRIS AND MES', r'TRIS MES')
    if self.re_search(pdb, r'1pvm'):
        line = self.re_substitute(line, r'IN PROTEIN', '')
    if self.re_search(pdb, r'1pys'):
        line = self.re_substitute(line, r'AMMONIUM SULFATE 28\%', r'28% AMMONIUM SULFATE')
    if self.re_search(pdb, r'1pyy'):
        line = self.re_substitute(line, r'GLYCYL\-GLYCYL\-GLYCINE, N\- OCTANOYLSUCROSE', r'100MM GLYCYL-GLYCYL-GLYCINE, 2.9MM N-OCTANOYLSUCROSE') #correction form paper
    if self.re_search(pdb, r'1qa0|1qb[69no]'):
        line = self.re_substitute(line, r'SIX UL.*', '')
    if self.re_search(pdb, r'1qa[st]'):
        line = self.re_substitute(line, r'FRAGMENTS.*', '')
    if self.re_search(pdb, r'1qb0'):
        line = self.re_substitute(line, r'.*', r'10MG/ML PROTEIN, 1.8M AMMONIUM SULFATE, 0.5M NACL, 0.1M TRIS CHLORIDE, 0.25MM BME') #guess at bme units
    if self.re_search(pdb, r'1qbb'):
        line = self.re_substitute(line, r'DERIVATIZATION.*', '')
    if self.re_search(pdb, r'1qcj'):
        line = self.re_substitute(line, r'PTEORIC.*', r'50MM TRIS PH 8.0') #correction from paper
    if self.re_search(pdb, r'1qe3'):
        line = self.re_substitute(line, r'150.*', r'150MM LIS04, 100MM TRIS PH 8.25')
    if self.re_search(pdb, r'1qg3'):
        line = self.re_substitute(line, r'400.*', r'PEG 400') #correction from paper
    if self.re_search(pdb, r'1qgh'):
        line = self.re_substitute(line, r'PEG.*', r'19-25% PEG 1000, 0.1M MES PH 5.0-6.2')
    if self.re_search(pdb, r'1qh4'):
        line = self.re_substitute(line, r'15%\s+PE', r'15% PEG 8000,') #fix from paper...
    if self.re_search(pdb, r'1qh6'):
        line = self.re_substitute(line, r'AMM.*', r'30% AMMONIUM SULFATE, 0.1M NACL, 0.1M MES PH 6.5') 
    if self.re_search(pdb, r'1qh7'):
        line = self.re_substitute(line, r'AMM.*', r'30% AMMONIUM SULFATE, 0.1M MES PH 6.5') 
    if self.re_search(pdb, r'1qhl'):
        line = self.re_substitute(line, r'50MG\/ML', r'50MG/ML PROTEIN') 
    if self.re_search(pdb, r'1qho|1qhp'):
        line = self.re_substitute(line, r'PEH 1450', r'PEG 1450') #fix from paper...
    if self.re_search(pdb, r'1qhu'):
        line = self.re_substitute(line, r'.*', r'40MG/ML PROTEIN, 19-22% PEG 4K, 0.05M TRIS CHLORIDE PH 7.5, 0.05-0.5M EDTA, 0.2M NACL') #a guess at the NACL units
    if self.re_search(pdb, r'1qi1'):
      line = self.re_substitute(line, r'AMMONIUM SULFATE 2.0 M', r'2.0M AMMONIUM SULFATE')
    if self.re_search(pdb, r'1qix'):
      line = self.re_substitute(line, r'25 MG/ML.*', r'25 MG/ML PROTEIN')
    if self.re_search(pdb, r'1qjm'):
      line = self.re_substitute(line, r'.* 40MG\/ML', r'40MG/ML PROTEIN')
    if self.re_search(pdb, r'1qll'):
      line = self.re_substitute(line, r'FOR APPROX.*', '')
    if self.re_search(pdb, r'1qlv'):
      line = self.re_substitute(line, r'25 MG.*\(', '')
      line = self.re_substitute(line, r'\)', '')
    if self.re_search(pdb, r'1qm4'):
      line = self.re_substitute(line, r'0.1.*', r'0.1M HEPES PH 7.5')
    if self.re_search(pdb, r'1qmd'):
      line = self.re_substitute(line, r'PH 4\.7 OR 4\.8', r'PH 4.7-4.8')
    if self.re_search(pdb, r'1qnn'):
      line = self.re_substitute(line, r'WITHIN.*', '')
    if self.re_search(pdb, r'1qnu'):
      line = self.re_substitute(line, r'SA\s+NH4SO4', r'AMMONIUM SULFATE')
    if self.re_search(pdb, r'1qo0'):
      line = self.re_substitute(line, r'AMIC\-AMIR COMPLEX', r'PROTEIN')
    if self.re_search(pdb, r'1qqf'):
      line = self.re_substitute(line, r'K.*', r'50MM POTASSIUM PHOSPHATE')
    if self.re_search(pdb, r'1qr4'):
        line = self.re_substitute(line, r'10-100 MM MGCL2/CACL2,', r'50-100 MM MGCL2') #fix from paper...
    if self.re_search(pdb, r'1qrh|1qri'):
        line = self.re_substitute(line, r'RESERVOIR: .*', '')
    if self.re_search(pdb, r'1qtn'):
        line = self.re_substitute(line, r'4 SODIUM', r'4M SODIUM') 
    if self.re_search(pdb, r'1r0a'):
        line = self.re_substitute(line, r'PH,', r'PH')
    if self.re_search(pdb, r'1r4w'):
        line = self.re_substitute(line, r'DROP:.*', r'PH 4.0,')
    if self.re_search(pdb, r'1r5c'):
        line = self.re_substitute(line, r'DINUCLEOTIDE.*', r'PH 5.4,')
    if self.re_search(pdb, r'1r6a'):
        line = self.re_substitute(line, r'NA.*', r'0.1M SODIUM CITRATE, 0.5M AMMONIUM SULFATE, 1.2M LITHIUM SULFATE, PH 5.8') #correction from paper
    if self.re_search(pdb, r'1r6c'):
        line = self.re_substitute(line, r'.* MIXED 1:1', '')
    if self.re_search(pdb, r'1r6w'):
        line = self.re_substitute(line, r'.*', r'15MG/ML PROTEIN, 12-13% PEG MME 5000, 100MM SODIUM ACETATE PH 5.5, 60MM MGCL2, 2.5MM SHCHC')
    if self.re_search(pdb, r'1r76'):
        line = self.re_substitute(line, r'HEPES.*', r'15% ISOPROPANOL, 20% PEG 4000, 0.1M IMIDAZOLE PH 7.8') #correction from paper
    if self.re_search(pdb, r'1r7s'):
        line = self.re_substitute(line, r'2NM', r'0.002MM')
    if self.re_search(pdb, r'1r85'):
        line = self.re_substitute(line, r'25.*', r'14% PEG 4000, 10MM ZNSO4, 0.1M MES PH 6.45') #correction from paper
    if self.re_search(pdb, r'1r87'):
        line = self.re_substitute(line, r'MES', r'0.1M MES')
    if self.re_search(pdb, r'1r9h'):
        line = self.re_substitute(line, r'SEEDING.*', r'PH 6.5')
    if self.re_search(pdb, r'4rhn'):
      line = self.re_substitute(line, r'\,N0\.1', r' 0.1')
    if self.re_search(pdb, r'1rih'):
      line = self.re_substitute(line, r'\(.*\)', '') #correction from paper
    if self.re_search(pdb, r'1rlu|1rq[27]'):
      line = self.re_substitute(line, r'ETHYL.*', r'PH 5.6')
    if self.re_search(pdb, r'1rlz'):
        line = self.re_substitute(line, r'NAD', r'3MM NAD') #correction from paper
    if self.re_search(pdb, r'1rm[7qtwy]'):
      line = self.re_substitute(line, r'.*APHA', r'PROTEIN')
    if self.re_search(pdb, r'1roz|1rqd'):
      line = self.re_substitute(line, r'1.*', r'64-70% V/V MPD, 0.1M TRIS PH 8.0, 3MM NAD, 100MM KCL') #correction from paper
    if self.re_search(pdb, r'1rqw'):
      line = self.re_substitute(line, r'.*', r'40MG/ML PROTEIN, 0.05M ADA PH 6.8, 0.6M NA/K TARTRATE, 20% GLYCEROL')
    if self.re_search(pdb, r'1rtx'):
      line = self.re_substitute(line, r'1 CADMIUM', r'1M CADMIUM')
    if self.re_search(pdb, r'1ru7'):
      line = self.re_substitute(line, r'TRISHCL, KSCN', r'0.1M TRIS CHLORIDE, 0.15M KSCN')
    if self.re_search(pdb, r'2lkf|1rux'):
      line = self.re_substitute(line, r'\(', '')
      line = self.re_substitute(line, r'\)', '')
    if self.re_search(pdb, r'1rya|1vdc'):
        line = self.re_substitute(line, r'\(OR [-A-Z0-9%, ]+\)', '')
    if self.re_search(pdb, r'1ryq|1s36|1sen|1sgw|1she|1sl[78]|1twl|1vjk|1vk1|1xi[3689]|1xe1|1xg7|1xhc|1xk[8c]|1xma|1y8[012]|1yb[3xz]|1ycy|1yd7|1yem'):
        line = self.re_substitute(line, r'MODIFIED.*', '')
    if self.re_search(pdb, r'1s0p'):
      line = self.re_substitute(line, r'MM[- ]+MERCAPTOETHANOL', r'MM MERCAPTOETHANOL')
    if self.re_search(pdb, r'1s14'):
      line = self.re_substitute(line, r'POTASSIUM TARTRATE,  SODIUM CHLORIDE', r'0.2M POTASSIUM TARTRATE, 0.1M NACL') #fix from paper
    if self.re_search(pdb, r'1s20'):
      line = self.re_substitute(line, r'THE PROTEIN.*', r'PH 7.5,')
    if self.re_search(pdb, r'1s2e'):
      line = self.re_substitute(line, r'HEPES\-NA\s+BUFFER', r'0.1M SODIUM HEPES') #fix from paper
    if self.re_search(pdb, r'1s50'):
      line = self.re_substitute(line, r'2 TRIS.*', r'2MM TRIS, 20MM NACL, 1MM EDTA, 10MM SODIUM GLUTAMATE, PH 8.0') #fix from author
    if self.re_search(pdb, r'1s6t'):
      line = self.re_substitute(line, r'PEG', r'20% PEG')
    if self.re_search(pdb, r'1s7y'):
      line = self.re_substitute(line, r'10.*', r'10MM CITRATE, 20MM NACL, 1MM EDTA, 10MM SODIUM GLUTAMATE, PH 4.8') #fix from author
    if self.re_search(pdb, r'1sbf'):
      line = self.re_substitute(line, r'.*', r'34MG/ML PROTEIN, 755UM SUGAR, 0.1M HEPES PH 7.2, 1MM CACL2, 1MM MNCL2, 0.5M NACL')
    if self.re_search(pdb, r'1sc1'):
      line = self.re_substitute(line, r'WAS ADDED.*', r' PH 7.4')
    if self.re_search(pdb, r'1sc4'):
      line = self.re_substitute(line, r'MALONATE-BOUND.*', '')
    if self.re_search(pdb, r'1sfh'):
      line = self.re_substitute(line, r'.*', r'2.5M SODIUM POTASSIUM PHOSPHATE PH 5.5')
    if self.re_search(pdb, r'1sfi'):
        line = self.re_substitute(line, r'6MM C', r'6MM CALCIUM') # FIXME: calcium what?
    if self.re_search(pdb, r'1sh8'):
      line = self.re_substitute(line, r'NAFORM 2M\, 0\.1M NAACET\.', r'2M SODIUM FORMATE, 0.1M SODIUM ACETATE')
    if self.re_search(pdb, r'1sl6'):
      line = self.re_substitute(line, r'1 HEPES', r'1M HEPES')
    if self.re_search(pdb, r'1swb'):
      line = self.re_substitute(line, r'5\.5H', '')
    if self.re_search(pdb, r'1swt'):
      line = self.re_substitute(line, r'.*CRYSTALLIZED IN', '')
    if self.re_search(pdb, r'1sx8'):
        line = self.re_substitute(line, r'PEG', r'15% PEG') # Correction from author
    if self.re_search(pdb, r'1sx[nqsz]'):
        line = self.re_substitute(line, r'SODIUM.*', '') 
    if self.re_search(pdb, r'1sz6'):
      line = self.re_substitute(line, r'0\.1M', r'0.1M GLYCINE')
    if self.re_search(pdb, r'1szj'):
      line = self.re_substitute(line, r'.*', r'8MG/ML PROTEIN, 0.5MM NAD, 1.0MM EDTA, 0.1M PHOSPHATE PH 6.1, 2.7M AMMONIUM SULFATE')
    if self.re_search(pdb, r'1t5r'):
        line = self.re_substitute(line, r'.*', r'20-25MG/ML PROTEIN, 30% JEFFAMINE M-600, 0.1M TRIS CHLORIDE PH 8.0-8.9')
    if self.re_search(pdb, r'1t8a'):
        line = self.re_substitute(line, r'.*', r'1.8M SODIUM POTASSIUM PHOSPHATE PH 6.5, 0.2M GUANIDINIUM CHLORIDE')
    if self.re_search(pdb, r'1t8q'):
        line = self.re_substitute(line, r'\bNM\b', r'MM') #another guess
    if self.re_search(pdb, r'7taa'):
        line = self.re_substitute(line, r'METHOD.*', '')
    if self.re_search(pdb, r'1tei'):
        line = self.re_substitute(line, r'.*', r'15% PEG')
    if self.re_search(pdb, r'1tf6'):
        line = self.re_substitute(line, r'CADAVERINE-2HCL', r'CADAVERINE')
    if self.re_search(pdb, r'1thk'):
        line = self.re_substitute(line, r'2\.5', r'2.5M') #another guess
    if self.re_search(pdb, r'1tiy'):
        line = self.re_substitute(line, r'NAN3', r'NA')
    if self.re_search(pdb, r'1tkk|1w15|1wa[012]'):
        line = self.re_substitute(line, r'SUSPEND(ING|ED).*', '')
    if self.re_search(pdb, r'1tmo'):
        line = self.re_substitute(line, r'CACODYLATE BUFFER PH 6\.5 0\.1M', r'0.1M CACODYLATE BUFFER PH 6.5')
    if self.re_search(pdb, r'1tol|2h5x'):
        line = self.re_substitute(line, r'AS A PRECIPITANT.*', '')
    if self.re_search(pdb, r'1toq|1tp8'):
        line = self.re_substitute(line, r'METHYL ALPHA GALACTOSE', '') #ligand, not really used for crystallization (paper)
    if self.re_search(pdb, r'1s0l|1too|1tp0'):
        line = self.re_substitute(line, r'29% AMMONIUM SULFATE W/V', r'29% W/V AMMONIUM SULFATE')
    if self.re_search(pdb, r'1tqc'):
        line = self.re_substitute(line, r'SODIUM.*', r'0.1M SODIUM CITRATE, 18-24% PEG 8000, 0.2M AMMONIUM ACETATE, PH 6.3') #correction from paper
    if self.re_search(pdb, r'1tr0'):
        line = self.re_substitute(line, r'PEG.*', r'20% PEG 3000, 0.2M NACL, 0.1M HEPES PH 7.5') #correction from paper
    #if self.re_search(pdb, r'1tr9'):
    #    line = self.re_substitute(line, r'CRYO.*', '') 
    if self.re_search(pdb, r'1tr1'):
        line = self.re_substitute(line, r'NA\/K PHOSPHATE 1\.3 M.*', r'1.3M NA/K PHOSPHATE PH 8.3')
    if self.re_search(pdb, r'2tss'):
        line = self.re_substitute(line, r'CITRATE-PHOSPHATE OR ACETATE BUFFER', r'CITRATE PHOSPHATE')
    if self.re_search(pdb, r'1tt4'):
        line = self.re_substitute(line, r'MGS', r'MAGNESIUM SULFATE') #looked at het atoms in file...
    if self.re_search(pdb, r'1tu0'):
        line = self.re_substitute(line, r'BEFORE MOUNTING.*', '') 
    if self.re_search(pdb, r'1tuw'):
        line = self.re_substitute(line, r'\(11.*', '') 
    if self.re_search(pdb, r'1tux'):
        line = self.re_substitute(line, r'.*', r'5MG/ML PROTEIN, 50MM TRIS PH 7.4, 12% AMMONIUM SULFATE') 
    if self.re_search(pdb, r'1txx'):
        line = self.re_substitute(line, r'DROPS.*', r'0.1M SODIUM SUCCINATE PH 4.2, 20% W/V PEG MME 2000, 2MM CUPRIC ACETATE') 
    if self.re_search(pdb, r'1u1x'):
        line = self.re_substitute(line, r'CRYSTALS .*', r'10MM 3-HYDROXYANTHRANILIC ACID, PH 4.8')
    if self.re_search(pdb, r'1u4q'):
        line = self.re_substitute(line, r'283', '')
    if self.re_search(pdb, r'1u6m'):
        line = self.re_substitute(line, r'05M.*', r'0.5M SODIUM CITRATE PH 5.0')
    if self.re_search(pdb, r'1u71'):
        line = self.re_substitute(line, r'PHOSPHATE', r'0.1M PHOSPHATE')
    if self.re_search(pdb, r'1u8g'):
        line = self.re_substitute(line, r'2\.4', r'2.4M')
    if self.re_search(pdb, r'1umu'):
        line = self.re_substitute(line, r'THE CRYSTALS WERE\s+FROZEN.*', '')
    if self.re_search(pdb, r'1umz|1un1'):
        line = self.re_substitute(line, r'MG ML-1\s+PROTEIN SOLUTION\s+1:1 WITH', r'MG/ML PROTEIN, ')
    if self.re_search(pdb, r'1uoj'):
        line = self.re_substitute(line, r'\(NH4\)2SO4 1\.5 M', r'1.5M AMMONIUM SULFATE')
    if self.re_search(pdb, r'1uoz'):
        line = self.re_substitute(line, r'THE.*', r'10MG/ML PROTEIN, 1MM THIOCELLOPENTAOSE')
    if self.re_search(pdb, r'1up0'):
        line = self.re_substitute(line, r'THE.*', r'10MG/ML PROTEIN, 1MM 1-BETA-METHYL-CELLOTRIOSIDE-THIO-GLUCOSIDE')
    if self.re_search(pdb, r'1up2'):
        line = self.re_substitute(line, r'12 \% PEG 4K, 12', r'12')
        line = self.re_substitute(line, r'THE.*', r'10MG/ML PROTEIN, 1MM GLUCOSE-ISOFAGOMINE')
    if self.re_search(pdb, r'1up3'):
        line = self.re_substitute(line, r'MES', r'MES PH')
        line = self.re_substitute(line, r'INCUBATED.*', '')
    if self.re_search(pdb, r'1upi'):
        line = self.re_substitute(line, r'.* SITTING DROPS\s+IN INTELLIPLATES,', '')
        line = self.re_substitute(line, r'B-MERCAPTO-ETHANOL .*', '')
    if self.re_search(pdb, r'1uqw'):
        line = self.re_substitute(line, r'.*', r'15% PEG 8K, 0.2M ZINC ACETATE, 0.1M SODIUM ACETATE PH 6.0, 5% GLYCEROL')
    if self.re_search(pdb, r'1ur3'):
        line = self.re_substitute(line, r'.*', r'17.5% PEG 4K, 0.2M IMIDAZOLE MALATE PH 7.0, 0.1M AMMONIUM SULFATE, 2.5% GLYCEROL, 0.1M SPERMIDINE')
    if self.re_search(pdb, r'1urz'):
        line = self.re_substitute(line, r'.*', r'25% PEG 4K, 0.1M SODIUM ACETATE PH 4.5, 15MM DDAO')
    if self.re_search(pdb, r'1us2'):
        line = self.re_substitute(line, r'20 MM \(1 UL\) XYLOPENTAOSE', r'20 MM XYLOPENTAOSE')
    if self.re_search(pdb, r'1us4'):
        line = self.re_substitute(line, r'VAPOUR.*', r'10 MG/ML PROTEIN, 20.3% PEG4000, 0.09M SODIUM CITRATE PH 5.0,')
    if self.re_search(pdb, r'1us[cf]'):
        line = self.re_substitute(line, r'.*', r'3.1MG/ML PROTEIN, 21% PEG 4K, 0.1M SODIUM ACETATE PH 4.7')
    if self.re_search(pdb, r'1uuf'):
        line = self.re_substitute(line, r'NACL.*', r'0.1M NACL, 0.1M TRIS, 10MM SODIUM ACETATE, 0.1MM ZINC ACETATE, PH 4.75')
    if self.re_search(pdb, r'1uun'):
        line = self.re_substitute(line, r'DETERGENTS.*', '')
    if self.re_search(pdb, r'1uu[vw]'):
        line = self.re_substitute(line, r'.*', r'2M AMMONIUM SULFATE, 0.1M MES, 2-3% DIOXANE')
    if self.re_search(pdb, r'1uuz'):
        line = self.re_substitute(line, r'IMIDAZOLE\/MALATE 0\.2M', r'0.2M IMIDAZOLE MALATE')
    if self.re_search(pdb, r'1uv0'):
        line = self.re_substitute(line, r'PEG 8000 20\% \(W\/V\)', r'20% W/V PEG 8000')
    if self.re_search(pdb, r'1uvh'):
        line = self.re_substitute(line, r'.*', r'0.1M HEPES PH 7.0-7.8, 1.5-2.0M AMMONIUM SULFATE')
    if self.re_search(pdb, r'1uw8'):
        line = self.re_substitute(line, r'TRIS', r'0.1M TRIS')
    if self.re_search(pdb, r'1uw[9a]|1uz[dh]'):
        line = self.re_substitute(line, r'PEG 4', r'PEG 4000') # fix from paper or fix from thesis
    if self.re_search(pdb, r'1uw[qrstu]'):
        line = self.re_substitute(line, r'CRYO - 25\% ETHYLENE GLYCOL', '')
    if self.re_search(pdb, r'1ux[abe]'):
        line = self.re_substitute(line, r'PROTEIN.*', r'PH 7.5') #fix from paper
    if self.re_search(pdb, r'1uyo'):
        line = self.re_substitute(line, r'MPD\.', r'MPD ')
        line = self.re_substitute(line, r'6\%,', r'6%')
    if self.re_search(pdb, r'1uzb'):
        line = self.re_substitute(line, r'THE SODIUM CITRATE WAS .*', '')
    if self.re_search(pdb, r'1uzq'):
        line = self.re_substitute(line, r'BOTH .*', r'5MM EDTA')
    if self.re_search(pdb, r'1v1[ab]'):
        line = self.re_substitute(line, r'.* WAS MIXED WITH\s*RESERVOIR\s*SOLUTION CONTAINING', '')
    if self.re_search(pdb, r'1v6h'):
        line = self.re_substitute(line, r'PEG.*', r'16.5% PEG 20K, 0.1M HEPES PH 6.1')
    if self.re_search(pdb, r'1v8g'):
        line = self.re_substitute(line, r'27\.5', r'27.5%')
    if self.re_search(pdb, r'1vew'):
        line = self.re_substitute(line, r'AND CONSISTED OF.*', '')
    if self.re_search(pdb, r'1vjk'):
        line = self.re_substitute(line, r'CACODYLATE', r'CACODYLATE PH 6.5')
    if self.re_search(pdb, r'1vjq'):
        line = self.re_substitute(line, r'MICRO-SEEDS.*', '')
#    if self.re_search(pdb, r'1vjz'):
#        line = self.re_substitute(line, r'.*277K\.', '') FIXME: need to do this before temp fixes?
    if self.re_search(pdb, r'1vk5'):
        line = self.re_substitute(line, r'AMMONIUM.*', r'0.8M AMMONIUM SULFATE, 0.1M HEPES, 0.04M MAGNESIUM SULFATE, 0.41% CHAPS PH 8.5')
    if self.re_search(pdb, r'1vkv'):
        line = self.re_substitute(line, r'\(CRYSTAL TWO.*', '')
    if self.re_search(pdb, r'1vlx'):
        line = self.re_substitute(line, r'AROUND.*', '')
    if self.re_search(pdb, r'1vm0'):
        line = self.re_substitute(line, r'POTASSIUM.*', r'0.2M POTASSIUM NITRATE, 0.1M MOPS PH 7.0')
    if self.re_search(pdb, r'1vsj'):
        line = self.re_substitute(line, r'N10', r'10')
    if self.re_search(pdb, r'1vpn|1vps'):
        line = self.re_substitute(line, r'RESERVOIR:.*', '')
        line = self.re_substitute(line, r'& ETHANOL', r'% ETHANOL,')
    if self.re_search(pdb, r'1vyq'):
        line = self.re_substitute(line, r'CONTAINING 3-FOLD EXCESS OF INHIBITOR', '')
    if self.re_search(pdb, r'1vzm'):
        line = self.re_substitute(line, r'DROPS.*', r'0.2M MGCL2, 30% PEG 4000, 0.1M TRIS CHLORIDE PH 8.5')
    if self.re_search(pdb, r'1w0f'):
        line = self.re_substitute(line, r'0\.1', r'0.1M')
        line = self.re_substitute(line, r'0\.025M C', r'0.025M CALCIUM CHLORIDE') #fix from paper
    if self.re_search(pdb, r'1w16'):
        line = self.re_substitute(line, r'.*', r'2.5M NACL, 0.1M CACL2, 0.1M HEPES PH 7.5')
    if self.re_search(pdb, r'1w2z'):
        line = self.re_substitute(line, r'.*', r'20% PEG 3350, 0.28M KI, 21.58MG/ML PROTEIN')
    if self.re_search(pdb, r'1w3o'):
        line = self.re_substitute(line, r'CITRATE OR MES BUFFERED', '')
    if self.re_search(pdb, r'1w4[opq]'):
        line = self.re_substitute(line, r'PEG.*', r'25% W/V PEG 4000')
    if self.re_search(pdb, r'1w4[wy]'):
        line = self.re_substitute(line, r'FERULIC.*', '')
    if self.re_search(pdb, r'1w54'):
        line = self.re_substitute(line, r'28\,5\s*\%', r'28.5% ')
        line = self.re_substitute(line, r'\)\s*ABOVE .*', '')
    if self.re_search(pdb, r'1w5[6mnq]'):
        line = self.re_substitute(line, r'ON GLASS.*', '')
    if self.re_search(pdb, r'1w5j'):
        line = self.re_substitute(line, r'\%30', r', 30%')
        line = self.re_substitute(line, r'HAMPTON.*', '')
    if self.re_search(pdb, r'1w6[m-q]'):
        line = self.re_substitute(line, r'THE (GA)?LACTOSE COMPLEX.*', '')
    if self.re_search(pdb, r'1w70'):
        line = self.re_substitute(line, r'.* PEPTIDE', r'14MG/ML PROTEIN,')
        line = self.re_substitute(line, r'\bSA\b', r'AMMONIUM SULFATE') #from paper
    if self.re_search(pdb, r'1w9h'):
        line = self.re_substitute(line, r'10 MG\/ML', r'10MG/ML PROTEIN,')
    if self.re_search(pdb, r'1wb[45]'):
        line = self.re_substitute(line, r'.*', r'1M SODIUM ACETATE, 100MM HEPES PH7.5, 50MM CD ACETATE, 5% GLYCEROL')
    if self.re_search(pdb, r'1wkb'):
        line = self.re_substitute(line, r'ADA\(6\.7\)', r'ADA PH 6.7')
    if self.re_search(pdb, r'1wwc'):
        line = self.re_substitute(line, r'.* VERSUS', '')
    if self.re_search(pdb, r'1x7f'):
        line = self.re_substitute(line, r'0\.5 SODIUM', r'0.5M SODIUM') #my guess
    if self.re_search(pdb, r'1xdw'):
        line = self.re_substitute(line, r'OR PEG 2000', '')
        line = self.re_substitute(line, r'OR LITHIUM', '')
    if self.re_search(pdb, r'1xg5'):
        line = self.re_substitute(line, r'\(TOTAL 7\%\)', '')
    if self.re_search(pdb, r'1xjr'):
        line = self.re_substitute(line, r'\bS2M\s+RNA\b', r'RNA')
    if self.re_search(pdb, r'1xkw'):
        line = self.re_substitute(line, r'OR\s+10\s*K', '')
    if self.re_search(pdb, r'1xkl|1y7i'):
        line = self.re_substitute(line, r'\bSA\b', r'SALICYLIC ACID')
    if self.re_search(pdb, r'1xlm'):
        line = self.re_substitute(line, r'05 TRIS', r'0.5M TRIS')
    if self.re_search(pdb, r'1xm8'):
        line = self.re_substitute(line, r'0\.100', r'0.100M') # fix from author
        line = self.re_substitute(line, r'0\.200', r'0.200M') # fix from author
    if self.re_search(pdb, r'1xq[gj]'):
        line = self.re_substitute(line, r'SODIUM.*', r'0.2M SODIUM CITRATE, 0.1M TRIS PH 8.2')
    if self.re_search(pdb, r'1xt5'):
        line = self.re_substitute(line, r'\(OR HEPES\)', '')
    if self.re_search(pdb, r'1xx6'):
        line = self.re_substitute(line, r'.*', r'0.2M SODIUM CITRATE-POTASSIUM CITRATE, 20% PEG 3350, 2MM ATP, 2MM MAGNESIUM CHLORIDE')
    if self.re_search(pdb, r'2xyl'):
        line = self.re_substitute(line, r'SOAK.*', '')
    if self.re_search(pdb, r'1y5y'):
        line = self.re_substitute(line, r'CALCIUM.*', r'CALCIUM CHLORIDE, 0.1M SODIUM ACETATE PH 4.6, 10-20% (V/V) ISOPROPANOL')
    if self.re_search(pdb, r'1y60'):
        line = self.re_substitute(line, r'\(H4MPT\)', '')
    if self.re_search(pdb, r'1y6e'):
        line = self.re_substitute(line, r'MODIFIED.*', '')
    if self.re_search(pdb, r'1y8w|1ydz|1ye[01i2noquv]|1yg[5df]|1yh[9e]'):
        line = self.re_substitute(line, r'BATCH.*', '')
    if self.re_search(pdb, r'1yfo'):
        line = self.re_substitute(line, r'ETHYLENE .*', '')
    if self.re_search(pdb, r'1yh6'):
        line = self.re_substitute(line, r'0\.1MB\s*-\s*TRIS', r'0.1M BIS-TRIS')
    if self.re_search(pdb, r'1yhr|1yi[eh]'):
        line = self.re_substitute(line, r'1 ATM N2', '')
    if self.re_search(pdb, r'1yyy'):
        line = self.re_substitute(line, r'7\.5PH', r'PH 7.5')
    if self.re_search(pdb, r'1z7j'):
        line = self.re_substitute(line, r'0.L', r'0.1')
    if self.re_search(pdb, r'1zlw'):
        line = self.re_substitute(line, r'0\.2 IMIDIZOLE', r'0.2M IMIDAZOLE') # guess on my part
    if self.re_search(pdb, r'1zme'):
        line = self.re_substitute(line, r'.* PREPARED', '')
    if self.re_search(pdb, r'1znj'):
        line = self.re_substitute(line, r'02 ZINC', r'02M ZINC')
    if self.re_search(pdb, r'1zpd'):
        line = self.re_substitute(line, r'.* PROTEIN SOLUTION', '')
        line = self.re_substitute(line, r'lineEAK .*', '')
    if self.re_search(pdb, r'1zw3'): # According to paper, shouldn't be there
        line = self.re_substitute(line, r'PH 6.1,', '')
    if self.re_search(pdb, r'1zxq'):
        line = self.re_substitute(line, r'.* CRYSTALLIZATION SOLUTION WITH', '')
    if self.re_search(pdb, r'1zxt'):
        line = self.re_substitute(line, r'\:\s+MOTHER LIQUOR', '')
    if self.re_search(pdb, r'23[01]l'):
        line = self.re_substitute(line, r'M.*', r'15MG/ML PROTEIN, 0.55M NACL, 1.8M NA/KPO4 PH 6.9')
    if self.re_search(pdb, r'232l'):
        line = self.re_substitute(line, r'M.*', r'15MG/ML PROTEIN, 0.55M NACL, 1.8M NA/KPO4 PH 7.1')
    if self.re_search(pdb, r'2abw'):
        line = self.re_substitute(line, r'BUFFERED .*\)', r'50MM MES') #just a guess, the paper doesn't give the amount!
    if self.re_search(pdb, r'2ax2'):
        line = self.re_substitute(line, r'TRIS\-\s*DL', r'TRIS')
    if self.re_search(pdb, r'2b5i'):
        line = self.re_substitute(line, r'15\/\s*4', '')
    if self.re_search(pdb, r'2cek'):
        line = self.re_substitute(line, r'PUTATIVE ANTI\-ALZHEIMER DRUG', '')
    if self.re_search(pdb, r'2g3f'):
        line = self.re_substitute(line, r'IMIDAZOLI.*', r'IMIDAZOLE ACETIC ACID, 0.2M SODIUM ACETATE, 2% W/V BENZAMIDINE HYDROCHLORIDE') #from paper
    if self.re_search(pdb, r'2g45'):
        line = self.re_substitute(line, r'OR CALCIUM', '')
    if self.re_search(pdb, r'2gg4'):
        line = self.re_substitute(line, r'.*', r'12.5% W/V PEG 4000, 0.05M POTASSIUM CHLORIDE, 2.5% DMSO, 50MM TRIS PH 8.5') #from paper
    if self.re_search(pdb, r'2gg6'):
        line = self.re_substitute(line, r'.*', r'1M AMMONIUM SULFATE, 0.1M POTASSIUM CHLORIDE, 1% PEG 400, 50MM TRIS PH 8.5, 5MM S3P') #from paper
    if self.re_search(pdb, r'2gg[ad]'):
        line = self.re_substitute(line, r'.*', r'1M AMMONIUM SULFATE, 0.1M KCL, 1% PEG 400, 50MM SODIUM HEPES PH 7.5, 5MM S3P, 40MM GLYPHOSATE') #from paper
    if self.re_search(pdb, r'2gib'):
        line = self.re_substitute(line, r'15\/\s*4.*OH', '')
    if self.re_search(pdb, r'2gm1'):
        line = self.re_substitute(line, r'\(90 UM\)', '')
    if self.re_search(pdb, r'2gq0'):
        line = self.re_substitute(line, r'OR PEG.*', '')
    if self.re_search(pdb, r'2gqu'):
        line = self.re_substitute(line, r'\(EP\-UDPGLCNAC\)', '')
    if self.re_search(pdb, r'2gt4'):
        line = self.re_substitute(line, r'5MM .*HCL P8', r'5MM GDP-MANNOSE, 5MM GLUCOSE, 100 MM TRIS CHLORIDE PH 8')
    if self.re_search(pdb, r'2b2b'):
        line = self.re_substitute(line, r'.*', r'15-20% MPD')
    if self.re_search(pdb, r'2b92'):
        line = self.re_substitute(line, r'FROM.* SUPPLIED', '')
    if self.re_search(pdb, r'2bel'):
        line = self.re_substitute(line, r'C\(PROTEIN.*', r'8MG/ML PROTEIN')
    if self.re_search(pdb, r'2bf[b-f]'):
      line = self.re_substitute(line, r'MANGANESE IONS.*','')
    if self.re_search(pdb, r'2bfq'):
        line = self.re_substitute(line, r'0.2.*CITRTAE', r'0.2M AMMONIUM ACETATE, 0.1M SODIUM CITRATE') #my guess
    if self.re_search(pdb, r'2bfr'):
        line = self.re_substitute(line, r'0.2 MAGNESIUM', r'0.2M MAGNESIUM') #my guess
    if self.re_search(pdb, r'2bhi'):
        line = self.re_substitute(line, r'\(15\/4 EO\/OH\)', '')
    if self.re_search(pdb, r'2bhj'):
        line = self.re_substitute(line, r'HEPES PH 7', r'HEPES PH 7,')
    if self.re_search(pdb, r'2bil'):
        line = self.re_substitute(line, r'MSPG', r'SUCCINATE PHOSPHATE GLYCINE') # succinic acid phosphate glycine buffer system
    if self.re_search(pdb, r'2bly'):
        line = self.re_substitute(line, r'5 0 MM PH 4\.5 SODIUM ACETATE', r'50 MM SODIUM ACETATE PH 4.5')
    if self.re_search(pdb, r'2bm2'):
        line = self.re_substitute(line, r'PEG.*', r'13-19% PEG 3000, 100MM SODIUM ACETATE, PH 5')
    if self.re_search(pdb, r'2bnw'): # FIXME: lookup paper to find conc units
        line = self.re_substitute(line, r'2\.4\s*NA2MALONATE, PH 7\.5', '')
    if self.re_search(pdb, r'2bp1'):
        line = self.re_substitute(line, r'PROTEIN\:', '')
    if self.re_search(pdb, r'2bra'):
        line = self.re_substitute(line, r'42\%', r'23.5%') # correction from paper, 42% was cryoprotectant
    if self.re_search(pdb, r'2br9'):
        line = self.re_substitute(line, r'PROTEIN\s+IN.*', '')
    if self.re_search(pdb, r'2brw'):
        line = self.re_substitute(line, r'\(PEGMME\)', '')
    if self.re_search(pdb, r'2btu'):
        line = self.re_substitute(line, r'\(TRIMETHYLAMINE\-N\-OXIDE\)', '')
    if self.re_search(pdb, r'2bw[ac]'):
        line = self.re_substitute(line, r'CEL12A\s*\(PROTEIN\)', r'PROTEIN')
    #if self.re_search(pdb, r'2bw[stvx]'):
    #    line = self.re_substitute(line, r'SOAKED .*', '')
    if self.re_search(pdb, r'2c1p'):
        line = self.re_substitute(line, r'10 *', '')
    if self.re_search(pdb, r'2c3a'):
        line = self.re_substitute(line, r'\&K', r'6K')
    if self.re_search(pdb, r'2c2v'):
        line = self.re_substitute(line, r'.* VAPOUR DIFFUSION', '')
    if self.re_search(pdb, r'2caq'):
        line = self.re_substitute(line, r'PBS .*', r'PH 7.4, 5MM BETA-MERCAPTOETHANOL, 10% PEG 200') #from paper
    if self.re_search(pdb, r'2clb'):
        line = self.re_substitute(line, r'CACL2.*', r'M CACL2, 0.05M TRIS CHLORIDE PH 8.5') # from paper
    if self.re_search(pdb, r'2cgz'):
        line = self.re_substitute(line, r'.*', r'2M LITHIUM SULFATE, 3.5M AMMONIUM SULFATE, 1.5M SODIUM CITRATE PH 6.5, 10MM PROTEIN')
    if self.re_search(pdb, r'2ch9'):
        line = self.re_substitute(line, r'ACETIC\s+ACID', '')
    if self.re_search(pdb, r'2crx'):
        line = self.re_substitute(line, r'25\%', '')
    if self.re_search(pdb, r'2dck'):
        line = self.re_substitute(line, r'SODIUM PHOSPHATE BUFFER\s+\(', '')
    if self.re_search(pdb, r'2dw6'):
        line = self.re_substitute(line, r'L\-TARTRATE', r'TARTRATE')
    if self.re_search(pdb, r'2dw[de]|2hv[jk]'):
        line = self.re_substitute(line, r'\(PH .*', r'PH 6.5')
    if self.re_search(pdb, r'2esn'):
        line = self.re_substitute(line, r'1MHEPES', r'1M HEPES')
    if self.re_search(pdb, r'2eu[ps]'):
        line = self.re_substitute(line, r'\bMDP\b', r'MPD')
    if self.re_search(pdb, r'2eyi'):
        line = self.re_substitute(line, r'POLYETHYLENE GLYCOL 5000 MONOMETHYL ESTER', '')
    if self.re_search(pdb, r'2ez0|2ex[wy]'):
        line = self.re_substitute(line, r'(36\%\s*)?PEG\s*200\/300', r'35-40% PEG 300') #actually in 1:2 ratio, but hard to fix properly... different amounts given in paper
    if self.re_search(pdb, r'2f1k'):
      line = self.re_substitute(line, r'.*', r'0.1 M TRIS CHLORIDE PH 8.0, 30% PEG 6000, 4MM NADP') 
    if self.re_search(pdb, r'2f6[247]'):
      line = self.re_substitute(line, r'0\.2\s+AMMONIUM\s+SULFATE,\s*0\.1', r'0.2M AMMONIUM SULFATE, 0.1M') 
    if self.re_search(pdb, r'2f8i'):
      line = self.re_substitute(line, r'SODIUM\s+R', r'SODIUM PHOSPHATE, 12MG/ML PROTEIN') #from paper
    if self.re_search(pdb, r'2faz'):
      line = self.re_substitute(line, r'P3350.*PROTEIN', r'PEG 3350, 0.2M LITHIUM CITRATE') 
    if self.re_search(pdb, r'2fbh'):
      line = self.re_substitute(line, r'PEG3350\s+20\%', r'20% PEG 3350') 
    if self.re_search(pdb, r'2fbm'):
      line = self.re_substitute(line, r'20\%V\s+PEG3350', r'20% PEG 3350') 
    if self.re_search(pdb, r'2fbq'):
      line = self.re_substitute(line, r'PEG.*', r'25% PEG MME 5K,0.2M CACL2,0.1M BIS-TRIS, 2MM CYSTEINE, PH 6.5') 
    if self.re_search(pdb, r'2fd3|2fch'):
      line = self.re_substitute(line, r'HEPES\s+15\s*MM', r'15MM HEPES') 
    if self.re_search(pdb, r'2fe[cde]'):
      line = self.re_substitute(line, r'PEG\s*400\s+37\%', r'37% PEG 400')
    if self.re_search(pdb, r'2fha'):
      line = self.re_substitute(line, r'/', r',') 
    if self.re_search(pdb, r'2fhy'):
      line = self.re_substitute(line, r'ZMP', '')
    if self.re_search(pdb, r'3fil'):
      line = self.re_substitute(line, r'DROP 400NL PROTEIN SOLUTION &\s*400NL RESERVOIR SOLUTION, RESERVOIR, VAPOR\s*DIFFUSION, HANGING DROP,', '')    
    if self.re_search(pdb, r'2fiy'):
      line = self.re_substitute(line, r'\bP\b', r'PEG') 
    if self.re_search(pdb, r'2fs6'):
      line = self.re_substitute(line, r'\(4000\).*\(8\.5\)', r'0.1 M  TRIS CHLORIDE PH 8.0') 
    if self.re_search(pdb, r'2f2t'):
      line = self.re_substitute(line, r'0\.2\s+AMMONIUM\s+SULFATE\s+0\.1\s+SODIUM', r'0.2M AMMONIUM SULFATE 0.1M SODIUM') 
    if self.re_search(pdb, r'2ft[lm]'):
      line = self.re_substitute(line, r'20.*', '') 
    if self.re_search(pdb, r'2fxa'):
      line = self.re_substitute(line, r'\bPED\b', r'PEG') 
    if self.re_search(pdb, r'2fw[aij]'):
      line = self.re_substitute(line, r'SOAKED PH 7', '') 
    if self.re_search(pdb, r'2fyc'):
      line = self.re_substitute(line, r'500', r'500MM') 
    if self.re_search(pdb, r'2g5o'):
      line = self.re_substitute(line, r'TRIS\s+P 8', r'TRIS PH 8') 
    if self.re_search(pdb, r'2ga[gh]'):
      line = self.re_substitute(line, r'FUORATE', r'FUROATE') # from paper
    if self.re_search(pdb, r'2glq'):
      line = self.re_substitute(line, r'OVER .* MONTHS', '') 
    if self.re_search(pdb, r'2gv[gl]'):
      line = self.re_substitute(line, r'BACL2\s+AS\s+ADDITIVE', '') # conc. not mentioned in paper
    if self.re_search(pdb, r'2h9b'):
      line = self.re_substitute(line, r'PROTEIN:', '')
    if self.re_search(pdb, r'2h9y'):
        line = self.re_substitute(line, r'P550 MME OR\s+P600', r'PEG MME 550')
        line = self.re_substitute(line, r'OR\s+NA\s+ACETATE', '')
    if self.re_search(pdb, r'2ha[023567]'):
        line = self.re_substitute(line, r'OR\s+PEG600', '')
        line = self.re_substitute(line, r'OR\s+NA\s+ACETATE', '')
    if self.re_search(pdb, r'2haq'):
        line = self.re_substitute(line, r'.*', r'0.02M TRIS PH 8.5, 0.02% SODIUM AZIDE, 40% PEG 3350, 10MG/ML PROTEIN')
    if self.re_search(pdb, r'2hdv'):
        line = self.re_substitute(line, r'605', '')
    if self.re_search(pdb, r'2hh7'):
        line = self.re_substitute(line, r'PEG4000.*CITRATE', r'PEG4000, 0.1M SODIUM CITRATE')
    if self.re_search(pdb, r'2his'):
        line = self.re_substitute(line, r'PRE-COMPLEXED.*', '')
    if self.re_search(pdb, r'2hk5'):
        line = self.re_substitute(line, r'.*', r'1.9-2.2M AMMONIUM SULFATE, 0.1M TRIS PH 8.5') # from paper
    if self.re_search(pdb, r'2hoo'):
        line = self.re_substitute(line, r'\bBTP\b', r'S-BENZOYL THIAMINE MONOPHOSPHATE')
    if self.re_search(pdb, r'2hop'):
        line = self.re_substitute(line, r'\bPT\b', r'PYRITHIAMINE')
    if self.re_search(pdb, r'2hpc'):
        line = self.re_substitute(line, r'FRAGMENT D', r'PROTEIN')
    if self.re_search(pdb, r'2huw'):
        line = self.re_substitute(line, r'LIGAND \(CPYVN\) WAS ADDED TO A 1\.5 M EXCESS TO A SOLUTION OF', '')
    if self.re_search(pdb, r'2imd|2ime|2imf'):
        line = self.re_substitute(line, r'0\.1M CAPS PH 6\.1\. PROTEIN', r'0.1M CAPS PH 6.1')
    if self.re_search(pdb, r'2iw5'):
        line = self.re_substitute(line, r'.*PLUS 0', '')
    if self.re_search(pdb, r'2iwb'):
        line = self.re_substitute(line, r'PROTEIN.*', r'6.8MG/ML PROTEIN')
    if self.re_search(pdb, r'2iyk'):
        line = self.re_substitute(line, r'\(15/4EO/OH\)', '')
    if self.re_search(pdb, r'2j0x'):
        line = self.re_substitute(line, r'2\%.*', r'1% MPD, 1% ETHYLENE GLYCOL')
    if self.re_search(pdb, r'2j59'):
        line = self.re_substitute(line, r'OR LI2SO4', '')
    if self.re_search(pdb, r'2j5i'):
        line = self.re_substitute(line, r'.*', r'11% W/V PEG 20000, 8% V/V PEG MME 550, 0.8M SODIUM FORMATE, 0.2% BUTANE-1,4-DIOL, 0.05M MES PH 5.6')
    if self.re_search(pdb, r'2j78'):
        line = self.re_substitute(line, r'4K.*', r'4K, 0.1M  IMIDAZOLE, PH 7, 0.2M CALCIUM ACETATE')
    if self.re_search(pdb, r'2jfn'):
        line = self.re_substitute(line, r'55.*MME', r'55, 10% PEG MME')
    if self.re_search(pdb, r'2jgd'):
        line = self.re_substitute(line, r'.*', r'10MG/ML PROTEIN, 12% PEG 4000, 50MM SODIUM CITRATE PH5.6')
    if self.re_search(pdb, r'2jgn'):
        line = self.re_substitute(line, r'PROTEIN:', '')
    if self.re_search(pdb, r'2nip'):
        line = self.re_substitute(line, r'PROTEIN WAS HELD.*', '')
    if self.re_search(pdb, r'2not'):
        line = self.re_substitute(line, r'THE.*', r'15MG/ML PROTEIN, 50MM TRIS SULFATE, 50MM AMMONIUM ACETATE PH 8.5')
    if self.re_search(pdb, r'2nsb'):
        line = self.re_substitute(line, r'CHLORIDE 0\.2M', r'CHLORIDE')
    if self.re_search(pdb, r'2nt4'):
        line = self.re_substitute(line, r'20\%.*', '')
    if self.re_search(pdb, r'2o1x|2nqk'):
        line = self.re_substitute(line, r'OR\s+PEG\s+\d+', '')
    if self.re_search(pdb, r'2or7'):
        line = self.re_substitute(line, r'4\%.*', r'4% 1,2,3-HEPTANETRIOL, PH 4.6')
    if self.re_search(pdb, r'2ou7|2owb'):
        line = self.re_substitute(line, r'AMPPNP', '')
    if self.re_search(pdb, r'2ooh'):
        line = self.re_substitute(line, r'\(HYDROXYMETHYL.*', r'PH 7.5')
    if self.re_search(pdb, r'2p0[59]'):
        line = self.re_substitute(line, r'X\/V', r'V/V')
    if self.re_search(pdb, r'2p1e'):
        line = self.re_substitute(line, r'\- SOAKED 30 MIN IN', r',')
    if self.re_search(pdb, r'2pda'):
        line = self.re_substitute(line, r'.*', r'11% PEG 6000, 100MM MGCL2, 100MM CACODYLATE PH6.2, 100MM PYRUVATE')
    if self.re_search(pdb, r'2q76'):
        line = self.re_substitute(line, r'LARGE PRISMS OF\s*ABOUT 0.30 MM X 0.05 MM X 0.05 MM WERE OBTAINED AFTER SEVERAL\s*WEEKS\.','')
    if self.re_search(pdb, r'2qc5'):
        line = self.re_substitute(line, r',12,5%', r' 12.5%')
    if self.re_search(pdb, r'2qi9'):
        line = self.re_substitute(line, r'EITHER OF TRIS&#8209,HCL PH 8\.4 OR GLYCINE-NAOH PH\s*9\.4', r'TRIS CHLORIDE PH 8.4')
    if self.re_search(pdb, r'2prj'):
        line = self.re_substitute(line, r'SPERMINE', r'1MM SPERMINE, 1MM IMP') # correction from paper
    if self.re_search(pdb, r'2ps0'):
        line = self.re_substitute(line, r'ZNZNUA.*', r'PROTEIN')
    if self.re_search(pdb, r'2psw|2ob0'):
        line = self.re_substitute(line, r'PROTEIN:.*', r'11.8 MG/ML PROTEIN')
    if self.re_search(pdb, r'2vb1'):
        line = self.re_substitute(line, r'ETHYLENE GLYCOL PROTEIN', r'ETHYLENE GLYCOL')
    if self.re_search(pdb, r'2vhb'):
        line = self.re_substitute(line, r'PRECIP.*', r'25 MG/ML PROTEIN, 1.2M AMMONIUM SULFATE, 0.2M SODIUM PYROPHOSPHATE, PH 6.4, 3% V/V ETHYLENE GLYCOL')
    if self.re_search(pdb, r'2v8a'):
        line = self.re_substitute(line, r'ABOVE A RESERVOIR OF', '')
    if self.re_search(pdb, r'2vb7'):
        line = self.re_substitute(line, r'NO LIGAND', '')
    if self.re_search(pdb, r'2vy6'):
        line = self.re_substitute(line, r'K/NA TARTRATE\s*AT 1\.2 M', '1.2M POTASSIUM SODIUM TARTRATE')
    if self.re_search(pdb, r'2wiv'):
        line = self.re_substitute(line, r'\-1', '')
    if self.re_search(pdb, r'2wmp'):
        line = self.re_substitute(line, r'\(COMPLEX\)', '')
    if self.re_search(pdb, r'2wng'):
        line = self.re_substitute(line, r'100 NL\s*SIRP \(18.6 MG/ML\) PLUS 100 NL PRECIPITANT',r'18.6 MG/ML SIRP')
    if self.re_search(pdb, r'2wqw'):
        line = self.re_substitute(line, r'PLUS RESERVOIR 2 PLUS 1', '')
    if self.re_search(pdb, r'2wrs'): #FIXME: See if conc is in paper
        line = self.re_substitute(line, r'POWDER OF COMPOUND 18 IN THE DROP\.', '')
    if self.re_search(pdb, r'2wyi'):
        line = self.re_substitute(line, r'CLEAVED SPGH38', r'PROTEIN')
    if self.re_search(pdb, r'2x6a'): # FIXME: See if conc is in paper
        line = self.re_substitute(line, r'ADDITIVES: FOS\-CHOLINE\-ISO\-11\-6 U \(ANATRACE\) NONYL MALTOSIDE \(ANATRACE\) FOS\-CHOLINE ISO\-9 \(ANATRACE\)', '')
    if self.re_search(pdb, r'2x89'):
        line = self.re_substitute(line, r'0\.1MNAACETEATE4\.6', r'0.1M AMMONIUM ACETATE PH4.6')
    if self.re_search(pdb, r'2xan'):
        line = self.re_substitute(line, r'100 MM BIS\-TRIS, PH 5\.9\s*PROTEIN WAS MIXED WITH', r'100 MM BIS-TRIS PH 5.9')
    if self.re_search(pdb, r'2xud|2xuf|2xug|2xuh|2xui|2xuj|2xuk|2xuo|2xup|2xuq'):
        line = self.re_substitute(line, r'OR\s+WITH PEG\-550 MME 30% \(V/V\) IN', '')
    if self.re_search(pdb, r'2yxg'):
        line = self.re_substitute(line, r'OIL\-BATCH', '')
    if self.re_search(pdb, r'2zj3|2zj4'):
        line = self.re_substitute(line, r'10-FOLD EXCESS OF (2-DEOXY-2-\s*AMINOGLUCITOL-6-PHOSPHATE|FRUCTOSE-6-\s*PHOSPHATE)', '')
    if self.re_search(pdb, r'2zp6'):
        line = self.re_substitute(line, r'\(METAL BASIS\)', '')
    if self.re_search(pdb, r'3bis'): # When they say 'X% chem A or chem B', pick chem A 
        line = self.re_substitute(line, r'OR AMMONIUM FLUORIDE', '')
    if self.re_search(pdb, r'3dp[wxz]|3dq[1-9ac-fh-nou]'): # temperature appears twice!
        line = self.re_substitute(line, r'CRYSTALS WERE GROWN AT 4  DEGREES  C AND', '')
    if self.re_search(pdb, r'3faq'): # FIXME: Check from paper that it is 0.2M
        line = self.re_substitute(line, r'PEG3350', r'0.2 M PEG 3350')
    if self.re_search(pdb, r'3fup'):
        line = self.re_substitute(line, r'6\.5/6\.7', r'6.6')
    if self.re_search(pdb, r'3gqy|3gr4|3h6o'): # FIXME: Activator??
        line = self.re_substitute(line, r'0\.005M ACTIVATOR,', '')
    if self.re_search(pdb, r'3hic'): # FIXME: Not sure of concs
        line = self.re_substitute(line, r'1M BIS\-TRIS PH 6\.5 \[100MM\]\+ 50\% PEG\s*3350 \[25\%\] \+ LITHIUM SULFATE \[200MM\]', r'100MM BIS-TRIS PH 6.5, 50% PEG 3350, 200MM LITHIUM SULFATE')
    if self.re_search(pdb, r'3hof'):  # FIXME: MD MORPHEUS not sure of concs
        line = self.re_substitute(line, r'30\%-42\.5\% MPD_P1K_P3350 MIX \(MDL\s*MORPHEUS SCREEN\), 0\.1M BUFFER 1 MIX \(MDL MORPHEUS SCREEN\)', \
              r'10% MPD, 10% PEG 1K, 10% PEG 3350, 0.1M IMIDAZOLE, 0.1M SODIUM CACODYLATE, 0.1M MES, 0.1M BIS-TRIS')
    if self.re_search(pdb, r'3hrs'):
        line = self.re_substitute(line, r'CONTAINING OPERATOR SEQUENCE', '')
    if self.re_search(pdb, r'3i2y|3i30|3i34|3i37'):
        line = self.re_substitute(line, r'PMSF', '')
    if self.re_search(pdb, r'3km6'):
        line = self.re_substitute(line, r'4MG/ML', r'4 MG/ML PROTEIN')
    if self.re_search(pdb, r'3kmn'):
        line = self.re_substitute(line, r'C47S/Y108V GST', r'PROTEIN')
    if self.re_search(pdb, r'3krb|3meb'):
        line = self.re_substitute(line, r'GILAA\.014(52|71)\.A', r'PROTEIN')
    if self.re_search(pdb, r'3k65'): # FIXME: MD MORPHEUS not sure of concs
        line = self.re_substitute(line, r'10\% BUFFER 1 MIX', r'0.1M IMIDAZOLE, 0.1M SODIUM CACODYLATE, 0.1M MES, 0.1M BIS-TRIS')
        line = self.re_substitute(line, r'10\% ALCOHOLS MIX', r'0.12 M 1,6-HEXANEDIOL, 0.12 M 1-BUTANOL, 0.12M 1,2-PROPANEDIOL, 0.12M 2-PROPANOL, 0.12M 1,4-BUTANEDIOL, 0.12M 1,3-PROPANEDIOL')
        line = self.re_substitute(line, r'40\% EDO\-P8K MIX', r'12% ETHYLENE GLYCOL, 12% PEG 8000')
    if self.re_search(pdb, r'3l41'):
        line = self.re_substitute(line, r'PH UNK,', '')
    if self.re_search(pdb, r'3lj9'):
        line = self.re_substitute(line, r'THE AZIDE COMPLEX WAS PREPARED BY\s*SOAKING OVERNIGHT IN', '')
    if self.re_search(pdb, r'3m1k'):
        line = self.re_substitute(line, r'1 MM FRAGMENT', r'1 MM PROTEIN')
    if self.re_search(pdb, r'3ncg'):
        line = self.re_substitute(line, r"\(NOT PH'ED\)", '')
    if self.re_search(pdb, r'3ne5'):
        line = self.re_substitute(line, r'\(7\.5\)', r'PH 7.5')
    if self.re_search(pdb, r'3new'):
        line = self.re_substitute(line, r'CO-CRYSTALLIZED WITH 1 MM COMPOUND 10', '')
    if self.re_search(pdb, r'3ndf'): # FIXME: MD MORPHEUS not sure of concs
        line = self.re_substitute(line, r'0\.12M ALCOHOLS \(MORPHEUS\), 0\.1M BUFFER\s*1', r'0.12 M 1,6-HEXANEDIOL, 0.12 M 1-BUTANOL, 0.12M 1,2-PROPANEDIOL, 0.12M 2-PROPANOL, 0.12M 1,4-BUTANEDIOL, 0.12M 1,3-PROPANEDIOL, 0.1M IMIDAZOLE, 0.1M SODIUM CACODYLATE, 0.1M MES, 0.1M BIS-TRIS')
    if self.re_search(pdb, r'3ogd'):
        line = self.re_substitute(line, r'BIS\-TRIS 6\.0\-\s*6\.6', r'BIS-TRIS PH 6.0-6.6')
    if self.re_search(pdb, r'3odq'):
        line = self.re_substitute(line, r'0\.2 M SALT OF\s*SEVERAL VARIETIES,', '')
    if self.re_search(pdb, r'3oce'):
        line = self.re_substitute(line, r'46\.3 MG/ML BRABA\.00047\.A\.A6 PS00513\s*AGAINST JCSG\+ CONDITION G3',r'46.6 MG/ML PROTEIN')
        line = self.re_substitute(line, r'CRSYTAL TRACKING ID 215219G3, 3C PROTEASE CLEAVED, PH\s*8\.5, VAPOR DIFFUSION, SITTING DROP,',r'PH 8.5')
    if self.re_search(pdb, r'3ocf'):
        line = self.re_substitute(line, r'86\.6 MG/ML OF BRABA\.00047\.A\.A5 PS00511\s*FULL LENGHT TAG AGAINST JCSG\+ CONDITION A9', r'86.6 MG/ML PROTEIN')
        line = self.re_substitute(line, r'CRYSTAL TRACKING ID 215952A9, PH 7\.5, VAPOR\s*DIFFUSION, SITTING DROP,', r'PH 7.5')
    if self.re_search(pdb, r'3p4f'): # FIXME: Any concs in paper?
        line = self.re_substitute(line, r'\(BUFFERED WITH\s*HYDROCHLORIC ACID/SODIUM HYDROXYDE TO PH 7\.0\)', r' PH 7.0')
    if self.re_search(pdb, r'307d'):
        line = self.re_substitute(line, r'AND.*', r'9.5-35% MPD')
    if self.re_search(pdb, r'32c2'):
        line = self.re_substitute(line, r'AT', '')
    if self.re_search(pdb, r'3cu4'):
        line = self.re_substitute(line, r'\(SALT RX SCREEN\-22\)', '')
    if self.re_search(pdb, r'3cow'):
        line = self.re_substitute(line, r'2\.5 MM OF INHIBITOR 2', '')
    if self.re_search(pdb, r'3coy'):
        line = self.re_substitute(line, r'6 MM OF INHIBITOR\s*3', '')
    if self.re_search(pdb, r'3coz'):
        line = self.re_substitute(line, r'6 MM OF INHIBITOR\s*4', '')
    if self.re_search(pdb, r'3e8j'):
        line = self.re_substitute(line, r'\(NOT PH\'ED\)', '')
    if self.re_search(pdb, r'3fn3'):
        line = self.re_substitute(line, r'\(NH4AC\)', '')

    if self.re_search(pdb, r'3g1d'):
        line = self.re_substitute(line, r'4000', r'POLYETHYLENE GLYCOL 4000')    
    if self.re_search(pdb, r'3h9e'):
        line = self.re_substitute(line, r'ETHYLENE GLYCOL \(PROTEIN BUFFER', r'ETHYLENE GLYCOL')
    if self.re_search(pdb, r'3kk4'):
        line = self.re_substitute(line, r'THIS\-CL', r'TRIS CHLORIDE')
    if self.re_search(pdb, r'3kzv'):
        line = self.re_substitute(line, r'1/1600 CHYMOTRYPSIN, PH 6\.0', r'0.0625% V/V CHYMOTRYPSIN PH6.0')    
    if self.re_search(pdb,r'3lhr'):
        line = self.re_substitute(line, r'A RESERVOIR SOLUTION COMPOSED OF','')
    if self.re_search(pdb, r'3mqb|3mqc'):
        line = self.re_substitute(line, r'WERE USED AS ADDITIVES FOR\s*OPTIMAL CRYSTAL GROWTH\.', '')
    if self.re_search(pdb, r'3v7[uwy]|3v8[0mnpqr]'):
        line = self.re_substitute(line, r'GLYCEROL 6%', r'6% GLYCEROL')
    if self.re_search(pdb, r'3o7i'):
        line = self.re_substitute(line, r'PH 7.0 TRIS-HCL', r'TRIS CHLORIDE PH 7.0')
    if self.re_search(pdb, r'3pm6'):
        line = self.re_substitute(line, r'COIMA.00345.A.A1 PS00465\s*AGAINST PROPLEX SCREEN CONDITION E11,', r'PROTEIN')
    if self.re_search(pdb, r'3pss'):
        line = self.re_substitute(line, r'REDUCTIVELY METHYLATED PROTEIN,', '')
    if self.re_search(pdb, r'3pvb'):
        line = self.re_substitute(line, r'DOUGLAS INSTRUMENTS ORYX8 CRYSTALLOGRAPHY ROBOT AS', '')
    if self.re_search(pdb, r'3qao|2wvz'):
        line = self.re_substitute(line, r'3350', r'POLYETHYLENE GLYCOL 3350')
    if self.re_search(pdb, r'3rap'):
        line = self.re_substitute(line, r'PEG.*', r'20-25% PEG 8000, 100MM TRIS CHLORIDE PH 8, 100MM MGCL2')
    if self.re_search(pdb, r'3ubp'):
        line = self.re_substitute(line, r'1OOMM', r'100MM')
    if self.re_search(pdb, r'3vhb'):
        line = self.re_substitute(line, r'AMMONIUM.*', r'1.3M AMMONIUM SULFATE, 0.1 M  SODIUM PYROPHOSPHATE, 3% ETHYLENE GLYCOL, PH 6.4')
    if self.re_search(pdb, r'462d'):
        line = self.re_substitute(line, r'.*', r'50MM CACODYLATE PH 7.0, 100MM MGCL2, 300MM KCL, 50% MPD')
    if self.re_search(pdb, r'480d'):
        line = self.re_substitute(line, r'X\s+\(', '')
    if self.re_search(pdb, r'4mat'):
        line = self.re_substitute(line, r'DIFFRACTION.*', '')
    if self.re_search(pdb, r'4rsk'):
        line = self.re_substitute(line, r'THE\s+COMPLEX.*', '')
    if self.re_search(pdb, r'4vhb'):
        line = self.re_substitute(line, r'THIOCYANATE.*', '')
    if self.re_search(pdb, r'4thn|5gds'):
        line = self.re_substitute(line, r'CRYSTAL\s+OF.*', '')
    if self.re_search(pdb, r'[567]msf'):
        line = self.re_substitute(line, r'PROTEIN.*', r'1.5% PEG 8000, 0.35M NA PHOSPHATE PH 7.4, 0.02% NA AZIDE')
    
    if self.verbose>1:
      print "parse:9", line
      
    line = self.re_substitute(line, r'ADDED\s+TO\s+THE\s+PROTEIN\s+SAMPLES', '')      
    line = self.re_substitute(line, r'BOTH SOLUTIONS', r'SOLUTIONS')
    line = self.re_substitute(line, r'\d+\s+HOURS?(\s+OF)?\s+SOAK(ING)?', '')
    line = self.re_substitute(line, r'\s+', r' ')
    line = self.re_substitute(line, r'\d+/\d+ PROTEIN SOLUTION/WELL SOLUTION', '')
    line = self.re_substitute(line, r'OF PROTEIN STOCK SOLUTION', '')
    line = self.re_substitute(line, r'\~', '')
    line = self.re_substitute(line, r'\bMGS?\s+PER\s+MLS?', r'MG/ML ')
    line = self.re_substitute(line, r'MG\.ML-1', r'MG/ML')
    line = self.re_substitute(line, r'MG\s+ML-1', r'MG/ML')
    line = self.re_substitute(line, r'\bMG\s+ML\b', r'MG/ML')
    line = self.re_substitute(line, r'G/L', r'MG/ML ')
    line = self.re_substitute(line, r'\b([0-9.]+)\s*MGS?/\s*ML\s+PROTEIN\s+CONCENTRATION', r'\1 MG/ML PROTEIN')
    line = self.re_substitute(line, r'(THE)?\s*PROTEIN\s+CONC\.?\s*(:|=|WAS|OF|IS|,)*\s*([0-9.]+)\s*MGS?/\s*ML', r' \3 MG/ML PROTEIN ')
    line = self.re_substitute(line, r'(THE)?\s*PROTEIN\s+CONCENTR?ATION\s*(=|WAS|OF|IS|:|,)*\s*([-0-9. ]+)\s*MGS*/\s*ML', r' \3 MG/ML PROTEIN ')
    line = self.re_substitute(line, r'(THE)?\s*PROTEIN\s+CONCENTR?ATION\s*(=|WAS|OF|IS|:|,)*\s*([-0-9. ]+)\s*MM', r' \3 MM PROTEIN ')
    line = self.re_substitute(line, r'(THE)?\s*PROTEIN\s+WAS\s+CONCENTRATED\s+TO\s+([0-9. ]+)\s*MGS*/\s*ML', r' \2 MG/ML PROTEIN ')
    line = self.re_substitute(line, r'(THE)?\s*PROTEIN\s+CONCENTRATION\s*:?', '')
    line = self.re_substitute(line, r'CONCENTRATION\s+(OF)?\s*PROTEIN\s*(WAS|IS|:)?\s*([0-9.]+)\s*MGS?\s*/\s*ML', r'\3 MG/ML PROTEIN')
    line = self.re_substitute(line, r'PROTEIN\s+WAS\s+CRYSTALLI[ZS]ED\s+AT\s+([0-9.]+)\s*MGS?\s*/\s*ML', r'\1 MG/ML PROTEIN')
    line = self.re_substitute(line, r'PROTEIN\s*[A-Z]*(AT|WAS|IS|:)?\s*\(?([0-9.]+)\s*MGS?\s*(/|PER)\s*ML\s*\)?', r' \2 MG/ML PROTEIN ')
    line = self.re_substitute(line, r'PROTEIN\s+WAS\s+AT\s+([0-9.]+)\s*MGS?\s*/\s*ML', r'\1 MG/ML PROTEIN') #note new as of 20060216...
    line = self.re_substitute(line, r'MGS?/\s*ML(S|E)?', r'MG/ML ')
    line = self.re_substitute(line, r'(\d+)MG\s+ML', r'\1 MG/ML')
    line = self.re_substitute(line, r'([0-9\.]+)\s*MG\.ML\s*\-1', r'\1 MG/ML')
    line = self.re_substitute(line, r'([0-9.]+)\s*MG/ML\s+OF\s+PROTEIN\s*(CONCENTRATION)?', r'\1 MG/ML PROTEIN ')

    line = self.re_substitute(line, r'([0-9.]+)\%(\w+)', r'\1% \2') # need a space between % and words to recognize units and chemical name
    line = self.re_substitute(line, r',\s*AND\b', r', ')
    line = self.re_substitute(line, r'\w*\bAND\b\w*', r', ')

    if self.verbose>1:
      print "parse:9a", line
    
    line = self.re_substitute(line, r'\bNA,\s*K\s+', r'SODIUM POTASSIUM ')  # fix for 1fnh and others?
    
    # Remove HYDRATES without losing 'DIHYDROGEN', 'MONOHYDROGEN' and 'HYDROGEN'
    line = self.re_substitute(line, r'(TETRA|TRI|THRI|TRY|THREE|DI|DE|PENTA|HEPTA|HEXA|MONO| )-?[GH]YDO?RATED?', '')
    line = self.re_substitute(line, r'(TETRA|TRI|THRI|TRY|THREE|PENTA|HEPTA|HEXA)-?HYDROGEN', '')
    line = self.re_substitute(line, r'(DATA .*)?\s*COLLECTED .*', '')

    # Removing 'bad words'
    for bad_word in bad_word_list:
      if self.verbose>11:
        print "badword: ", repr(bad_word)
      line = self.re_substitute(line, r'\b'+bad_word+r'\b', '')
      if self.verbose>11:
        print line
        print
    
    line = self.re_substitute(line, r'X-RAY DIFFRACTION .*', '')
    line = self.re_substitute(line, r'((PRIOR TO|BEFORE) .*)?\s*COLLECTION.*', '')
    line = self.re_substitute(line, r'CRYOPROTECTION\s+CONDITIONS:?', '')
    line = self.re_substitute(line, r'FOR CRYOPROTECTION', '')
    line = self.re_substitute(line, r'(WAS USED)?\s*(AS)?\s*A?\s*CRYOPRO?T?ECTING\s*AGENT', '')
    line = self.re_substitute(line, r'\(?CRYO$', '')
    line = self.re_substitute(line, r'AT AMBIENT PRESSURE', '')
    line = self.re_substitute(line, r'\bSERVED\b', '')
    line = self.re_substitute(line, r'\bBEING\b|\bADDING\b|\bSAMPLE\b|\bALLOWED\b', '')
    line = self.re_substitute(line, r'(\bMIXTURE\b|\bANALOGUE\b|\bEITHER\b|\bRESPECTIVELY\b|\bTRANSFERR?(ED|ING)\b)', '')

    line = self.re_substitute(line, r'WAS THEN ADDED AS CRYO', '')
    line = self.re_substitute(line, r'(ADDED)?\s*AS\s*(THE|A)?\s*CRYO\-? ?PRO?T?ECTANT', '')
    line = self.re_substitute(line, r'CRYO-(PROTECTANT)?', '')
    line = self.re_substitute(line, r'CRYOCOOLED', '')
    line = self.re_substitute(line, r'(CRYSTAL\s+WAS|CRYSTALS\s+WERE)?\s*TRANSFERRED', '')
    line = self.re_substitute(line, r'CRYO\s?PROTECTION WAS', '')
    line = self.re_substitute(line, r'CRYOPROTR?ECTED', '')

    line = self.re_substitute(line, r'CRYOPROTECTION', '')
    line = self.re_substitute(line, r'FROZEN IN [A-Z].*', '')
    line = self.re_substitute(line, r'FROZEN', '')
    line = self.re_substitute(line, r'FOLLOWED BY A?\b', '')
    line = self.re_substitute(line, r'CRYSTALLIZATION\s+CONDITIONS:', '')
    line = self.re_substitute(line, r'.* CRYSTALLIZATION\s+SOLUTION:', '')
    line = self.re_substitute(line, r'INHIBITOR\s+WAS\s+ADDED .*', '')
    line = self.re_substitute(line, r'INHIBITOR\s+SOAK(ED|ING) .*', '')
    line = self.re_substitute(line, r'NUCLEATION .*', '')
    line = self.re_substitute(line, r'SUBSEQUENTLY', '')
    line = self.re_substitute(line, r'CAT WHISKER', '')
    line = self.re_substitute(line, r'HAMPTON RESEARCH', '')
    line = self.re_substitute(line, r'EVERY OTHER DAY', '')
    line = self.re_substitute(line, r'PERIOD FIVE MONTHS', '')
    line = self.re_substitute(line, r'C\.\s+ALBICANS', '')

    if self.verbose>1:
      print "parse:9b", line
    
    line = self.re_substitute(line, r'CRYSTALS\s+WERE\s+EXPOSED .*', '')
    line = self.re_substitute(line, r'CRYSTALS\s+OF\s+THE\s+NATIVE .*', '')
    line = self.re_substitute(line, r'PRIOR TO ', '')  # was r'PRIOR TO .*',
    line = self.re_substitute(line, r'THE CONCENTRATION OF (.*) WAS ADJUSTED TO\s*(\d+%)\s*V?/?V?', r'\2 \1')
    line = self.re_substitute(line, r'AD?JUSTED (TO|WITH|AT|ON)', '')
    line = self.re_substitute(line, r'CONSISTED (OF|AN|ON)', '')
    line = self.re_substitute(line, r'COMPRISED OF', '')
    line = self.re_substitute(line, r'CONSISTING OF', '')
    line = self.re_substitute(line, r'ANAEROBIC \(AR .*', '')
    line = self.re_substitute(line, r'\(UNDER ANAEROBIC CONDITIONS\)', '')
    line = self.re_substitute(line, r'\((EMERALD|HAMPTON|INDEX) SCREEN.*\)', '')
    line = self.re_substitute(line, r'\(HAMPTON\s*RESEARCH\)', '')
    line = self.re_substitute(line, r'REFERENCE\s*\d\b', '')
    line = self.re_substitute(line, r'(REFERENCE|CONCERNING|DETAILS|PROCEDURES|WITHIN)', '')
    
    if self.verbose>1:
      print "parse:9c", line
      
    line = self.re_substitute(line, r'\(FOR DETAILS .*\)', '')
    #line = self.re_substitute(line, r'\bSEE .*', '')
    line = self.re_substitute(line, r'\bSEE ', '')
    line = self.re_substitute(line, r'\(SEE .*\)', '')
    line = self.re_substitute(line, r'LATER SOAKED .*', '')
    line = self.re_substitute(line, r'THEN IT WAS SOAKED .*', '')
    line = self.re_substitute(line, r'.*CRYSTALS GROW FROM', '')
    line = self.re_substitute(line, r'\b(IN|AGAINST)\s*(THE)?\s+SAME\s+BUFFER', '')
    
    if self.verbose>1:
      print "parse:9d", line
      
    if self.re_search(line, r'^DROP:') or self.re_search(pdb, r'1aq6|1lsh'):
      if self.re_search(line, r'\bWELL:'):
        line = self.re_substitute(line, r'.* WELL:', '')
      elif self.re_search(line, r'RESERVOIR\s+RESERVOIR:'):
        line = self.re_substitute(line, r'.*RESERVOIR\s+RESERVOIR:', '')
      elif self.re_search(line, r'PROTEIN\s+RESERVOIR:'):
        line = self.re_substitute(line, r'.*PROTEIN\s+RESERVOIR:', '')

    if self.verbose>1:
      print "parse:10", line
    
    if self.re_search(line, r'WELL\s+SOLUTION\s+CONTAINING'):
      if not self.re_search(line, r'\bE\. COLI TS\b'):
        line = self.re_substitute(line, r'.*WELL\s+SOLUTION\s+CONTAINING', '')
      else:
        line = self.re_substitute(line, r'.*WELL\s+SOLUTION\s+CONTAINING', r'20MM POTASSIUM PHOSPHATE, PH 7.8,')

        
        
    if self.re_search(line, r'HANGING') or self.re_search(pdb, r'1a21|1a29|1a33|1azv|1biy|1bj1|1bkh|1bn7|1c1a|1ddk|1fjs|1ft1|1gzm|1uzj'):
      line = self.re_substitute(line, r'.* RESERVI?OI?R\s+CONTAINE?D', '')
      line = self.re_substitute(line, r'.* RESERVI?OI?R\s+SOLUTION,?\s+CONTAIN(ING|ED)', '')
      line = self.re_substitute(line, r'.* AGAINST', '')
      line = self.re_substitute(line, r'.* IN WELL', '')
      line = self.re_substitute(line, r'.* WELL,', '')
      line = self.re_substitute(line, r'.* WELL\s+CONTAINED', '')
      line = self.re_substitute(line, r'.* WELL\s+SOLUTION\s+COMPOSED\s+OF', '')
      line = self.re_substitute(line, r'.* WITH RESERVOIR', '')
      line = self.re_substitute(line, r'.* GROWN USING THE HANGING DROP METHOD FROM', '')
      line = self.re_substitute(line, r'HANGING\s+DROP\s+CONSISITED .*', '')
      line = self.re_substitute(line, r'\+ G5 .*', '')
      line = self.re_substitute(line, r'(THE\s+)?PROTEIN\s+CONCENTR?ATION\s+(WAS|IS).*', '')
      if not self.re_search(pdb, r'1c5[no]|1ft2|1h6m|1h8f'):
        line = self.re_substitute(line, r'.*RESERVOIR\s+SOLUTION\s+(OF)?', '')
      if not self.re_search(pdb, r'1bkh|1qg5'):
        line = self.re_substitute(line, r'DROP\s+CONTAINED .*', '')
      if self.re_search(pdb, r'1guk'):
        line = self.re_substitute(line, r'DISSOLVED.*', '')
      if self.re_search(pdb, r'1azv'):
        line = self.re_substitute(line, r'.* SOLUTION OF', '')
      if self.re_search(pdb, r'1bc2'):
        line = self.re_substitute(line, r'6UL DROPS.*', '')
      if self.re_search(pdb, r'1d3l'):
          line = self.re_substitute(line, r'.*DROP METHODS:', '')
      if self.re_search(pdb, r'2e2a|1h14'):
          line = self.re_substitute(line, r'HANGING-DROP.*', '')
      if self.re_search(pdb, r'1[89]gs'):
          line = self.re_substitute(line, r'DROPS WERE .*', '')
      if self.re_search(pdb, r'1fjs|1olt'):
          line = self.re_substitute(line, r'.* RESERVOIR(;|:)', '')
      if self.re_search(pdb, r'1bn7|1gzj|1nmt'):
        line = self.re_substitute(line, r'.*UL RESERVOIR', '')
      if self.re_search(pdb, r'1b35|1c5m|1h2[cd]|1hkw|2wsy|2exr|2f2g'):
        line = self.re_substitute(line, r'.*WELL\s+SOLUTION\s+(CONSISTED)?:?', '')
        line = self.re_substitute(line, r'DROP COMPOSITION:.*', '')
        line = self.re_substitute(line, r'\)', '')
      if self.re_search(pdb, r'1ahp|1aim|1ap2|1avm|1b7v|1gl2|2hlc|1lk9|1odb'):
        line = self.re_substitute(line, r'(THE|BY|IN)? HANGING(-| )DROPS?.*', '')
      if self.re_search(pdb, r'1qjs'):
        line = self.re_substitute(line, r'2 NACL', r'2M NACL')
        line = self.re_substitute(line, r'PROTEIN COMPLEX .*', r'65 MG/ML PROTEIN')
      if self.re_search(pdb, r'1w8v'):
        line = self.re_substitute(line, r'.*METHOD', '')
      line = self.re_substitute(line, r'USING (A|THE)\s+HANGING DROP (SETUP|SYSTEM)', '')
      line = self.re_substitute(line, r'.*CRYSTALLIZED BY HANGING DROP METHOD\b', '')
      line = self.re_substitute(line, r'HANGING\s+DROP\s+(METHOD|EXPERIMENT|TECHNIQUE)', '')
      line = self.re_substitute(line, r'HANGING\s+DROP(:|S)?', '')
    if self.re_search(line, r'SITTING') and not self.re_search(pdb, r'1a21|1a29|1a33|1azv|1bj1|1c1a|1fjs|1ft1'):
      line = self.re_substitute(line, r'AGAINST RESERVOIR .*', '')
      line = self.re_substitute(line, r'THE CONCENTRAT?ION OF .* RESERVOIR WAS .*', '')
      line = self.re_substitute(line, r'RESERVOIR WAS .*', '')
      line = self.re_substitute(line, r'RESERVOIRS CONTAINED.*', '')
      line = self.re_substitute(line, r'WAS REPLACED BY .*', '')
      if self.re_search(pdb, r'1a75'):
        line = self.re_substitute(line, r'DROP:.*', '')
        line = self.re_substitute(line, r'.*RESERVOIR: 1 ML', '')
      if self.re_search(pdb, r'1a04|1gmj|1mhe|1uw7'):
        line = self.re_substitute(line, r'SITTING.*', '')
      line = self.re_substitute(line, r'SITTING\s*DROP\s*(METHOD|EXPERIMENT|TECHNIQUE)', '')
      line = self.re_substitute(line, r'SITTING(-|\s*)DROPS?', '')
      line = self.re_substitute(line, r'SITTING\s*WELLS?', '')
      
    # MICROs, OILs
    line = self.re_substitute(line, r'OIL\-? ?(MICRO)? ?BATCH\s*(METHOD)?', '')
    line = self.re_substitute(line, r'MACRO\s*\-?BATCH', '')
    line = self.re_substitute(line, r'(MODIFIED\s*MICROBATCH|OIL\s*MICRO ?BATCH)', '')
    line = self.re_substitute(line, r'MICROFLUIDIC\s+FREE\s+INTERFACE','')
    line = self.re_substitute(line, r'PLUG\-BASED\s+MICROFLUIDICS', '')
    line = self.re_substitute(line, r'M?ICROB[AU]TCH (CRYSTALLI[ZS]ATION )?UNDER PARAFF?INE? OIL', '')
    line = self.re_substitute(line, r'GEL-TUBE METHOD', '')
    line = self.re_substitute(line, r'(PERMEABLE OIL|PRECIPITATION|HANGING(\s*\-\s*DROP)?|SITTING|EXPERIMENT(S|AL)?)+', '')
    
    # FIXME: whose tracking id is this?
    line = self.re_substitute(line, r'TRACKING ID [A-Z0-9]{8,9}', '')

    line = self.re_substitute(line, r'CRYSTALS WERE REDUCED .*', '')
    line = self.re_substitute(line, r'REDUCED\s+(USING|WITH).*', '')
    line = self.re_substitute(line, r'CRYSTALS WERE STABILIZED IN .*', '')
    line = self.re_substitute(line, r'STABILIZED IN .*', '')

    # MOTHER LIQUOR
    line = self.re_substitute(line, r'MOTHER LIQUOR(\s+CONTAINING)', '')
    line = self.re_substitute(line, r'.*MOTHER\s+LIQUOR\s+\=', '')
    line = self.re_substitute(line, r'.*MOTHER\s+LIQUOR:', '')
    line = self.re_substitute(line, r'.*MOTHER\s+LIQUOR\s+CONTAIN(S|ING|ED)', '')
    line = self.re_substitute(line, r'\b[0-9]*\s*(UL|ML)\s+OF MOTHER LIQUOR', '')
    line = self.re_substitute(line, r'MOTHER LIQUOR', '')
    line = self.re_substitute(line, r'LIQUOR', '')
    if self.verbose>1:
      print "parse:11", line

    line = self.re_substitute(line, r'\b([0-9.]+\s*\+\s*)?[0-9.]+\s*(UL|ML)\s*DROPS?', '')
    #line = self.re_substitute(line, r'[0-9.]+\s*[MU]LS?\s+(OF\s+)?(PROTEIN|DROPS|RESERVOIR)', '')
    line = self.re_substitute(line, r'MMSODIUM', r'MM SODIUM') #2hmy
    line = self.re_substitute(line, r'\(PDB ENTRY.*\)', '') #1rnx, 1rny
    line = self.re_substitute(line, r'4.7 \(V/V\)', r'4.7% (V/V)') #2tdt
    line = self.re_substitute(line, r'AMSO4,N50', r'AMSO4, 50') #1vip
    line = self.re_substitute(line, r'\bA\.S\.', r'AMMONIUM SULFATE') #1bk4
    line = self.re_substitute(line, r'AS,0.2 2', r'AMMONIUM SULFATE, 0.2 M 2') #1bqa 1bqd
    line = self.re_substitute(line, r'AMMON\. SULPH\.', r'AMMONIUM SULFATE') #1ml8
    line = self.re_substitute(line, r'AMMONIUM SULFATE ON', r'AMMONIUM SULFATE') #1kac
    line = self.re_substitute(line, r'\(BAKER\)', '') #1coz
    line = self.re_substitute(line, r'=+', '') #1ajr
    line = self.re_substitute(line, r'([0-9])+M M ', r'\1MM ') #1eon
    line = self.re_substitute(line, r'DEAD SEA', '') # Yes, some people use dead sea water
    line = self.re_substitute(line, r'(\bVIA|\bREVERSE)','')
    
    line = self.re_substitute(line, r'\b(IN)?\s*WATER', '')
    
    # (1) blah (2) blah (3) blah etc.
    line = self.re_substitute(line, r'\(\d\)', '')
    
    # #1, #2, #3 etc.
    line = self.re_substitute(line, r'\s+\#\d+(\s+)', r'\1')
    
    # x% MORE y
    line = self.re_substitute(line, r'\d+\s*%\s+MORE\s+\S+', '')
    
    line = self.re_substitute(line, r'PLUS \d+ UL RESERVOIR SOLUTION:', '')
    
    line = self.re_substitute(line, r'(\bA )?SOLUTIONS*', '')
    line = self.re_substitute(line, r' ADDITIONAL','')
    line = self.re_substitute(line, r'\s+IN\s+[A-Z]+\s*([A-Z]+)?\s+BUFFER', '')
    line = self.re_substitute(line, r'\bBUFFER\s+X\b', '')
    line = self.re_substitute(line, r'(\bPH UNBUFFERED|\bUNBUFFERED|\(?(PH)?\s*NO\s+BUFFER\)?|\bBUFFERED (WITH|TO)|\b(A )?BUFFER(ED)?)+', '')
    line = self.re_substitute(line, r'^.*\sPROTEIN CRYSTALLI[ZS]ED FROM', '')
    line = self.re_substitute(line, r'AURORA A PROTEIN', r'PROTEIN')
    line = self.re_substitute(line, r'PROTEIN\s+WAS\s+CRYSTALLI[ZS]ED\s+(FROM|IN)?', r' ')
    line = self.re_substitute(line, r'\d:\d RATIO', '')
    line = self.re_substitute(line, r'\bRATIO\s+OF\s+\d:\d', '')
    line = self.re_substitute(line, r'\bRATIO\s+\d\s*(TO|-)\s*\d', '')
    line = self.re_substitute(line, r'(CO\-)?CRYSTALLI[ZS]ED USING', '')
    line = self.re_substitute(line, r'(CO\-)?CRYSTA?LLI[ZS]ED', '')
    line = self.re_substitute(line, r'CRYSTALS WERE OBTAINED FROM A SOLUTION THAT CONTAINED', '')
    line = self.re_substitute(line, r'CRYSTALS\s*WERE\s*(THEN)?\s*GROWN\s*(AT)?', '')
    line = self.re_substitute(line, r'IMPROVED CRYSTALS .*', '')
    line = self.re_substitute(line, r'CRYSTALS\s+WERE', '')
    line = self.re_substitute(line, r'CRYSTAL COULD NOT .*', '')
    line = self.re_substitute(line, r'\bFROM PREVIOUS CRYSTALS .*', '')
    line = self.re_substitute(line, r'\bTHE MIXED DROPS .*', '')
    line = self.re_substitute(line, r'CRYSTALS GREW BY MIXING .*', '')
    line = self.re_substitute(line, r'CRYSTAL GROWTH TOOK .*', '')
    line = self.re_substitute(line, r'\bA SINGLE CRYSTAL OF .*', '')
    line = self.re_substitute(line, r'SINGLE CRYSTALS WERE WASHED .*', '')
    line = self.re_substitute(line, r'(THE)?\s*NATIVE', '')
    line = self.re_substitute(line, r'.* THE DROPLET CONSISTED .* WHICH CONTAINED', r'4 DEG C,')
    line = self.re_substitute(line, r'WASHED CRYSTALS .*', '')
    line = self.re_substitute(line, r'MACROSEEDS WERE.*', '')
    line = self.re_substitute(line, r'MACROSEED(ING?|ED)', '')
    line = self.re_substitute(line, r'\bGLYCEROL\s+ADDED .*', '')
    line = self.re_substitute(line, r'\bFROM REDUCTION .*', '')
    line = self.re_substitute(line, r'\(\s*A\s+REDUCTANT\s*\)', '')
    line = self.re_substitute(line, r'\(\s*AN\s+OXIDANT\s*\)', '')
    line = self.re_substitute(line, r'\bBATCH TECHNIQUES*', '')
    line = self.re_substitute(line, r'(\bBATCH\s+METHOD|\bMICRO[- ]?BAT?CH|\bBATCH|\bUNDER-?\s*OIL)+', '')
    line = self.re_substitute(line, r'(\bAGAINST(\s+A)?|\bFINAL|\bANHYDROUS|\bMICRODIALYSIS|\bCAPILLARY)+', '')
    line = self.re_substitute(line, r'(SANDWICH|CRYSCHEM|NUNC|96 WELL|24 WELL)\s+PLATES?', '')
    line = self.re_substitute(line, r'(\bDIALYSIS|\bBUTTONS?|MICROGRAVITY)+', '')
    line = self.re_substitute(line, r'\b(IN\s*)?(THE)? PRESEN[CS]E OF', '')
    line = self.re_substitute(line, r'\bIN\s+THE\s+RANGE', '')
    line = self.re_substitute(line, r'\bWITHIN\s+THE\s+.*RANGE', '')
    line = self.re_substitute(line, r'\bWAS\s+DILUTED \d(/|:)\d', '')
    line = self.re_substitute(line, r'\bDILUTED\s+TWICE', '')
    line = self.re_substitute(line, r'\bCONDITION\s+([0-9]{2}\s+)?[A-H]1?[0-9]\b', '')
    line = self.re_substitute(line, r'(\bDILUTED|\bGRADIENT|\bCONDITIONS?)+', '')
    line = self.re_substitute(line, r'\b(ARGON|NITROGEN|ANAEROBIC|AR)\s*ATMOSPHERE', '')
    line = self.re_substitute(line, r'\bANAEROBIC', '')
    line = self.re_substitute(line, r'SE\-MET PROTEIN', r'PROTEIN')
    line = self.re_substitute(line, r'\bSUSPENDED OVER .* (WELLS?|RESERVOIR)', '')
    line = self.re_substitute(line, r'.* WELL SOLUTION CONTAINED', '')
    line = self.re_substitute(line, r'PROTEIN SOLUTION:', '')
    line = self.re_substitute(line, r'PROTEIN\s+SOLUTION\s+WAS\s+MIXED\s*(\d:\d)?', r'PROTEIN ')
    
    # Time: hours, days, minutes ...
    line = self.re_substitute(line, r'\bFEW (WEEKS|DAYS)?', '')
    line = self.re_substitute(line, r'(\d+-\s*)?\d+\s*(WEEKS?|DAYS?|HOURS?\b|MINUTES?|MINS?\b)', '')
    line = self.re_substitute(line, r'\b(ONE|TWO|FOUR) WEEKS?', '')
    line = self.re_substitute(line, r'^WEEKS', '')
    line = self.re_substitute(line, r'\bFOR\s*\d+\s*HRS?', '')
    line = self.re_substitute(line, r'\bON A SILICONIZED COVERSLIP .*', '') #1fhi
    line = self.re_substitute(line, r'\bSILICONIZED GLASS COVER SLIDES', '')
    line = self.re_substitute(line, r'\(COLD ROOM\)', '')
    line = self.re_substitute(line, r'\b4,?000 OR 8,?000', r'4000') #830c, 456c
    line = self.re_substitute(line, r'\b4000-6000', r'4000') #1a3k

    if self.verbose>1:
      print "parse:12", line
    
    line = self.re_substitute(line, r'(THE) DROP CONTAINED \d+:\d+ MIX(TURE) OF (WELL|RESERVOIR|PRECIPITANT)', '')
    line = self.re_substitute(line, r'.* MIXED WITH\w* WELL BUFFER', '')
    line = self.re_substitute(line, r'\d+\.?\d*\s*\-?\s*FOLD(\s+M(OLAR)?)?\s+EXCESS\s+O?FO?\s+\S+', '')
    line = self.re_substitute(line, r'(FIVE|TEN|THREE)\s*\-?\s*FOLD(\s+MOLAR)?\s+EXCESS\s+O?FO?\s+\S+', '')
    line = self.re_substitute(line, r'MIXED \d:\d WITH', '')
    line = self.re_substitute(line, r'USED AS CRYOPROTECTANT', '')
    line = self.re_substitute(line, r'PROTEIN:WELL\s*=?\s*\d:\d', '')
    line = self.re_substitute(line, r'CRYSTAL SOAKED (IN|WITH) .*', '')

    if self.verbose>5:
      print "parse12a", line
    
    #line = self.re_substitute(line, r'\(?SOAKED (IN|INTO|FOR|WITH|BY|TO):? .*', '')
    # replaced with:
    line = self.re_substitute(line, r'\(?SOAKED (IN|INTO|FOR|WITH|BY|TO):?', '')
    line = self.re_substitute(line, r'SOAKED OVERNIGHT .*', '')
    line = self.re_substitute(line, r'OVERNIGHT', '')
    line = self.re_substitute(line, r'(AN\s+)?EQUAL\s+PART\b', '')
    line = self.re_substitute(line, r'COMPLEX PREPARED BY', '')
    line = self.re_substitute(line, r'\(FLUKA\)', '')
    line = self.re_substitute(line, r'(\bNANODROP|\bDROPLETS?|\bNEOMYCIN B|\bEVAPORATION|\bRECRYSTALLIZATION|\bINCUBATED)+', '')
    line = self.re_substitute(line, r'CRYSTALS? (WERE|WAS)', '')
    line = self.re_substitute(line, r'(\bCRYSTALS|\bSLOW|\bFLASH|\bCOOL(ING|ED)|\bA?\s*PRECIPITATING AGENT|\bTRAYS?|OBTAINED)+', '')
    line = self.re_substitute(line, r'\bCRYSTALLI[ZS]ATION\s*(IN)?', '')
    line = self.re_substitute(line, r'INHIBITOR CONCENTRATION .*', '')
    line = self.re_substitute(line, r'INHIBITORS?', '')
    line = self.re_substitute(line, r'\blineEAK(-| )*SEED(ED|ING).*', '')
    line = self.re_substitute(line, r'\bMICROSEEDS.*', '')
    line = self.re_substitute(line, r'\b\(MERCK', '')
    line = self.re_substitute(line, r'\bCOCKTAIL', '')
    line = self.re_substitute(line, r'\(SATURATION\)', '')
    line = self.re_substitute(line, r'\bSATURATION *', '')
    line = self.re_substitute(line, r'\bMICRO\s+SEED(ING)*', '')
    line = self.re_substitute(line, r'\bMICRO-\s+AND\s+MACRO-SEED(ING)?.*', '')
    line = self.re_substitute(line, r'\bTITRATED\s+(TO|WITH)\s*(NAOH|HCL|BASE|ACID)?', '')
    line = self.re_substitute(line, r'\bWITH\s+(NAOH|HCL|BASE|ACID)', '')
    line = self.re_substitute(line, r'\bMICRO-?SEED(ING|ED)', '')
    line = self.re_substitute(line, r'OPTIMIZED', '')
    line = self.re_substitute(line, r'\(ANATRACE\)', '')
    line = self.re_substitute(line, r'\bSTREAK\s*-?SEED(ING|ED)', '')
    line = self.re_substitute(line, r'\bSEED(ING|ED)', '')
    line = self.re_substitute(line, r'OPTIMAL GROWTH', '')
    line = self.re_substitute(line, r'\b(AS)?\s*PRECIP[IA]TANT\b', '')
    line = self.re_substitute(line, r'\b(AS)?\s*AN\s+ADDITIVE\b', '')
    line = self.re_substitute(line, r'COUNTER\-?\s*DIFFUSION\s*(METHOD)?', '')
    
    if self.verbose>5:
      print "parse12b", line
    line = self.re_substitute(line, r'STEP-WISE', '')
    line = self.re_substitute(line, r'(\bTRANSFER\b|\bCONTAINING\b|\bADDITIVES?:?|\bTECHNIQUES?|\bMIXED|\bCRYO-?PRO?T?ECTANT)+', '')
    line = self.re_substitute(line, r'(\bSATURATING|\bSATURATED|\bSAT\.|\bSATN\.|\bSATD\b|\bSOAK\b|\bDISSOLVED\b)+', '')
    line = self.re_substitute(line, r'(\bEQUILI?BRATED?|\bEQUILIBRATION|\bSTABILIZED?|\bWELL(:|S)?|\bDROP(S|LET)?)+', '')
    line = self.re_substitute(line, r'(\bWAS\b|\bWERE\b|\bIS\b|\bFROM\b|\bPLUS\b|\bCOLD|\bNOT\b|SAME|\bALONE)+', '')
    line = self.re_substitute(line, r'(\bRATIO|\bSTOCKS?|\bEACH|\bUSING|\bOVER( A)?\b|\bBEFORE|\bAFTER|\bFOR\b|TOTAL)+', '')
    line = self.re_substitute(line, r'(\bDEPOSIT(ED|ING)?)', '')
    line = self.re_substitute(line, r'(PROTECTED\b|\bTHEY\b|\bINTO\b|\bTO\b)', '')
    line = self.re_substitute(line, r'(\bPRECIPITAT(ING|ED|E))+', '')
    line = self.re_substitute(line, r'\bMPD IN\b', r'MPD, ')
    line = self.re_substitute(line, r'(\bNONE\b|\bTHIS\b|\bTHE\b|\bWITH\s+A\b|\bWITHOUT\b|\bWITH\b|\bIN\s+A\b|\bIN\b|CONTAINED|AROUND|MIXING|\bANY\b|\bADDITION\b)+', '')    
    
    line = self.re_substitute(line, r'(ALL\s*OTHER|ARE\s*DEEP\s*RED|CLASSICS\s*II|COULD\s*BE|ELECTRON\s*DENSITY\s*MAPS?|EXPRESSION\s*TAG\s*REMOVED|MOUNTED\s*ON\s*NYLON\s*LOOP)', '')
    line = self.re_substitute(line, r'(EXPRESSION\s*TAG|LESS\s*THAN|LOWER|MORE\s*THAN|MOTHER\s*LIQUOR|NEXT\s*DAY|NYLON\s*LOOP|ON\s*ICE|ONE\s*DAY|PDB\s*ENTRY|PER\s*CENT)','')
    line = self.re_substitute(line, r'(US\s*SPACE\s*SHUTTLE|PRIOR\s*SET\s*UP|PROTEIN\s*DATA\s*BANK\s*ENTRY|SEALED\s*24\s*PLATE|SET\s*UP|SETTING\s*UP|SILVER\s*BULLET|SINGLE\s*THIN\s*PLATES)', '')
    line = self.re_substitute(line, r'UNDER\s*(MINERAL|PARAFFIN|PARRAFIN)\s*OIL', '')
    
    # Sizes
    line = self.re_substitute(line, r'SIZE\s*(OF)?\s*\d+\s*X\s*\d+\s*UM', '')
    line = self.re_substitute(line, r'SIZE\s*(OF)?\s*\d+\s*UM', '')
    
    if self.verbose>5:    
      print "parse12c", line
    
    line = self.re_substitute(line, r'\bGROWN (IN)?', '')
    line = self.re_substitute(line, r'\bUNDER RED LIGHT', '')
    line = self.re_substitute(line, r'\bCRS?YSTALS?', '')
    line = self.re_substitute(line, r'(\bSETUP|STORED|LYOPHILI[SZ]ED|\bJUST|\bHYDRA\b|ROBOT\b|NUNC|\bBOX\b|\bCRYO\b)', '')
    line = self.re_substitute(line, r'(\bNEAR PHYSIOLOGICAL PH\b|CONCENTRATION OF APPLIED|SMALL|TUBES|FRESH(LY)?)+', '')
    line = self.re_substitute(line, r'(\bRE[CS]ERVOIR[S:]?|\bGEOMETRY|\bEXCESS|\bWAS\b|\bTHERMAL GRADIENT|\bCOMBINED)+', '')
    line = self.re_substitute(line, r'(1\s+VOLUME\s+OF\s+|\bIT\b|\bOF\b|\bBY\b|\bTHEN\b|\bBOTTOM|\bFOUR\b|SEVERAL|\bDAYS|BROUGHT( TO)?)+', '')
    line = self.re_substitute(line, r'LIQUID\s*(DIFFUSION|NITROGEN|PROPANE|N2)', '')
    line = self.re_substitute(line, r'(VAPOU?R|LIQUID|DIFFUSION|METHOD|PREPARED|APPROX(IMATELY)?|(AN\s+)?EQUAL|VOLUM?N?E?S?)+', '')
    line = self.re_substitute(line, r'(\bDARK\b|SUPPLEMENTED|\bNULL|RESULTING|PURE|CONCENTRATION|THERMAL|ROOM|INITIAL|\bMADE)+', '')
    line = self.re_substitute(line, r'(\bAVERAGE|\bFREEZING\s*(COND)?|\bSOAKED)', '')
    line = self.re_substitute(line, r'(\bUSED|\bCLEAVED|\bENHE?ANCED|\bPEAK([0-9])?|\bFULL)', '')
    line = self.re_substitute(line, r'\bDRIED\s+(UP)?\b', '')
    line = self.re_substitute(line, r'\bACID\)', r'ACID')

    if self.verbose>5:
      print "parse12c", line
    
    # Remove ratios
    line = self.re_substitute(line, r'([0-9]:)?[0-9]:[0-9]', '')
    
    line = self.re_substitute(line, r'[.,|]\s*A\s*$','')
    line = self.re_substitute(line, r'[-.,:;+( ]+\s*$','')
    line = self.re_substitute(line, r'\((?!.+\))','')
    
    
    # Any '+' that isn't 'NAD+' gets converted to ' '
    line = self.re_substitute(line, r'(?<!(NAD| ZN))\+',r' ')
    
    line = self.re_substitute(line, r'REMARK 2[89]0', '')
    line = self.re_substitute(line, r'(\bONTO|\bPERIOD\b|\bREPLACEMENTS\b|\bWEEKS?\b|\bDURING\b|\bWHICH\b)', '')

    if self.verbose>5:
      print "parse12d", line
    
    # Protein id converted to "PROTEIN"
    line = self.re_substitute(line, r'[A-Z]{5}\.[0-9]{5}\.[A-Z](\.[A-Z][0-9])?(\.[A-Z0-9]+)?(\s+[A-Z]{2}[0-9]{5})?', r'PROTEIN')
    line = self.re_substitute(line, r'PROTEIN\s+\(\s*PROTEIN\s*\)', r'PROTEIN')
    
    line = self.re_substitute(line, r'(PACT|EMERALD BIOSYSTEMS|WIZARD([\s\-]I?I?I)?|JCSG|HAMPTON|INDEX|SCREEN|QIAGEN|CRYOS\s+SUITE)', '')
    
    line = self.re_substitute(line, r'\bAT\s+A\b', '')
    
    # XX at NN UNITS -> NN UNITS XX
    line = self.re_substitute(line, r'^\s*([A-Z ]+)\s+AT\s+([-0-9.]+\s*('+self.UNITS_REGEXP+'))', r'\2 \1')
    
    if self.verbose>5:
      print "parse12e", line
     
    # XX MM PROTEIN (XX MG/ML) -> XX MG/ML PROTEIN
    line = self.re_substitute(line,r'\s*\d+\s*MM\s*PROTEIN\s*\((\d+\s*MG/ML\s*)\)', r'\1 PROTEIN')
    
    # VV VOL CHEM (NN UNITS) -> NN UNITS CHEM
    line = self.re_substitute(line, r'[0-9.]+\s*[MU]LS? +([-A-Z ]+)\s+\(\s*([-0-9.]+\s*('+self.UNITS_REGEXP+')\s*)\)', r'\2 \1')   
    
    # CHEM UNITS -> UNITS CHEM
    line = self.re_substitute(line, r'^\s*([-A-Z ]+)\s+(\d+\.?\d*\s*('+self.UNITS_REGEXP+'))\s*$', r'\2 \1')
    
    if self.verbose>5:
      print "parse12f", line
    
    # XX (PH P, NN Y) -> NN Y XX (PH P)
    line = self.re_substitute(line, r'^\s*([-A-Z ]+)\s+\(\s*(PH\s*[0-9.]+),?\s+([-0-9.]+\s*('+self.UNITS_REGEXP+')\s*)\)', r'\3 \1 (\2)')
    
    # VV VOL XX (NN UNITS) -> NN UNITS XX
    line = self.re_substitute(line, r'[0-9.]\s*[MU]LS? ([-A-Z ]+)\s+\(\s*([-0-9.]+\s*('+self.UNITS_REGEXP+'))\s*\)', r'\2 \1')

    if self.verbose>5:  
      print "parse12g", line  
      
    # X NN%  ->  NN% X
    line = self.re_substitute(line, r'^\s*([A-Z ]+)\s+([-0-9.]+\s*%)\s*$', r'\2 \1')      
    
    # xx MG PROTEIN/ML -> xx MG/ML PROTEIN
    line = self.re_substitute(line, r'([0-9.])\s+MG\s+PROTEIN/ML',r'\1 MG/ML PROTEIN')
    
    line = self.re_substitute(line, r',\s*A[NST]\b', '')
    
    # Clear trailing spaces
    line = self.re_substitute(line, r'\s+$','')
    
    if self.verbose>5:
      print "parse12h", line
    
    # Remove volume of protein
    line = self.re_substitute(line, r'\d+\.?\d*?\s*[MU]LS?\s+PROTEIN', '')
    
    line = self.re_substitute(line, r'(TRIS|MES|HEPES|PHOSPHATE|CITRATE|ACETATE)\s*\(([0-9\.]*)\)', r'\1 PH \2')
    line = self.re_substitute(line, r'(TRIS|MES|HEPES|PHOSPHATE|CITRATE|ACETATE)\s+(NA(OH)?)', r'SODIUM \1')
    
    # When chem and ph are the one word e.g. 'HEPESPH'
    line = self.re_substitute(line, r'(PEG\s*\d+|TRIS|MES|HEPES|PHOSPHATE|CITRATE|ACETATE|CHLORIDE|MALATE)PH\s*(\d+\.?\d*)', r'\1 PH \2')
    
    if self.verbose>1:
      print "parse:13", line
     
    # Remove volumes at end of line
    line = self.re_substitute(line,'\(?[0-9.]+\s*[MU]LS?,?\s*\)?$', '')
    
    # convert "x% - y%" ranges to "x-y%"
    line = self.re_substitute(line, r'([ 0-9.]+)([%UMGL/]+)\s*-\s*([ 0-9.]+[%UMGL/]+\s*)', r'\1-\3')
      
    if self.verbose>1:
      print "parse:14", line  
    
    # Search for 'chem conc,'
    if self.re_search(line, r'[-0-9.]+\s*('+self.UNITS_REGEXP+r')\s*[,;] '):
      # Put in | to the right of each concentration
      if self.verbose>9:
        print "Step1:", repr(line)
      line=self.re_substitute(line, r'([-0-9.]+\s*('+self.UNITS_REGEXP+r')\s*[,;]) ', r'\1| ')
      if self.verbose>9:
        print "Step2:", repr(line)
      line=self.re_substitute(line, r'[,;|]([^|^,^;]+) ([-0-9.]+\s*('+self.UNITS_REGEXP+r'))\s*(,|;)\s*\|', r'|\2 \1|')
      if self.verbose>9:
        print "Step3:", repr(line)
    
    # Search for 'conc chem'    
    if self.re_search(line, r'[-0-9.]+\s*('+self.UNITS_REGEXP+r') '):
      
      # Put in | to the left of each concentration
      line=self.re_substitute(line, r'([-0-9.]+\s*('+self.UNITS_REGEXP+r') )', r'|\1')

      # Remove volumes at end of component, e.g. 3 UL |0.5M sodium chloride
      line = self.re_substitute(line,'\(?[0-9.]+\s*[MU]LS?\)?,?\s*\|', r'|')
      
      if self.verbose>1:
        print '==> ', repr(line)

      # Split into separate solutions, 'comps' is a list of solns
      comps=line.split('|')
      failed=1
      pH = ''
      comps_failed = [1] * len(comps)
      comps_failed[0]=0 # because comps[0] is never evaluated

      # When "X% CHEM1 OR Y% CHEM2", used to skip over "Y% CHEM2"
      skip_next=False

      for index in range(1,len(comps)):

        # Skip if this is an "OR Y% CHEM"
        # NB: Not marked as a failed component
        if skip_next:
          comps_failed[index]=0
          skip_next=False
          if self.verbose>1:
            print "skipping 'OR Y% CHEM2...'"
          continue

        if self.phdebug>0 or self.verbose>0:
          print "before pH: comps["+str(index)+"]=", repr(comps[index])

        comps[index], pH, pH_UPPER = self.parse_pH(comps[index])

        # getting rid of some extras...
        if self.verbose > 0:
          print "after pH: comps["+repr(index)+"]=", repr(comps[index])
        comps[index] = self.re_substitute(comps[index], r',\s*,', ', ')
        comps[index] = self.re_substitute(comps[index], r',\s*\)', '')
        comps[index] = self.re_substitute(comps[index], r',+\s*$', '')
        comps[index] = self.re_substitute(comps[index], r'\s+', ' ')

        comps[index] = self.re_substitute(comps[index], r'\(\s*\)', '')
        comps[index] = self.re_substitute(comps[index], r'\s+:?', ' ')
        comps[index] = self.re_substitute(comps[index], r'^[-]', '')
        comps[index] = self.trim_string(comps[index])
        if self.verbose > 2:
          print 'Component ' , index , ': ' , repr(comps[index])

        # Remove volumes
        comps[index] = self.re_substitute(comps[index],'\b\(?[0-9.]+\s*[MU]LS?\)?\b', '')
          
        # skip rubbish - one letter, number, set of non-alphanumeric chars
        if self.is_rubbish(comps[index]):
          if self.verbose>1:
            print "skipping rubbish..."
          continue
        
        if self.failed_debug>0:
          print "comps[index]=", repr(comps[index])

        # If we have an 'OR' at the end then skip the next component
        if self.re_match_groups(comps[index], r'\s+OR$'):
          skip_next=True
        
        # Pull out concentration and chem
        if self.re_match_groups(comps[index], r'^([- 0-9.]+('+self.UNITS_REGEXP+r') )(.*)'):
          if self.failed_debug>0:
            print "found conc, not failed:", repr(comps[index])          
          failed=0
          comps_failed[index]=0
          CONC.append(self.matchgroups[1])
          chem=self.matchgroups[3]

          # If it is "XXX OR YYY" remove the " OR YYY" part
          chem = self.re_substitute(chem, r'\s+OR\s+.*$', '')
          chem = self.re_substitute(chem, r'\s+OR$', '')
          CHEMICALS.append(chem)
          PH.append(pH)
          PH_UPPER.append(pH_UPPER)

          comp_cnt=len(CONC)-1
          if self.verbose>0:
            print "chem:0", CHEMICALS[comp_cnt]
          # fixup w/v v/v, etc
          if self.re_search(CHEMICALS[comp_cnt], r'\(?\s*[WV]+\s*/\s*[WV]+\s*\)?'):
            CHEMICALS[comp_cnt] = self.re_substitute_groups(CHEMICALS[comp_cnt], r'(\(?\s*[WV]+\s*/\s*[WV]+\s*\)?)', '')
            CONC[comp_cnt] = CONC[comp_cnt] + ' ' + self.matchgroups[1]

          CONC[comp_cnt]=self.trim_string(CONC[comp_cnt])
          CHEMICALS[comp_cnt]=self.trim_string(CHEMICALS[comp_cnt])
          
          # Now convert the name, but only if not known
          if not self.alia.has_alias(CHEMICALS[comp_cnt]):
            if self.verbose>0:
              print "pre convert_name: ", repr(CHEMICALS[comp_cnt])
            CHEMICALS[comp_cnt]=self.convert_name(CHEMICALS[comp_cnt])
            if self.verbose>0:
              print "post convert_name: ", repr(CHEMICALS[comp_cnt])

          #check for illegal strings
          if self.re_search(CHEMICALS[comp_cnt], r'\. |, '):
            # just take the first one and discard the remainder
            split_list=re.split(r'\. |, ',CHEMICALS[comp_cnt])
            if len(split_list)>0:
              for split_str in split_list:
                if split_str.strip(' ')!='':
                  if self.verbose>0:
                    print "Take the first one from", CHEMICALS[comp_cnt], "->", repr(split_str.strip(' ')) 
                  CHEMICALS[comp_cnt] = split_str.strip(' ')
                  break
        else:
          # Concentration not found in this item in comps array
          if self.failed_debug>0:
            print pdb, " could not find conc in", repr(comps[index])
          if self.verbose > 0:
            print "\tFailed on " + repr(comps[index])
      # End of loop over comp[]

      self.NUM_PARTS = len(comps_failed)
      self.NUM_FAILED_PARTS = sum(comps_failed)
          
      # comps loop finished, so if any concentations found:
      if failed == 0:
        for i in range(len(CONC)):
          # Exclude empty chems
          if self.is_rubbish(CHEMICALS[i]):
            if self.verbose>0:
              print "Excluding rubbish: ", repr(CHEMICALS[i])
            self.NUM_FAILED_PARTS+=1
            continue

          # Look for concentration range e.g. '0.1 - 0.01'
          if self.re_match_groups(CONC[i],r'^([0-9.]+)[-~ ]*([0-9.]*)(.*)$'):
            conc_flt=self.parser_get_float(self.matchgroups[1])
            upper_conc_flt=self.parser_get_float(self.matchgroups[2])
            unit_str=string.strip(self.matchgroups[3])
            upper_unit_str=unit_str
            (conc_flt, unit_str)=self.parser_standardise_conc_units(conc_flt, unit_str)
            if upper_conc_flt!=None:
              (upper_conc_flt, upper_unit_str)=self.parser_standardise_conc_units(upper_conc_flt, upper_unit_str)
            
            # Sometimes they specify 0-X as concentration, use upper limit (X) in this case
            if conc_flt==0.0 and upper_conc_flt>0.0:
              conc_flt=upper_conc_flt
            
              
          # Else look for a single concentration e.g. '0.1'
          elif self.re_match_groups(CONC[i],r'^([0-9.]+)(.+)$'):
            conc_flt=self.parser_get_float(self.matchgroups[1])
            unit_str=string.strip(self.matchgroups[2])
            (conc_flt, unit_str)=self.parser_standardise_conc_units(conc_flt, unit_str)
            upper_conc_flt=None

          # Else reject!
          else:
            print "Can't find conc in: ", repr(CONC[i]), " pdb code:", pdb, " chem:", repr(CHEMICALS[i])
            self.NUM_FAILED_PARTS+=1
            continue

           
          # FINAL CLEANUP AND REJECTION OF BAD VALUES 

          # Reject if concentration too low or not a float
          if not isinstance(conc_flt, float) or conc_flt<=0.0:
            print "Bad concentration: ", repr(conc_flt)," pdb code:", pdb, " chem:", repr(CHEMICALS[i])
            self.NUM_FAILED_PARTS+=1
            continue

          # Either 'upper_conc_flt' is a positive float or set it to None
          if not isinstance(upper_conc_flt, float) or upper_conc_flt<=0.0:
            upper_conc_flt = None

          # If no units supplied e.g. '%', assume it was 'V/V'
          if unit_str.strip(' ')=='':
            unit_str='V/V'

          # Standardise units, reject bad units
          elif unit_str not in ['W/V', 'V/V', 'M']:
            print "Bad units: ", repr(unit_str), " pdb code:", pdb, " chem:", repr(CHEMICALS[i])
            self.NUM_FAILED_PARTS+=1
            continue

          # Standardize chem names, reject bad chem names
          # If a non-chem or unknown, then deemed to have failed
          self.CHEM_TOTAL+=1
          self.RAW_CHEMICALS.append(CHEMICALS[i])
          resolved_chem_name=self.alia.resolve_chem_name(CHEMICALS[i], PH[i])
          if resolved_chem_name=='Unknown':
            self.CHEM_UNKNOWN+=1
            self.CHEM_FAIL+=1
            self.NUM_FAILED_PARTS+=1
            self.CHEM_UNKNOWN_DICT[pdb] = self.CHEM_UNKOWN_DICT.setdefault(pdb, [])
            self.CHEM_UNKNOWN_DICT[pdb].append(CHEMICALS[i])
            continue

          if resolved_chem_name in non_chem_list:
            self.CHEM_NON_CHEM+=1
            self.CHEM_FAIL+=1
            #self.NUM_FAILED_PARTS+=1
            continue

          self.CHEM_PASS+=1

          # Fixup incorrectly assigned units
          # i.e. solids with 'V/V' units should be 'W/V'
          unit_str = self.resolve_units(resolved_chem_name, unit_str)

          # Insert final chem names, concs, pHs etc.
          self.UOMS.append(unit_str)
          self.CONCENTRATIONS.append(conc_flt)
          self.CONCENTRATION_UPPER_LIMITS.append(upper_conc_flt)
          self.pH.append(PH[i])
          self.pH_UPPER.append(PH_UPPER[i])       
          self.CHEMICALS.append(resolved_chem_name)

        # End of looping over successful chems

        # Make sure that pH is assigned to chems that are truly buffers
        # i.e. is within pKa range and if molar conc, the conc is not too
        # large etc.
        self.check_pH_assignment()

        # Show results
        if self.verbose >= 1:
          self.printResults(pdb)          
        return True, False

    # No concentrations were found
    if self.verbose>0:
      print pdb, "NO_CONC: line=", repr(line)
    if self.failed_debug>0:
      print pdb, "has no conc in", repr(line)
    self.NUM_PARTS = 100
    self.NUM_FAILED_PARTS = 100
    return False, True

# ### End of parse_conditions() ### #


  # Extract pH here
  def parse_pH(self, component): 
    pH=None
    pH_UPPER=None

    # If there is a pH 
    if self.re_search(component, r'[^B-Z]PH\s*[-0-9., ]+'):

      # Look for "PH XX OR (PH) YY"
      if self.re_match_groups(component,r'PH\s*\(?\s*([0-9.]+)\s+OR\s+P?H?\s*([0-9.]+)'):
        if self.phdebug>0:
          print "PH XX OR (PH) YY" 
        pH = self.parser_get_float(self.matchgroups[1])
        pH_UPPER =  self.parser_get_float(self.matchgroups[2])
        if self.phdebug>0:
          print "pH=", repr(pH)
          print "pH_UPPER=", repr(pH_UPPER)
        component = self.re_substitute(component,r'PH\s*\(?\s*[0-9.]+\s+OR\s+P?H?\s*[0-9.]+\s*\)','')
        return component, pH, pH_UPPER

      # strip out the pH; yes twice, some chems have two
      if self.re_search(component, r'\bPH\s*\d+(\.\d+)?,?\s+PH\s*\d+(\.\d+)?'):
        if self.phdebug>0:
          print "Has 2 PHs: ", repr(component)
        component = self.re_substitute(component, r'\bPH\s*[-0-9,. ]+', r'',1)
      if self.phdebug>0:
        print "pH:10", repr(component)
      component = self.re_substitute(component, r'\d+\s+[MU]LS?', '')
      component = self.re_substitute_groups(component, r'[^B-Z]PH\s*([-0-9,. ]+)', ' ')
      if self.phdebug>0:
        print "pH:11", repr(component)
      pH_str=self.trim_string(self.matchgroups[1])

      # if range of pHs, get upper limit
      if self.re_match_groups(pH_str,r'^\s*([0-9.]+)\s*-\s*([0-9.]+)'):
        if self.phdebug>0:
          print "Has pH range:", component
        pH=self.parser_get_float(self.matchgroups[1])
        pH_UPPER=self.parser_get_float(self.matchgroups[2])
      else:
        pH=self.parser_get_float(pH_str)
        

      if (self.verbose > 0 or self.phdebug>0):
        print 'Got pH: ' , repr(pH)
        print 'Got pH_UPPER: ' , repr(pH_UPPER)

    return component, pH, pH_UPPER

  def check_pH_assignment(self):
    for idx in range(len(self.pH)):
      if self.pH[idx]!=None:
        if self.verbose>9:
          print "self.is_buffer("+self.CHEMICALS[idx]+","+repr(self.pH[idx])+") = ", self.is_buffer(self.CHEMICALS[idx], self.pH[idx])
        if not self.is_buffer(self.CHEMICALS[idx], self.pH[idx]) or \
                        self.CONCENTRATIONS[idx]>0.2 and self.UOMS[idx]=='M':
          self.reassign_pH(idx)
          

  def reassign_pH(self, idx_nonbuf):
    # Go over all chems and reassign to the first likely candidate
    # Is buffer within pKa range and conc < 0.2M
    done=False
    for idx in range(len(self.pH)):
      if idx!=idx_nonbuf and self.pH[idx]==None and \
             self.is_buffer(self.CHEMICALS[idx], self.pH[idx_nonbuf]) and  \
             self.CONCENTRATIONS[idx]<=0.2 and self.UOMS[idx]=='M':
        self.pH[idx]=self.pH[idx_nonbuf]
        self.pH[idx_nonbuf]=None
        if self.verbose>8:
          print "BUFFER SWAP!!", repr(idx_nonbuf), ' -->', repr(idx)
        done=True  
        break
    if not done:
      # If nothing reassigned, then try again without the < 0.2M condition
      for idx in range(len(self.pH)):
        if idx!=idx_nonbuf and self.pH[idx]==None and self.UOMS[idx]!='M' and \
                    self.is_buffer(self.CHEMICALS[idx], self.pH[idx_nonbuf]):
          self.pH[idx]=self.pH[idx_nonbuf]
          self.pH[idx_nonbuf]=None
          done=True  
          if self.verbose>8:
            print "BUFFER SWAP!!", repr(idx_nonbuf), ' -->', repr(idx)
          break

    
  def printResults(self, pdb):
    print "\nRESULTS:"
    for i in range(len(self.CHEMICALS)):
      print "#",repr(i),":",pdb,":-",
      if self.pH_UPPER[i]:
        print "UPPER: %6.3f" % self.pH_UPPER[i],
      else:
        print "\t",
      if self.TEMPERATURE:
        print "TEMPERATURE: %5d" % self.TEMPERATURE,
      else:
        print "\t",
      if self.CONCENTRATIONS[i]:
        print "CONC: %12.5f" % self.CONCENTRATIONS[i],
      else:
        print "\t",
      if self.CONCENTRATION_UPPER_LIMITS[i]:
        print "CONC_UL: %12.5f" % self.CONCENTRATION_UPPER_LIMITS[i],
      else:
        print "\t",
      if self.UOMS[i]:
        print "UOMS: %s" % repr(self.UOMS[i]),
      else:
        print "\t",
      print "CHEMS: "+repr(self.CHEMICALS[i]),
      if self.CHEMICALS[i]:
        for j in range(2,len(self.CHEMICALS)):
          if i!=j and self.CHEMICALS[i] == self.CHEMICALS[j] and self.CHEMICALS[i]!='Unknown':
            print "--->DUPLICATE?!"
      if self.pH[i]:
        print "\tpH: %6.3f" % self.pH[i]
      else:
        print "\t"
      print
    print
    for i in range(len(self.RAW_CHEMICALS)):
      print "#",repr(i),":",pdb,":-",
      print "\tRAW_CHEMS: "+repr(self.RAW_CHEMICALS[i]),
    print        

  # Used in the automated PDB database creation script to set up
  # parsing pdb lines
  def setValues(self,line):
    line=self.re_substitute(line,r'REMARK 280','')
    if self.re_search(line,r'CRYSTALLIZATION CONDITIONS:'):
      line=self.re_substitute(line,r'CRYSTALLIZATION CONDITIONS:','')
      self.got_xtal_cond=True
    if self.got_xtal_cond:
      self.xtal_cond=self.xtal_cond + " " + self.init_strclean(line)
      #print self.xtal_cond


  # This routine categorises parts of each pdb entry and splits them into
  # piece in order to parse separately
  # e.g. cryo conditions are parsed separately from reservoir conditions
  # Line is the text for the whole pdb entry
  def wellComponentSplit(self, line, pdb_code):
    # Must always be in upper case
    line=self.init_strclean(line)
    
    # Try to look for cryoconditions
    class_obj=CRYSTAL_PARSER_USECLASSIFIER(self.verbose, failed_debug=False)
    match_obj, category=class_obj.classify(line)
    if match_obj!=None:
      # Cryoconditions were found
      start_str_idx=match_obj.start(0)
      end_str_idx=match_obj.end(0)

      # Parse cryo conditions
      if self.verbose>5:
        print "Parsing part1:",category,":", repr(line[start_str_idx:end_str_idx])
      parse_ok1, was_blank1=self.parseWellComponent(line[start_str_idx:end_str_idx], category, pdb_code)

      # Parse from the end of cryo conditions to end of line as 'reservoir'
      if self.verbose>5:
        print "Parsing part2: reservoir:", repr(line[end_str_idx:])
      parse_ok2, was_blank2=self.parseWellComponent(line[end_str_idx:], 'reservoir', pdb_code)

      # Parse from the start of line to start of cryo conditions as 'reservoir'
      if self.verbose>5:
        print "Parsing part3: reservoir:", repr(line[:start_str_idx])
      parse_ok3, was_blank3=self.parseWellComponent(line[:start_str_idx], 'reservoir', pdb_code)

      # If any well component was ok, then overall is ok
      parse_ok=parse_ok1 or parse_ok2 or parse_ok3

      # Only return blank if all well components are blank
      was_blank=was_blank1 and was_blank2 and was_blank3

    else: 
      # If can't find any markers, just parse the whole line as 'reservoir'
      if self.verbose>5:
        print "Could not find cryo conds, parsing entire line as 'reservoir'"
      parse_ok, was_blank=self.parseWellComponent(line, 'reservoir', pdb_code)
    if parse_ok:
      self.CODE_PASS+=1
    elif was_blank:
      self.CODE_BLANK+=1
    else:
      self.CODE_FAIL+=1
      self.CODE_FAIL_LIST.append(pdb_code)

        
  # This parses a section of a pdb entry
  # 'component' is either 'reservoir' or 'cryoprotect'
  # 'line' is the text for that component  
  # 'pdb_code' is obvious
  # Returns pass/fail, was_blank 
  def parseWellComponent(self, line, component, pdb_code):

    # Catch blank lines
    if line=='':
      return False, True
      
    # Must always be in upper case
    self.xtal_cond=self.init_strclean(line)

    # Call main parsing routine
    pass_flag, was_blank=self.parse_conditions(pdb_code)

    # When parsing, some parts of the line can be parsed, some parts cannot
    # This tries to estimate which pdb entries could be parsed fully and which
    # could be parsed partially
    if component=='reservoir' and was_blank==False:
      if self.verbose>9:
        print "pdb_code=", pdb_code, "NUM_PARTS=", repr(self.NUM_PARTS), \
              "NUM_FAILED_PARTS=", repr(self.NUM_FAILED_PARTS)
      self.TOTAL_PARTS.setdefault(pdb_code,0)
      self.TOTAL_FAILED_PARTS.setdefault(pdb_code,0)
      if self.NUM_PARTS>=1:
        self.TOTAL_PARTS[pdb_code] += self.NUM_PARTS-1
        if self.NUM_FAILED_PARTS>0:
          self.TOTAL_FAILED_PARTS[pdb_code] += self.NUM_FAILED_PARTS

      if self.verbose>9:
        print "self.TOTAL_FAILED_PARTS["+repr(pdb_code)+"]="+repr(self.TOTAL_FAILED_PARTS[pdb_code])
        print "self.TOTAL_PARTS["+repr(pdb_code)+"]="+repr(self.TOTAL_PARTS[pdb_code])
        
   
    if pass_flag:
      for i in range(len(self.CHEMICALS)):
        # NB: chem is standardised
        chem=self.CHEMICALS[i]
        units=self.UOMS[i]
        conc=self.CONCENTRATIONS[i]
        ph=self.pH[i]
        if self.verbose>0:
          print "component:", component
          print "chem:", repr(chem)
          print "pdb_code:", pdb_code

        # Conditions are stored by pdb_code and component
        self.CONDS.setdefault(pdb_code,{})  
        self.CONDS[pdb_code][component]=self.CONDS[pdb_code].get(component, [])+[[conc, units, chem, ph]]
        self.CHEM_HISTO[chem]=self.CHEM_HISTO.get(chem, 0)+1

      for i in range(len(self.RAW_CHEMICALS)):
        # NB: raw_chem is not standardised
        raw_chem=self.RAW_CHEMICALS[i]
        if self.verbose>0:
          print "component:", component
          print "raw_chem:", raw_chem
          print "pdb_code:", pdb_code
        self.RCHEM_CODES[raw_chem]=self.RCHEM_CODES.get(raw_chem, [])+[pdb_code]
        self.RCHEM_HISTO[raw_chem]=self.RCHEM_HISTO.get(raw_chem, 0)+1

      return True, False

    return False, was_blank

