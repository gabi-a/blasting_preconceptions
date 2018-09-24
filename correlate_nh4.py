from __future__ import print_function
import sys
import pickle
import numpy as np

chemsdict = pickle.load(open("db/chems_dict.pkl2","rb"))
pdbcodes = pickle.load(open("db/nonempty_seq_pdbcodes.pkl2","rb"))
numcodes = len(pdbcodes)

nh4results = []
for i,pdbcode in enumerate(pdbcodes):
    sys.stdout.flush()
    print(f"Progress: {i}/{numcodes}",end='\r')

    with open("db/blastout/"+pdbcode+".csv","rb") as csvfile:
        blastresult = np.genfromtxt(csvfile,dtype=None,delimiter=",")

    try:
        if not len(blastresult) > 0:
            continue
    except:
        continue

    conds1 = chemsdict[pdbcode]

    for seqid, seqident in zip(blastresult['f1'], blastresult['f2']):
        pdbcode2 = seqid[:4].decode("ascii").lower()
        if pdbcode2 not in pdbcodes:
            continue
        conds2 = chemsdict[pdbcode2]

    ammoniumSulfate1 = None
    for cond in conds1:
        if cond["chem"] == "AMMONIUM SULFATE" and cond["units"] == "M":
            ammoniumSulfate1 = float(cond["conc"])
            break

    ammoniumSulfate2 = None
    for cond in conds2:
        if cond["chem"] == "AMMONIUM SULFATE" and cond["units"] == "M":
            ammoniumSulfate2 = float(cond["conc"])
            break
            
    if ammoniumSulfate1 and ammoniumSulfate2:
        nh4results.append((np.abs(ammoniumSulfate1-ammoniumSulfate2), seqid))
        
nh4results = np.asarray(nh4results)
np.save("db/chem_results", nh4results)
