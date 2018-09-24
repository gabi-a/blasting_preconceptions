import pickle

with open("db/chems_dict.pkl","rb") as f:
    conds = pickle.load(f)

chems = {"POLYETHYLENE GLYCOL":{}, "AMMONIUM SULFATE":{}} #, "HEPES":{}, "SODIUM ACETATE":{}, "MES":{}, "SODIUM CHLORIDE":{}, "BIS-TRIS":{}, "AMMONIUM ACETATE":{}, "TRIS":{}}

for well in conds.values():
    if len(well) > 0:
        for chem in well:
            for k in chems.keys():
                if k in chem["chem"]:
                    chems[k][chem["units"]] = 1 + chems[k].setdefault(chem["units"], 0)

print(chems)