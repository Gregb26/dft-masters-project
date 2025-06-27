"""
get_wyckpos.py:
    Extracts the Wyckoff positions from a given .cif file.
Usage:
    python get_wyckpos.py file.cif.
Inputs:
    file.cif.
Outputs
    Wyckoff positions.
Dependencies:
    spglib, pymatgen.
"""

import spglib

from abinit_tools.argparse_utils import parse_args
from pymatgen.core import Structure

def main():
    args = parse_args(
        description="Extracts the Wyckoff positions from a given .cif file.",
        positional_args=[
            ("cif_file", "Input cif file path")
        ]
    )

    cif_file = args.cif_file
    # get structure from pymatgen
    structure = Structure.from_file(cif_file)

    # Convert to tuple (lattice, positions, atomic numbers)
    lattice = structure.lattice.matrix
    positions = [site.frac_coords for site in structure]
    numbers = [site.specie.Z for site in structure]

    cell = (lattice, positions, numbers)

    dataset = spglib.get_symmetry_dataset(cell)

    print(dataset.wyckoffs)
    print(dataset.equivalent_atoms)

if __name__ == "__main__":
    main()