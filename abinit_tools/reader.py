import argparse
import numpy as np
import glob

from natsort import natsorted
from abipy.abilab import abiopen
from ase.units import Bohr

def reader(files, param):
    energy = []
    params = []

    for f in files:
        print("Processing {}".format(f))

        with abiopen(f) as gsr:
            # get lattice structure and convert it to bohr
            lattice = gsr.structure.lattice.matrix
            lattice_bohr = lattice / Bohr

            energy.append(gsr.energy)

            if param == 'volume':
                params.append(float(np.linalg.det(lattice_bohr)))
            elif param == 'ecut':
                params.append(float(gsr.ecut.to("Ha")))
            elif param == 'nkpt':
                params.append(float(gsr.nkpt))
            elif param == 'acell':
                params.append(np.linalg.norm(lattice_bohr, axis=1).tolist())
            elif param == 'rprim':
                acell = np.linalg.norm(lattice_bohr, axis=1)
                params.append((lattice_bohr/acell[:,...]).tolist())
            else:
                raise TypeError(f"Unknown parameter '{param}'. Valid options are 'volume', 'ecut', 'nkpt', 'acell', and 'rprim'")
    return energy, params

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--param", required=True,
                        help="Parameter to extract from file: volume, ecut, nkpt, acell, rprim")
    args = parser.parse_args()

    # get file from command line
    files = natsorted(glob.glob("*GSR.nc"))

    energy, params = reader(files, args.param)
    print('Energy ', energy)
    print(f"Parameter '{args.param}' ", params)

if __name__ == "__main__":
    main()
