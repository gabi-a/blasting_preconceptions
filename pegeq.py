import numpy as np
from scipy import stats
import pickle

chemsdict = pickle.load(open("db/chems_dict.pkl","rb"))
pdbcodes = pickle.load(open("db/nonempty_pdbcodes.pkl","rb"))

PEGcount = 0
PEGcount_knownunits = 0
PEGdata = []
for pdbcode in pdbcodes:
    conds = chemsdict[pdbcode]
    for cond in conds:
        if "POLYETHYLENE GLYCOL" in cond["chem"]:
            PEGcount += 1
            if cond["units"] == "W/V":
                conc = float(cond["conc"])
                PEGcount_knownunits += 1
            elif cond["units"] == "V/V":
                conc = 1.1 * float(cond["conc"])
                PEGcount_knownunits += 1
            else:
                continue
            weight = int(cond["chem"][-1])
            PEGdata.append((conc, weight))

PEGdata = np.asarray(PEGdata)
slope, intercept, r_value, p_value, std_err = stats.linregress(np.log(PEGdata[:,1]), PEGdata[:,0])