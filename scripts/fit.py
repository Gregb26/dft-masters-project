"""
fit.py

Fits a model to given data.

Usage:
    python fit.py --param PARAM --fit FIT, in the directory with *GSR.nc file to analyze

Inputs:
    *GSR.nc files, --param: ecut, nkpt, volume, --fit: murnaghan, birch-murnaghan, lorentzian, --preview: yes, no

Outputs:
    Best fit parameters, covriance matrix, plot of data + fit

Dependencies:
    numpy, matplotlib, natsort, scipy, abinit_tools, abipy
"""

import numpy as np
import argparse
import glob

from natsort import natsorted
from abinit_tools.reader import read_files
from abinit_tools.plot_config import setup
from scipy.optimize import curve_fit

# defining common fit functions
def murnaghan(V, V_0, E_0, B_0, B_1):
    """
    Murnaghan equation of state establishing the relationship between the volume and the pressure of a body.
    Inputs:
        V: Volume
        V_0: Volume at equilibrium (usually what we want to extract from this fit)
        E_0: Energy at equilibrium
        B_0: Bulk modulus at ambient pressure
        B_1: First derivative of the bulk modulus at ambient pressure
    Output:
        total energy E(V)
    """
    return E_0 + B_0*V_0*((1 / (B_1*(B_1 - 1)))*(V/V_0)**(1-B_1) + V / (B_1*V_0) - 1 /(B_1 -1) )

def birch_murnaghan(V, V_0, E_0, B_0, B_1):
    """
    Birch-Murnaghan equation of state establishing the relationship between the volume and the pressure of a body.
    More precise than the Murnaghan equation of state.
    Inputs:
        V: Deformed volume
        V_0: Volume at equilibrium (usually what we want to extract from this fit)
        E_0: Energy at equilibrium
        B_0: Bulk modulus at ambient pressure
        B_1: First derivative of the bulk modulus at ambient pressure
    Outputs:
        total energy E(V).
    """
    return E_0 + (9*V_0*B_0/16)*(((V_0/V)**(2/4)-1)**3*B_1+((V_0/V)**(2/3)-1)**2*(6-4*(V_0/V)**(2/3)))

def lorentzian(x, a, b, c):
    """
    Lorentzian function.
    Inputs:
        x: data
        a: intensity scaling
        b: center of peak
        c: full width at half maximum (FWHM)
    Outputs:
        Lorentzian function evaluated at x
    """
    return (a/np.pi)*((c/2)/((x-b)**2+(c/2)**2))

def fit_curve(x_data, y_data, fit=lorentzian):
    """
    Fits a curve to the data using scipy.optimize.curve_fit and returns optimal parameters.
    Inputs:
        x_data: 1xN array
        y_data: 1xN array
        fit: function: type of fit to perform. Default is lorentzian.
    Outputs: array: array of optimal parameters
    """
    # initial guess required by scipy.optimize.curve_fit
    if fit == lorentzian:
        p0 = [min(y_data), x_data[np.argmin(y_data)], 1.0]
    elif fit in [murnaghan, birch_murnaghan]:
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--param", required=True, help="Parameter to extract from file: ecut, volume, nkpt")
    parser.add_argument("--fit", required=True, help="Type of fit to perform: murnaghan, birch-murnaghan, lorentzian" )
    parser.add_argument("--preview", choices=['no', 'yes'], default='no', help="Display the plot interactively: yes, no. Default is no")
    args = parser.parse_args()

    files = natsorted(glob.glob("*GSR.nc"))
    energy, params = read_files(files, args.param)

    fit_dispatch = {
        "lorentzian": lorentzian,
        "murnaghan": murnaghan,
        "birch-murnaghan": birch_murnaghan
    }

    if args.fit not in fit_dispatch:
        raise ValueError(f"Unknown fit type '{args.fit}'")

    fit_func = fit_dispatch[args.fit]
    popt, pcov = fit_curve(params, energy, fit=fit_func)

    print("Optimal parameters: ", popt)
    print("Covariance matrix: ", pcov)

    # Plot
    plt = setup(use_pgf=(args.preview == "no"))

    x_fit = np.linspace(min(params), max(params), 200)
    y_fit = fit_func(x_fit, *popt)

    plt.plot(params, energy, 'ok', label='Data')
    plt.plot(x_fit, y_fit, '-k', label='Fit')
    plt.xlabel(args.param)
    plt.ylabel("Energy (Ha)")
    plt.legend()
    plt.title(f"{args.fit} fit")
    plt.tight_layout()
    plt.savefig("out.pgf")

    if args.preview == 'yes':
        plt.show()

if __name__ == "__main__":
    main()
