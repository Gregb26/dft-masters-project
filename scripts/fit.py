"""
fit.py

Fits a model to given data.

Usage:
    python fit.py --param PARAM --fit FIT --preview yes/no, in the directory with *GSR.nc file to analyze

Inputs:
    *GSR.nc files, --param {ecut, nkpt, volume}, --fit {murnaghan, birch-murnaghan, lorentzian, gaussian}
     --preview {yes, no}

Outputs:
    Best fit parameters, covariance matrix, plot of data + fit

Dependencies:
    abinit_tools abipy natsort numpy, matplotlib, scipy
"""

import numpy as np
import glob
import abinit_tools.fits

from natsort import natsorted
from reader import reader
from abinit_tools.plot_config import setup
from abinit_tools.argparse_utils import parse_args
from scipy.optimize import curve_fit

def fit_curve(x_data, y_data, fit=abinit_tools.fits.lorentzian):
    """
    Fits a curve to the data using scipy.optimize.curve_fit and returns optimal parameters.
    Inputs:
        x_data: 1xN array
        y_data: 1xN array
        fit: function: type of fit to perform. Default is lorentzian.
    Outputs: array: array of optimal parameters
    """
    # initial guess required by scipy.optimize.curve_fit
    if fit == abinit_tools.fits.lorentzian:
        p0 = [min(y_data), x_data[np.argmin(y_data)], 1.0]
    elif fit in [abinit_tools.fits.murnaghan, abinit_tools.fits.birch_murnaghan]:
        V0_guess = x_data[np.argmin(y_data)]  # volume at minimum energy
        E0_guess = min(y_data)
        B0_guess = 0.5  # Ha/Bohr^3 — rough estimate
        B1_guess = 4.0
        p0 = [V0_guess, E0_guess, B0_guess, B1_guess]
    else:
        raise ValueError("Unknown fit function")
    # fit
    popt, pcov = curve_fit(fit, x_data, y_data, p0=p0)
    return popt, pcov

def main():
    args = parse_args(
        description="Fit energy to given parameter.",
        optional_args=[
            {
                "--param": {
                    "help": "Fit energy versus this parameter",
                    "choices": ["ecut", "volume", "nkpt", "acell", "rprim"],
                    "required": True,
                    "type": str,
                }
            },
            {
                "--fit": {
                    "help": "Type of fit to perform",
                    "choices": ["lorentzian", "gaussian", "murnaghan", "birch-murnaghan"],
                    "required": True,
                    "type": str,
                }
            },
            {
                "--preview": {
                    "action": "store_true",
                    "help": "Display the plot on screen, but does not save the plot."
                }
            }
        ]
    )

    files = natsorted(glob.glob("*GSR.nc"))
    energy, params = reader(files, args.param)

    fit_dispatch = {
        "lorentzian": abinit_tools.fits.lorentzian,
        "murnaghan": abinit_tools.fits.murnaghan,
        "birch-murnaghan": abinit_tools.fits.birch_murnaghan,
    }

    if args.fit not in fit_dispatch:
        raise ValueError(f"Unknown fit type '{args.fit}'")

    fit_func = fit_dispatch[args.fit]
    popt, pcov = fit_curve(params, energy, fit=fit_func)

    print("Optimal parameters: ", popt)
    print("Covariance matrix: ", pcov)

    # Plot
    plt = setup(use_pgf= not args.preview)

    x_fit = np.linspace(min(params), max(params), 200)
    y_fit = fit_func(x_fit, *popt)

    plt.plot(params, energy, 'ok', label='Data')
    plt.plot(x_fit, y_fit, '-k', label='Fit')
    plt.xlabel(args.param)
    plt.ylabel("Energy (Ha)")
    plt.legend()
    plt.title(f"{args.fit} fit")
    plt.tight_layout()

    if args.preview:
        plt.show()
    else:
        plt.savefig("out.pgf")

if __name__ == "__main__":
    main()
