import argparse
import spglib
from pymatgen.core import Structure

def main():
    parser = argparse.ArgumentParser(description="Get the Wyckoff positions from a .cif file")
    parser.add_argument("cif_file", help="Input .cif file")
    args = parser.parse_args()

    cif_file = args.cif_file

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