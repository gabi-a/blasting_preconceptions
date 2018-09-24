import pickle

chemsdict = pickle.load(open("db/chems_dict.pkl","rb"))
pickle.dump(chemsdict,open("db/chems_dict.pkl2","wb"),protocol=2)
pdbcodes = pickle.load(open("db/nonempty_seq_pdbcodes.pkl","rb"))
pickle.dump(pdbcodes,open("db/nonempty_seq_pdbcodes.pkl2","wb"),protocol=2)