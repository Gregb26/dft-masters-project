import argparse
import numpy as np
import glob

from natsort import natsorted
from abipy.abilab import abiopen

def get_parameter(gsr, param):
    """
    Fetches parameters from GSR file
    Inputs:
        gsr: GSR output file
        param: parameter to read in the GSR file. Options: ecut, nkpt, acell
    return: the read parameters in the GSR file
    """
    if param == "ecut":
        return gsr.ecut.to("Ha")
    elif param == "volume":
        return np.linalg.det(gsr.structure.lattice.matrix)
    elif param == "nkpt":
        return gsr.nkpt
    else:
        raise ValueError(f"Unknown parameter '{param}'. Valid options are: ecut, nkpt, volume.")


def read_files(files, param):
    energy = []
    params = []

    for f in files:
        print("Processing: ", f)
        with abiopen(f) as gsr:
            energy.append(gsr.energy)
            params.append(float(get_parameter(gsr,  param)))

    return energy, params

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--param", required=True, help="Parameter to extract from file: ecut, volume, nkpt")
    args = parser.parse_args()

    files = natsorted(glob.glob("*GSR.nc"))
    energy, params = read_files(files, args.param)

    print("Energy: ")
    print(energy)
    print("Params: ")
    print(params)

if __name__ == "__main__":
    main()
