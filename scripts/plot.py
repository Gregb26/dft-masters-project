"""
plot.py

Plots data, usually total_energy vs some parameter to eyeball the best parameter (the one that
minimizes the total energy).

Usage:
    python plot.py --param PARAM, in the directory with *GSR.nc file to analyze

Inputs:
    *GSR.nc files, --param: ecut, nkpt, volume, acell.

Outputs:
    Plot of total_energy vs param

Dependencies:
    matplotlib, natsort, abinit_tools.reader
"""

import matplotlib.pyplot as plt
import argparse
import glob

from natsort import natsorted
from abinit_tools.reader import reader

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--param", required=True, help="Parameter to extract from file: ecut, volume, nkpt, acell")
    args = parser.parse_args()

    files = natsorted(glob.glob("*GSR.nc"))
    energy, params = reader(files, args.param)

    print(energy)
    print(params)

    plt.plot(params, energy, "*k")
    plt.plot(params, energy, "--k")
    plt.ylabel("Energy (Ha)")
    plt.xlabel(f"{args.param}")
    plt.show()

if __name__ == "__main__":
    main()




