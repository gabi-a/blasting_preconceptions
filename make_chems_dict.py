import xml.etree.ElementTree as ET
import pickle

tree = ET.parse('Parse/output/cond_resolved_out.xml')
root = tree.getroot()

pdbcodes = [child.attrib['code'] for child in root]

pickle.dump(pdbcodes, open("db/nonempty_pdbcodes.pkl","wb"))

chems_dict = {}
for pdbcode in root:
    conds = []
    for child in pdbcode[0]:
        conds.append(child.attrib)
    chems_dict[pdbcode.attrib['code']] = conds

pickle.dump(chems_dict, open("db/chems_dict.pkl","wb"))