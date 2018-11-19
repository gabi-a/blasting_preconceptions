import numpy as np
import matplotlib.pyplot as plt

lines = np.load("blast_lines.npy")

plt.hist(lines,bins=100)
plt.xlim(0,1000)
plt.savefig("images/blastlines",dpi=800)
plt.show()
