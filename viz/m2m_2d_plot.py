"""A plot showing the geometry and configuration used in deriving the M2M 
operation."""
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches 


def make_m2m_plot():
    plt.close('all')
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111)
    o = np.array([1, -1.5])
    oprime = np.array([-0.35, -1.25])
    r0 = oprime - o
    r = np.array([-1, 1]) - o
    #origin 1
    ax.plot([1], [-1.5], color='k', marker='o', markersize=12)
    plt.text(1.00, -1.65, r"$O$", fontsize=12)
    #origin 2
    ax.plot([oprime[0]], [oprime[1]], color='k', marker='o', markersize=12)
    plt.text(oprime[0]-0.15, oprime[1]-0.15, r"$O'$", fontsize=12)
    #Cluster around origin 2
    circ2 = mpatches.Circle((oprime[0], oprime[1]), radius=0.5, color='k',
     fill=False, linestyle='--')
    ax.add_patch(circ2)
    #r0
    ax.arrow(o[0], o[1], 0.92*r0[0], 0.92*r0[1], head_width=0.05, 
    head_length=0.1, fc='k', ec='k')
    plt.text(0.5*r0[0]+o[0], 0.5*r0[1]+o[1], r"$\mathbf{r}_{0}$", fontsize=12)
    #rho_{max}
    ax.arrow(oprime[0], oprime[1], -np.sqrt(0.3)/2, np.sqrt(0.3)/2, 
    head_width=0.05, head_length=0.1, fc='k', ec='k')
    plt.text(oprime[0]-0.3, oprime[1]+0.15, r"$\rho$", fontsize=12)
    #r
    ax.arrow(o[0], o[1], r[0], r[1], head_width=0.05, head_length=0.1, fc='k', ec='k')
    plt.text(0.5*r[0]+o[0], 0.5*r[1]+o[1], r"$\mathbf{r}$", fontsize=12)
    ax.plot([1.04*r[0] + o[0]], [1.04*r[1] + o[1]], marker='o', markersize=12)
    #(r-r0)
    ax.arrow(oprime[0], oprime[1], 1.02*(r[0]-r0[0]), 0.97*(r[1]-r0[1]), 
    head_width=0.05, head_length=0.1, fc='k', ec='k')
    plt.text(0.5*(r[0]-r0[0])+oprime[0]-.4, 0.5*(r[1]-r0[1])+oprime[1], 
    r"$\mathbf{r}-\mathbf{r}_{0}$", fontsize=12)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_axis_off()
    plt.show()
