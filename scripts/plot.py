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

import glob

from natsort import natsorted
from reader import reader
from abinit_tools.plot_config import setup
from abinit_tools.argparse_utils import parse_args

def main():
    args = parse_args(
        description='Plot data from GSR.nc ABINIT output files.',
        optional_args=[
            {
                "--param":{
                    "help": "Plot of total energy vs this parameter",
                    "choices": ["ecut", "volume", "nkpt", "acell", "rprim"],
                    "required": True,
                    "type": str,
                }
            },
            {
                "--preview":{
                    "action": "store_true",
                    "help": "display the plot on screen, but does not save the plot."
                }
            }
        ]
    )

    files = natsorted(glob.glob("*GSR.nc"))
    energy, params = reader(files, args.param)

    print(energy)
    print(params)

    # plot
    plt = setup(use_pgf= not args.preview)

    plt.plot(params, energy, "*k")
    plt.plot(params, energy, "--k")
    plt.ylabel("Energy (Ha)")
    plt.xlabel(f"{args.param}")
    plt.tight_layout()

    if args.preview:
        plt.show()
    else:
        plt.savefig("out.pgf")

if __name__ == "__main__":
    main()




