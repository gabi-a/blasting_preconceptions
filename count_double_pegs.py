import pickle

with open("db/chems_dict.pkl","rb") as f:
    conds = pickle.load(f)

doubles = 0
atall = 0
total_peg = 0
total = 0
highmw = 0
for well in conds.values():
    peg = 0
    for sol in well:
        if 'POLYETHYLENE GLYCOL' in sol["chem"]:
            weight = int(sol["chem"].split(" ")[-1])
            if weight >= 1450:
                highmw += 1
            peg += 1
            total_peg += 1
    if peg > 0:
        atall += 1
    if peg > 1:
        doubles += 1
    total += 1

print(f"PEG appears: {total_peg} times across {total} wells or {total_peg/total*100:2.3f}%")
print(f"PEG with MW >= 1450 appears: {highmw} times across {total} wells or {highmw/total*100:2.3f}%")
print(f"PEG occurs in: {atall}/{total} wells or {atall/total*100:2.3f}%")
print(f"PEG occurs more than once in: {doubles}/{total} wells or {doubles/total*100:2.3f}%")
