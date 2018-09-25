import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr

C6results = np.load("db/c6_results.npy")
PEGresults = np.load("db/peg_results.npy")
NH4results = np.load("db/nh4_results.npy")

C6filter = np.where((C6results[:,0] != -1) & (C6results[:,0] <= 1))
plt.hist2d(C6results[C6filter,1][0],C6results[C6filter,0][0],bins=50,norm=clr.LogNorm())
plt.colorbar()
plt.xlabel("Identity %")
plt.ylabel("C6 Distance Metric")
plt.title("C6 Histogram")
plt.figure()
plt.hist2d(PEGresults[:,1],PEGresults[:,0], bins=50,norm=clr.LogNorm())
plt.colorbar()
plt.xlabel("Identity %")
plt.ylabel("PEGEq Concentration Distance (W/V)")
plt.title("PEGEq Histogram")

plt.figure()
plt.hist2d(NH4results[:,1],NH4results[:,0], bins=50,norm=clr.LogNorm())
plt.colorbar()
plt.xlabel("Identity %")
plt.ylabel("Ammonium Sulfate Concentration Distance (M)")
plt.title("Ammonium Sulfate Histogram")

plt.show()