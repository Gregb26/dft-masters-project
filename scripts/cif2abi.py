"""
cif2abi.py

Converts crystal structure data in a .cif file to an .abi ABINIT-compatible structure block.
Automatically converts to a primitive cell using pymatgen.

Usage:
    python cif2abi.py crystal.cif

Inputs:
    .cif file as command line argument

Outputs:
    .abi file with ABINIT-compatible structure block

Dependencies:
    pymatgen, numpy, ase
"""
import numpy as np
import argparse
import sys
import os

from pymatgen.core import Structure as PMGStructure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from ase.units import Bohr

def clean_format(x, tol=1e-14, precision=2):
    """
    Returns clean string for float x.
    Inputs:
        x: float to be cleaned
        tol: numbers smaller than this will be set to zero
        precision: number of decimals to keep
    Outputs:
        cleaned float
    """
    if abs(x) < tol:
        x = 0
    return f"{x:.{precision}f}"

def main():

    parser = argparse.ArgumentParser(description="Convert .cif file to .abi ABINIT-compatible structure block.")
    parser.add_argument("cif_file", help=".cif to convert")
    parser.add_argument("--full", choices=['no', 'yes'], default='no', help="Writes a minimal working example .abi file: yes")
    args = parser.parse_args()

    cif_path = args.cif_file

    struct = PMGStructure.from_file(cif_path)
    primitive = SpacegroupAnalyzer(struct).get_primitive_standard_structure()

    # get lattice vectors in angstrom
    latt = primitive.lattice.matrix

    # converting to Bohr
    latt_bohr = latt / Bohr

    # acell: norms of lattice vectors
    acell = [np.linalg.norm(vec) for vec in latt_bohr]

    # rprim: normalized lattice vectors
    rprim = [vec / np.linalg.norm(vec) for vec in latt_bohr]

    # atomic numbers
    atomic_number = [site.specie.Z for site in primitive]

    # extract the different types of elements
    unique_z = sorted(set(atomic_number))

    # typat: type index to each atom based on its atomic number
    typat = [unique_z.index(z) + 1 for z in atomic_number]

    # extract base filename without extension
    basename = os.path.splitext(os.path.basename(cif_path))[0]

    # get full path to parent directory of cif_files/
    parent_dir = os.path.dirname(os.path.abspath(cif_path))
    project_root = os.path.dirname(parent_dir) # one level up (parent directory)

    # create abi_files/ path relative to project root
    abi_dir = os.path.join(project_root, "abi_files")
    abi_path = os.path.join(abi_dir, basename + ".abi")

    # ensure abi_files/ exists
    os.makedirs(abi_dir, exist_ok=True)

    # writing in the .abi file
    with open(abi_path, "w") as f:

        f.write("# Abinit crystal structure\n")
        f.write("acell " + ' '.join(clean_format(a) for a in acell) + "  # in Bohr\n")
        f.write("rprim\n")
        for vec in rprim:
            f.write("  " + ' '.join(clean_format(x) for x in vec) + "\n")

        f.write(f"natom {len(primitive)}\n")
        f.write(f"ntypat {len(unique_z)}\n")
        f.write("znucl " + ' '.join(str(z) for z in unique_z) + "\n")
        f.write("typat " + ' '.join(str(t) for t in typat) + "\n")

        f.write("xred\n")
        for site in primitive:
            f.write("  " + ' '.join(clean_format(x) for x in site.frac_coords) + "\n")
        f.write("\n")

        if args.full == "yes":
            f.write("# pseudopotentials\n")
            f.write('pp_dirpath "$ABI_PSP"\n')
            f.write('pseudos ""\n')
            f.write('\n')

            f.write('# exchange-correlation functional\n')
            f.write('ixc 11 # PBE\n')
            f.write('\n')

            f.write('# planewave basis set\n')
            f.write('ecut 20 # planewave energy cutoff\n')
            f.write('\n')

            f.write('# kpoint grid\n')
            f.write('kptopt 1\n')
            f.write('ngkpt 8 8 8\n')
            f.write('nshiftk 4\n')
            f.write('shiftk\n')
            f.write('  0.5 0.5 0.5\n')
            f.write('  0.5 0.0 0.0\n')
            f.write('  0.0 0.5 0.0\n')
            f.write('  0.0 0.0 0.5\n')
            f.write('\n')

            f.write('# SCF procedure\n')
            f.write('nstep 50\n')
            f.write('toldfe 1.0d-8\n')
            f.write('diemac 12.0\n')
            f.write('\n')

            f.write('# postprocessing\n')
            f.write('prtvol 1\n')

            print('Writing minimal working example with crystal structure information in an ABINIT readable .abi file')
        elif args.full == "no":
            print('Writing crystal structure file in an ABINIT readable .abi file.')
        else:
            raise ValueError("Incorrect input. --full accepts the following values: yes, no. Default is no")

if __name__ == "__main__":
    main()