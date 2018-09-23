#
# Copyright (C) 2008-2014 CSIRO Australia
#

import re

from CrystalParser_base import CRYSTAL_PARSER_BASE


MPD_REGEXP_LIST= [
    r'\(\s*/-\)-2-METHYL-2,4-PENTANEDIOL',
    r'MPD \(2-METHYL-2\s*[-,]\s*4-\s*PENTANEDIOLE?\)',
    r'\(4S\)\s*\-\s*2\s*\-\s*METHYL\-\s*2,4\-PENTANEDIOL \(MPD\)',
    r'\b2-METHYL\s*-2\s*[-,]\s*4-\s*PENTANEDIOLE?',
    r'2-\s*METHL?YL?\-\s*2[-,]4,?\s*-\s*PENTAN?E?-?\s*D(12\-)?IOLE?',
    r'2-METHYL-PENTANEDIOL',
    r'(\(\+/\-\)\-)?2,4-\s?METHYL\s*PENTANEDIOL',
    r'2-METHYL-?PENTANE?-2,4(-| )DIOLE?',
    r'METHYL-?\s*PENTANE-?\s*DIOL',
    r'METHANE\s*PENTANE-?\s*DIOL',
    r'^2-MPD\b',
    r'^MPD \(MPD\)?',
    ]

class CRYSTAL_PARSER_NAMES(CRYSTAL_PARSER_BASE):

  def __init__(self, verbose, failed_debug, use_chem_classes, correcter_obj):
    CRYSTAL_PARSER_BASE.__init__(self, verbose, failed_debug, use_chem_classes, correcter_obj)
  
  def convert_name(self,str):
    if self.verbose>0:
      print "convert_name:1",repr(str)

    str = self.re_substitute(str, r',[\s*,]+', r', ')
    str = self.re_substitute(str, r'\s+\)', r'')
    str = self.re_substitute(str, r'^SATU?RATED *', r'')
    str = self.re_substitute(str, r'^REDUCED *',r'')
    str = self.re_substitute(str, r'\b([A-Z]+)_\s*([K NAH]+[234]?)\b', r'\2 \1')
    str = self.re_substitute(str, r'POT?A?SSIUM', r'POTASSIUM')
    str = self.re_substitute(str, r'POTT?ASIUM', r'POTASSIUM')
    str = self.re_substitute(str, r'SODIUM[-/]POTASSIUM', r'SODIUM POTASSIUM')
    str = self.re_substitute(str, r'\bK\s?[-/,]?\s*NA-?', r'SODIUM POTASSIUM ')
    str = self.re_substitute(str, r'\(NA[-,/]?K\)-?', r' SODIUM POTASSIUM ')
    str = self.re_substitute(str, r'\bNA\s?[-/,+]?\s?K[-2+.]?', r'SODIUM POTASSIUM ')
    str = self.re_substitute(str, r'\bNA[-,/]\s*POTASSIUM', r'SODIUM POTASSIUM ')
    str = self.re_substitute(str, r'\bNA,?-K-?', r'SODIUM POTASSIUM ')

    # PEE
    str = self.re_substitute(str, r'^PENTAERT?H?Y?THRIT?OLE? ?ETH?Y?L?OXYLATE ?\(?(1|15)/?\s*4? ?([EP]O/OH)\)?\)?', r'PENTAERYTHRITOL ETHOXYLATE (15/4 EO/OH)')
    str = self.re_substitute(str, r'PENTAERT?H?Y?THRIT?OLE? ?ETH?Y?L?OXYLATE', r'PENTAERYTHRITOL ETHOXYLATE')
    str = self.re_substitute(str, r'PENTAERYTHRITOL ETHOXYLATE \(MR 797', r'PENTAERYTHRITOL ETHOXYLATE (15/4 EO/OH)')
    str = self.re_substitute(str, r'PENTAERYTHROL ETHOXYLATE', r'PENTAERYTHRITOL ETHOXYLATE')
    str = self.re_substitute(str, r'PEE\s+\(?15/4\)?', r'PENTAERYTHRITOL ETHOXYLATE (15/4 EO/OH)')
    
    # PEP
    str = self.re_substitute(str, r'PENTAERYTHRIT?R?OLE? ?PROPOXYLATE ?\(?5/\s*4 ?(PO/OH)?\)?', r'PENTAERYTHRITOL PROPOXYLATE (5/4 PO/OH)')
    str = self.re_substitute(str, r'PENTAERYTHRITOL PROPOXYLATE 426', r'PENTAERYTHRITOL PROPOXYLATE (5/4 PO/OH)')
    str = self.re_substitute(str, r'PENTAERYTHRITOL PROPOXYLATE 629', r'PENTAERYTHRITOL PROPOXYLATE (17/8 PO/OH)')
    str = self.re_substitute(str, r'PENTAERYTHRITOL PROPOXYLATE PO/OH 5/4', r'PENTAERYTHRITOL PROPOXYLATE (5/4 PO/OH)')
    str = self.re_substitute(str, r'PENTAE(RY)?THRITR?OL PROP[EO]XYLATE', r'PENTAERYTHRITOL PROPOXYLATE')
    str = self.re_substitute(str, r'PEP 629', r'PENTAERYTHRITOL PROPOXYLATE (17/8 PO/OH)')
    str = self.re_substitute(str, r'PEP \(17/8 PO/OH', r'PENTAERYTHRITOL PROPOXYLATE (17/8 PO/OH')
    str = self.re_substitute(str, r'^PEP$', r'PENTAERYTHRITOL PROPOXYLATE')
    str = self.re_substitute(str, r'PENTAETHYTHROTOL\-PTHOXYLATE', r'PENTAERYTHRITOL')    
    
    # NDSB
    str = self.re_substitute(str, r'NDSB ?\-?([0-9]+)',r'NDSB \1')
    str = self.re_substitute(str, r'([0-9]+) ?\-?(NDSB|NSBD)', r'NDSB \1')

    if self.verbose>0:
      print "convert_name:2",repr(str)

      
    str = self.re_substitute(str, r'MONO-?HYDRO(GEN)?\s*(MONO)?PHOS?PH?ATE?', r'HYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'DI-?HYDRO(GEN)?\s*(DI)?PHOS?PH?ATE?', r'DIHYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'MONOPHOSPHATE', r'PHOSPHATE')
    str = self.re_substitute(str, r'DIPHOSPHATE', r'PHOSPHATE')


    # XXX-BASIC -> XXXBASIC
    str = self.re_substitute(str, r'MONO-BASIC', r'MONOBASIC')
    str = self.re_substitute(str, r'DI-BASIC', r'DIBASIC')
    str = self.re_substitute(str, r'TRI-BASIC', r'TRIBASIC')

    # SODIUM DIHYDROGEN-DIPOTASSIUM HYDROGEN PHOSPHATE
    str = self.re_substitute(str, r'NAH2(PO4)?/K2HPO4', r'SODIUM DIHYDROGEN-DIPOTASSIUM HYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'(POTASSIUM|K)2?\s*H\s*PHOSPHATE\s*/\s*(SODIUM|NA)\s*H2\s*PHOSPHATE',r'SODIUM DIHYDROGEN-DIPOTASSIUM HYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'NAH2/K2H2?\s*PO4', r'SODIUM DIHYDROGEN-DIPOTASSIUM HYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'K2HPO4\.\dH2[O0]/NAH2PO4', r'SODIUM DIHYDROGEN-DIPOTASSIUM HYDROGEN PHOSPHATE') #1h4h
    str = self.re_substitute(str, r'\bNA\s*[-,/]?\s*K2?\.?\s*PHOSPHA?TE', r'SODIUM DIHYDROGEN-DIPOTASSIUM HYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'\bNAH?2?[-,/]?\s*POTASSIUM PHOSPHATE', r'SODIUM DIHYDROGEN-DIPOTASSIUM HYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'K2H2?PO4[-.,/]+NAH2?PO4', r'SODIUM DIHYDROGEN-DIPOTASSIUM HYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'\bK2[-/,]?NAH?2?PO4', r'SODIUM DIHYDROGEN-DIPOTASSIUM HYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'\bNAK2PO4', r'SODIUM DIHYDROGEN-DIPOTASSIUM HYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'\bNA[-,/]?K2\s*PO4', r'SODIUM DIHYDROGEN-DIPOTASSIUM HYDROGEN PHOSPHATE')

    # Ambiguous 'sodium potassium phosphate'
    # I know it is ambiguous. But it's either assign to this or 'Unknown'
    # Also Hampton uses this definition!
    str = self.re_substitute(str, r'\(NA[,/]K\)PO4', r'SODIUM DIHYDROGEN-DIPOTASSIUM HYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'\bPOTASSIUM\s*SODIUM\s*PHOSPHATE\b', r'SODIUM DIHYDROGEN-DIPOTASSIUM HYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'PHOSPHATE SODIUM POTASSIUM', 'SODIUM DIHYDROGEN-DIPOTASSIUM HYDROGEN PHOSPHATE')

    # DISODIUM HYDROGEN-POTASSIUM DIHYDROGEN PHOSPHATE
    str = self.re_substitute(str, r'NA2H?/KH2?\s*PO4', r'DISODIUM HYDROGEN-POTASSIUM DIHYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'NA2H2?PO4/K2?H2?PO4', r'DISODIUM HYDROGEN-POTASSIUM DIHYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'\bN[-,/]KPO4', r'DISODIUM HYDROGEN-POTASSIUM DIHYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'SODIUM POTASSIUM\s*PI\b', r'DISODIUM HYDROGEN-POTASSIUM DIHYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'KH2?PO4[-.,/]+NA2H2?PO4', r'DISODIUM HYDROGEN-POTASSIUM DIHYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'\bK[-/,]?NA2H?2?PO4', r'DISODIUM HYDROGEN-POTASSIUM DIHYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'\bNA2KPO4', r'DISODIUM HYDROGEN-POTASSIUM DIHYDROGEN PHOSPHATE')
    str = self.re_substitute(str, r'\bNA2[-,/]?K\s*PO4', r'DISODIUM HYDROGEN-POTASSIUM DIHYDROGEN PHOSPHATE')


    # SODIUM PHOSPHATE (generic)
    if not self.re_match_groups(str, r'(DISODIUM HYDROGEN-POTASSIUM DIHYDROGEN PHOSPHATE|SODIUM DIHYDROGEN-DIPOTASSIUM HYDROGEN PHOSPHATE)'):
      str = self.re_substitute(str, r'NA?H?2?PO4/NA2?H2?PO4', r'SODIUM PHOSPHATE')
      str = self.re_substitute(str, r'\bNA2?H2?PO4/NA2?H2?PO4', r'SODIUM PHOSPHATE')
      str = self.re_substitute(str, r'\bNAH\(2\)PO\(4\)', r'SODIUM PHOSPHATE')
      str = self.re_substitute(str, r'^NAPO4', r'SODIUM PHOSPHATE')
      str = self.re_substitute(str, r'\bNA[23]?\s*H?2?\s*PO[43]', r'SODIUM PHOSPHATE')
      str = self.re_substitute(str, r'\bNAH?2?-?\s*PHOSPHATE', r'SODIUM PHOSPHATE')
      str = self.re_substitute(str, r'\bNA-?PI\b', r'SODIUM PHOSPHATE')
      str = self.re_substitute(str, r'\bPHOSPHATE SALINE\b', r'SODIUM PHOSPHATE')
      str = self.re_substitute(str, r'^SODIUM PH(O|A)SPH?ATE', r'SODIUM PHOSPHATE')

    # SODIUM DIHYDROGEN PHOSPHATE
    str = self.re_substitute(str, r'\bNA\s*PHOSPHATE\s+\(NA\s*H2\s*PO4\)\-\d+M', r'SODIUM DIHYDROGEN PHOSPHATE') # Some people like to include stock & conc in the name 

    # DIPOTASSIUM HYDROGEN PHOSPHATE
    str = self.re_substitute(str, r'\bK\s*PHOSPHATE\s+\(K2\s*H\s*PO4\)\-\d+M', r'DIPOTASSIUM HYDROGEN PHOSPHATE') # Some people like to include stock & conc in the name

    # POTASSIUM PHOSPHATE (generic)
    if not self.re_match_groups(str, r'(DISODIUM HYDROGEN-POTASSIUM DIHYDROGEN PHOSPHATE|SODIUM DIHYDROGEN-DIPOTASSIUM HYDROGEN PHOSPHATE)'):
      str = self.re_substitute(str, r'\bK\s*[-,/]\s*PHOSPHATE', r'POTASSIUM PHOSPHATE')
      str = self.re_substitute(str, r'\bKH2PO4[-/]K2HPO4', r'POTASSIUM PHOSPHATE')
      str = self.re_substitute(str, r'\bKH?\(2\)H?PO\(4\)', r'POTASSIUM PHOSPHATE')
      str = self.re_substitute(str, r'\bK[23]?\s*H?2?\s*PO[43]', r'POTASSIUM PHOSPHATE')
      str = self.re_substitute(str, r'\bK2?H?2?-?\s*PHOSPHATE', r'POTASSIUM PHOSPHATE')
      str = self.re_substitute(str, r'POTASSIUMPHOSPHATE', r'POTASSIUM PHOSPHATE')
      str = self.re_substitute(str, r'\bKPI\b', r'POTASSIUM PHOSPHATE')

    # DISODIUM DIHYDROGEN PYROPHOSPHATE
    str = self.re_substitute(str, r'\bNA2?H2P2O7', r'DISODIUM DIHYDROGEN PYROPHOSPHATE')
    str = self.re_substitute(str, r'\bNA2P2O7H2', r'DISODIUM DIHYDROGEN PYROPHOSPHATE')

    # SODIUM PYROPHOSPHATE
    str = self.re_substitute(str, r'\bNA4P207', r'SODIUM PYROPHOSPHATE')


    # PHOSPHATES
    str = self.re_substitute(str, r'H2P(O|0)[34]', r'PHOSPHATE')
    str = self.re_substitute(str, r'2HP(O|0)[34]', r'PHOSPHATE')
    str = self.re_substitute(str, r'\bPHOSPHORIC ACID', r'PHOSPHATE')
    str = self.re_substitute(str, r'\bPHOS[HP][PH]?AS?TE\)?', r'PHOSPHATE')
    str = self.re_substitute(str, r'\bPH(O|A)SPHA?TE\)?', r'PHOSPHATE')
    str = self.re_substitute(str, r'PHOS?PHATE?S?', r'PHOSPHATE')

    str = self.re_substitute(str, r'SAT\'D ', r'')
    str = self.re_substitute(str, r'\bSAT\.?\b', r'')
    str = self.re_substitute(str, r'\bMONO-?\s*(POTASSIUM|K)-?\b', r'POTASSIUM ')
    str = self.re_substitute(str, r'\bMONO-?\s*(SODIUM|NA)-?\b', r'SODIUM ')
    str = self.re_substitute(str, r'\bMONO-?\s*(AMMON?IUM|NH3)\b', r'AMMONIUM ')
    str = self.re_substitute(str, r'\b(MONO|DI)-?\s*(LITHIUM)\b', r'LITHIUM')
    str = self.re_substitute(str, r'(DI|MONO)?HYDROGEN\s*SULFATE', r'HYDROGEN SULFATE')

    str = self.re_substitute(str, r'\bNA[-/_]H[23]?\W\s*', r'SODIUM ')
    str = self.re_substitute(str, r'\(NA\)[23]?-?\s*', r'SODIUM ')
    str = self.re_substitute(str, r'^NA\s*[-/_]\s*(?!K[-/,])', r'SODIUM ')
    str = self.re_substitute(str, r'^SSODIUM\b', r'SODIUM')

    if self.verbose>0:
      print "convert_name:3",repr(str)
    # for Syrrx and JCSG specific files...  NP means non-plumbed, for the robots.
    str = self.re_substitute(str, r'^NP_', r'')

    str = self.re_substitute(str, r'\s+', r' ')
    str = self.re_substitute(str, r'AMMONIUM\s*(H|HYDROGEN)?\s*PHOSPH?ATE', r'AMMONIUM PHOSPHATE')
    str = self.re_substitute(str, r'NH4\s*PHOSPHATE\/\(NH4\)\s*PHOSPHATE', r'AMMONIUM PHOSPHATE')

    str = self.re_substitute(str, r'\bH2O2\b', r'HYDROGEN PEROXIDE')
    str = self.re_substitute(str, r'\b(\w+)IC\s+ACID\s+SODIUM\s+SALT\b', r'SODIUM \1ATE')
    
    str = self.re_substitute(str, r'\bBUFFERED', r'')
    str = self.re_substitute(str, r'\bBUFFER?', r'')


    str = self.re_substitute(str, r'\bSPG\b', r'SUCCINATE PHOSPHATE GLYCINE')
    
    str = self.re_substitute(str, r'([^1-9\']+)\s*-PHOSPHATE', r'\1 PHOSPHATE')
    str = self.re_substitute(str, r'CITRATE/?\s*PHOSPHATE', r'CITRATE PHOSPHATE')
    str = self.re_substitute(str, r'PHOSPHATE-?\/?\s*-?CITRATE', r'CITRATE PHOSPHATE')
    str = self.re_substitute(str, r'PHOSPHO[-/]CITRATE', r'CITRATE PHOSPHATE')
    str = self.re_substitute(str, r'PHOSPHATE-?/?CITRIC ACID', r'CITRATE PHOSPHATE')

    str = self.re_substitute(str, r'ACES N-\[2-ACETAMIDO\]-2-\s*AMINOETHANE SUL?FONIC ACID', r'ACES')
    
    str = self.re_substitute(str, r'\bACET[EA]T[EA]', r'ACETATE')
    str = self.re_substitute(str, r'\bACT?ET[EA]TE', r'ACETATE')
    str = self.re_substitute(str, r'\bACE?A?T[EA]E?A?TE', r'ACETATE')
    str = self.re_substitute(str, r'\bAC?ETATE?', r'ACETATE')
    str = self.re_substitute(str, r'\bACET(AT|E)?$', r'ACETATE')
    str = self.re_substitute(str, r'\b2 ACETATE', r'ACETATE')
    str = self.re_substitute(str, r'^NAO?AC/HO?AC', r'SODIUM ACETATE')
    str = self.re_substitute(str, r'^NA\(?OAC\)?', r'SODIUM ACETATE')
    str = self.re_substitute(str, r'^NACH2COOH\b', r'SODIUM ACETATE')
    str = self.re_substitute(str, r'^NA\(?CH3COOH?\)?\b', r'SODIUM ACETATE')
    str = self.re_substitute(str, r'^CH3CO(O|2)NA\b', r'SODIUM ACETATE')
    str = self.re_substitute(str, r'\bNA\(AC\)', r'SODIUM ACETATE')
    str = self.re_substitute(str, r'^NAACETATE', r'SODIUM ACETATE')
    str = self.re_substitute(str, r'^NAACE$', r'SODIUM ACETATE')
    str = self.re_substitute(str, r'^NAAC\s*[-/.,]\s*HAC\b', r'SODIUM ACETATE')
    str = self.re_substitute(str, r'^HAC\b', r'ACETATE') # TSP acetic acid?
    str = self.re_substitute(str, r'^NAAC[^A-Z]', r'SODIUM ACETATE')
    str = self.re_substitute(str, r'^NAAC$', r'SODIUM ACETATE')
    str = self.re_substitute(str, r'^ACNA$', r'SODIUM ACETATE') #1zzy, 1x24?

    str = self.re_substitute(str, r'^KO?\s*AC\b', r'POTASSIUM ACETATE')
    str = self.re_substitute(str, r'^AMOAC\b', r'AMMONIUM ACETATE')
    str = self.re_substitute(str, r'^CH3CO(O|2)NH4\b', r'AMMONIUM ACETATE')
    str = self.re_substitute(str, r'AMOAC', r'AMMONIUM ACETATE')
    str = self.re_substitute(str, r'NH4\(?O?AC\)?\b', r'AMMONIUM ACETATE')
    str = self.re_substitute(str, r'\(NH4\)\s*2?O?AC\b', r'AMMONIUM ACETATE')
    str = self.re_substitute(str, r'AMM?\s*\.ACETATE', r'AMMONIUM ACETATE')
    str = self.re_substitute(str, r'^CA\(CH3CO(O|2)\)2?\b', r'CALCIUM ACETATE')
    str = self.re_substitute(str, r'CA\s*\(OAC\)\s*2?', r'CALCIUM ACETATE')
    str = self.re_substitute(str, r'^LIACETATE', r'LITHIUM ACETATE')
    str = self.re_substitute(str, r'LI\(CH3COO\)', r'LITHIUM ACETATE')
    str = self.re_substitute(str, r'\(OAC\)-?2', r' ACETATE')
    str = self.re_substitute(str, r'\(AC\)2', r' ACETATE')
    str = self.re_substitute(str, r'OAC[^A-Z]', r' ACETATE')
 #   str = self.re_substitute(str, r'^ACO$', r'ACETATE') #1h9w?
    str = self.re_substitute(str, r'\(ACETATE\)2?', r' ACETATE')
    str = self.re_substitute(str, r'ACC?ETT?AET?E?', r'ACETATE')
    str = self.re_substitute(str, r'ACETATE ACETATE', r'ACETATE')
    str = self.re_substitute(str, r'\bACETIC ACID/SODIUM ACETATE', r'SODIUM ACETATE')
    str = self.re_substitute(str, r'\bACETATE/ACETIC ACID', r'ACETATE')
    str = self.re_substitute(str, r'\b(ACETIC|ACETATE)\s+ACID', r'ACETATE')
    str = self.re_substitute(str, r'^ACETATE/KOH', r'POTASSIUM ACETATE')
    str = self.re_substitute(str, r'^K\s*ACETATE', r'POTASSIUM ACETATE')
    str = self.re_substitute(str, r'\b(SODIUM|NA)\s+AC$', r'SODIUM ACETATE')
    str = self.re_substitute(str, r'\bACETATE[-/]\s*NAOH', r'SODIUM ACETATE')
    str = self.re_substitute(str, r'^MA ACETATE', r'SODIUM ACETATE') #1nqk
    str = self.re_substitute(str, r'^SOI?DIUM ?ACETATE(,N)?', r'SODIUM ACETATE')
    str = self.re_substitute(str, r'^AMMM?OU?NIU[MN]\s*\-?\(?\s*ACETATE?', r'AMMONIUM ACETATE') 
    str = self.re_substitute(str, r'^AMMONIU[MN]\s*\-?ACETATE?\s+\(\s*SODIUM ACETATE\)', r'AMMONIUM ACETATE') 
    str = self.re_substitute(str, r'CH3COONH4', r'AMMONIUM ACETATE')
    str = self.re_substitute(str, r'MG\(CH3COO\)2?', r'MAGNESIUM ACETATE')
    str = self.re_substitute(str, r'CH3COOMG', r'MAGNESIUM ACETATE')
    str = self.re_substitute(str, r'CH3COO', r'ACETATE')
    str = self.re_substitute(str, r'AC2CU', r'COPPER(II) ACETATE')

    str = self.re_substitute(str, r'ZI?NC?\(II\)', r'ZINC ')
    str = self.re_substitute(str, r'(ZN|ZINC)-?\s*ACETATE', r'ZINC ACETATE')
    str = self.re_substitute(str, r'(ZN|ZINC)\s*\(?ACO\)?2?', r'ZINC ACETATE')
    str = self.re_substitute(str, r'ZNO?AC2?\b', r'ZINC ACETATE')
    str = self.re_substitute(str, r'(ZINC|ZN)\s*\(\s*ACETATE\)? ?2', r'ZINC ACETATE')
    
    str = self.re_substitute(str, r'\bZNSO\(4\)', r'ZINC SULFATE')
    str = self.re_substitute(str, r'(\bZN\+2\b|\bZN2?)', r'ZINC ')
    str = self.re_substitute(str, r'ZI?NC? ?_CL', r'ZINC CHLORIDE')

    str = self.re_substitute(str, r'^CAAC(2|ETATE)?\b', r'CALCIUM ACETATE')
    str = self.re_substitute(str, r'^CALI?[CS]IUM ACETATE', r'CALCIUM ACETATE')

    str = self.re_substitute(str, r'AMPPCP', r'AMP-PCP')
    str = self.re_substitute(str, r'AMP/?\s*PNP', r'AMP-PNP')
    str = self.re_substitute(str, r'TWEEN\-20', r'TWEEN 20')

    if self.verbose>0:
      print "convert_name:4",repr(str)
    str = self.re_substitute(str, r'^CO\s*(CL2|CHLORIDE)', r'COBALT CHLORIDE')  #TSP
    str = self.re_substitute(str, r'^CO\(ACETATE\)2', r'COBALT ACETATE')  #TSP
    str = self.re_substitute(str, r'\bHEXAMMINE', r'HEXAMINE')  #TSP
    str = self.re_substitute(str, r'^CO\(NH3\)6CL3', r'COBALT HEXAMINE CHLORIDE')  #TSP
    str = self.re_substitute(str, r'^\[CO\(NH3\)\s*6?\]\s*CL3', r'COBALT HEXAMINE CHLORIDE')  #TSP 2g6f doesn't have the '6'
    str = self.re_substitute(str, r'^COL?BALT?(OUS)?\s*CHLO[RD]IDE?', r'COBALT CHLORIDE')  #TSP
    str = self.re_substitute(str, r'^CO(BALT)?\s*\(II\)\s*CHLORIDE', r'COBALT CHLORIDE')  #TSP
    str = self.re_substitute(str, r'^COBALTIC HEXAMINE CHLORIDE', r'COBALT HEXAMINE CHLORIDE')  #TSP
    str = self.re_substitute(str, r'^HEXAMINE COBALT$', r'COBALT HEXAMINE CHLORIDE')  #TSP
    str = self.re_substitute(str, r'^HEXAA?MM?INE\-? ?COBALT(\(III\))? ?(TRI)?CHLORIDE', r'COBALT HEXAMINE CHLORIDE')
    str = self.re_substitute(str, r'^COBALT\s*(\(III\))?\s*HEXAMINE\s*(CHLORIDE)?$', r'COBALT HEXAMINE CHLORIDE')  #TSP
    str = self.re_substitute(str, r'^K3FE\(CN\)6', r'POTASSIUM FERROCYANIDE')  #TSP
    str = self.re_substitute(str, r'^FESO4', r'IRON(II) SULFATE')  #TSP
    str = self.re_substitute(str, r'^FE\(II\)', r'IRON(II)')  #TSP
    str = self.re_substitute(str, r'^FERROUS CITRATE', r'IRON(II) CITRATE')  #TSP
    str = self.re_substitute(str, r'^FERROUS SULPHATE', r'IRON(II) SULFATE')  #TSP
    str = self.re_substitute(str, r'FECL3', r'IRON(III) CHLORIDE')
    str = self.re_substitute(str, r'^SRCL2', r'STRONTIUM CHLORIDE')  #TSP
    str = self.re_substitute(str, r'STRONTIUM CHLORIDE \(SRCL2\)', r'STRONTIUM CHLORIDE')
    str = self.re_substitute(str, r'^SR\(NO3\)2', r'STRONTIUM NITRATE')  #TSP
    str = self.re_substitute(str, r'^SMCL3', r'SAMARIUM CHLORIDE')  #TSP
    str = self.re_substitute(str, r'^HOCL3', r'HOLMIUM CHLORIDE')  #TSP
    str = self.re_substitute(str, r'^GDCL3', r'GADOLINIUM CHLORIDE')  #TSP
    str = self.re_substitute(str, r'^LUCL3', r'LUTETIUM CHLORIDE')  #TSP
    str = self.re_substitute(str, r'^ERCL3', r'ERBIUM CHLORIDE')  #TSP
    str = self.re_substitute(str, r'^HGCL2', r'MERCURY CHLORIDE')  #TSP
    str = self.re_substitute(str, r'^Y CHLORIDE', r'YTTRIUM CHLORIDE')
    str = self.re_substitute(str, r'YTRIUM CHLORIDE', r'YTTRIUM CHLORIDE')
    str = self.re_substitute(str, r'^YCL[23]\b', r'YTTRIUM CHLORIDE')
    str = self.re_substitute(str, r'YTTERBIUM\s*\(II\)\s*CHLORIDE', r'YTTERBIUM CHLORIDE')
    str = self.re_substitute(str, r'^YBCL[23]\b', r'YTTERBIUM CHLORIDE')
    str = self.re_substitute(str, r'^TMCL[23]\b', r'THULIUM CHLORIDE')
    str = self.re_substitute(str, r'^EMTS\s*\(THIMEROSAL\)', r'THIMEROSAL')  #TSP
    str = self.re_substitute(str, r'^THIMERSOL', r'THIMEROSAL')
    str = self.re_substitute(str, r'^(EMTS|THIMERASOL)', r'THIMEROSAL')  #TSP
    str = self.re_substitute(str, r'^BACL2', r'BARIUM CHLORIDE')  #TSP
    str = self.re_substitute(str, r'^NA2W[O0]4', r'SODIUM TUNGSTATE')  #TSP
    str = self.re_substitute(str, r'^W[O0]4\b', r'TUNGSTATE')  #TSP
    str = self.re_substitute(str, r'^NA2MO+4', r'SODIUM MOLYBDATE')  #TSP
    str = self.re_substitute(str, r'^NA3?VO[34]\b', r'SODIUM VANADATE')  #TSP
    str = self.re_substitute(str, r'^NA\s*F\b', r'SODIUM FLUORIDE')  #TSP
    str = self.re_substitute(str, r'^KF\b', r'POTASSIUM FLUORIDE')  #TSP
    str = self.re_substitute(str, r'POTASSIUM FLURIDE', r'POTASSIUM FLUORIDE')
    str = self.re_substitute(str, r'^NH4F\b', r'AMMONIUM FLUORIDE')  #TSP
    str = self.re_substitute(str, r'AMMONMIUM FLUORIDE', r'AMMONIUM FLUORIDE')
    str = self.re_substitute(str, r'^NH4I\b', r'AMMONIUM IODIDE')  #TSP
    str = self.re_substitute(str, r'AMMOUNIUM TARTRATE', r'AMMONIUM TARTRATE')
    
    str = self.re_substitute(str, r'K/NA TARTRATE', r'SODIUM POTASSIUM TARTRATE')
    str = self.re_substitute(str, r'^NAI\b', r'SODIUM IODIDE')  #TSP
    str = self.re_substitute(str, r'^KI\b', r'POTASSIUM IODIDE')  #TSP
    str = self.re_substitute(str, r'^NAIO4\b', r'SODIUM PERIODATE')  #TSP
    str = self.re_substitute(str, r'\bPB\(II\)', r'LEAD')  #TSP
    str = self.re_substitute(str, r'^PB\b', r'LEAD')  #TSP
    str = self.re_substitute(str, r'^RB\b', r'RUBIDIUM')  #TSP
    str = self.re_substitute(str, r'^RBCL\b', r'RUBIDIUM CHLORIDE')
    str = self.re_substitute(str, r'^UO2\b', r'URANYL')  #TSP
    str = self.re_substitute(str, r'^K2PTCL4\b', r'POTASSIUM TETRACHLOROPLATINATE')  #TSP
    str = self.re_substitute(str, r'^AL\(NO3\)3\b', r'ALUMINUM NITRATE')  #TSP
    str = self.re_substitute(str, r'^ALCL3\b', r'ALUMINUM CHLORIDE')  #TSP
    str = self.re_substitute(str, r'^NH4VO3', r'AMMONIUM VANADATE')
    str = self.re_substitute(str, r'^EU\(NO3\)3', r'EUROPIUM NITRATE')
    str = self.re_substitute(str, r'^CA\(NO3\)2', r'CALCIUM NITRATE')
    str = self.re_substitute(str, r'^BECL2', r'BERYLLIUM CHLORIDE')  #TSP
    str = self.re_substitute(str, r'^KHPHTHALATE\/\s*NAOH', r'SODIUM POTASSIUM PHTHALATE')  #TSP

    str = self.re_substitute(str, r'CITRATE-AMMONIUM', r'AMMONIUM CITRATE')
    str = self.re_substitute(str, r'AMM?CITRATE?', r'AMMONIUM CITRATE')
    str = self.re_substitute(str, r'AMMONIUM\-?\s*H(YDROGEN)?\s+\(?CIT(RAT)?E?', r'AMMONIUM CITRATE')
    str = self.re_substitute(str, r'\b(B|D)I\s*-?\s*AMMO(M|N)IUM', r'AMMONIUM ')
    str = self.re_substitute(str, r'AQ?MMONIO?UM*', r'AMMONIUM')
    str = self.re_substitute(str, r'AN?MMO(M|N)IUM', r'AMMONIUM')
    str = self.re_substitute(str, r'AMMN?ON(ON)?IM?UM', r'AMMONIUM')
    str = self.re_substitute(str, r'AMOM?N?NIUM', r'AMMONIUM')    
    str = self.re_substitute(str, r'AMM(M|N)?O?NO?I?UM\-?', r'AMMONIUM ')

    str = self.re_substitute(str, r'^BETA-ME$', r'BETA-MERCAPTOETHANOL')
    str = self.re_substitute(str, r'^B-?\s*ME$', r'BETA-MERCAPTOETHANOL')
    str = self.re_substitute(str, r'^2-\s*ME$', r'BETA-MERCAPTOETHANOL')
    str = self.re_substitute(str, r'MERCAPTOEHTANOL', r'MERCAPTOETHANOL')

    str = self.re_substitute(str, r'^OX(IDIZED )?BME$', r'OXIDIZED BETA-MERCAPTOETHANOL')
    str = self.re_substitute(str, r'^OXIDIZED/REDUCED\s+BME$', r'BETA-MERCAPTOETHANOL')

    str = self.re_substitute(str, r'\(?\(?NH4\)?\)?\s*2\(?S[O0]4\)?', r'AMMONIUM SULFATE')
    str = self.re_substitute(str, r'NH4[-.,/]?SO4', r'AMMONIUM SULFATE')
    str = self.re_substitute(str, r'K2?[-.,/]?SO[34]', r'POTASSIUM SULFATE')
    str = self.re_substitute(str, r'2?\(SO4\)2?', r' SULFATE')
    str = self.re_substitute(str, r'\(SO4\)', r' SULFATE')
    str = self.re_substitute(str, r'\(SO4', r' SULFATE')
    str = self.re_substitute(str, r'\(?NH\)?2SO4', r'AMMONIUM SULFATE')
    str = self.re_substitute(str, r'(SULFATE|SO4)\(NH4\)2', r'AMMONIUM SULFATE')
    str = self.re_substitute(str, r'H?2SO4', r' SULFATE')
    str = self.re_substitute(str, r'2SO3', r' SULFITE')
    str = self.re_substitute(str, r'SO4', r' SULFATE')
    str = self.re_substitute(str, r'SUL?(PH|F|P)L?ATE?', r'SULFATE')
    str = self.re_substitute(str, r'SAL(PH|F|P)ATE', r'SULFATE')
    str = self.re_substitute(str, r'SLU(PH|F)ATE?', r'SULFATE')
    str = self.re_substitute(str, r'NA2 SULFATE', r'SODIUM SULFATE')
    str = self.re_substitute(str, r'NA2S2O3', r'SODIUM SULFITE')

    str = self.re_substitute(str, r'AM(M|MONIUM)?\s*SULFATE', r'AMMONIUM SULFATE')
    str = self.re_substitute(str, r'AMMOINIUM SULFATE', r'AMMONIUM SULFATE')
    str = self.re_substitute(str, r'AMMONIUM SULFA?T?$', r'AMMONIUM SULFATE')
    str = self.re_substitute(str, r'AMMONIUM SULAFTE', r'AMMONIUM SULFATE')
    str = self.re_substitute(str, r"SULFATE D'AMMONIUM", r'AMMONIUM SULFATE')

    str = self.re_substitute(str, r'\(NH2\)\s*2', r'AMMONIUM ')
    str = self.re_substitute(str, r'^NH[43]CL\b', r'AMMONIUM CHLORIDE')
    str = self.re_substitute(str, r'AMMONIUM CHLOREDE', r'AMMONIUM CHLORIDE')
    str = self.re_substitute(str, r'AMMONIUM\s+CHLORIDE', r'AMMONIUM CHLORIDE')
    str = self.re_substitute(str, r'^NH4NO3', r'AMMONIUM NITRATE')
    str = self.re_substitute(str, r'AMMONIUM NITRAT(,|RE)', r'AMMONIUM NITRATE')
    str = self.re_substitute(str, r'^NH4OH', r'AMMONIUM HYDROXIDE')
    str = self.re_substitute(str, r'^NH4SCN', r'AMMONIUM THIOCYANATE')
    str = self.re_substitute(str, r'^NH4BR$', r'AMMONIUM BROMIDE')
    str = self.re_substitute(str, r'^NH4H2PO$', r'AMMONIUM PHOSPHATE')
    str = self.re_substitute(str, r'\bAMM PO4', r'AMMONIUM PHOSPHATE')
    str = self.re_substitute(str, r'^NH4-?', r'AMMONIUM ')
    str = self.re_substitute(str, r'^\(NH4\)2?', r'AMMONIUM ')
    str = self.re_substitute(str, r'^\(NH\)4-?', r'AMMONIUM ')
    str = self.re_substitute(str, r'\(?NH4\)?', r'AMMONIUM ')
    str = self.re_substitute(str, r'\bPHOSPHATE\s*AMMONIUM\b', r'AMMONIUM PHOSPHATE')

    str = self.re_substitute(str, r' COOH', r' FORMATE')
    str = self.re_substitute(str, r'\bNAHCOO\b', r'SODIUM FORMATE')
    str = self.re_substitute(str, r'\bNACOOH\b', r'SODIUM FORMATE')
    str = self.re_substitute(str, r'\bFORMI?ATE?', r'FORMATE')
    str = self.re_substitute(str, r'^FORMATE SODIUM', r'SODIUM FORMATE')
    str = self.re_substitute(str, r'\bFORMIC\s*ACID', r'FORMATE')

    if self.verbose>0:
      print "convert_name:5",repr(str)
    str = self.re_substitute(str, r'^NAHCO3', r'SODIUM BICARBONATE')

    str = self.re_substitute(str, r'ISO\-?\s*PR?OR?P[AO]N[OA]L', r'ISOPROPANOL')
    str = self.re_substitute(str, r'^ISOPRO?PANOL?E?N?$', r'ISOPROPANOL')
    str = self.re_substitute(str, r'^ISO-?PROP$', r'ISOPROPANOL')
    str = self.re_substitute(str, r'2-?\s*PROP[AO]N[OA]L', r'ISOPROPANOL')
    str = self.re_substitute(str, r'I-?\s*PROPANOL', r'ISOPROPANOL')
    str = self.re_substitute(str, r'PROPAN-2-OL', r'ISOPROPANOL')

    str = self.re_substitute(str, r'N-?\s*PROPANOL', r'PROPANOL')
    str = self.re_substitute(str, r'1-?\s*PROPANOL', r'PROPANOL')
    str = self.re_substitute(str, r'^ISOPROPYL ALCOHOL', r'ISOPROPANOL')
    str = self.re_substitute(str, r'ISOPROPANOOL', r'ISOPROPANOL')
    str = self.re_substitute(str, r'^IPR$', r'ISOPROPANOL')

    str = self.re_substitute(str, r'1,\s*2\-?\s*PRO?PANE?DIOL', r'1,2-PROPANEDIOL')
    str = self.re_substitute(str, r'1[-,]\s*3\-PROPANEDIOL', r'1,3-PROPANEDIOL')
    str = self.re_substitute(str, r'N-?\s*BUTANOL', r'BUTANOL')
    str = self.re_substitute(str, r'N-\s*OCTANOYLSUCROSE', r'OCTANOYLSUCROSE')

    str = self.re_substitute(str, r'\s+', r' ')

    str = self.re_substitute(str, r'SULPH', r'SULF')
    str = self.re_substitute(str, r'AMMONIUM-', r'AMMONIUM ')
    str = self.re_substitute(str, r'\s+', r' ')

    str = self.re_substitute(str, r'BIS?\s*[-/._0]?\s*TR(I|-)S', r'BIS TRIS') # problem with 1zya????
    str = self.re_substitute(str, r'TRISPROPANE', r'TRIS PROPANE')
    str = self.re_substitute(str, r'\(BTP\)', r'')
    str = self.re_substitute(str, r'\bBTP(ROP)?\b', r'BIS TRIS PROPANE')
    str = self.re_substitute(str, r'BIS TRIS[ \-]PROPANE:NAOH', r'BIS TRIS PROPANE')
    str = self.re_substitute(str, r'BIS-TRIS-PROPANE', r'BIS TRIS PROPANE')
    str = self.re_substitute(str, r'\bBIS$', r'BIS TRIS')
    str = self.re_substitute(str, r'\bMES-?\s*BIS\s*TRIS\b', r'MES BIS TRIS')
    str = self.re_substitute(str, r'\(CITRATE/MES\)',r'CITRATE MES')

    str = self.re_substitute(str, r'^HEPES-?\s*SODIUM\s*(SALT)?', r'SODIUM HEPES')
    str = self.re_substitute(str, r'^NA, +HEPES', r'SODIUM HEPES')
    str = self.re_substitute(str, r'^HEPES\s*[-./]\s*NA(OH)?', r'SODIUM HEPES')
    str = self.re_substitute(str, r'^HEPES\s*[-./]\s*KOH', r'POTASSIUM HEPES')
    str = self.re_substitute(str, r'^K\s*HEPES', r'POTASSIUM HEPES')
    str = self.re_substitute(str, r'^HEPES\s*[-./_]\s*NA', r'SODIUM HEPES')
    str = self.re_substitute(str, r'^HEPES\s*\(NAOH\)', r'SODIUM HEPES')
    str = self.re_substitute(str, r'^NAOH\s*[-./_]\s*HEPES', r'SODIUM HEPES')
    str = self.re_substitute(str, r'^HEPES[-/ ]HCL', r'HEPES')
    str = self.re_substitute(str, r'^HEPE?R?S\b', r'HEPES')
    str = self.re_substitute(str, r'^HPETES\b', r'HEPES') # a guess as HPETEs are unstable and not soluble in aqueus solutions
    str = self.re_substitute(str, r'^N-\(2-HYDROXYETHYL\)PIPERAZINE-N\'-\(2-ETHANESULFONIC ACID\)?\s*\(HEPES\)', r'HEPES')
    str = self.re_substitute(str, r'^2?-?\(?4-\(2-HYDROXYETHYL\)-1-PIPERZAINYL\)?\s*ETHANESULFONIC\s*ACID', r'HEPES')

    str = self.re_substitute(str, r'^AMPSO[-./]\s*KOH', r'POTASSIUM AMPSO')

    str = self.re_substitute(str, r'([0-9]),([0-9][0-9][0-9])', r'\1\2')

    str = self.re_substitute(str, r'^CAL?CL\(?2?\0?', r'CALCIUM CHLORIDE')
    str = self.re_substitute(str, r'CALU?(C|S)IU[MN]\-?\s*CHLORIDE', r'CALCIUM CHLORIDE')
    str = self.re_substitute(str, r'CAL CHLORIDE', r'CALCIUM CHLORIDE')
    str = self.re_substitute(str, r'CABR2', r'CALCIUM BROMIDE')
    str = self.re_substitute(str, r'^CA[-2 ]', r'CALCIUM ')

    str = self.re_substitute(str, r'^CDAC', r'CADMIUM ACETATE')
    str = self.re_substitute(str, r'^CDCL2?', r'CADMIUM CHLORIDE')
    str = self.re_substitute(str, r'^CDS04?', r'CADMIUM SULFATE')
    str = self.re_substitute(str, r'^CD2?\+?\b', r'CADMIUM ')
    str = self.re_substitute(str, r'MERCURIUM', r'MERCURY')
    str = self.re_substitute(str, r'\s+', r' ')

    str = self.re_substitute(str, r'CITRATE/\s*CITRIC ACID', r'CITRATE')
    str = self.re_substitute(str, r'\bACID CITRIC', r'CITRATE')
    str = self.re_substitute(str, r'\bCITRIC\s*(ACID)?', r'CITRATE')
    str = self.re_substitute(str, r'CITRATE[-/]?\s*(NAOH|SODIUM|NA)\)?', r'SODIUM CITRATE')
    str = self.re_substitute(str, r'CITRATE\s*[-/,.]\s*', r'CITRATE ')
    str = self.re_substitute(str, r'\bCITR(TE)?$', r'CITRATE')
    str = self.re_substitute(str, r'^NACITR(AT)?E?', r'SODIUM CITRATE')
    str = self.re_substitute(str, r'^SODIUMCITRATE', r'SODIUM CITRATE')
    str = self.re_substitute(str, r'^NAC[TI]$', r'SODIUM CITRATE')
    str = self.re_substitute(str, r'\bNA3CIT/H3CIT', r'TRISODIUM CITRATE-CITRIC ACID')
    str = self.re_substitute(str, r'\bH3CIT/NA3CIT', r'TRISODIUM CITRATE-CITRIC ACID')
    str = self.re_substitute(str, r'\bNA3-?\s*CIT(RATE)?$', r'TRISODIUM CITRATE')
    str = self.re_substitute(str, r'\bNA-?\s*CIT(RATE)?$', r'SODIUM CITRATE')
    str = self.re_substitute(str, r'\bTRIS-?\s*(NA|SODIUM)\s*CIT(RATE)?', r'TRISODIUM CITRATE')
    str = self.re_substitute(str, r'\bCIT$', r'CITRATE')
    str = self.re_substitute(str, r'CITRAC?TE\)?', r'CITRATE')
    str = self.re_substitute(str, r'H?CITR?ATED?', r'CITRATE')

    str = self.re_substitute(str, r'ISOCITRATE\s*ACID', r'ISOCITRATE')

    str = self.re_substitute(str, r'^NI ', r'NICKEL ')
    str = self.re_substitute(str, r'\bNICKEL\s*\(II\)', r'NICKEL')
    str = self.re_substitute(str, r'^NICL2?', r'NICKEL CHLORIDE')
    str = self.re_substitute(str, r'^NICKLE', r'NICKEL ')
    str = self.re_substitute(str, r'^CU ', r'COPPER ')
    str = self.re_substitute(str, r'^CUCL2?', r'COPPER CHLORIDE')
    str = self.re_substitute(str, r'^CUPRIC', r'COPPER')
    str = self.re_substitute(str, r'\bCOPPER\s*\(II\)', r'COPPER')
    str = self.re_substitute(str, r'^CSCL', r'CESIUM CHLORIDE')
    str = self.re_substitute(str, r'^CESEIUM', r'CESIUM')
    str = self.re_substitute(str, r'^CAESIUM', r'CESIUM')

    str = self.re_substitute(str, r'[^A-Z]CO ', r'COBALT')

    if self.verbose>0:
      print "convert_name:6",repr(str)

    str = self.re_substitute(str, r'\s+', r' ')

    str = self.re_substitute(str, r'\bK[-,/.]', r'POTASSIUM ')
    str = self.re_substitute(str, r'\bK3?\s*CIR?T(RATE)?', r'POTASSIUM CITRATE')
    str = self.re_substitute(str, r'\bK3?\s*\(?CIT(RATE)?\b', r'POTASSIUM CITRATE')
    str = self.re_substitute(str, r"\bSODIUM\'", r'SODIUM ')
    str = self.re_substitute(str, r"\bSOUDIUM ", r'SODIUM ')
    str = self.re_substitute(str, r'([^A-Z])NA ', r' \1 SODIUM ')

    str = self.re_substitute(str, r'SOLDIUM', r'SODIUM')
    str = self.re_substitute(str, r'SO?[DC]O?IUM', r'SODIUM')
    str = self.re_substitute(str, r'SODU?IU?[NM]', r'SODIUM')
    str = self.re_substitute(str, r'SODIUM[-/.]', r'SODIUM ')
    str = self.re_substitute(str, r'^NA2?\s*-?\s+', r'SODIUM ')
    str = self.re_substitute(str, r'^NA/SODIUM ', r'SODIUM ')
    str = self.re_substitute(str, r'^NA[-./,]H?\b', r'SODIUM ')

    str = self.re_substitute(str, r'POTASSIUM/SODIUM', r'SODIUM POTASSIUM')

    str = self.re_substitute(str, r'^LI ', r'LITHIUM ')
    str = self.re_substitute(str, r'^LI-', r'LITHIUM ')
    str = self.re_substitute(str, r'^L[IY]TH?IUM\b', r'LITHIUM ')
    str = self.re_substitute(str, r'^LICL2?', r'LITHIUM CHLORIDE')
    str = self.re_substitute(str, r'^LIBR$', r'LITHIUM BROMIDE')
    str = self.re_substitute(str, r'^LINO3', r'LITHIUM NITRATE')
    str = self.re_substitute(str, r'^LI3?CITRATE', r'LITHIUM CITRATE')
    str = self.re_substitute(str, r'^\(?LI\)?(THIUM)?\s*SULFATE', r'LITHIUM SULFATE')
    str = self.re_substitute(str, r'\bLI2?\(?S[O0]4\)?', r'LITHIUM SULFATE')
    str = self.re_substitute(str, r'\bLI\(2\)S[O0]\(4\)', r'LITHIUM SULFATE')
    str = self.re_substitute(str, r'\bLISULF\b', r'LITHIUM SULFATE')
    str = self.re_substitute(str, r'\bLI2', r'LITHIUM')

    str = self.re_substitute(str, r'(DL-)?MALIC ACID', r'MALATE')
    str = self.re_substitute(str, r'D\-L\s+MALIC ACID', r'MALATE')
    str = self.re_substitute(str, r'D,L\-MALATE', r'MALATE')
    str = self.re_substitute(str, r'MALEIC\s*ACID/NAOH', r'SODIUM MALEATE')
    str = self.re_substitute(str, r'MALEIC\s*ACID', r'MALEATE')
    str = self.re_substitute(str, r'MALETE', r'MALEATE')
    str = self.re_substitute(str, r'MALEATE/HCL', r'MALEATE')
    str = self.re_substitute(str, r'MALEATE (SODIUM|DISODIUM SALT)', r'SODIUM MALEATE')
    str = self.re_substitute(str, r'MALONIC ACID', r'MALONATE')
    str = self.re_substitute(str, r'SODIUM MA?(L|N)O(N|L)ATE', r'SODIUM MALONATE')
    str = self.re_substitute(str, r'\bNA2?\(?MALONATE\)?', r'SODIUM MALONATE')
    str = self.re_substitute(str, r'\bDI(SODIUM|NATRIUM)MALONATE', r'SODIUM MALONATE')
    str = self.re_substitute(str, r'\bTRISMALEATE', r'TRIS MALEATE')
    str = self.re_substitute(str, r'\bTRIS-MAL\/\s*NAOH', r'SODIUM TRIS MALEATE')
    str = self.re_substitute(str, r'\bMMT\b', r'MALATE MES TRIS') #one of Janet's buffers

    str = self.re_substitute(str, r'\bMEOH', r'METHANOL')
    str = self.re_substitute(str, r'\bETOH\b', r'ETHANOL')
    str = self.re_substitute(str, r'\bETHENOL\b', r'ETHANOL')
    str = self.re_substitute(str, r'METHANOL/ETHANOL', r'METHANOL-ETHANOL')

    str = self.re_substitute(str, r'M(A|E)GE?N?(E|I)SR?S?U?IS?U?M', r'MAGNESIUM')
    str = self.re_substitute(str, r'MAGENSIUM', r'MAGNESIUM')
    str = self.re_substitute(str, r'MAGNESESIUM',r'MAGNESIUM')
    str = self.re_substitute(str, r'MAGNESIUMCHLORIDE?\b', r'MAGNESIUM CHLORIDE')
    str = self.re_substitute(str, r'MG\s*CHLORI?D?E?', r'MAGNESIUM CHLORIDE')
    str = self.re_substitute(str, r'\bMGACETATE', r'MAGNESIUM ACETATE')
    str = self.re_substitute(str, r'\bMA?G2?CL\(2\)', r'MAGNESIUM CHLORIDE')
    str = self.re_substitute(str, r'\bMA?G2?CL2?\b', r'MAGNESIUM CHLORIDE')
    str = self.re_substitute(str, r'\bMG ', r'MAGNESIUM ')
    str = self.re_substitute(str, r'\bMG-ACE', r'MAGNESIUM ACE')
    str = self.re_substitute(str, r'\bMG2?\-? ?ATP', r'MAGNESIUM ATP')
    str = self.re_substitute(str, r'\bMG-?ADP', r'MAGNESIUM ADP')
    str = self.re_substitute(str, r'\bMGAC2?', r'MAGNESIUM ACETATE')
    str = self.re_substitute(str, r'\bMGOAC', r'MAGNESIUM ACETATE')
    str = self.re_substitute(str, r'\bMG(OAC)-?2', r'MAGNESIUM ACETATE')
    str = self.re_substitute(str, r'\bMG\(?FORMA?T?E?\)?2?', r'MAGNESIUM FORMATE')
    str = self.re_substitute(str, r'\bMGS[O0]4', r'MAGNESIUM SULFATE')
    str = self.re_substitute(str, r'MAGNESIUM/\s*CALCIUM SULFATE', r'MAGNESIUM CALCIUM SULFATE')
    str = self.re_substitute(str, r'\(MG\)2?\s*(SULFATE|SO4)', r'MAGNESIUM SULFATE')
    str = self.re_substitute(str, r'SULFATE DE MAGNESIUM', r'MAGNESIUM SULFATE') 
    str = self.re_substitute(str, r'\bMG\(?NO3\)?2?', r'MAGNESIUM NITRATE')
    str = self.re_substitute(str, r'\bMG(2\+|-)', r'MAGNESIUM ')
    str = self.re_substitute(str, r'\bMG\(II\)', r'MAGNESIUM ')

    str = self.re_substitute(str, r'\bMANGANESE\s*\(II\)\s*CHLORIDE', r'MANGANESE CHLORIDE')
    str = self.re_substitute(str, r'\bMANGANESECHLORIDE', r'MANGANESE CHLORIDE')
    str = self.re_substitute(str, r'\bMNCL2?\b', r'MANGANESE CHLORIDE')
    str = self.re_substitute(str, r'\bMNS[0O]4?\b', r'MANGANESE SULFATE')
    str = self.re_substitute(str, r'\bMN2?\b', r'MANGANESE ')
    str = self.re_substitute(str, r'\bMANGANOUS\b', r'MANGANESE ')

    str = self.re_substitute(str, r'TRIS\s*[-/,.]?\s*\(?HYDROXYMETHYL\)?[-/,. ]?AMINOMETHANE(\s*\(TRIS\))?', r'TRIS ')
    str = self.re_substitute(str, r'TRIS/TRISHCL', r'TRIS CHLORIDE')
    str = self.re_substitute(str, r'TRISHCL\b', r'TRIS CHLORIDE')
    str = self.re_substitute(str, r'TRIS[-_./]\s*BASE', r'TRIS')
    str = self.re_substitute(str, r'TRIS\s*[-/,.]\s*', r'TRIS ')

    str = self.re_substitute(str, r'\s+', r' ')

    str = self.re_substitute(str, r'TRIS\s*HYDROCH[RL]O[LR]IDE', r'TRIS CHLORIDE')
    str = self.re_substitute(str, r'TRIS[-/_]?\s*HCL\/\s*NAOH', r'SODIUM TRIS CHLORIDE')
    str = self.re_substitute(str, r'TRIS?\s*[-/_*(]?\s*H?CL', r'TRIS CHLORIDE')
    str = self.re_substitute(str, r'TRIS\(HCL\)', r'TRIS CHLORIDE')
    str = self.re_substitute(str, r'TRIS (\+|WELL:)', r'TRIS')
    str = self.re_substitute(str, r'\.TRIS', r'TRIS')
    str = self.re_substitute(str, r'TRIZMA', r'TRIS')
    str = self.re_substitute(str, r'\bTIRS\b', r'TRIS')
    str = self.re_substitute(str, r'\bTRIC[-/,.]H?CL', r'TRIS CHLORIDE')
    str = self.re_substitute(str, r'\bTRIS[-/,. ]?AC$', r'TRIS ACETATE')
    str = self.re_substitute(str, r'\bTRIS\(HOAC\)', r'TRIS ACETATE')
    str = self.re_substitute(str, r'\bTRIS\(H ACETATE', r'TRIS ACETATE')

    str = self.re_substitute(str, r'\bCHOLINE-CL', r'CHOLINE')
    str = self.re_substitute(str, r'\bG[DU]HCL', r'GUANIDINE HYDROCHLORIDE')

    str = self.re_substitute(str, r'CHLOR$', r'CHLORIDE')
    str = self.re_substitute(str, r'[^A-Z]NACL[^A-Z]', r'SODIUM CHLORIDE')
    str = self.re_substitute(str, r'[^A-Z]KCL[^A-Z]', r'POTASSIUM CHLORIDE')
    str = self.re_substitute(str, r'^NA_?CL2?\b', r'SODIUM CHLORIDE')
    str = self.re_substitute(str, r'\bKCL\)', r'POTASSIUM CHLORIDE')
    str = self.re_substitute(str, r'\bK\s*CL2?\b', r'POTASSIUM CHLORIDE')
    str = self.re_substitute(str, r'\bCL2?$', r' CHLORIDE')
    str = self.re_substitute(str, r'DICH?LORIDE', r' CHLORIDE')  #TSP

    str = self.re_substitute(str, r'^NACO$', r'SODIUM CACODYLATE')
    str = self.re_substitute(str, r'^NACACOD?$', r'SODIUM CACODYLATE')
    str = self.re_substitute(str, r'\bNACAC\.?/CAC\.ACID', r'SODIUM CACODYLATE')
    str = self.re_substitute(str, r'\bNACAC\.?$', r'SODIUM CACODYLATE')
    str = self.re_substitute(str, r'^NA-?\s*CACODYLATE$', r'SODIUM CACODYLATE')
    str = self.re_substitute(str, r'^K-?\s*CACODYLATE$', r'POTASSIUM CACODYLATE')
    str = self.re_substitute(str, r'^SODIUMCACODYLATE$', r'SODIUM CACODYLATE')
    str = self.re_substitute(str, r'\(CACODYLATE\)', r' CACODYLATE')
    str = self.re_substitute(str, r'CACODYLATE CACODYLATE', r'CACODYLATE')
    str = self.re_substitute(str, r'\bCOC(O|A)DYLATE', r'CACODYLATE')
    str = self.re_substitute(str, r'\bCARCODYLATE', r'CACODYLATE')
    str = self.re_substitute(str, r'\bCA?CODYLA?TA?E', r'CACODYLATE')
    str = self.re_substitute(str, r'\bCACODYLA$', r'CACODYLATE')
    str = self.re_substitute(str, r'\bCACOD$', r'CACODYLATE')
    str = self.re_substitute(str, r'^CAC$', r'CACODYLATE')
    str = self.re_substitute(str, r'\bNA\(CH3\)2ASO2?', r'SODIUM CACODYLATE')
    str = self.re_substitute(str, r'CACOD\.ACID / SODIUM CACODYLATE', r'SODIUM CACODYLATE')
    str = self.re_substitute(str, r'^ODIUM CACODYLATE$', r'SODIUM CACODYLATE')

    str = self.re_substitute(str, r'\s+', r' ')

    str = self.re_substitute(str, r'\bK2[O0]1\b', r'POTASSIUM OXIDE')

    str = self.re_substitute(str, r'^NA-?TRICINE', r'SODIUM TRICINE')
    str = self.re_substitute(str, r'^TRICINE-NA$', r'SODIUM TRICINE')
    str = self.re_substitute(str, r'^GLY-NAOH', r'SODIUM GLYCINE')
    str = self.re_substitute(str, r'^GLY\b', r'GLYCINE')

    str = self.re_substitute(str, r'^NAAZIDE', r'SODIUM AZIDE')
    str = self.re_substitute(str, r'\bNAN\(?3\)?\b', r'SODIUM AZIDE')
    str = self.re_substitute(str, r'\bACIDE', r' AZIDE')
    str = self.re_substitute(str, r'^NABR\b', r'SODIUM BROMIDE')
    str = self.re_substitute(str, r'^KBR\b', r'POTASSIUM BROMIDE')
    str = self.re_substitute(str, r'^NAC2H3O2\b', r'SODIUM ACETATE')
    str = self.re_substitute(str, r'^(NA|SODIUM)\s*FORMI?(ATE)?', r'SODIUM FORMATE')
    str = self.re_substitute(str, r'^K\s*FORMATE', r'POTASSIUM FORMATE')
    str = self.re_substitute(str, r'^NAHEPES', r'SODIUM HEPES')
    str = self.re_substitute(str, r'HEPE\-NA', r'SODIUM HEPES')
    str = self.re_substitute(str, r'^NAK\b', r'SODIUM POTASSIUM ')
    str = self.re_substitute(str, r'\s+', r' ')
    str = self.re_substitute(str, r'^NAH?2?NO3\b', r'SODIUM NITRATE')
    str = self.re_substitute(str, r'^K2?H?NO3\b', r'POTASSIUM NITRATE')
    str = self.re_substitute(str, r'^NAOH\b', r'SODIUM HYDROXIDE')
    str = self.re_substitute(str, r'NATRIUM', r'SODIUM')
    str = self.re_substitute(str, r'NAGLUTAMATE', r'SODIUM GLUTAMATE')
    str = self.re_substitute(str, r'(L-)?GLUTAMIC\s*ACID', r'GLUTAMATE')
    str = self.re_substitute(str, r'(L-)?GLUTA?MA?TE?', r'GLUTAMATE')
    str = self.re_substitute(str, r'L-METHIONINE', r'METHIONINE')
    str = self.re_substitute(str, r'L-SERINE', r'SERINE')
    str = self.re_substitute(str, r'L-TRYPTOPHAN', r'TRYPTOPHAN')
    str = self.re_substitute(str, r'\bL-CYS(TEINE?)?', r'CYSTEINE')
    str = self.re_substitute(str, r'L-LYSINE', r'LYSINE')

    str = self.re_substitute(str, r'NH2 SULFATE', r'AMMONIUM SULFATE')
    str = self.re_substitute(str, r'AMM[PO]U?NN?IUM _?SUL(PA)?[FH]A?TE2?', 'AMMONIUM SULFATE')

    if self.verbose>0:
      print "convert_name:7",repr(str)

    str = self.re_substitute(str, r'SODIUM 4-TOUENE SULFONATE', r'SODIUM PARA-TOLUENE SULFONATE')
    str = self.re_substitute(str, r'\bNAPTS\b', r'SODIUM PARA-TOLUENE SULFONATE')

    str = self.re_substitute(str, r'^OEG', r'PEG')
    str = self.re_substitute(str, r'PDG', r'PEG')

    str = self.re_substitute(str, r'T-BUOH', r'TERT-BUTANOL')
    str = self.re_substitute(str, r'^T-\s*BUTANOL', r'TERT-BUTANOL')
    str = self.re_substitute(str, r'^TERTIARY BUTANOL', r'TERT-BUTANOL')
    str = self.re_substitute(str, r'^SEC-BUTANOL', r'TERT-BUTANOL')
    str = self.re_substitute(str, r',?2-METHYLPROPANE-2-OL\s*\(TERTIARY BUTANOL\)', r' TERT-BUTANOL')
    str = self.re_substitute(str, r'^1(,|\-)3\s*-?BUTANEDIOL?E?', r'1,3-BUTANEDIOL')
    str = self.re_substitute(str, r'^1\\?(,|\.)\s*4\s*-?\s*BUTANO?D?E?\-?DIOL', r'1,4-BUTANEDIOL')
    str = self.re_substitute(str, r'^1,4\s*-?BUTYLDIOL', r'1,4-BUTANEDIOL')
    str = self.re_substitute(str, r'BUTANE[\- ]1,4\-DIOL', r'1,4-BUTANEDIOL')
    
    str = self.re_substitute(str, r'1\s*,\s*5\s*-\s*DIAMINO\-?PENTANE\s*(DI)?', r'1,5-DIAMINOPENTANE DIHYDROCHLORIDE')
    str = self.re_substitute(str, r'1,3\s*\-\s*DIAMINO\-PROPANE', r'1,3-DIAMINOPROPANE')

    str = self.re_substitute(str, r'N-\s*\[TRIS\(HYDROXYMETHYL\)METHYL\]-2-?\s*AMINOETHANESULFONATE', r'TES')
    str = self.re_substitute(str, r'TRIS-?\s*\[\(HYDROXYMETHYL\)METHYL\]-2-AMINOSULFONATE', r'TES')

    str = self.re_substitute(str, r'^2,2,2-TRIFLUO?RO ?ETHANOL', r'TRIFLUOROETHANOL')

    str = self.re_substitute(str, r'1,3-DIBROMPROPANE', r'1,3-DIBROMOPROPANE')
#    TSP substitutions starting on 20040326
    str = self.re_substitute(str, r'^SOLIUM\s*-?\s*ACETATE', r'SODIUM ACETATE')
    str = self.re_substitute(str, r'^SODIUM CITR$', r'SODIUM CITRATE')
    str = self.re_substitute(str, r'^SODIUM CITRAT$', r'SODIUM CITRATE')
    str = self.re_substitute(str, r'^SODIUM\-CITRATE', r'SODIUM CITRATE')
    str = self.re_substitute(str, r'^SODIUM CITRATE/[ ]*CITRIC ACID', r'SODIUM CITRATE')
    str = self.re_substitute(str, r'^T(RI)?\s*-?\s*SODIUM CITRATE?', r'TRISODIUM CITRATE')
    str = self.re_substitute(str, r'^SOO?DIUM CITRATE?', r'SODIUM CITRATE')
    str = self.re_substitute(str, r'^SODIUM CITRATE/? *CITRATE', r'SODIUM CITRATE')
    str = self.re_substitute(str, r'^SODIUM CITRATE *\)+', r'SODIUM CITRATE')
    str = self.re_substitute(str, r'^CITRATE SODIUM', r'SODIUM CITRATE')
    str = self.re_substitute(str, r'^TRIETHANOLAMINE[-/]HCL', r'TRIETHANOLAMINE')
    str = self.re_substitute(str, r'^SODIUM NITRTATE', r'SODIUM NITRATE')
    str = self.re_substitute(str, r'SODIUM NITRITE \(NO2', r'SODIUM NITRITE')
    str = self.re_substitute(str, r'CACO(L|C)YDATE', r'CACODYLATE')
    str = self.re_substitute(str, r'CACODILATE', r'CACODYLATE')
    str = self.re_substitute(str, r'CACODYLA$', r'CACODYLATE')
    str = self.re_substitute(str, r'CADOD?YLATE', r'CACODYLATE')
    str = self.re_substitute(str, r'CAODYLATE', r'CACODYLATE')
    str = self.re_substitute(str, r'CACODYLATE/HCL', r'CACODYLATE')
    str = self.re_substitute(str, r'NA(-| )?CACODYLATE', r'SODIUM CACODYLATE')
    str = self.re_substitute(str, r'CACODOYLATE', r'CACODYLATE')
    str = self.re_substitute(str, r'CACADYLATE', r'CACODYLATE')
    str = self.re_substitute(str, r'(CACODYLATIC|CACODYLIC|CACODYLATE)\s*ACID', r'CACODYLATE')
    str = self.re_substitute(str, r'(CACODYLIC ACID|CACODYLATE)/NAOH', r'SODIUM CACODYLATE')

    str = self.re_substitute(str, r'^PIPERAZINE[-/ ]HCL', r'PIPERAZINE')
    str = self.re_substitute(str, r'^NAMES$', r'SODIUM MES')
    str = self.re_substitute(str, r'MES/SODIUM', r'SODIUM MES')
    str = self.re_substitute(str, r'^HEPP\b', r'HEPPS')
    str = self.re_substitute(str, r'^TEA\b', r'TRIETHANOLAMINE')
    str = self.re_substitute(str, r'^NAPIPES', r'PIPES')
    str = self.re_substitute(str, r'^MOPSO-NA[+]?', r'MOPSO')
    str = self.re_substitute(str, r'^TRICIN$', r'TRICINE')
    str = self.re_substitute(str, r'\bNA2?\(?SUCC(INATE)?', r'SODIUM SUCCINATE')
    
    str = self.re_substitute(str, r'^SUCCINIC ACID', r'SUCCINATE')
    str = self.re_substitute(str, r'\bORTHOBORIC ACID', r'BORATE')
    str = self.re_substitute(str, r'\bBORIC ACID', r'BORATE')
    str = self.re_substitute(str, r'\bNA2B4O7', r'SODIUM BORATE')
    str = self.re_substitute(str, r'\bASCORMBATE', r'ASCORBATE')
    str = self.re_substitute(str, r'\bNA-?\s*ASCORBATE', r'SODIUM ASCORBATE')
    str = self.re_substitute(str, r'^NA(SCN|THIOCYANATE)', r'SODIUM THIOCYANATE')
    str = self.re_substitute(str, r'^KSCN\b', r'POTASSIUM THIOCYANATE')
    str = self.re_substitute(str, r'^K\s*THIOCYANATE', r'POTASSIUM THIOCYANATE')
    str = self.re_substitute(str, r'^KCNS\b', r'POTASSIUM THIOCYANATE')
    str = self.re_substitute(str, r'POTASSIUM THIOC[YI]N?(AN)?ATE', r'POTASSIUM THIOCYANATE')
    str = self.re_substitute(str, r'^KSECN\b', r'POTASSIUM SELENOCYANATE')
    str = self.re_substitute(str, r'^KCN\b', r'POTASSIUM CYANIDE')
    str = self.re_substitute(str, r'\bHNO3\b', r'NITRATE')

    str = self.re_substitute(str, r'^KMES', r'POTASSIUM MES')
    str = self.re_substitute(str, r'^KMOPS', r'POTASSIUM MOPS')
    str = self.re_substitute(str, r'^MES~', r'MES')
    str = self.re_substitute(str, r'2\-MES', r'MES')
    str = self.re_substitute(str, r'^MES SODIUM', r'SODIUM MES')
    str = self.re_substitute(str, r'\(MES\s+(OR|OF)?\s*MOPS\)', r'MES')
    str = self.re_substitute(str, r'^MES[-/.]\s*NA(OH)?', r'SODIUM MES')
    str = self.re_substitute(str, r'^MES[-/.]\s*SODIUM\s*HYDROXIDE', r'SODIUM MES')
    str = self.re_substitute(str, r'^MES[-/.]\s*K(OH)?', r'POTASSIUM MES')
    str = self.re_substitute(str, r'^MES[-/.]?\s*HCL', r'MES')
    str = self.re_substitute(str, r'2-\(N-\s*MORPHOLINO\)( |\-)?ETHANE ?SULFONIC ACID', r'MES')
    str = self.re_substitute(str, r'2-\[N-\s*MORPHOLINO\]ETHANE-?SULFONIC ACID', r'MES')
    str = self.re_substitute(str, r'2-N-\s*MORPHOLINO-?\s*ETHANESULFONIC ACID', r'MES')
    str = self.re_substitute(str, r'(2-\s*)?MORPHOLIN(E|O)-?\s*ETHANE?SULFONIC ACID', r'MES')
    str = self.re_substitute(str, r'MORPHOLIN(E|O)\s*ETHANE?SULFONATE', r'MES')
    str = self.re_substitute(str, r'-?2\(N-MORPHOLINO-\)\s*ETHANE?SULFONATE', r' MES')
    str = self.re_substitute(str, r'MORPHOLIN(E|O)-?\s*SULFONIC ACID', r'MES')
    str = self.re_substitute(str, r'\bMES[-/]\s*ACETATE', r'MES ACETATE')
    str = self.re_substitute(str, r'\bMES\s+\(?\s*MES\b', r'MES')
    str = self.re_substitute(str, r'\b3\-MOPS\b', r'MOPS')
    str = self.re_substitute(str, r'3-\s*\(N-\s*MORPHOLINO\)-PROPANESULFONIC ACID', r'MOPS')
    str = self.re_substitute(str, r'3-\s*\(N-\s*MORPHOLINO\)-PROPANESULFONIC ?(AC)?', r'MOPS')
    str = self.re_substitute(str, r'N-\s*MORPHOLINO\s*-?PROPANESULFONIC ACID', r'MOPS')
    str = self.re_substitute(str, r'^2-\s*\(CYCLOHEXYLAMINO\)ETHANESULFONIC ACID \(CHES\)', r'CHES')
    str = self.re_substitute(str, r'CHES \(2\-\(N\-CYCLOHEXYLAMINO\) ETHANE SULFONIC ACID', r'CHES')
    str = self.re_substitute(str, r'^CHESS\b', r'CHES')
    str = self.re_substitute(str, r'^BES-?\s*NAOH', r'SODIUM BES')
    str = self.re_substitute(str, r'^BICINE-?\s*NAOH', r'SODIUM BICINE')
    str = self.re_substitute(str, r'^TAPS\/\s*KOH', r'POTASSIUM TAPS')
    str = self.re_substitute(str, r'^NABICINE', r'SODIUM BICINE')
    str = self.re_substitute(str, r'^BICIN$', r'BICINE')
    str = self.re_substitute(str, r'^IMM?ADAZOLE', r'IMIDAZOLE')
    str = self.re_substitute(str, r'IM+ID[AI]ZOLE?', r'IMIDAZOLE')
    str = self.re_substitute(str, r'IMIDA[ZS]OLE?[-/]HCL', r'IMIDAZOLE')
    str = self.re_substitute(str, r'IMIDAZOLE[-/]\s*MALEATE', r'IMIDAZOLE MALEATE')
    str = self.re_substitute(str, r'^IM-MAT\b', r'IMIDAZOLE MALATE')
    str = self.re_substitute(str, r'\bIMIDAZOLE[-/]\s*(MALIC ACID|MALATE)', r'IMIDAZOLE MALATE')
    str = self.re_substitute(str, r'\bMALATE[-/]IMIDAZOLE', r'IMIDAZOLE MALATE')
    str = self.re_substitute(str, r'IMIDAZOLE-\s*ACETATE', r'IMIDAZOLE ACETATE')
    str = self.re_substitute(str, r'N\-\[2-ACETAMIDO\]-2-\s*IMINODIACETIC ACID', r'ADA')
    str = self.re_substitute(str, r'N\-\s*\(2\-?ACETAMIDO?E?\)\s*IMINODIACETIC ACID( \(ADA\))?', r'ADA')
    str = self.re_substitute(str, r'BENZAMIDINE CHLORIDE', r'BENZAMIDINE HYDROCHLORIDE')
    str = self.re_substitute(str, r'\bAMMONIA\b', r'AMMONIUM')
    str = self.re_substitute(str, r'MONODISPERSE', r'')
    str = self.re_substitute(str, r'FLOU?RIDE', r'FLUORIDE')
    str = self.re_substitute(str, r'^TETRAETHYL AMMONIUM CHLORIDE \(E4NCL\)', r'TETRAETHYLAMMONIUM CHLORIDE')
    str = self.re_substitute(str, r'^NET4CL', r'TETRAETHYLAMMONIUM CHLORIDE')
    str = self.re_substitute(str, r'TRI(S )?\(2\s*\-\s*CARBOXYETHYL\)\s*PHOSPHINE \(TCEP',r'TRIS CARBOXYETHYL PHOSPHINE')
    str = self.re_substitute(str, r'^TCEP \(TRIS CARBOXYETHYL PHOSPHINE\)', r'TRIS CARBOXYETHYL PHOSPHINE')
    str = self.re_substitute(str, r'^TRIS 2?-?\(?CARBOXYETHYL\)?-?\s*PHOSPHINE', r'TRIS CARBOXYETHYL PHOSPHINE')
    str = self.re_substitute(str, r'^TRIS\(2-CARBOXY-ETHYL\)PHOSPHINE-HCL', r'TRIS CARBOXYETHYL PHOSPHINE')
    str = self.re_substitute(str, r'^SPERMINE\s*TETRAHYDROCH?LORIDE', r'SPERMINE')
    str = self.re_substitute(str, r'^SPERI?MINE\s*TETRA(\-HC(L|I)|CH?LORIDE)', r'SPERMINE')
    str = self.re_substitute(str, r'^SPERMINE?[-.,]?\s*(4?HCL)?', r'SPERMINE')
    str = self.re_substitute(str, r'PHENYL\s*METHYLSULFONYL(-| )FLUORIDE', r'PMSF')
    str = self.re_substitute(str, r'PHENYLMETHANESULFONYL-FLUORIDE', r'PMSF')
    
    # MPD
    for regexp in MPD_REGEXP_LIST:
      str = self.re_substitute(str, regexp, 'MPD')  

    
    str = self.re_substitute(str, r'1[.,]\s*6\s*-?,?HE?A?XA?NE?\s*DIOLE?', r'1,6 HEXANEDIOL')
    str = self.re_substitute(str, r'HEAXANE-1,2-DIOL', r'1,2 HEXANEDIOL')
    str = self.re_substitute(str, r'HEXANIDIOL', r'HEXANEDIOL')
    str = self.re_substitute(str, r'G[RL][YI]E?CER?OL?E?\)?\s*(WAS|AS)?\s*A?\s*(CRYO)?\s*-?\s*(PROTECTANT)?', r'GLYCEROL')
    str = self.re_substitute(str, r'GLYERC?OL(\s+ANHYD?ROUS)?', r'GLYCEROL')
    str = self.re_substitute(str, r'^GLUTATHION$', r'GLUTATHIONE')
    str = self.re_substitute(str, r'\bGLUTATHIONE-SULFONIC ACID', r'GLUTATHIONE SULFONIC ACID')
    str = self.re_substitute(str, r'\bGSH\b', r'GLUTATHIONE')
    str = self.re_substitute(str, r'^\-GLUTATHIONE', r'GLUTATHIONE')
    str = self.re_substitute(str, r'\bS-HEXYL\s*GLUTATHIONE', r'S-HEXYLGLUTATHIONE')
    str = self.re_substitute(str, r'^GUAD-HCL \(LIGAND\)', r'GUANIDINE HYDROCHLORIDE')
    str = self.re_substitute(str, r'^GUANIDINE(-| )?(HCL|HYDROCHLORIDE)', r'GUANIDINE HYDROCHLORIDE')
    str = self.re_substitute(str, r'^GUANIDINIUM (HYDRO)?CHLORIDE', r'GUANIDINE HYDROCHLORIDE')
    str = self.re_substitute(str, r'^\(?GLCNAC\)?\d?', r'N-ACETYL GLUCOSAMINE')
    str = self.re_substitute(str, r'^N-\s*ACETYL-GLUCOSAMINE-6-?PHOSPHATE', r'N-ACETYL GLUCOSAMINE-6-PHOSPHATE')
    str = self.re_substitute(str, r'\bISOTHIOCYANATE\b', r'THIOCYANATE')
    str = self.re_substitute(str, r'\bG6P\b', r'GLUCOSE 6 PHOSPHATE')
    str = self.re_substitute(str, r'\bGLUCOSE-?\s*6-?\s*PHOSPHATE\b', r'GLUCOSE 6 PHOSPHATE')
    str = self.re_substitute(str, r'\bB-D-GLUCOSE6PHOSPHATE\b', r'B-D-GLUCOSE 6 PHOSPHATE')
    str = self.re_substitute(str, r'\bD(\(\+\))?\s+GLUCOSE\b', r'D-GLUCOSE')
    str = self.re_substitute(str, r'D\-\-GLUCOSE', r'D-GLUCOSE')
    str = self.re_substitute(str, r'D\-\-TREHALOSE', r'TREHALOSE')
    str = self.re_substitute(str, r'D\-\-GALACTOSE', r'GALACTOSE')
    str = self.re_substitute(str, r'\(?D?\)?\-?\s*SUCROE?SE?\b', r'SUCROSE')
    str = self.re_substitute(str, r'\bDMF\b', r'DIMETHYLFORMAMIDE')
    str = self.re_substitute(str, r'\bDIMETHYL\s+FORMAMIDE\b', r'DIMETHYLFORMAMIDE')
    str = self.re_substitute(str, r'\bTFE\b', r'TRIFLUOROETHANOL')
    str = self.re_substitute(str, r'FLOURO', r'FLUORO')
    str = self.re_substitute(str, r'\b5F-LA\b', r'5-FLUOROLEVULINIC ACID')

    str = self.re_substitute(str, r'CH?L?R?ORIDE', r'CHLORIDE')
    str = self.re_substitute(str, r'CHL?R?OLIDE', r'CHLORIDE')
    str = self.re_substitute(str, r'CL?HOL?O?RIDE', r'CHLORIDE')
    str = self.re_substitute(str, r'CL2(?!\w)', r' CHLORIDE')
    str = self.re_substitute(str, r'CL\(2\)', r' CHLORIDE')

    str = self.re_substitute(str, r'D(I|E)OXI?ANI?E?$', r'DIOXANE')
    str = self.re_substitute(str, r'DOIXANE', r'DIOXANE')
    str = self.re_substitute(str, r'1,?\s*4\s*-?\s*DIOXANE', r'DIOXANE')
    str = self.re_substitute(str, r'MPD IN (THE|DROP|DEPOSIT|WATER) .*', r'MPD')
    str = self.re_substitute(str, r'^SODIUM ACETATE, POTASSIUM PHOSPHATE', r'SODIUM ACETATE POTASSIUM PHOSPHATE')
    str = self.re_substitute(str, r'\(DL-DITHIOTHREITOL\)', r'')
    str = self.re_substitute(str, r'\bDITHIO?THREITOL\b', r'DTT')
    str = self.re_substitute(str, r'DITHIOERYTHRITOL\(DTE\)', r'DITHIOERYTHRITOL')
    str = self.re_substitute(str, r'\bDITHIOERYTHREITOL\b', r'DITHIOERYTHRITOL')
    str = self.re_substitute(str, r'\bDTE\b', r'DITHIOERYTHRITOL')
    str = self.re_substitute(str, r'\b(B|BETA|2)-MERCAPT?OT?ETHAN[OA]LE?\b', r'BETA-MERCAPTOETHANOL')
    str = self.re_substitute(str, r'\b(B|BETA|2)-?\s*MERCAPTO[- ]?ETHAN[OA]L\b', r'BETA-MERCAPTOETHANOL')
    str = self.re_substitute(str, r'^2?-?MERCAPTO-?ETH[AO]N[OA]L\b', r'BETA-MERCAPTOETHANOL')
    str = self.re_substitute(str, r'\bLAURYLDIMETHYLAMINE-N-OXIDE\b', r'LDAO')
    str = self.re_substitute(str, r'N,N\-DIMETHYLDECYLAMINE\-N\-OXIDE \(DDAO\)', r'DDAO')
    str = self.re_substitute(str, r'N,N\-DIMETHYLUNDECYLAMIN\-N\-\s*OXIDE \(C11DAO\)', r'UDAO')
    str = self.re_substitute(str, r'\bGLYCINE[-/]NAOH', r'GLYCINE')
    str = self.re_substitute(str, r'SODIUM EDTA', r'EDTA')
    str = self.re_substitute(str, r'SODIUM EGTA', r'EGTA')
    str = self.re_substitute(str, r'\bDIMETHYL\s*SULFOXIDE\b', r'DMSO')
    str = self.re_substitute(str, r'\bDMSO\s*\(DMSO\)', r'DMSO')
    str = self.re_substitute(str, r'\bACETOACETYL-COA', r'ACETOACETYL COENZYME A')
    str = self.re_substitute(str, r'\bACETYL-?COA$', r'ACETYL COENZYME A')
    str = self.re_substitute(str, r'\bACCOA$', r'ACETYL COENZYME A')
    str = self.re_substitute(str, r'\bCOA$', r'COENZYME A')
    str = self.re_substitute(str, r'\bCOENZYMEA\b', r'COENZYME A')
    str = self.re_substitute(str, r'POTASSIUM/\s*SODIUM TARTRATE\b', 'POTASSIUM SODIUM TARTRATE')
    str = self.re_substitute(str, r'\bGSG4', r'4-DEOXY-4-THIO-ALPHA-D-GLUCOPYANOSE') #1qm5
    str = self.re_substitute(str, r'PRODUCT INHIBITOR \(GPS\)', r'GUANOSINE MONOPHOSPHATE') #1b4p
    str = self.re_substitute(str, r'\bGPS', r'GUANOSINE MONOPHOSPHATE') #3bir
    str = self.re_substitute(str, r'\b2?\'?`?GMP', r'GUANOSINE MONOPHOSPHATE') #3bir+
    str = self.re_substitute(str, r'\bFBP\b', r'FRUCTOSE 1,6-DIPHOSPHATE') #1a5z 
    str = self.re_substitute(str, r'FRUCTOSE 1,6-[DB]IS? ?PHOSPHATE', r'FRUCTOSE 1,6-DIPHOSPHATE')
    str = self.re_substitute(str, r'\bF6P\b', r'FRUCTOSE 6-PHOSPHATE') #1d9q+
    str = self.re_substitute(str, r'\bFRUCTOSE\s*-?\s*6P\b', r'FRUCTOSE 6-PHOSPHATE')
    str = self.re_substitute(str, r'FRUCTOSE-6-PHOSPHATE\b', r'FRUCTOSE 6-PHOSPHATE')
    str = self.re_substitute(str, r'\bBH2\b', r'DIHYDROBIOPTERIN') #1lrm
    str = self.re_substitute(str, r'\bBH4\b', r'TETRAHYDROBIOPTERIN') #1kw0,1mmk,1mmt
    str = self.re_substitute(str, r'\b5FU\b', r'5-FLUOROURACIL') #1h7x
    str = self.re_substitute(str, r'\b4CABP\b', r'2-CARBOXYARABINITOL-1,5-DIPHOSPHATE') #1rbo
    str = self.re_substitute(str, r'\bTHDP\b', r'THIAMINE DIPHOSPHATE') #1qpb
    str = self.re_substitute(str, r'\bTDP\b', r'THYMIDINE DIPHOSPHATE') #2ft0 note- there may be a problem here...
    str = self.re_substitute(str, r'\bTMP\b', r'THIAMINE MONOPHOSPHATE') #2hom
    str = self.re_substitute(str, r'\bTHIAMINE PHOSPHATE\b', r'THIAMINE MONOPHOSPHATE')
    str = self.re_substitute(str, r'\bTPP\b', r'THIAMINE PYROPHOSPHATE') #2hoj, 2hok, 2hol
    str = self.re_substitute(str, r'\bTHIAMIN\b', r'THIAMINE') #2gli
    str = self.re_substitute(str, r'\bOSB\b', r'2-SUCCINYLBENZOATE') #1fhv
    str = self.re_substitute(str, r'\bOTGP\b', r'1-S-OCTYL-BETA-D-THIOGLUCOPYRANOSIDE') #2lyn
    str = self.re_substitute(str, r'\bOSG\b', r'S-OCTYL-BETA-D-THIOGLUCOSIDE') #2fz6
    str = self.re_substitute(str, r'\bLIS\b', r'(2S,4S)-2-AMINO-4,5-EPOXIPENTANOIC ACID 3-OXIRAN-2YLALANINE') #1o90,1o93
    str = self.re_substitute(str, r'\bLCISAMB\b', r'L-2-AMINO-4-METHOXY-CIS-BUT-3-ENOIC ACID') #1o92
    str = self.re_substitute(str, r'\bNOG\b', r'N-OXALYOLGLYCINE') #1h2k,m
    str = self.re_substitute(str, r'\b2-CABP\b', r'2-CARBOXYARABINITOL-1,5-DIPHOSPHATE') #1gk8
    str = self.re_substitute(str, r'\bA-ME-\s*MAN\b', r'ALPHA-O-METHYL-MANNOSIDE') #1egi
    str = self.re_substitute(str, r'\b3PGA?\b', r'3-PHOSPHOGLYCERATE') #1upp
    str = self.re_substitute(str, r'\bCPRPP\b', r'CARBOCYCLIC PHOSPHORIBOSYLPYROPHOSPHATE') #1ecc
    str = self.re_substitute(str, r'\bCTMC\b', r'CETYL TRIMETHYLAMMONIUM CHLORIDE') #1p33
    str = self.re_substitute(str, r'\b(CTAB|CETYL\s*AMMONIUM\s*BROMIDE|HEXADECYL\s*TRIMETHYL\s*AMMONIUM\s*BROMIDE)\b', r'CETYL TRIMETHYLAMMONIUM BROMIDE')
    str = self.re_substitute(str, r'\bCETYL\-?\s*TRIMETH?YLAMMONIUM BROMIDE', r'CETYL TRIMETHYLAMMONIUM BROMIDE')
    str = self.re_substitute(str, r'\bAKG\b', r'2-OXYGLUTARIC ACID') #1h2l
    str = self.re_substitute(str, r'\bNAAD\b', r'NICOTINIC ACID ADENINE DINUCLEOTIDE') #1kqp
    str = self.re_substitute(str, r'\bALF4\b', r'TETRAFLUOROALUMINATE') #1rk2
    str = self.re_substitute(str, r'\bAP6A\b', r'DIADENOSINE HEXAPHOSPHATE') #1vc8,9 from paper
    str = self.re_substitute(str, r'\bQSI\b', r'5-O-[N-(L-GLUTAMINYL)-SULFAMOYL]ADENOSINE') #1qtq
    str = self.re_substitute(str, r'OXONIC ACID POTASSIUM SALT',r'POTASSIUM OXONATE')
    str = self.re_substitute(str, r'DIHYDROOROTATE \(DHO\)', r'4,5-DIHYDROOROTIC ACID')
    str = self.re_substitute(str, r'\bDHO\b', r'4,5-DIHYDROOROTIC ACID')

    if self.verbose>0:
      print "convert_name:8",repr(str)    
    
    str = self.re_substitute(str, r'\bFLURBIPORFEN\)', r'FLURBIPORFEN')
    str = self.re_substitute(str, r'\bDIHEPTANOYL- PHOSPHATEIDYLCHOLINE\b', r'1,2-DIHEPTANOYL-SN-GLYCER-3-PHOSPHOCHOLINE')
    str = self.re_substitute(str, r'(2\-)?HYDROXYETHYL\s+DISULFIDE', r'2-HYDROXYETHYLDISULFIDE')
    str = self.re_substitute(str, r'\bBEZENE SULFORNIC ACID', r'BEZENE SULFONIC ACID')  #1fk6
    str = self.re_substitute(str, r'\bPYRIDOXAL-5\'?', r"PYRIDOXAL 5'")
    str = self.re_substitute(str, r"\bPYRIDOZ?XAL\s*5?'?[- ]PHOSPHATE\b", r"PYRIDOXAL 5'-PHOSPHATE")
    str = self.re_substitute(str, r'1,2,\s*3,?-HEPTANETRIOL', r'1,2,3-HEPTANETRIOL') #2or7
    str = self.re_substitute(str, r'\bHEPTANE-1,2,3-TRIOL', r'1,2,3-HEPTANETRIOL')
    str = self.re_substitute(str, r'HEPTANE-?\s*TRIOLE?', r'HEPTANETRIOL')
    str = self.re_substitute(str, r'\bGHRPAM\)', r'GHRP-AMIDE')
    str = self.re_substitute(str, r'\b8-\s*AZAXANTHIN\b\)?', r'8-AZAXANTHINE')
    str = self.re_substitute(str, r'\bMANOHEPTOSE', r'MANNOHEPTOSE')
    str = self.re_substitute(str, r'\b2-DEOXY-2-AMINO D-\s*GLUCITOL 6-PHOSPHATE', r'2-AMINO-2-DEOXY GLUCITOL-6-PHOSPHATE')
    str = self.re_substitute(str, r'\b2-AMINO-2-DEOXY GLUCITOL-6P\b', r'2-AMINO-2-DEOXY GLUCITOL-6-PHOSPHATE')
    str = self.re_substitute(str, r'\bD/L-ORNITHINE', r'ORNITHINE')
    str = self.re_substitute(str, r'\bN-DECYLPENTAOXYETHYLENE\s+\(C10E5\)', r'N-DECYLPENTAOXYETHYLENE')

    str = self.re_substitute(str, r'\bMIXED [0-9]:[0-9]', r'')
    str = self.re_substitute(str, r'SURROGATE', r'')
    str = self.re_substitute(str, r'VIRUS', r'')
    str = self.re_substitute(str, r'DIFFUSED', r'')
    str = self.re_substitute(str, r'(\bTITRATED|\bCONTAINING|\bINCLUDING|\bADJUSTED|\bGRADIENT|\bMIX(ED|TURE)?)+', r'')
    str = self.re_substitute(str, r'(\bSATURATED?|\bCONCENTRATION|\bOIL\-? ?BATCH,?\b|\bUNDER OIL\b|\bDIALY[SZ]ED)+', r'')
    str = self.re_substitute(str, r'(\bPRESENT\b|\bBOTH|\bMADE|\bSAME|\bONLY|\bUSED|\bEND\b|\bIN\b)+', r'')
    str = self.re_substitute(str, r'\bTHE(SE|N)?\b', r'')
    str = self.re_substitute(str, r'(\bSALT\b|\bADDED|\bFINAL\b|\bINCUBATED|\bMETHOD\b|\bROOM)+', r'')
    str = self.re_substitute(str, r'(\bCRYSTAL\b|\bLIGAND)+', r'')
    str = self.re_substitute(str, r'\bTEMPERATURE:?', r'')
    str = self.re_substitute(str, r'\bSYSTEM II',r'')


    str = self.re_substitute(str, r'PEPTIDE:PROTEIN', r'')
    str = self.re_substitute(str, r'\bCONC\.?\b', r'')

    str = self.re_substitute(str, r'\d*\s+MLS?\b', r'')

    str = self.re_substitute(str, r'\bTARTR?\b', r'TARTRATE')
    str = self.re_substitute(str, r'\bTAR?T(A|E)?R?ATE\b', r'TARTRATE')
    str = self.re_substitute(str, r'\bT(A|E)RTA?RATE\b', r'TARTRATE')
# Note: tartrate is a contraction of tartarate... http://www.chem.qmul.ac.uk/iupac/ions/RC831.html
    str = self.re_substitute(str, r'POTASSIUM SODIUM TARTRATE', r'SODIUM POTASSIUM TARTRATE')
    str = self.re_substitute(str, r'\bMGTARTRATE', r'MAGNESIUM TARTRATE')
    str = self.re_substitute(str, r'SODIUM SODIUM', r'SODIUM')
    str = self.re_substitute(str, r'\bNA,? *TARTRATE', r'SODIUM TARTRATE')
    str = self.re_substitute(str, r'\bLISOLEUCINE', r'L-ISOLEUCINE')
    str = self.re_substitute(str, r'\bL\-LEUCINE', r'L-ISOLEUCINE')
    str = self.re_substitute(str, r'\bL\-SER\b', r'L-SERINE')
    str = self.re_substitute(str, r'\bL\-TRP\b', r'L-TRYPTOPHAN')
    str = self.re_substitute(str, r'\bL\-PRO\b', r'L-PROLINE')
    str = self.re_substitute(str, r'\bL\-HIS\b', r'L-HISTIDINE')
    str = self.re_substitute(str, r'\bL\-PHE\b', r'L-PHENYLALANINE')
    str = self.re_substitute(str, r'\bL\-ALA\b', r'L-ALANINE')
    str = self.re_substitute(str, r'\bL\-ALLO\-THR\b', r'L-ALLO-THREONINE')
    str = self.re_substitute(str, r'\bMES(-|/)TRIS', r'TRIS MES')
    str = self.re_substitute(str, r'\(MES\)', r'')
    str = self.re_substitute(str, r'\(DTT\)', r'')
    str = self.re_substitute(str, r'\- ', r'-')
    str = self.re_substitute(str, r' \-', r'-')

    if self.verbose>0:
      print "convert_name:9",repr(str)

    str = self.re_substitute(str, r'([0-9]+)\s*,\s*([0-9]+)\s*([A-Z])', r'\1,\2-\3')

    # cleanup PEG smears, ignoring chain length info
    str = self.re_substitute(str, r'(HIGH|H|L|M|MID|BROAD)?\s*(MW)?\s*PEG\s+SMEARS?\s*(MEDIUM|HIGH)?', r'SMEAR')
    str = self.re_substitute(str, r'(H|L|B|M)MW PGSM', r'SMEAR')
    
    # Cleanup PEGs
    str = self.re_substitute(str, r'PEG[-_I]', r'PEG ')
    str = self.re_substitute(str, r'/ PEG', r'PEG')
    str = self.re_substitute(str, r'\.PEG', r'PEG')
    str = self.re_substitute(str, r'([0-9]+)\s*\%PEG', r'\1 % PEG')
    str = self.re_substitute(str, r'\b(\d+)K\-PEG\b', r'PEG \1K') #2fr8
    str = self.re_substitute(str, r'\b(\d+)\-PEG\b', r'PEG \1')
    str = self.re_substitute(str, r'PEG (\d+), +(\d{3})', r'PEG \1\2') 
    str = self.re_substitute(str, r'GLYCOLE$', r'GLYCOL')
    str = self.re_substitute(str, r'\bPEG\s*(\d+)DA', r'PEG \1')
    str = self.re_substitute(str, r'PEG \[([0-9]+ ?[0-9]*)\]',r'PEG \1')
    str = self.re_substitute(str, r'EHT(LY|YL)ENE', r'ETHYLENE')
    str = self.re_substitute(str, r'MONOMETHYL\s*ETHER\s+\(MME\)', r'MME')
    str = self.re_substitute(str, r'MONOMETHYL\s*ETHERS?\s*\(P(EG)?\s*MME\)',r'MME')
    str = self.re_substitute(str, r'(PEG)?\s*MONO\s*-?\s*METHYL\s*-?\s*ETHER\s*\((PEG)?\s*MME\)', r'PEG MME')
    str = self.re_substitute(str, r'POLYETHYLENE\s*GLYCOL\s*(MONO)?METHYL\s*ETHER', r'PEG MME')
    str = self.re_substitute(str, r'POLYETH[YE]LENE\s*(GLYCOL)?\s*(MME|MONOMETHYL\s*ETHER)', r'PEG MME')
    str = self.re_substitute(str, r'PEG\s+([0-9]+),?\s*(MONO)?METHYL\s*ETHER\s*\(?(MME)?', r'PEG MME \1')
    str = self.re_substitute(str, r'POLYL?\(?ETHYLENE\)?\s*GLYCOL?E?(-)?', r'PEG ')
    str = self.re_substitute(str, r'POLYETHELYENEGLYCOL-',r'PEG ')
    str = self.re_substitute(str, r'PL?OLY-?\s*ETHY?LENE?\s*GLYCOL', r'PEG')
    str = self.re_substitute(str, r'POLYETHYLGLYCOL', r'PEG')
    str = self.re_substitute(str, r'MOMOM?ETHYL', r'MONOMETHYL')
    str = self.re_substitute(str, r'MONO\s*-?\s*METHYL\s*ESTER', r'MME')
    str = self.re_substitute(str, r'MONO?\s*-?\s*METHYL\s*-?ETHER\s*\(MME\)', r'MME')
    str = self.re_substitute(str, r'MONO?\s*-?\s*METHYL\s*-?ETH(ER|YL)', r'MME') # japanese L? 2gxg
    str = self.re_substitute(str, r'PEG\s+MONOMETHYL', r'PEG MME')
    str = self.re_substitute(str, r'PEG\s+METHYL\s+ETHER', r'PEG MME')
    str = self.re_substitute(str, r'POLYETHYLENE MME', r'PEG MME')
    str = self.re_substitute(str, r'MONO\s*METHYL-?\s*PEG', r'PEG MME')
    str = self.re_substitute(str, r'POLY\s*\(ETHYLENE GLYCOL\)', r'PEG')
    str = self.re_substitute(str, r'\bMETHYL\s*ETH(YL|ER)\s+PEG', r'PEG MME')
    str = self.re_substitute(str, r'MME\s*-?\s*PEG-?', r'PEG MME')
    str = self.re_substitute(str, r'POLYETHYLENE\s*GLYCEROL', r'PEG')
    
    if self.re_search(str, r'PEG'):
      str = self.re_substitute(str, r'( |\()MR ', r' ')
      str = self.re_substitute(str, r'\(', r'')
      str = self.re_substitute(str, r'\)', r'')
      str = self.re_substitute(str, r'MW', r'')
      str = self.re_substitute(str, r'MEAN', r'')

    str = self.re_substitute(str, r'PEGMME', r'PEG MME')
    str = self.re_substitute(str, r'PEGME', r'PEG MME')
    str = self.re_substitute(str, r'PEGM+ ', r'PEG MME')
    str = self.re_substitute(str, r'ME?-?PEG', r'PEG MME')
    str = self.re_substitute(str, r'4K-?\s*PEG', r'PEG 4000')
    str = self.re_substitute(str, r'-MME', r' MME')
    str = self.re_substitute(str, r'MMME', r' MME')
    str = self.re_substitute(str, r'PEG\s*ME ([0-9]*)', r'PEG MME \1')
    str = self.re_substitute(str, r'\(PEG\)', r'PEG')
    str = self.re_substitute(str, r'PEG\s*PEG', r'PEG')
    str = self.re_substitute(str, r'PEG\s+(4000|6000)K', r'PEG \1') #1dys
    str = self.re_substitute(str, r'PEG\s+4000\%', r'PEG 4000') #2fyc
    str = self.re_substitute(str, r'PEG([0-9]+)', r'PEG \1')
    str = self.re_substitute(str, r'^EG 4K', r'PEG 4000') #1bed
    str = self.re_substitute(str, r'\bETGLY,?\b', r'ETHYLENE GLYCOL')
    str = self.re_substitute(str, r'\bEG\b', r'ETHYLENE GLYCOL')
    str = self.re_substitute(str, r'\bEL?TH[YE]L?(EN)?E?-?\s*GLYCOL\b', r'ETHYLENE GLYCOL')

    if self.verbose>0:
      print "convert_name:10",repr(str)

    if self.re_match_groups(str, r'PEG([ME ]*)([0-9]+\.[0-9]+)K'):
      try:
        peg_len = int(float(self.matchgroups[2])*1000.0)
      except ValueError:
        pass
      else:
        str = self.re_substitute(str, r'PEG([ME ]*)([0-9]+\.[0-9]+)K', 'PEG '+self.matchgroups[1]+repr(peg_len))    
    
    # there has to be a better way to do this, but \300 is interpreted as the
    # 300th group, and doing r'\3' + '00' gets interpreted as unicode
    str = self.re_substitute(str, r'PEG([ME ]*)([0-9]+)K', r'PEG \1\2__X000X__')
    str = self.re_substitute(str, r'\bPEK ', r'PEG ')
    str = self.re_substitute(str, r'\bPEK([0-9]+)K', r'PEG \1__X000X__') 
    str = self.re_substitute(str, r'\bPEK([0-9]+)', r'PEG \1') 
    str = self.re_substitute(str, r'\bPEF([0-9]+)', r'PEG \1') 
    str = self.re_substitute(str, r'__X000X__', r'000')
    str = self.re_substitute(str, r'PEG\s+([0-9]+)\s*MM?E', r'PEG MME \1')

    str = self.re_substitute(str, r'PEG\s*MMES', r'PEG MME')
    str = self.re_substitute(str, r'PEG\s*MME([0-9])', r'PEG MME \1')
    str = self.re_substitute(str, r'PEG\s*MME-', r'PEG MME ')
    str = self.re_substitute(str, r'PEG 499', r'PEG 400')     #1bdf
    str = self.re_substitute(str, r'PEG 3340', r'PEG 3350')
    str = self.re_substitute(str, r'\bP8K\b', r'PEG 8000')
    str = self.re_substitute(str, r'PEG 3\.35K', r'PEG 3350')
    str = self.re_substitute(str, r'(PEG)?\s*P3350', r'PEG 3350') #1q0l,2gax,2hei,2fne 
    str = self.re_substitute(str, r'\bP4000', r'PEG 4000') 
    str = self.re_substitute(str, r'\bP8000', r'PEG 8000') 
    str = self.re_substitute(str, r'\bPEF3350\)?', r'PEG 3350') 
    str = self.re_substitute(str, r'\bPGE\-(\d+)', r'PEG \1') 
    str = self.re_substitute(str, r'\bPEG\s*10\s*000\b', r'PEG 10000') 
    str = self.re_substitute(str, r'\bME2KPEG', r'PEG MME 2000') 
    str = self.re_substitute(str, r'\bMETHOXY\s*PEG', r'PEG MME') 
    str = self.re_substitute(str, r'\bMEOPEG', r'PEG MME') 
    str = self.re_substitute(str, r'\bDIMETHYL(-| )PEG', r'PEG DME') 
    str = self.re_substitute(str, r'\bPEG(-| )500\s*DME\b', r'PEG DME 500') 
    str = self.re_substitute(str, r'\bP4K\b', r'PEG 4000') 
    str = self.re_substitute(str, r'\bPEG(V|L)\b', r'PEG') #1q98, 2bdz
    str = self.re_substitute(str, r'\bPEG\s*(\d+)\.(\d+)', r'PEG \1\2')
    str = self.re_substitute(str, r'\bPEG\s*(\d+)\/\d+', r'PEG \1')
    str = self.re_substitute(str, r'\bPEG\s*(\d+)\s+([^0]\d+)', r'PEG \1')

    str = self.re_substitute(str, r'^TEG\b', r'TRIETHYLENE GLYCOL')

    str = self.re_substitute(str, r'\bJEFF[A|(ER)]MINE\s*\-?(M|ED)?\-?600', r'JEFFAMINE 600')
    str = self.re_substitute(str, r'\bJEFF(AMINE)??\s*E?D?E?\s*\-?2001', r'JEFFAMINE ED-2001')
    str = self.re_substitute(str, r'ZWITTERGENT 314', r'ZWITTERGENT 3-14')

    # strip trailing +
    if self.re_search(str, r'PEG'):
      str = self.re_substitute(str, r'\s*\+\s*$', r'')

    str = self.re_substitute(str, r'POLYETHYLENE MME', r'PEG MME')
    str = self.re_substitute(str, r'\bPMME\s*([0-9]+)', r'PEG MME \1')
    str = self.re_substitute(str, r'\bETHL?Y?I?L?E?NE\s*_?GLYCOL\s*(AS)?\s*(CRYO)?', r'ETHYLENE GLYCOL')
    
    str = self.re_substitute(str, r'MM PEG 5000', r'PEG MME 5000')
    str = self.re_substitute(str, r'PEG\s+P(\d+)', r'PEG \1')
    str = self.re_substitute(str, r'\bPEG\s*(\d+)\s+PEG\s*(\d+)', r'PEG \1')

    str = self.re_substitute(str, r'POLYPROPROPYLENE', r'POLYPROPYLENE')
    str = self.re_substitute(str, r'PPG\s*P?400', r'POLYPROPYLENE GLYCOL 400')
    str = self.re_substitute(str, r'POLYPROPYLENE\s*-?\s*GLYCOL\s*P?400', r'POLYPROPYLENE GLYCOL 400')
    str = self.re_substitute(str, r'POLY\s*-?\s*ACR[YI]LIC\s*ACID\s*(\d+)\s*(SODIUM)?', r'POLYACRYLIC ACID \1')

    str = self.re_substitute(str, r'\s+', r' ')

    str = self.re_substitute(str, r' ON$', r'')
    str = self.re_substitute(str, r'\bAT\b', r'')
    str = self.re_substitute(str, r'\bTO\b', r'')
    str = self.re_substitute(str, r'(-| )H?O?AC$', r' ACETATE')
    if not self.re_search(str, r'\bCON\s+A'):
      str = self.re_substitute(str, r'\(?<!COENZYME\)?\s*A\b', r'')
      str = self.re_substitute(str, r',\s*A\s+', r'')

    str = self.re_substitute(str, r'^N?-?\s*OCTYL-?\s*B?(ETA)?-?D?-?\s*GLUCO(PYRANO)?SIDE', r'BETA-OCTYL-GLUCOPYRANOSIDE')
    str = self.re_substitute(str, r'^(1-N-)?B(ETA)?-?\s*OCTYL\s*(-D)?-?\s*GLUCO\s*(PYRANO)?SIDE', r'BETA-OCTYL-GLUCOPYRANOSIDE')
    str = self.re_substitute(str, r'^(BETA)?[BN]?-?\s*(OCTYL|OCTA)-?\s*GLUCO(PYRANO)?SIDE', r'BETA-OCTYL-GLUCOPYRANOSIDE')
    str = self.re_substitute(str, r'^BETA-D-\s*(OCTYL|OCTA)?GLUCOPYRANOSIDE', r'BETA-OCTYL-GLUCOPYRANOSIDE')
    str = self.re_substitute(str, r'^(OCTYL|OCTA)\.GLUCOPYRANOSIDE', r'BETA-OCTYL-GLUCOPYRANOSIDE')
    str = self.re_substitute(str, r'^B(ETA)?-?OG\b', r'BETA-OCTYL-GLUCOPYRANOSIDE')
    str = self.re_substitute(str, r'^TRITON\-X\b', r'TRITON X')
    str = self.re_substitute(str, r'TRITON[ \-]?X[\- ]?(\d+)', r'TRITON X\1')
    str = self.re_substitute(str, r'\bBETAIN\b', r'BETAINE')
    str = self.re_substitute(str, r'\bSULFOBETAIN\b', r'SULFOBETAINE')
    str = self.re_substitute(str, r'\bNG\b', r'N-NONYL-B-D-GLUCOSIDE')
    

    if self.verbose>0:
      print "convert_name:11",repr(str)    
    
# what to do with cofactors, like SAH (S-ADENOSYL-L-HOMOCYSTEINE), PLP, NAD, etc?
    str = self.re_substitute(str, r'^SAH\b', r'S-ADENOSYLHOMOCYSTEINE')
    str = self.re_substitute(str, r'^NICOTINAMIDE\s*ADENINE\s*DINUCLEOTIDE\b', r'NAD')

    str = self.re_substitute(str, r'^PHB$', r'P-HYDROXYBENZOATE')
    str = self.re_substitute(str, r'^P\-HYDROXYBENZOIC\s*ACID$', r'P-HYDROXYBENZOATE')
    str = self.re_substitute(str, r'^PGA$', r'2-PHOSPHOGLYCOLATE')
    str = self.re_substitute(str, r'^2\-PHOSPHOGLYCOLIC\s*ACID$', r'2-PHOSPHOGLYCOLATE')
    str = self.re_substitute(str, r'^DHQ$', r'DIHYDROQUERCETIN')
    str = self.re_substitute(str, r'\bS3P\b', r'SHIKIMATE-3-PHOSPHATE')
    str = self.re_substitute(str, r'SHIKIMATE\-3 PHOSPHATE',r'SHIKIMATE-3-PHOSPHATE')

    str = self.re_substitute(str, r'^UNDECYL(\-| )?MALTO(PYRANO)?SIDE', r'UNDECYLMALTOSIDE')
    str = self.re_substitute(str, r'^N\-DODECYL(\-| )B?(ETA)?\-(D\-)?MALTO(PYRANO)?SIDE', r'N-DODECYL-BETA-D-MALTOSIDE')
    str = self.re_substitute(str, r'^ADENOSINE TRIPHOSPHATE \(ATP\)', r'ATP')
    str = self.re_substitute(str, r'^CELLOHEXAOASE', r'CELLOHEXAOSE')
    str = self.re_substitute(str, r'\bP[LR]UCORONIC', r'PLURONIC')
    str = self.re_substitute(str, r'\bTASCIMATE\b', r'TACSIMATE')
    str = self.re_substitute(str, r'\bTACISMATE\b', r'TACSIMATE')
    str = self.re_substitute(str, r'\bTRIMETHYL? ?AMINE\s+(CHLORIDE|CL)\b', r'TRIMETHYLAMINE HYDROCHLORIDE')
    str = self.re_substitute(str, r'\bTRIMETHYL? ?AMINE((-| )N-OXIDE)\b', r'TMAO')
    str = self.re_substitute(str, r'TMAO\s+\(TMAO\)', r'TMAO')
    str = self.re_substitute(str, r'THIOFLAVIN T', r'THIOFLAVIN-T')
    
    str = self.re_substitute(str, r'-?PO4', r' PHOSPHATE')
    str = self.re_substitute(str, r'([^\d])[-_]PHOSPHATE', r'\1 PHOSPHATE')
    str = self.re_substitute(str, r'(CONDITION|RESER?VOIR|DETERGENT|REAGENT)', r'')
    

    str = self.re_substitute(str, r'COMPOUND\s+\d\s+\((\w+)\)', r'\1')
    str = self.re_substitute(str, r'COMPOUND\s+\d+\s+',r'')
    str = self.re_substitute(str, r'(SUBSTRATE|COMPOUND)', r'')
    

    str = self.re_substitute(str, r'\s+', r' ')

# Notes: ACOV is a substrate (#1hb1-4), as is ACV (#1bk0, 1blz), ACMC (#1qiq, 1qje-f) and ACVG (#1odm-n)- all modified peptides; 
# detergents- C8E4: n-octyltetraoxyethylene, C6DAO: n-hexyldimethylaminoxide, C12E9: nonaethylene glycol monododecyl ether (Hampton)
# detergents- CYMAL-X: cyclohexyl-X-beta-D-maltoside where X refers to 5,6,etc for pentyl, hexyl, etc.
# detergents- 3-(DECYL-METHYLAMMONIUM)PROPANE-1-SULFONATE is also known as ZWITTERGENT 3-10
# detergents- OSG: S-octyl-beta-D-thioglucoside (2fz6)
# XUBP is XDP is D-XYLULOSE-2,2-DIOL-1,5-BISPHOSPHATE (#1rco)
# AMPSO is a buffer
# SHCHC is 2-succinyl-6-hydroxy-2,4-cyclohexadiene-1-carboxylate
# PLURONIC is a difunctional block copolymer surfactant!
# problems but no papers: 2i6e (B-S-TRIS?), 2cu0, 2pw1, ??
# YC-17 is a macrolide (ringed lactone)
# PALO is N-phosphonacetyl-L-ornithine
    if self.re_search(str, r'^\(NH[42]\)\s*2\s*SO4$|^AMMONIUM\s*WS4$|^AM SO4$|^AMM\.SULFATE|^AMMONIUM SULFACE$|^AMMONIUM SUPLHATE$|^AMMONIUMSULFATE$|^AMMSO4$|^AMSO4$|^AS$|^AMS$|^A2S$|^AMM\.SUL$|^A\.S\.?$|^A/S$|^\(NH[42]\)\s*SULFATE$|^\s*AMMONIUM\s*\)?\s*SULFATE\s*$'):
      return 'AMMONIUM SULFATE'
    if self.verbose>0:
      print "convert_name:12",repr(str)
      
    # deal with different proteins...
    str = self.re_substitute(str, r'\bWT\-TTR\b', r'PROTEIN')
    str = self.re_substitute(str, r'4,5\-OAM', r'PROTEIN')
    str = self.re_substitute(str, r'\bLANGERIN\s+CRD\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bVP1\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bZNZNUA\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bKLHXK1\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bYEAST CHD1 TANDEM CHROMODOMAINS\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bWILD-TYPE RK\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bUVRB\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bUBIQUITIN\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bTYRRSTT\+TRNA\(TYR\)', r'PROTEIN')
    str = self.re_substitute(str, r'TRYPSIN-LIGAND', r'PROTEIN')
    str = self.re_substitute(str, r'\bTRYPSIN\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bTRPS\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bTHROMBIN\:SURAMIN\b', r'')
    str = self.re_substitute(str, r'\bTHERMOLYSIN\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bTENA\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bTA PROTEIN\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bSRC SH2\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bSSO7D\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bSHMT\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bSERCA\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bSAC7D\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bRBP\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bREDUCTIVELY METHYLATED PROTEIN\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPURR\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPROTEIN\s*A\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPROTEIN MMP8\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPROTEIN WIND\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPROTEIN SAMPLE\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPROTEIN PTPN5\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPROTEIN R1E\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPROTEIN Y53[FS]\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPROTEIN RAB11B-G(DP|PPNHP)\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPROT\b', r'PROTEIN') #1o3w fix
    str = self.re_substitute(str, r'\bPPE\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPOLYPEPTIDE\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPORTAL\s+PROTEIN\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPLC\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPHYCOCYANIN\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPER\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPDF\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPCDK2/CYCLIN\s*A?\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPAC181-AMIC\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bP/CAF\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bP450\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bOPPA\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bMURINE DELTA114 INOS\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bMICAL\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bMAB231\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bLEUCYL\-TRNA SYNTHETASE MOLAR PROTEIN\:TRNA 1\.\.2\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bIPNS\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bINHIBITORY ANTITHROMBIN-III\b', r'PROTEIN')
    str = self.re_substitute(str, r'(HUMAN )?INSULIN\b', r'PROTEIN')
    str = self.re_substitute(str, r'\b(HUMAN)?\s*HEMOGLOBIN\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bMYOGLOBIN', r'PROTEIN')
    str = self.re_substitute(str, r'\bHR\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bHB\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bPROTEIN HMK\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bHIVPR\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bHEXB\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bHEWL\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bHEN EGG-WHITE LYSOZYME \(BOEHRINGER\)', r'PROTEIN')
    str = self.re_substitute(str, r'\bGRB2-SH2\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bGLYCOGENIN\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bGABARAP\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bFV FRAGMENT\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bFOSA\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bFIBRILLARIN\b', r'PROTEIN')
    str = self.re_substitute(str, r'(\bFAB\'13B5|\bFAB192\b|\bFAB198\b|\bFAB\b)', r'PROTEIN')
    str = self.re_substitute(str, r'\bF17BG\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bF93\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bEF\s*-TU\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bE4-68\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bE1\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bDAHPS\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bDEOXYHB\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bCON\s+A\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bCOMPLEX$', r'PROTEIN')
    str = self.re_substitute(str, r'\bCHEY N59R\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bCARBOXYHEMOGLOBIN\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bBUK2\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bBCM7\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bAPO-R2 PROTEIN\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bAPPRO\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bANX12\b', r'PROTEIN')
    str = self.re_substitute(str, r'\bAKR7A5\b', r'PROTEIN')
    str = self.re_substitute(str, r'PROTEIN REPA', r'PROTEIN')
    str = self.re_substitute(str, r'PROTEIN MGMPK', r'PROTEIN')
    str = self.re_substitute(str, r'PROTEIN PPE \(SERVA\)', r'PROTEIN')
    str = self.re_substitute(str, r'PROTEIN PROTEIN', r'PROTEIN')
    str = self.re_substitute(str, r'PROTEIN COMPLEX', r'PROTEIN')
    str = self.re_substitute(str, r'PROTEIN PROTEIN', r'PROTEIN')
    str = self.re_substitute(str, r'^\s*[\(\)]\s*PROTEIN\s*$', r'PROTEIN')
    str = self.re_substitute(str, r'^\s*PROTEIN\s*[\(\)]\s*$', r'PROTEIN')
    
    if self.verbose>5:
      print "convert_name:12a",repr(str)
    
    # Remove 'protein' at start and end of line where more specific text is available 
    str = self.re_substitute(str, r'^(.*\S+)\s*PROTEIN$', r'\1')
    str = self.re_substitute(str, r'^PROTEIN\s*(.*\S+)$', r'\1')

    if self.verbose>5:
      print "convert_name:12b",repr(str)
    
    # peptides, as there seem to be a few of these...
    str = self.re_substitute(str, r'\bTRIPEPTIDE\b', r'PEPTIDE')
    str = self.re_substitute(str, r'\bMFLE\b', r'PEPTIDE')
    str = self.re_substitute(str, r'\bN-AC-NPI-CO2H', r'PEPTIDE')
    str = self.re_substitute(str, r'\bNPI\b', r'PEPTIDE')
    str = self.re_substitute(str, r'\bPEPTIDE DSYTC', r'PEPTIDE')
    str = self.re_substitute(str, r'\bSUBSTRATE\s+PEPTIDE', r'PEPTIDE')
    str = self.re_substitute(str, r'\bMC-PEPTIDE', r'PEPTIDE')
    str = self.re_substitute(str, r'\bTRAP\-TAIL', r'PEPTIDE')

    if self.verbose>5:
      print "convert_name:12c",repr(str)
    
    # and now for other macromolecules...
    str = self.re_substitute(str, r'\b[567]NT\s+RNA\b', r'RNA')
    str = self.re_substitute(str, r'\bDUPLEX\s+DNA\b', r'DNA DUPLEX')
    str = self.re_substitute(str, r'\bSINGLE\s+STRAND\s+OLIGONUCLEOTIDE', r'OLIGONUCLEOTIDE')
    str = self.re_substitute(str, r'\bHYBID\s+\(DOUBLE\s+STRAND\)', r'DNA:RNA DUPLEX')
    str = self.re_substitute(str, r'^RNA DUPLEX$', r'DNA:RNA DUPLEX')
    str = self.re_substitute(str, r'^DUPLEX$', r'DNA DUPLEX') #473d
    str = self.re_substitute(str, r'^DNA DECAMER$', r'DNA') #467d
    str = self.re_substitute(str, r'^10MER$', r'DNA DUPLEX') #1xuw,1xux
    str = self.re_substitute(str, r'DNA \(SINGLE STRAND\)|DNA\s+STRAND', r'DNA')

    if self.verbose>5:
      print "convert_name:12d",repr(str)
    
    str = self.re_substitute(str, r'NA2S2O[34]', r'SODIUM THIOSULFATE')
    str = self.re_substitute(str, r'\(NADH\)', r'NADH')
    str = self.re_substitute(str, r'\bMPD\s+MPD\b', r'')
    str = self.re_substitute(str, r'\bSULFATE\)', r'SULFATE')
    str = self.re_substitute(str, r'\bCHLORIDE\)', r'CHLORIDE')
    str = self.re_substitute(str, r'^NA$', r'SODIUM ION')
    str = self.re_substitute(str, r'\bETDA\b', r'EDTA')
    str = self.re_substitute(str, r'\bEDTA\)', r'EDTA')
    str = self.re_substitute(str, r'\bMES\)', r'MES')
    str = self.re_substitute(str, r'\bDTT\)', r'DTT')
    str = self.re_substitute(str, r'\bAZIDE\)', r'AZIDE')
    str = self.re_substitute(str, r'\bPROTEIN\)', r'PROTEIN')
    str = self.re_substitute(str, r'MERCAPTOETHANOL\)', r'MERCAPTOETHANOL')
    str = self.re_substitute(str, r'\d+ *HRS', r'')
    str = self.re_substitute(str, r'\d+ *MINS', r'')
    str = self.re_substitute(str, r'24 HOURS', r'')
    str = self.re_substitute(str, r'\d+ *HOURS? PRIOR', r'')
    str = self.re_substitute(str, r'DEGREES', r'')
    str = self.re_substitute(str, r'INHIBITORS?', r'')
    str = self.re_substitute(str, r'KCL\)', r'KCL')
    str = self.re_substitute(str, r'[-/_ ]+HCL$', r'')
    str = self.re_substitute(str, r'[.]\dH2(O|0)$',r'')
    str = self.re_substitute(str, r'\bAS\b', r'')
    str = self.re_substitute(str, r'[-.+:;, ]+\s*$', r'')
    str = self.re_substitute(str, r'(\(\+\))$',r'')
    str = self.re_substitute(str, r'\(\s*\)$', r'')
    str = self.re_substitute(str, r'\d*\s*MGS*/ML$',r'')
    str = self.re_substitute(str, r'\d*\s*ML$',r'')
    str = self.re_substitute(str, r'\d\.\d$',r'')
    str = self.re_substitute(str, r'\(\s*$',r'')
    str = self.re_substitute(str, r'\s*$',r'')
    str = self.re_substitute(str, r'&',r'')
    str = self.re_substitute(str, r'[-_]$',r'')
    str = self.re_substitute(str, r'\[\]',r'')
    str = self.re_substitute(str, r'\[$',r'')
    str = self.re_substitute(str, r'\]$',r'')
    str = self.re_substitute(str, r'^\s*\)$',r'')
    str = self.re_substitute(str, r'\s*\($',r'')
    str = self.re_substitute(str, r'\s*$',r'')
    str = self.re_substitute(str, r'\'+$',r'')
    str = self.re_substitute(str, r'[-.+:;, ]+$', r'')
    str = self.re_substitute(str, r'^\s+',r'')
    str = self.re_substitute(str, r'\s+$',r'')
    str = self.re_substitute(str, r',-$', r'')

    str = self.remove_unmatched_brackets(str)
    
    if self.verbose>0:
      print "convert_name:13",repr(str)
    # If there are no matched brackets then remove trailing bracket 
    if re.match('.+\(.+\)', str)==None:
      str = str.rstrip(')')

    if self.verbose>0:
      print "convert_name:14",repr(str)

    str = self.re_substitute(str, r'(NA|SODIUM)(\s|-)?ADA',r'ADA')

    return (str)
