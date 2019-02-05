import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches


def make_m2l_plot():
    plt.close('all')
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111)
    o = np.array([0, 0])
    oprime = np.array([0.5, 1.5])
    r = 0.5
    theta_o1 = 7*np.pi/8
    theta_o2 = np.pi/6.0
    #vector from origin to oprime.
    o2op = oprime-o
    lo2op = np.sqrt((o2op[0]**2) + (o2op[1]**2))
    #origin
    ax.plot(o[0], o[1], color='k', marker='o', markersize=12)
    plt.text(o[0]+0.05, o[1]+0.05, r"$O$", fontsize=12)
    #cluster about origin1
    circ1 = mpatches.Circle((o[0], o[1]), radius=r, color='k', fill=False, linestyle='--')
    ax.add_patch(circ1)
    #radius about origin1
    #rho_{max}
    ax.arrow(o[0], o[1], 0.8*r*np.cos(theta_o1), 0.8*r*np.sin(theta_o1), 
            head_width=0.05, head_length=0.1, fc='k', ec='k')
    plt.text(o[0]-0.3, o[1]+0.15, r"$\rho_{max}$", fontsize=12)
    #origin 2
    ax.plot([oprime[0]], [oprime[1]], color='k', marker='o', markersize=12)
    plt.text(oprime[0], oprime[1]+0.1, r"$\mathbf{r}_{0}$", fontsize=12)
    #Cluster around origin 2
    circ2 = mpatches.Circle((oprime[0], oprime[1]), radius=r, color='k', 
    fill=False, linestyle='--')
    ax.add_patch(circ2)
    #radius about origin2
    #rho_{max}
    ax.arrow(oprime[0], oprime[1], 0.80*r*np.cos(theta_o2), 0.8*r*np.sin(theta_o2), 
            head_width=0.05, head_length=0.1, fc='k', ec='k')
    plt.text(oprime[0]+0.3, oprime[1]+0.1, r"$\rho_{max}$", fontsize=12)
    #line connecting origin 1 to circle around r0:
    theta = np.arctan((oprime[1]-o[1])/(oprime[0]-o[0]))
    #distance between origin to circle around oprime:
    dr = lo2op - r
    r = np.linspace(0, dr, num=200)
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    plt.plot(x, y, linestyle='-.', color='0.5')
    plt.text(x[115]+0.01, y[115], r"$\chi\rho_{max}$", fontsize=12)
    plt.arrow(x[-2], y[-2], x[-1]-x[-2], y[-1]-y[-2], head_width=0.05, head_length=0.1,
            length_includes_head=True, fc='0.5', ec='0.5')
    ax.set_xlim(-1, 2)
    ax.set_ylim(-1, 2)
    ax.set_axis_off()
    plt.show()