"""
reader.py:
    Reads data from ABINIT output files _GSR.nc to extract total energy and a given parameters. Available parameters are
    ecut, volume, nkpt, acell, rprim.
Usage:
    python reader.py, in the directory that containts the GSR.nc files to analyze.
Inputs:
    GSR.nc ABINIT ouput files.
Outputs:
    energy, parameter.
Dependencies:
    abipy, ase, natsort
"""

import numpy as np
import glob

from natsort import natsorted
from abipy.abilab import abiopen
from ase.units import Bohr
from abinit_tools.argparse_utils import parse_args

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
    args = parse_args(
        description="Reads data from GSR.nc ABINIT ouput files.",
        optional_args=[
            {
                "--param": {
                    "help": "Parameter to extract from GSR.nc file",
                    "choices": ["ecut", "volume", "nkpt", "acell", "rprim"],
                    "required": True,
                    "type": str,
                }
            }
        ]
    )

    files = natsorted(glob.glob("*GSR.nc"))

    energy, params = reader(files, args.param)
    print('Energy ', energy)
    print(f"Parameter '{args.param}' ", params)

if __name__ == "__main__":
    main()
