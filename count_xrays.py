import os
import gzip
import sys

pdbdir = os.path.join(os.getcwd(),'db','pdb')
pdbfiles = os.listdir(pdbdir)

numpdbfiles = len(pdbfiles)

xray_count = 0

for i in range(numpdbfiles):

    sys.stdout.flush()
    print(f"Progress: {i}/{numpdbfiles}",end='\r')

    pdbfile = pdbfiles[i]
    name = os.path.splitext(os.path.basename(pdbfile))[0]
    with gzip.open(os.path.join(pdbdir,pdbfile), "rt") as f:
        lines = f.readlines()

    for line in lines:
        line = line.lower()
        if "remark 200" in line:
            if "xray" in line or "x-ray" in line or "x ray" in line:
                xray_count += 1 
                break

print(f"Number of structures determined by X-ray: {xray_count:d}/{numpdbfiles:d}")   
