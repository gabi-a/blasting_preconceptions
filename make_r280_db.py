import os
import gzip
import sys

pdbdir = os.path.join(os.getcwd(),'db','pdb')
pdbfiles = os.listdir(pdbdir)

r280db = open("db/r280db.txt","w")

numpdbfiles = len(pdbfiles)

for i in range(numpdbfiles):
    sys.stdout.flush()
    print(f"Progress: {i}/{numpdbfiles}",end='\r')

    pdbfile = pdbfiles[i]
    name = os.path.splitext(os.path.basename(pdbfile))[0]
    with gzip.open(os.path.join(pdbdir,pdbfile), "rt") as f:
        lines = f.readlines()

    r280db.writelines([name+':'+line for line in lines if "REMARK 280" in line])
