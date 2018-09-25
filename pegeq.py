import numpy as np
from scipy import stats
import pickle
import matplotlib.pyplot as plt

def main():
    chemsdict = pickle.load(open("db/chems_dict.pkl","rb"))
    pdbcodes = pickle.load(open("db/nonempty_pdbcodes.pkl","rb"))

    PEGcount = 0
    PEGcount_knownunits = 0
    PEGdata = []
    for pdbcode in pdbcodes:
        conds = chemsdict[pdbcode]
        for cond in conds:
            if "POLYETHYLENE GLYCOL" in cond["chem"]:
                PEGcount += 1
                if cond["units"] == "W/V":
                    conc = float(cond["conc"])
                    PEGcount_knownunits += 1
                else:
                    continue
                weight = int(cond["chem"].split(" ")[-1])
                PEGdata.append((conc, weight))

    PEGdata = np.asarray(PEGdata)

    means = []
    for i,weight in enumerate(np.unique(PEGdata[:,1])):
        concs = np.transpose(PEGdata[np.where(PEGdata[:,1]==weight),0])
        std = np.std(concs)
        mean = np.mean(concs)

        means.append((weight, mean, std, len(concs)))
        print("Mol Weight = %8d\tConc: Mean = %f\tSTD = %f\tCount = %d"%(weight, mean, std, len(concs)))

    means = np.asarray(means)

    slope, intercept, r_value, p_value, std_err = stats.linregress(np.log(PEGdata[:,1]), PEGdata[:,0])

    plt.text(6000, 38, f"y = {slope:.3f}x+{intercept:.3f}\n$r^2$ = {r_value**2:.3f}\np = {p_value:.3f}\nstd_err={std_err:.3f}",bbox=dict(facecolor='none', edgecolor='black',pad=10))

    pickle.dump(slope, open("db/pegeq.pkl","wb"))

    plt.scatter(means[:,0], means[:,1], color="r", zorder=1)
    max_count = np.max(means[:,3])
    for conc_stats in means:
        plt.errorbar(conc_stats[0],conc_stats[1],conc_stats[2], elinewidth=round(np.log((100*conc_stats[3]/max_count + 1))), ecolor=(conc_stats[3]/max_count, 0.5, 0.5), zorder=0)
    plt.xlabel("Molecular Weight")
    plt.ylabel("Mean Conc")
    plt.xscale("log")

    ticks = np.array(np.sort(np.unique(PEGdata[:,1])),dtype=int)
    plt.xticks(ticks[::2],ticks[::2], rotation=45)

    plt.plot(np.arange(np.min(means[:,0]), np.max(means[:,0]), 1), slope*np.log(np.arange(np.min(means[:,0]), np.max(means[:,0]), 1))+intercept)
    
    for i,weight in enumerate(np.unique(PEGdata[:,1])):
        if len(np.where(PEGdata[:,1] == weight)[0]) > 10:
            plt.subplot(5,5,i+1)
            plt.hist(PEGdata[np.where(PEGdata[:,1] == weight), 0][0],bins=100)
            plt.xlim((0,50))
            plt.text(20,plt.ylim()[1]*(9/10),f"Mol. Weight = {int(weight):d}")

    plt.show()

class PEG_Scorer:
    
    def __init__(self):
        self.pegslope = pickle.load(open("db/pegeq.pkl","rb"))
    
    def peg_score(self, peg1, peg2):
        dx = peg2[0] - peg1[0]
        peg1eq = peg1[1] + self.pegslope * dx
        score = np.abs(peg2[1] - peg1eq)
        return score

if __name__ == "__main__":
    main()