"""A plot showing the logartihm of the absolute error in 3 multipole expansions
of different order for a point located close to the origin."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def make_2d_mpole_err_plot(rprime, beta, apot_func, pot_func, e_func, 
    lims=[5, 15, 50], cmin=1e-20, cmax=1):
    """A function to generate the error between the exact potential and 3
    multipole approximations of varying order. 
    
    Arguments
    ---------
    rprime : float
        The location of the source charge relative to the origin. For best result
        0 <= rprime <= 0.5
    beta : float
        Angle subtending the vector to the source charge and the unit vector in
        the x direction.
    apot_func : function(complex_float, complex_float, lim)
         The function for approximating the potential at each point in C to 
         order 'lim'
    pot_func : function(np.array, np.array, float, float)
        A function returning the exact potential for a source charge.
    e_func : function(np.array, np.array)
        Function returning some measure between two different arrays.
    lims : optional, list of int
        Which orders of the mpole expansion to test.
    cmin : optional, float
        The smallest error marked by the colorbar.
    cmax : optional, float
        The largest error marked by the colorbar.
    """
    xv = np.linspace(-1, 1, 512)
    yv = np.linspace(-1, 1, 512)
    xx, yy = np.meshgrid(xv, yv)
    z = xx + 1j*yy
    zp = rprime*np.cos(beta) + 1j*rprime*np.sin(beta)
    appxs = []
    for l in lims:
        appxs.append(apot_func(z, zp, l))
    exactp = pot_func(xx, yy, rprime, beta)
    errs = []
    for appx in appxs:
        errs.append(e_func(exactp, appx))
    labels = []
    for l in lims:
        labels.append('p=%d' % l)
    plt.close('all')
    fig, ax = plt.subplots(1, len(lims), figsize=(8*len(lims), 8))
    for i in range(len(lims)):
        v = ax[i].imshow(errs[i], extent=[-1, 1, -1, 1], 
        norm=colors.LogNorm(cmin, cmax))
        ax[i].set_title(labels[i])
    cb = fig.colorbar(v, ax=ax)
    cb.set_label('Error', fontsize=16)
    plt.show()
    

