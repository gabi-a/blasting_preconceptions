#!/bin/env python
#
# Copyright (C) 2008-2014 CSIRO Australia
#

import csv
import os
import sys
import platform

# These are excluded from the conditions list because they are not crystal conditions
non_chem_list=[ \
                # PROTEINS, LIGANDS, NUCLEIC ACIDS ETC.
                'PROTEIN', 'RNA', 'DNA DUPLEX', 'OLIGONUCLEOTIDE', 'DNA:RNA DUPLEX',
                'DNA', 'LIGAND',  'PEPTIDE',
                
                # CATIONS WHERE ANION WAS NOT SPECIFIED
                'ZINC ION', 'MANGANESE ION', 'DITHIONITE ION', 'SODIUM ION',
                'MANGANESE ION', 'CADMIUM ION', 
                'CALCIUM ION', 'MAGNESIUM ION', 'IRON ION',
                
                # POLYMERS WHERE CHAIN LENGTH WAS NOT SPECIFIED
                'PENTAERYTHRITOL ETHOXYLATE POLYMER',
                'PEG', 'PEG MME', 'PENTAERYTHRITOL PROPOXYLATE POLYMER',
                'POLYVINYLPYRROLIDONE POLYMER',
                'JEFFAMINE POLYMER','ACRYLATE POLYMER',
                
                # OTHER NON-SPECIFIC CHEMS
                'BUTANEDIOL',
                
                # INSOLUBLES, MOSTLY USED FOR 'MICROBATCH UNDER OIL'
                "AL'S OIL", 'PARAFFIN OIL', 'SILICONE OIL',
                'METHYL SALICYLATE']

# These are chems for which the chemicals exist in CrystalTrak, but the aliases do not
# FORMAT: 'alias':'chem'
jchem_dict_extra = {'D2O':'DEUTERIUM OXIDE',
                    'TRITON X100':'TRITON X-100',
                    'NAACET':'SODIUM ACETATE',
                    'CAOAC':'CALCIUM ACETATE',
                    'KPHOSPHATE':'DIPOTASSIUM HYDROGEN-POTASSIUM DIHYDROGEN PHOSPHATE',
                    'DIBASIC POTASSIUM PHOSPHATE':'DIPOTASSIUM HYDROGEN PHOSPHATE',
                    'MONOBASIC SODIUM PHOSPHATE':'SODIUM DIHYDROGEN PHOSPHATE',
                    'MONOBASIC POTASSIUM PHOSPHATE':'POTASSIUM DIHYDROGEN PHOSPHATE',
                    'SODIUM PHOSPHATE, TRIBASIC':'TRISODIUM PHOSPHATE',
                    'NA4P2O7':'SODIUM PYROPHOSPHATE',
                    'BIS TRIS PROPANE':'BIS-TRIS PROPANE',
                    'CHLORURE DE SODIUM':'SODIUM CHLORIDE',
                    'BUTANOL':'1-BUTANOL',
                    'PEG 3400':'POLYETHYLENE GLYCOL 3350',
                    'PEG 3250':'POLYETHYLENE GLYCOL 3350',
                    'PEG 4450':'POLYETHYLENE GLYCOL 3350',
                    'COPPER CHLORIDE':'COPPER(II) CHLORIDE', # VF: might be (I) ??
                    '2OG':'ALPHA-KETOGLUTARATE',     
                    'PEG 550':'POLYETHYLENE GLYCOL MONOMETHYL ETHER 550',
                    'GLUCOSE 6 PHOSPHATE':'GLUCOSE-6-PHOSPHATE',
                    'GLUCOSE 6-PHOSPHATE':'GLUCOSE-6-PHOSPHATE',
                    'PEG 3550':'POLYETHYLENE GLYCOL 3350',
                    'COBALT HEXAMINE CHLORIDE':'HEXAMMINE COBALT(III) CHLORIDE',
                    'ETHANEDIOL':'ETHYLENE GLYCOL', 
                    'SODIUM HYDROXIDE-MES':'SODIUM MES',
                    'TRIS CARBOXYETHYL PHOSPHINE':'TCEP',
                    'DEOXYTHYMIDINE':'THYMIDINE',
                    'DL MALATE':'DL-MALIC ACID', 
                    'PEG 1550':'POLYETHYLENE GLYCOL 1500', 
                    'MALATE':'DL-MALIC ACID',
                    'C11DAO':'UDAO',
                    'POTASSIUM-SODIUM TARTRATE':'POTASSIUM SODIUM TARTRATE', 
                    'ASCORBATE':'L-ASCORBIC ACID',     
                    'UNDECYLMALTOSIDE':'N-UNDECYL-B-D-MALTOSIDE', 
                    'BETA-OCTYL-GLUCOPYRANOSIDE':'N-OCTYL-B-D-GLUCOPYRANOSIDE',
                    'DDT':'DITHIOTHREITOL', # FIXME: Not likely to be DDT, check each one to be sure
                    'TETRAMETHYL AMMONIUM CHLORIDE':'TETRAMETHYLAMMONIUM CHLORIDE', 
                    'PEG 3300':'POLYETHYLENE GLYCOL 3350', 
                    "PYRIDOXAL 5' PHOSPHATE":'PYRIDOXAL-5-PHOSPHATE',
                    "PYRIDOXAL 5-PHOSPHATE":'PYRIDOXAL-5-PHOSPHATE',
                    '2-OXYGLUTARIC ACID':'ALPHA-KETOGLUTARATE',
                    'MERCURY CHLORIDE':'MERCURY(II) CHLORIDE',
                    'FUMARATE':'FUMARIC ACID', 
                    'SUCCINATE PHOSPHATE GLYCINE':'SUCCINATE-PHOSPHATE-GLYCINE',
                    'PEG 5000':'POLYETHYLENE GLYCOL MONOMETHYL ETHER 5000',
                    r'15/4 EO/OH':'PENTAERYTHRITOL ETHOXYLATE (15/4 EO/OH)',
                    'LI3(C3H5O(COO)3)':'TRILITHIUM CITRATE',
                    'LITHIUM CITRATE':'TRILITHIUM CITRATE',
                    'PYRUVATE':'PYRUVIC ACID', # CAS 127-17-3
                    'NAD+':'NICOTINAMIDE ADENINE DINUCLEOTIDE', 
                    'GLUTAMATE':'GLUTAMIC ACID', 
                    'CITRATE PHOSPHATE':'PHOSPHATE-CITRATE',
                    'SODIUM CITRATE PHOSPHATE':'PHOSPHATE-CITRATE',
                    'N-ACETYL GLUCOSAMINE':'N-ACETYLGLUCOSAMINE',
                    'BIS TRIS PROPANE':'BIS-TRIS PROPANE',
                    'N-BOG':'N-OCTYL-B-D-GLUCOPYRANOSIDE',
                    'PEG 3500':'POLYETHYLENE GLYCOL 3350',
                    'UNDECYLMALTOSIDE':'N-UNDECYL-B-D-MALTOSIDE', 
                    '1,1,1,3,3,3-HEXAFLUORO-ISOPROPANOL':'1,1,1,3,3,3-HEXAFLUORO-2-PROPANOL', 
                    'MALATE MES TRIS':'DL-MALATE-MES-TRIS',
                    'BUTYRLACTONE':'GAMMA BUTYROLACTONE', 
                    'BUTYROLACTONE':'GAMMA BUTYROLACTONE',
                    'CARBONATE':'SODIUM CARBONATE',
                    'MES:NAOH':'SODIUM MES',
                    'MES-NAOH':'SODIUM MES',
                    'FRUCTOSE':'DL-FRUCTOSE',
                    'KANAMYCIN':'KANAMYCIN MONOSULFATE',
                    'L-XYLOSE':'DL-XYLOSE',                    
                    'HEPES:NAOH':'HEPES',
                    'TRIS BASE':'TRIS',
                    'NON- SULFOBETAINE 201':'NDSB 201',
                    'NONYLGLUCOSIDE':'N-NONYL-B-D-GLUCOSIDE',
                    'AMMONIUM H PHOSPHATE':'DIAMMONIUM HYDROGEN PHOSPHATE',
                    'L GLYCINE NAOH':'GLYCINE',
                    'PENTAERYTHRITOL ETHOXYLATE 15/4':'PENTAERYTHRITOL ETHOXYLATE (15/4 EO/OH)',
                    'SODIUM CL':'SODIUM CHLORIDE',
                    'SODIUM BR':'SODIUM BROMIDE',
                    'NAFORM':'SODIUM FORMATE',
                    'MAGNESIUM CL':'MAGNESIUM CHLORIDE',
                    'ZINCOAC':'ZINC ACETATE',
                    'NAMALATE':'SODIUM MALATE',
                    'GLYC':'GLYCINE',
                    'L GLYCINE':'GLYCINE',
                    'SODIUM I':'SODIUM IODIDE',
                    'CADMIUM CL':'CADMIUM CHLORIDE',
                    'CO CHLORIDE':'COBALT CHLORIDE',
                    'L PROLINE':'PROLINE',
                    'CARNITINE':'CARNITINE HYDROCHLORIDE',
                    'JEFF600':'JEFFAMINE M-600',
                    'ZINC AC':'ZINC ACETATE',
                    'PVP K 15':'POLYVINYLPYRROLIDONE K15',
                    'DEXTRAN SULFATE SODIUM':'DEXTRAN SULFATE',
                    'YTTRIUM(III) CHLORIDE':'YTTRIUM CHLORIDE',
                    'ETHYLENE IMINE':'ETHYLENE IMINE POLYMER',
                    'FE CHLORIDE':'IRON(III) CHLORIDE',
                    'PVPDNE K15':'POLYVINYLPYRROLIDONE K15',
                    'PVPDNE':'POLYVINYLPYRROLIDONE K15',
                    'AMMONIUM 2 SULFATE':'AMMONIUM SULFATE',
                    'TRIS(2-CARBOXYETHYL)PHOSPHINE':'TCEP',
                    }

                   
                    
                    
                    
                    
                    
                    
# These ones and their alia do not exist in CrystalTrak database
# FORMAT: 'alias':'chem'
# TODO: Move 'PROTEIN' etc. into classification code                    
local_chem_dict = { 'PROTEIN':'PROTEIN',
                    'LIGAND':'LIGAND',
                    'RNA':'RNA',
                    'DNA DUPLEX':'DNA DUPLEX',
                    'OLIGONUCLEOTIDE':'OLIGONUCLEOTIDE',
                    'BIS TRIS HEPES':'BIS TRIS HEPES',
                    'DNA:RNA DUPLEX':'DNA:RNA DUPLEX',
                    'DNA':'DNA',
                    'PEPTIDE':'PEPTIDE',
                    'BUTANEDIOL':'BUTANEDIOL',
                    'D-CAMPHOR':'D-CAMPHOR', # CAS: 464-49-3
                    'CAMPHOR':'D-CAMPHOR',
                    'CDK2':'PROTEIN',
                    'RENIN':'PROTEIN',
                    'MES':'MES',
                    'PRO-CASPASE3':'PROTEIN',
                    'THAUMATIN':'PROTEIN',
                    'MURA':'LIGAND',
                    'BACE':'PROTEIN',
                    'CHEY':'PROTEIN',
                    'HCL':'HYDROCHLORIC ACID', 
                    'ISOCITRATE':'ISOCITRATE',
                    'SODIUM CITRATE-POTASSIUM CITRATE':'SODIUM CITRATE-POTASSIUM CITRATE',
                    'ARG-PHE':'ARG-PHE',
                    'ADOCBL':'LIGAND',
                    'PAP':'LIGAND',
                    'OXANE':'OXANE',
                    'THP':'OXANE',
                    '4-HYDROXYPHENACYL COENZYME A':'4-HYDROXYPHENACYL COENZYME A',
                    'WRN EXONUCLEASE':'PROTEIN',
                    'ARABINOSE-5-PHOSPHATE':'ARABINOSE-5-PHOSPHATE',
                    'TRIMETHYLAMINE':'TRIMETHYLAMINE',
                    'MAGNESIUM CALCIUM SULFATE':'MAGNESIUM CALCIUM SULFATE',
                    'S-ADENOSYL-L-HOMOCYSTEINE':'LIGAND',
                    'PEG MME 200':'POLYETHYLENE GLYCOL MONOMETHYLETHER 2000', # We think PEG MME 200 is a typo
                    'POLYETHYLENE GLYCOL MONOMETHYLETHER 2000':'POLYETHYLENE GLYCOL MONOMETHYLETHER 2000',
                    'PEG MME 3350':'POLYETHYLENE GLYCOL MONOMETHYLETHER 350', # I think PEG MME 3350 is a typo
                    'PEG 350':'POLYETHYLENE GLYCOL MONOMETHYLETHER 350', # I think PEG 350 is a typo
                    'POLYETHYLENE GLYCOL MONOMETHYLETHER 350':'POLYETHYLENE GLYCOL MONOMETHYLETHER 350',
                    'PEG MME 500':'POLYETHYLENE GLYCOL MONOMETHYLETHER 550', # Another typo
                    'POLYETHYLENE GLYCOL MONOMETHYLETHER 550':'POLYETHYLENE GLYCOL MONOMETHYLETHER 550',
                    'PEG 40000':'POLYETHYLENE GLYCOL 40000',
                    'POLYETHYLENE GLYCOL 40000':'POLYETHYLENE GLYCOL 40000',
                    'PEG 35000':'POLYETHYLENE GLYCOL 35000',
                    'POLYETHYLENE GLYCOL 35000':'POLYETHYLENE GLYCOL 35000',
                    'KAINIC ACID':'KAINIC ACID', # CAS 487-79-6
                    'BESTATIN':'LIGAND',
                    'DITHIONITE':'DITHIONITE ION', # Or perhaps sodium dithionite
                    'DITHIONITE ION':'DITHIONITE ION',
                    'SODIUM ION':'SODIUM ION',
                    'SODIUM':'SODIUM ION',
                    'I2':'IODINE',
                    'IODINE':'IODINE',
                    'CADMIUM':'CADMIUM ION',
                    'CADMIUM ION':'CADMIUM ION',
                    'IRON ION':'IRON ION',
                    'DEOXYURIDINE MONOPHOSPHATE':'DEOXYURIDINE MONOPHOSPHATE',
                    'HEPPSO':'HEPPSO',
                    'POLYVINYLPYRROLIDONE':'POLYVINYLPYRROLIDONE POLYMER',
                    'POLYVINYLPYRROLIDONE POLYMER':'POLYVINYLPYRROLIDONE POLYMER',
                    'TETRAETHYLAMMONIUM CHLORIDE':'TETRAETHYLAMMONIUM CHLORIDE', 

                    'SODIUM BES':'SODIUM BES',
                    'SODIUM DITHIONATE':'SODIUM DITHIONATE',
                    'SODIUM NITRITE':'SODIUM NITRITE',
                    'SODIUM CHLORITE':'SODIUM CHLORITE',
                    'DISODIUM DIHYDROGEN PYROPHOSPHATE':'DISODIUM DIHYDROGEN PYROPHOSPHATE',
                    'MES/IMIDAZOLE':'MES-IMIDAZOLE',
                    'MES-IMIDAZOLE':'MES-IMIDAZOLE',
                    'DUMP':'DEOXYURIDINE MONOPHOSPHATE', # CAS: 964-26-1
                    '2-CARBOXYARABINITOL-1,5-DIPHOSPHATE':'LIGAND',
                    '4-HYDROXYBENZOATE':'4-HYDROXYBENZOATE',
                    'P-HYDROXYBENZOATE':'4-HYDROXYBENZOATE', # CAS: 456-23-5 CHEBI:17879
                    'URANYL ACETATE':'URANYL ACETATE',
                    'THULIUM CHLORIDE':'THULIUM CHLORIDE',
                    'SODIUM VANADATE':'SODIUM ORTHOVANADATE',
                    'SODIUM ORTHOVANADATE':'SODIUM ORTHOVANADATE',
                    'L-ALLO-THREONINE':'L-ALLO-THREONINE',
                    'SODIUM MOLYDBATE':'SODIUM MOLYDBATE',
                    'SODIUM CYANIDE':'SODIUM CYANIDE',
                    'POTASSIUM CYANIDE':'POTASSIUM CYANIDE',
                    'SILVER NITRATE':'SILVER NITRATE',
                    'RUBIDIUM CACODYLATE':'RUBIDIUM CACODYLATE',
                    'NICKEL ACETATE':'NICKEL ACETATE',
                    'MERCURY SULFATE':'MERCURY(II) SULFATE',
                    'MERCURY(II) SULFATE':'MERCURY(II) SULFATE',
                    'MERCURY(II) ACETATE':'MERCURY(II) ACETATE',
                    'MERCURY ACETATE':'MERCURY(II) ACETATE',
                    'SODIUM 4-(HYDROXYMERCURY)BENZOATE':'SODIUM 4-(HYDROXYMERCURY)BENZOATE',
                    'MANGANESE ACETATE':'MANGANESE(II) ACETATE', # VF: might be (III) ??
                    'MANGANESE SULFATE':'MANGANESE(II) SULFATE',
                    'MANGANESE(II) ACETATE':'MANGANESE(II) ACETATE',
                    'MANGANESE(III) ACETATE':'MANGANESE(III) ACETATE',
                    'MANGANESE(II) SULFATE':'MANGANESE(II) SULFATE',
                    'LUTETIUM(III) CHLORIDE':'LUTETIUM(III) CHLORIDE',
                    'LUTETIUM CHLORIDE':'LUTETIUM(III) CHLORIDE',
                    'LITHIUM CACODYLATE':'LITHIUM CACODYLATE',
                    'IRIDIUM(III) HEXAMMINE CHLORIDE':'IRIDIUM(III) HEXAMMINE CHLORIDE',
                    'HYDROGEN PEROXIDE':'HYDROGEN PEROXIDE',
                    'ERBIUM CHLORIDE':'ERBIUM(III) CHLORIDE',
                    'ERBIUM(III) CHLORIDE':'ERBIUM(III) CHLORIDE',
                    'ERBIUM ACETATE':'ERBIUM(III) ACETATE',
                    'ERBIUM(III) ACETATE':'ERBIUM(III) ACETATE',
                    'TARTARIC ACID':'TARTARIC ACID',
                    'TARTRATE':'TARTARIC ACID',
                    'COPPER ACETATE':'COPPER(II) ACETATE',
                    'COPPER(II) ACETATE':'COPPER(II) ACETATE',
                    'COBALT ACETATE':'COBALT(II) ACETATE',
                    'COBALT(II) ACETATE':'COBALT(II) ACETATE',
                    'CALCIUM SULFATE':'CALCIUM SULFATE',
                    'CALCIUM NITRATE':'CALCIUM NITRATE',
                    'CALCIUM CACODYLATE':'CALCIUM CACODYLATE',
                    'CALCIUM BROMIDE':'CALCIUM BROMIDE',
                    'CALCIUM':'CALCIUM ION',
                    'ORNITHINE':'ORNITHINE',
                    'HEXASACCHARIDE':'LIGAND',
                    'CALCIUM ION':'CALCIUM ION',
                    'MANGANESE':'MANGANESE ION',
                    'MANGANESE ION':'MANGANESE ION',
                    'BERYLLIUM CHLORIDE':'BERYLLIUM CHLORIDE',
                    'BERYLLIUM FLUORIDE':'BERYLLIUM FLUORIDE',
                    'AMMONIUM VANADATE':'AMMONIUM METAVANADATE',
                    'AMMONIUM METAVANADATE':'AMMONIUM METAVANADATE',
                    'ALUMINIUM NITRATE':'ALUMINIUM NITRATE',
                    'PENTAERYTHRITOL PROPOXYLATE':'PENTAERYTHRITOL PROPOXYLATE POLYMER', # MW unspecified
                    'PENTAERYTHRITOL PROPOXYLATE POLYMER':'PENTAERYTHRITOL PROPOXYLATE POLYMER',
                    'PENTAERYTHRITOL ETHOXYLATE POLYMER':'PENTAERYTHRITOL ETHOXYLATE POLYMER',
                    'PENTAERYTHRITOL ETHOXYLATE':'PENTAERYTHRITOL ETHOXYLATE POLYMER', # MW unspecified
                    'DGTP':'DEOXYGUANOSINE TRIPHOSPHATE', # CHEBI:16497
                    'DEOXYGUANOSINE TRIPHOSPHATE':'DEOXYGUANOSINE TRIPHOSPHATE',
                    'A861695':'LIGAND', #'2-((R)-2-METHYLPYRROLIDIN-2-YL)-1H-BENZIMIDAZOLE-4-CARBOXAMIDE',
                    'A861696':'LIGAND', #'2-[(2S)-2-METHYLPYRROLIDIN-2-YL]-1H-BENZIMIDAZOLE-7-CARBOXAMIDE',
                    'A906894':'LIGAND', # '3-OXO-2-PIPERIDIN-4-YL-2,3-DIHYDRO-1H-ISOINDOLE-4-CARBOXAMIDE',
                    'A927929':'LIGAND', # '2-{2-FLUORO-4-[(2S)-PIPERIDIN-2-YL]PHENYL}-1H-BENZIMIDAZOLE-7-CARBOXAMIDE',
                    'A968427':'LIGAND', # '7-(PYRROLIDIN-1-YLMETHYL)PYRROLO[1,2-A]QUINOXALIN-4(5H)-ONE',
                    'BPH-652':'LIGAND', # 'TRIPOTASSIUM 4-(3-PHENOXYPHENYL)-1-PHOSPHONATOBUTANE-1-SULFONATE', #PUBCHEMID: 25244957
                    'BPH-698':'LIGAND', # 'TRIPOTASSIUM 1-PHOSPHONATO-4-[4-(4-PROPYLPHENYL)PHENYL]BUTANE-1-SULFONATE', #PUBCHEMID: 45479616
                    'BPH-700':'LIGAND', # 'TRIPOTASSIUM 4-(4-PHENYLPHENYL)-1-PHOSPHONATOBUTANE-1-SULFONATE', #PUBCHEMID:25245319
                    'UBP302':'LIGAND', #'2-{[3-[(2S)-2-AMINO-2-CARBOXYETHYL]-2,6-DIOXO-3,6-DIHYDROPYRIMIDIN-1(2H)-YL]METHYL}BENZOIC ACID', # CAS: 745055-91-8, PUBCHEM: 45073461
                    'UBP310':'LIGAND', #'(S)-1-(2-AMINO-2-CARBOXYETHYL)-3-(2-CARBOXY-THIOPHENE-3-YL-METHYL)-5-METHYLPYRIMIDINE-2,4-DIONE',
                    'UBP316':'LIGAND', #'1-(2-AMINO-2-CARBOXYETHYL)-3-(2-CARBOXY-5-PHENYLTHIOPHENE-3-YLMETHYL)-5-METHYLPYRIMIDINE-2,4-DIONE',
                    'UBP315':'LIGAND', #'UBP-315',
                    'UBP318':'LIGAND', #'UBP-318',
                    'SADTA':'LIGAND',
                    'C6DAO':'N,N-DIMETHYLHEXYLAMINE-N-OXIDE', # CAS 34418-88-7
                    'N,N-DIMETHYLHEXYLAMINE-N-OXIDE':'N,N-DIMETHYLHEXYLAMINE-N-OXIDE',
                    'BV1':'LIGAND', 
                    'BV2':'LIGAND',
                    'BV3':'LIGAND',
                    'BV4':'LIGAND',
                    'BVDU':'LIGAND',
                    'GW995':'PROTEIN',
                    'C10E6':'HEXAETHYLENE GLYCOL DECYL ETHER',
                    'HEXAETHYLENE GLYCOL DECYL ETHER':'HEXAETHYLENE GLYCOL DECYL ETHER',
                    '17-DMAP-GA':'LIGAND', # 3q5j
                    '2PG':'2-PHOSPHOGLYCOLIC ACID',
                    '2-PHOSPHOGLYCOLIC ACID':'2-PHOSPHOGLYCOLIC ACID',
                    'POTASSIUM HEPES':'POTASSIUM HEPES',
                    'POTASSIUM MOPS':'POTASSIUM MOPS',
                    'BIS TRIS CHLORIDE':'BIS TRIS CHLORIDE',
                    'MALEATE':'MALEATE',
                    #'SODIUM BICINE':'SODIUM BICINE',
                    '2-HYDROXYETHYLDISULFIDE':'2-HYDROXYETHYLDISULFIDE',
                    'IRON(II) CITRATE':'IRON(II) CITRATE',
                    'IRON(II) SULFATE':'IRON(II) SULFATE',
                    'MOPSO':'MOPSO', # CAS: 79803-73-9
                    'URATE OXIDASE':'PROTEIN',
                    'MAGNESIUM SALTS':'MAGNESIUM ION', # FIXME: Look up papers for more info
                    'MAGNESIUM':'MAGNESIUM ION',
                    'MAGNESIUM ION':'MAGNESIUM ION',
                    'MANGANESE ION':'MANGANESE ION',
                    'IRON(II)':'IRON ION', # FIXME: Look up papers for more info
                    '2-HYDROXYETHYLDISULFIDE':'2-HYDROXYETHYLDISULFIDE',
                    'MAGNESIUM ATP':'MAGNESIUM ATP',
                    'MAGNESIUM ADP':'MAGNESIUM ADP',
                    'SODIUM SULFITE':'SODIUM SULFITE',
                    'POTASSIUM CACODYLATE':'POTASSIUM CACODYLATE',
                    'PEG':'PEG',
                    'PEG MME':'PEG MME',
                    'COENZYME A':'COENZYME A',
                    'TRIS MES':'TRIS MES', # This is a mixture of TRIS and MES, not common.
                    'SODIUM BICARBONATE':'SODIUM BICARBONATE',
                    'AMP':'AMP', # It IS in Janet's DB, but as a protein
                    '8-AZAXANTHINE':'8-AZAXANTHINE',
                    #'EGTA':'EGTA', # CHEBI:30740 CAS:67-42-5
                    'FMN':"FLAVIN MONONUCLEOTIDE",
                    "RIBOFLAVIN-5'-PHOSPHATE":'FLAVIN MONONUCLEOTIDE',
                    'AMMONIUM PHOSPHATE/SODIUM PHOSPHATE':'AMMONIUM PHOSPHATE-SODIUM PHOSPHATE',
                    'AMMONIUM PHOSPHATE-SODIUM PHOSPHATE':'AMMONIUM PHOSPHATE-SODIUM PHOSPHATE',
                    'OXIDIZED BETA-MERCAPTOETHANOL':'2-HYDROXYETHYLDISULFIDE',  # Oxidation process joins 2 BMEs
                    'OXIDIZED BME':'2-HYDROXYETHYLDISULFIDE',
                    'SODIUM MOLYBDATE':'SODIUM MOLYBDATE',
                    'PEG 800':'POLYETHYLENE GLYCOL 1000',
                    'POLYETHYLENE GLYCOL 800':'POLYETHYLENE GLYCOL 1000',
                    'MES ACETATE':'MES ACETATE',
                    'FORMATE':'FORMATE', # No formic acid in Janet's db!
                    'S-ADENOSYLHOMOCYSTEINE':'S-ADENOSYL-L-HOMOCYSTEINE',
                    'S-ADENOSYL-L-HOMOCYSTEINE':'S-ADENOSYL-L-HOMOCYSTEINE',
                    'SODIUM THIOSULFATE':'SODIUM THIOSULFATE',
                    'ZINC':'ZINC ION',
                    'ZINC ION':'ZINC ION',
                    'POTASSIUM GLUTAMATE':'POTASSIUM GLUTAMATE',
                    'THYMIDINE DIPHOSPHATE':'THYMIDINE DIPHOSPHATE',
                    'AMP-PCP':'AMP-PCP', # better name?
                    'POLYACRYLIC ACID':'ACRYLATE POLYMER',
                    'ACRYLATE POLYMER':'ACRYLATE POLYMER',
                    'POTASSIUM FERROCYANIDE':'POTASSIUM FERROCYANIDE',
                    'SAM':'LIGAND', # S-ADENOSYL-L-METHIONINE
                    #'CETYL TRIMETHYLAMMONIUM BROMIDE':'CETYL TRIMETHYLAMMONIUM BROMIDE',
                    'JEFFAMINE':'JEFFAMINE POLYMER',
                    'JEFFAMINE POLYMER':'JEFFAMINE POLYMER',
                    'AMPCPP':'LIGAND',
                    'SHIKIMATE-3-PHOSPHATE':'SHIKIMATE-3-PHOSPHATE',
                    'CHYMOTRYPSIN':'PROTEIN',
                    'ELASTASE':'PROTEIN',
                    '4,5-OAM':'PROTEIN',
                    'IMIDAZOLE ACETATE':'IMIDAZOLE ACETATE',
                    'MES HEPES':'MES HEPES',
                    'FRUCTOSE 6-PHOSPHATE':'FRUCTOSE 6-PHOSPHATE',
                    'BETA-GLYCEROLPHOSPHATE':'GLYCEROL 2-PHOSPHATE',
                    'GLYCEROL 2-PHOSPHATE':'GLYCEROL 2-PHOSPHATE',
                    'THIOCYANATE':'THIOCYANIC ACID',
                    'THIOCYANIC ACID':'THIOCYANIC ACID',
                    'UDP-GLUCOSE':'LIGAND',
                    'PROPYL-AMP':'LIGAND',
                    'CHS':'LIGAND',
                    'APS':'LIGAND',
                    'SODIUM ASCORBATE':'SODIUM ASCORBATE',
                    'COPPER(II) ACETATE':'COPPER(II) ACETATE',
                    'SIAP':'PROTEIN',
                    'TES':'TES',
                    'AMMONIUM TES':'AMMONIUM TES',
                    '1,2-DIHEPTANOYL-SN-GLYCER-3-PHOSPHOCHOLINE':'1,2-DIHEPTANOYL-SN-GLYCER-3-PHOSPHOCHOLINE',
                    'AMPC':'PROTEIN',
                    'SINEFUNGIN':'LIGAND',
                    'FMN REDUCTASE':'PROTEIN',
                    'DUTP':'PROTEIN',
                    'PTN':'PROTEIN',
                    'CELLOTETRAOSE':'CELLOTETRAOSE', # CAS 38819-01-1
                    'POTASSIUM OXONATE':'POTASSIUM OXONATE', # CAS 2207-75-2
                    '4,5-DIHYDROOROTIC ACID':'4,5-DIHYDROOROTIC ACID',
                    'THIMEROSAL':'THIMEROSAL',
                    '2-IMINOBIOTIN':'LIGAND',
                    '3-PHOSPHOGLYCERATE':'3-PHOSPHOGLYCERIC ACID',
                    '3-PHOSPHOGLYCERIC ACID':'3-PHOSPHOGLYCERIC ACID',
                    'DEOXYCHOLIC ACID':'DEOXYCHOLIC ACID',
                    'CY-DIGMP':'PROTEIN',
                    'GLYCEROLPHOSPHOSPHATE':'GLYCEROL 3-PHOSPHATE',
                    'GLYCEROL 3-PHOSPHATE':'GLYCEROL 3-PHOSPHATE',
                    'X29':'PROTEIN',
                    'HYDROXYCOBALAMIN':'LIGAND',
                    'HEMICHOLINIUM-3':'PROTEIN',
                    'TRIS MALATE':'TRIS MALATE',
                    'PMSF':'PMSF', # CHEBI:8102 CAS:329-98-6
                    'AGAROSE':'AGAROSE',
                    'AMMONIUM MALATE':'AMMONIUM MALATE',
                    'DHFR':'PROTEIN',
                    'PCTP':'PROTEIN', # phosphatidylcholine
                    'BENZYLAMINE':'BENZYLAMINE',
                    '2-PHOSPHOGLYCOLATE':'2-PHOSPHOGLYCOLATE',
                    'MES-IMIDAZOLE':'MES-IMIDAZOLE',
                    'MANGANESE ACETATE':'MANGANESE ACETATE',
                    'MNOAC':'MANGANESE ACETATE',
                    'POTASSIUM MALEATE':'POTASSIUM MALEATE',
                    'CELLOHEXAOSE':'CELLOHEXAOSE',
                    'DIHYDROQUERCETIN':'DIHYDROQUERCETIN',
                    'DECYLUBIQUINONE':'DECYLUBIQUINONE',
                    'SODIUM SALICYLATE':'SODIUM SALICYLATE',
                    'GAMMA LACTAM':'2-PYRROLIDINONE',
                    '2-PYRROLIDINONE':'2-PYRROLIDINONE',
                    'GDP-MANNOSE':'GDP-MANNOSE',
                    'TRIS BICINE':'TRIS-BICINE',
                    'BICINE/TRIS BASE':'TRIS-BICINE',
                    'TRIS-BICINE':'TRIS-BICINE',
                    'PEG DME 500':'POLYETHYLENE GLYCOL DIMETHYL ETHER 500',
                    'PEG 500 DME':'POLYETHYLENE GLYCOL DIMETHYL ETHER 500',
                    'POLYETHYLENE GLYCOL DIMETHYL ETHER 500':'POLYETHYLENE GLYCOL DIMETHYL ETHER 500',
                    'PEG DME 250':'POLYETHYLENE GLYCOL DIMETHYL ETHER 250',
                    'PEG 250 DME':'POLYETHYLENE GLYCOL DIMETHYL ETHER 250',
                    'POLYETHYLENE GLYCOL DIMETHYL ETHER 250':'POLYETHYLENE GLYCOL DIMETHYL ETHER 250',
                    'POTASSIUM FERRICYANIDE':'POTASSIUM FERRICYANIDE',
                    }
                    
class CRYSTAL_PARSER_ALIA():
  def __init__(self, verbose, use_chem_classes, correcter_obj):
    self.verbose=verbose
    self.use_chem_classes=use_chem_classes

    if self.use_chem_classes:
      if platform.system()=='Linux':
        import_path=os.path.join(os.environ['HOME'],'SVN','C3SoftwareProjects','c6','trunk', 'webgen_scripts')
      else:
        import_path=os.path.join('c:\\SVN\\C3SoftwareProjects\\c6\\trunk\\webgen_scripts')
      sys.path.append(import_path)
      if os.path.exists(os.path.join(import_path,'chem_class.py')):
        import chem_class
        self.chemClass_obj=chem_class.ChemClass()
      else:
        print "Error! Cannot import chem_class.py"
        sys.exit(1)

    
    # Used to correct small mistakes in non-acronym chemical names
    self.correcter_obj=correcter_obj
    
    # Load Janet's CT alias list
    self.jchem_dict=self.getJanetsChemDict(jchem_dict_extra)

    # Self-test
    self.alias_consistency_check()
    
    
# Reads a csv of Janet's chems+alia, converts everything to upper case                    
  def getJanetsChemDict(self, chem_dict):
    """ select name, chem_alias
        from chemicals ch, chemical_alias ca
        where ch.chemical_id=ca.chemical_id
        and ch.chemical_id not in (select chemical_id from proteins)
        union
        select c2.name, c2.name
        from chemicals c2
        where c2.chemical_id not in (select chemical_id from proteins)
    """
    jChemDictFile=os.path.join('input','chem+alias.csv')
    if not os.path.exists(jChemDictFile):
      print "Cannot find csv file: {0}".format(jChemDictFile)
      sys.exit(1)
    jchemCsvReader = csv.reader(open(jChemDictFile))
    jchem_dict={}
    for chem, alias in jchemCsvReader:
      # Convert to upper case
      chem_upper=chem.upper()
      alias_upper=alias.upper()
      # Avoid TRIS CHLORIDE, TRIS combination
      if chem_upper!="TRIS CHLORIDE" or alias_upper!="TRIS":
        jchem_dict[alias_upper]=chem_upper
      
    x=set(chem_dict.keys())
    y=set(jchem_dict.keys())    
    keys_intersect=x&y
    if len(keys_intersect)>0:
      print "Error: jchem supplement and alias csv file have alia in common:", repr(keys_intersect)
      #print "csv file=", repr(sorted(chem_dict.keys()))
      #print 
      #print "supplement=", repr(sorted(jchem_dict.keys()))
      sys.exit(1)
      
    values_diff=set(chem_dict.values())-set(jchem_dict.values())
    if len(values_diff)>0:
      print "Error: there are chem names in supplement dict that are not in Janet's dict. Must rename them to be same as Janet's:", repr(values_diff)
      sys.exit(1)
    
    jchem_dict.update(chem_dict)
    
    # remove csv header
    if jchem_dict.has_key("NAME"):
      del jchem_dict["NAME"]
    if jchem_dict.has_key("CHEM_ALIAS"):
      del jchem_dict["CHEM_ALIAS"]
    #print repr(jchem_dict)
    return jchem_dict

  # Checks for alias loops, duplicate aliases etc.
  def alias_consistency_check(self):

    all_stand_chems = self.jchem_dict.values()
    all_stand_chems+= local_chem_dict.values()
  
    for chem in all_stand_chems:
      if self.jchem_dict.get(chem, chem)!=chem or local_chem_dict.get(chem, chem)!=chem:
        print "Error: chem=", repr(chem), '-> returns: ', self.jchem_dict[chem], "instead of ", chem
        
    # Check that local_chem dict and Janet's CrystalTrak dict do not overlap
    common_key_set = set(self.jchem_dict.keys()) & set(local_chem_dict.keys())
    if len(common_key_set)!=0:
      print "Error: possible duplicate keys between jchem_dict and local_chem_dict:", repr(common_key_set)
      sys.exit(1)
    
    
    
  def has_alias(self, alias_name):
    return self.jchem_dict.has_key(alias_name) or local_chem_dict.has_key(alias_name) 
  
  # Standardise chemical names
  def resolve_chem_name(self, chem_name, ph=None):
    #print "resolve_chem_name: chem_name=", repr(chem_name), " ph=", repr(ph)
    rsv_chem_name='Unknown'
    if self.jchem_dict.has_key(chem_name):
      rsv_chem_name = self.jchem_dict[chem_name]
    elif local_chem_dict.has_key(chem_name):
      rsv_chem_name = local_chem_dict[chem_name]
    elif self.correcter_obj!=None:
      corrected_chem, debug_str=self.correcter_obj.correct(chem_name)
      #print "corrected_chem, debug_str =", corrected_chem, ",", debug_str
      if corrected_chem!=chem_name and corrected_chem!=None:
        # Check that correcter has produced a standardised name
        if corrected_chem not in local_chem_dict.values() and corrected_chem not in self.jchem_dict.values():
          # No - did not. Try the alias dictionaries.
          if self.jchem_dict.has_key(corrected_chem):
            rsv_chem_name = self.jchem_dict[corrected_chem]
          elif local_chem_dict.has_key(corrected_chem):
            rsv_chem_name = local_chem_dict[corrected_chem]
          else:
            print "CORRECTOR: changing ", repr(chem_name), " -> ", repr(corrected_chem), "but it is not a standardised name!",
            sys.stdout.flush()
            rsv_chem_name='Unknown'
        else:
          # Yes - did produce standardised name
          print "CORRECTOR: ", chem_name, " -> ", corrected_chem
          sys.stdout.flush()
          rsv_chem_name=corrected_chem
          
    # Convert to a class name
    if self.use_chem_classes:
      if ph!=None:
        class_list=self.chemClass_obj.ToBufferClassList(rsv_chem_name, ph)
      else:
        class_list=self.chemClass_obj.ToBufferClassList(rsv_chem_name, 'ALL')
      if len(class_list)>0:
        rsv_chem_name=class_list[0].upper()

    return rsv_chem_name  
  
if __name__== "__main__":
  pass
