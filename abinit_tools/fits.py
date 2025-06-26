import numpy as np

# common fit functions
def lorentzian(x, a, b, c):
    """
    Lorentzian function.
    Inputs:
        x: data
        a: intensity scaling
        b: center of peak
        c: full width at half maximum (FWHM)
    Outputs:
        Lorentzian function evaluated at x.
    """
    return (a/np.pi)*((c/2)/((x-b)**2+(c/2)**2))

def gaussian(x, mu, sigma):
    """
    Univariate Gaussian function.
    Inputs:
        x: data
        mu: mean (center of peak)
        sigma: standard deviation (spread)
    Returns
        Gaussian fucntion evaluated at x.
    """
    return np.exp(-(x-mu)**2/(2*sigma**2))/np.sqrt(2*np.pi*sigma**2)

# equation of states
def murnaghan(V, V_0, E_0, B_0, B_1):
    """
    Murnaghan equation of state establishing the relationship between the energy and volume of a body.
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
    Birch-Murnaghan equation of state establishing the relationship between the energy and the volume of a body.
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
