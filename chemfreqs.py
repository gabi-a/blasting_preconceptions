import pickle

with open("db/chems_dict.pkl","rb") as f:
    conds = pickle.load(f)

chems = {}
peg = 0
total_parsed = len(conds.keys())
for well in conds.values():
    for sol in well:
        chems[sol["chem"]] = chems.setdefault(sol["chem"], 0) + 1
        if 'POLYETHYLENE GLYCOL' in sol["chem"]:
            peg += 1

print("Total Parsed: %d"%total_parsed)

chems_sorted = sorted(chems.items(), key=lambda kv: kv[1])

print("%-60s\t%8d\t%3.2f%%"%('POLYETHYLENE GLYCOL (All)',peg,100*float(peg)/float(total_parsed)))
for c in reversed(chems_sorted):
    print("%-60s\t%8d\t%3.2f%%"%(c[0],c[1],100*float(c[1])/float(total_parsed)))