import sys
import pegeq
import pickle
import numpy as np

chemsdict = pickle.load(open("db/chems_dict.pkl","rb"))
pdbcodes = pickle.load(open("db/nonempty_seq_pdbcodes.pkl","rb"))
numcodes = len(pdbcodes)

PEGscorer = pegeq.PEG_Scorer()

pegresults = []
for i,pdbcode in enumerate(pdbcodes):

    sys.stdout.flush()
    print(f"Progress: {i}/{numcodes}",end='\r')

    conds1 = chemsdict[pdbcode]

    peg1 = None
    for cond in conds1:
        if "POLYETHYLENE GLYCOL" in cond["chem"] and cond["units"] == "W/V":
            weight = int(cond["chem"].split(" ")[-1])
            if weight >= 1450:
                peg1 = cond
                break

    if not peg1:
        continue

    with open("db/blastout/"+pdbcode+".csv","rb") as csvfile:
        blastresult = np.genfromtxt(csvfile,dtype=None,delimiter=",")
    
    try:
        if not len(blastresult) > 0:
            continue
    except:
        continue
    
    for seqid, seqident in zip(blastresult['f1'], blastresult['f2']):

        pdbcode2 = seqid[:4].decode("ascii").lower()
        if pdbcode2 not in pdbcodes:
            continue
        conds2 = chemsdict[pdbcode2]

        peg2 = False
        for cond in conds2:
            if "POLYETHYLENE GLYCOL" in cond["chem"] and cond["units"] == "W/V":
                weight = int(cond["chem"].split(" ")[-1])
                if weight >= 1450:
                    peg2 = cond
                    break
        if peg2:
            _peg1 = (int(peg1["chem"].split(" ")[-1]), float(peg1["conc"]))
            _peg2 = (int(peg2["chem"].split(" ")[-1]), float(peg2["conc"]))
            pegscore = PEGscorer.peg_score(_peg1, _peg2)
            pegresults.append((pegscore, seqident))

pegresults = np.asarray(pegresults)
np.save("db/peg_results_g95", pegresults)
