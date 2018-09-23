import pickle
import sys
import os
import subprocess
import numpy as np

pdbcodes = pickle.load(open("db/nonempty_pdbcodes.pkl","rb"))
with open("db/pdb_seqres.txt","rt") as f:
    sequenceslines = f.readlines()

blastoutdir = os.path.join(os.getcwd(),"db","blastout")
blastdb = os.path.join(os.getcwd(), "db", "blastdb")

numseqs = int(len(sequenceslines)/2)
pdbcodes_paired = []
blastdict = {}
for i,meta,seq in enumerate(zip(sequenceslines[0::2],sequenceslines[1::2])):
    sys.stdout.flush()
    print(f"Progress: {i}/{numseqs}",end='\r')

    pdbcode = meta[1:5]
    chain = meta[6]
    if chain != 'A': continue
    if pdbcode not in pdbcodes:
        print(f"Missing {pdbcode}")
        continue

    seqfile = open("blast/seqtemp.txt","w")
    seqfile.write(seq)
    seqfile.close()

    blastout = os.path.join(blastoutdir, pdbcode + ".csv")
    
    cmd = "blastp -query " + seqfile + " -db " + blastdb + " -out " + blastout + " -outfmt 10"
    
    try:
        subprocess.call(cmd, shell=True)
    except Exception as e:
        print(e)
        continue

    pdbcodes_paired.append(pdbcode)

    with open(blastout, "rb") as csvfile:
        blastdict[pdbcode] = np.genfromtxt(csvfile,dtype=None,delimiter=",")

pickle.dump(blastdict, open("blast_dict.pkl","wb"))
pickle.dump(pdbcodes_paired, open("nonempty_seq_pdbcodes.pkl","wb"))