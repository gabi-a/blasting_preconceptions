import pickle
import sys
import os
import subprocess
import numpy as np

pdbcodes = pickle.load(open("db/nonempty_pdbcodes.pkl","rb"))
with open("db/pdb_seqres.txt","rt") as f:
    sequenceslines = f.readlines()

blastoutdir = os.path.join(os.getcwd(),"db","blastout")
blastdb = os.path.join(os.getcwd(), "db", "blastdb","pdbaa")

numseqs = min(int(len(sequenceslines)/2),len(pdbcodes))
pdbcodes_paired = []
k = 0
for i,(meta,seq) in enumerate(zip(sequenceslines[0::2],sequenceslines[1::2])):

    sys.stdout.flush()
    print(f"Progress: {k}/{numseqs}",end='\r')

    pdbcode = meta[1:5]
    chain = meta[6]
    if chain != 'A': continue
    if pdbcode not in pdbcodes:
        continue

    seqfile = open("tmp/seqtemp.txt","w")
    seqfile.write(seq)
    seqfile.close()

    blastout = os.path.join(blastoutdir, pdbcode + ".csv")
    
    cmd = "blastp -query " +seqfile.name + " -db " + blastdb + " -out " + blastout + " -outfmt 10"
    
    try:
        subprocess.call(cmd, shell=True)
    except Exception as e:
        print(e)
        continue

    k += 1
    pdbcodes_paired.append(pdbcode)

pickle.dump(pdbcodes_paired, open("db/nonempty_seq_pdbcodes.pkl","wb"))