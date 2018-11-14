import pickle
unknown_chems = pickle.load(open("Parse/unknown_chems.pkl","rb"),encoding="latin1")
chems_unpacked = [item for sublist in unknown_chems.values() for item in sublist]
chems_count = {}
for chem in chems_unpacked:
    chems_count[chem] = chems_count.setdefault(chem, 0) + 1

chems_sorted = sorted(zip(chems_count.keys(), chems_count.values()), key=lambda x:x[1], reverse=True)

outfile = open("unknown_chems.csv","w")

maxlen = max([len(s) for s in chems_unpacked])

print(f"{'string':{maxlen+5}s}{'count':5s}",file=outfile)
for i,c in enumerate(chems_sorted):
    print(f"{c[0]:{maxlen+5}s}{c[1]:<5d}",file=outfile)

mean = sum(chems_count.values())/len(chems_count.values())
print(f"Mean count: {mean}")