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
plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.1)
plt.savefig("images/c6_hist2d",dpi=800,)

plt.figure()

C6filter = np.where((C6results[:,0] != -1) & (C6results[:,0] <= 1) & (C6results[:,1] > 90))
plt.hist2d(C6results[C6filter,1][0],C6results[C6filter,0][0],bins=50,norm=clr.LogNorm())
plt.colorbar()
plt.xlabel("Identity %")
plt.ylabel("C6 Distance Metric")
plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.1)
plt.savefig("images/c6_hist2d_zoom",dpi=800,)

plt.figure()

plt.hist2d(PEGresults[:,1],PEGresults[:,0], bins=50,norm=clr.LogNorm())
plt.colorbar()
plt.xlabel("Identity %")
plt.ylabel("PEGEq Concentration Distance (W/V)")
plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.1)
plt.savefig("images/pegeq_hist2d",dpi=800)

plt.figure()

filter = np.where(PEGresults[:,1] > 90)[0]
plt.hist2d(PEGresults[filter,1],PEGresults[filter,0], bins=50,norm=clr.LogNorm())
plt.colorbar()
plt.xlabel("Identity %")
plt.ylabel("PEGEq Concentration Distance (W/V)")
plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.1)
plt.savefig("images/pegeq_hist2d_zoom",dpi=800)

plt.figure()

plt.hist2d(NH4results[:,1],NH4results[:,0], bins=50,norm=clr.LogNorm())
plt.colorbar()
plt.xlabel("Identity %")
plt.ylabel("Ammonium Sulfate Concentration Distance (M)")
plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.1)
plt.savefig("images/nh4_hist2d",dpi=800)

plt.figure()

filter = np.where(NH4results[:,1] > 90)[0]
plt.hist2d(NH4results[filter,1],NH4results[filter,0], bins=50,norm=clr.LogNorm())
plt.colorbar()
plt.xlabel("Identity %")
plt.ylabel("Ammonium Sulfate Concentration Distance (M)")
plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.1)
plt.savefig("images/nh4_hist2d_zoom",dpi=800)

plt.show()