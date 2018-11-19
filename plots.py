import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
from matplotlib.ticker import NullFormatter

def superHist(data, datafilter):
    x = data[datafilter,0]
    y = data[datafilter,1]

    nullfmt = NullFormatter()

    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    bottom_h = left_h = left + width + 0.02

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]

    # start with a rectangular Figure
    plt.figure(figsize=(8, 8))

    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)

    # no labels
    axHistx.xaxis.set_major_formatter(nullfmt)
    axHisty.yaxis.set_major_formatter(nullfmt)

    axScatter.hist2d(data[datafilter,1],data[datafilter,0],bins=50,norm=clr.LogNorm())

    axHistx.hist(y, bins=50)
    axHisty.hist(x, bins=50, orientation='horizontal')

    axHistx.set_xlim(axScatter.get_xlim())
    axHisty.set_ylim(axScatter.get_ylim())

C6results = np.load("db/c6_results.npy")
PEGresults = np.load("db/peg_results_g1450.npy")
NH4results = np.load("db/nh4_results.npy")

C6filter = np.where((C6results[:,0] != -1) & (C6results[:,0] <= 1))[0]
print(f"Number of C6 pairs after filtering for errors: {len(C6filter)}/{C6results.shape[0]} total C6 pairs")
superHist(C6results, C6filter)
plt.savefig("images/c6_hist2d",dpi=800)

C6filter = np.where((C6results[:,0] != -1) & (C6results[:,0] <= 1) & (C6results[:,1] > 99))[0]
print(f"Number of C6 pairs after filtering for errors and with seqident > 99%: {len(C6filter)}/{C6results.shape[0]} total C6 pairs")
superHist(C6results, C6filter)
plt.savefig("images/c6_hist2d_g99",dpi=800)

PEGfilter = np.where((PEGresults[:,0] <= 100))[0]
print(f"Number of PEG pairs after filtering for conc < 100 W/V: {len(PEGfilter)}/{PEGresults.shape[0]} total PEG pairs")
superHist(PEGresults, PEGfilter)
plt.savefig("images/peg_hist2d",dpi=800)

PEGfilter = np.where((PEGresults[:,0] <= 100) & (PEGresults[:,1] > 99))[0]
print(f"Number of PEG pairs after filtering for conc < 100 W/V and with seqident > 99%: {len(PEGfilter)}/{PEGresults.shape[0]} total PEG pairs")
superHist(PEGresults, PEGfilter)
plt.savefig("images/peg_hist2d_g99",dpi=800)

NH4filter = np.where((NH4results[:,0] <= 5))[0]
print(f"Number of NH4 pairs after filtering for conc. < 5 M : {len(NH4filter)}/{NH4results.shape[0]} total NH4 pairs")
superHist(NH4results, NH4filter)
plt.savefig("images/nh4_hist2d",dpi=800)

NH4filter = np.where((NH4results[:,0] <= 5) & (NH4results[:,1] > 99))[0]
print(f"Number of NH4 pairs after filtering for conc. < 5 M and with seqident > 99%: {len(NH4filter)}/{NH4results.shape[0]} total NH4 pairs")
superHist(NH4results, NH4filter)
plt.savefig("images/nh4_hist2d_g99",dpi=800)

"""
print(len(np.where(C6results[:,0] > 1)[0]))
filter = np.where((C6results[:,0] != -1) & (C6results[:,0] <= 1))[0]
print(f"{len(C6results[:,0])-len(filter)}/{len(C6results[:,0])} results filtered from C6 hist")
plt.hist2d(C6results[filter,1],C6results[filter,0],bins=50,norm=clr.LogNorm())
plt.colorbar()
# plt.xlabel("Identity %")
# plt.ylabel("C6 Distance Metric")
plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.1)
plt.savefig("images/c6_hist2d",dpi=800,)

plt.figure()

filter = np.where((C6results[:,0] != -1) & (C6results[:,0] <= 1) & (C6results[:,1] > 99))
plt.hist2d(C6results[filter,1][0],C6results[filter,0][0],bins=50,norm=clr.LogNorm())
plt.colorbar()
# plt.xlabel("Identity %")
# plt.ylabel("C6 Distance Metric")
plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.1)
plt.savefig("images/c6_hist2d_g99",dpi=800,)

plt.figure()

filter = np.where(PEGresults[:,0] <= 100)[0]
print(f"{len(PEGresults[:,0])-len(filter)}/{len(PEGresults[:,0])} results filtered from PEG hist")
plt.hist2d(PEGresults[filter,1],PEGresults[filter,0], bins=50,norm=clr.LogNorm())
plt.colorbar()
# plt.xlabel("Identity %")
# plt.ylabel("PEGEq Concentration Distance (W/V)")
plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.1)
plt.savefig("images/pegeq_hist2d",dpi=800)

plt.figure()

filter = np.where(PEGresults[:,1] > 99)[0]
plt.hist2d(PEGresults[filter,1],PEGresults[filter,0], bins=50,norm=clr.LogNorm())
plt.colorbar()
# plt.xlabel("Identity %")
# plt.ylabel("PEGEq Concentration Distance (W/V)")
plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.1)
plt.savefig("images/pegeq_hist2d_g99",dpi=800)

plt.figure()


filter = np.where(NH4results[:,0] <= 5)[0]
print(f"{len(NH4results[:,0])-len(filter)}/{len(NH4results[:,0])} results filtered from ammonium sulfate hist")
plt.hist2d(NH4results[filter,1],NH4results[filter,0], bins=50,norm=clr.LogNorm())
plt.colorbar()
# plt.xlabel("Identity %")
# plt.ylabel("Ammonium Sulfate Concentration Distance (M)")
plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.1)
plt.savefig("images/nh4_hist2d",dpi=800)

plt.figure()

filter = np.where(NH4results[:,1] > 99)[0]
plt.hist2d(NH4results[filter,1],NH4results[filter,0], bins=50,norm=clr.LogNorm())
plt.colorbar()
# plt.xlabel("Identity %")
# plt.ylabel("Ammonium Sulfate Concentration Distance (M)")
plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.1)
plt.savefig("images/nh4_hist2d_g99",dpi=800)
"""
plt.show()
