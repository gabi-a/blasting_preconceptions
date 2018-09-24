import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(),"C6","c6","webgen_scripts"))
from ctypes import *
from datafetch import DatabaseScreenIterObj, IonData
from calc_score import CalcScore, C_SOLN, MAXCONC, ION
from config import PH_NOT_SPECIFIED, MAX_ELEMENT_NAME_LEN, MAX_UNIT_NAME_LEN

class C6_Scorer:

    def __init__(self):
        self.calcs = CalcScore()

    def c6_score(self, chems1, chems2):
        Solutions1 = C_SOLN * len(chems1)
        Solutions2 = C_SOLN * len(chems2)
        
        sol1 = Solutions1()
        sol2 = Solutions2()
        
        for i,s in enumerate(chems1):

            if s["pH"] != 'None':
                sol1[i] = self.calcs.make_soln(s["chem"], float(s["conc"]), s["units"], float(s["pH"]))
            else:
                sol1[i] = self.calcs.make_soln(s["chem"], float(s["conc"]), s["units"])

        for i,s in enumerate(chems2):
            
            if s["pH"] != 'None':
                sol2[i] = self.calcs.make_soln(s["chem"], float(s["conc"]), s["units"], float(s["pH"]))
            else:
                sol2[i] = self.calcs.make_soln(s["chem"], float(s["conc"]), s["units"])

        return self.calcs.well_score(sol1, sol2)[4]