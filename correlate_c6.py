from __future__ import print_function
import sys
import c6
import pickle
import numpy as np

chemsdict = pickle.load(open("db/chems_dict.pkl2","rb"))
pdbcodes = pickle.load(open("db/nonempty_seq_pdbcodes.pkl2","rb"))
numcodes = len(pdbcodes)

C6scorer = c6.C6_Scorer()

c6results = []
for i,pdbcode in enumerate(pdbcodes):
    sys.stdout.flush()
    print("Progress: %d/%d"%(i,numcodes))

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

        print("========================")
        print(conds1)
        print(conds2)
        c6score = C6scorer.c6_score(conds1, conds2)
        c6results.append((c6score, seqident))

c6results = np.asarray(c6results)
np.save("db/c6_results", c6results)
