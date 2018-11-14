ids = set()

with open("db/r280db.txt","r") as f:
    lines = f.readlines()

for line in lines:
    ids.add(line[3:7])

print(len(ids))