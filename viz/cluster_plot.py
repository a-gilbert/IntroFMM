"""Make a 3x1 group of plots demonstrating the difference in computing 
interactions between particles and clusters of particles."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def make_grps(ax_size, rs):
    ax_lc = np.array([ax_size[0], ax_size[1]])
    ax_len = np.array([ax_size[2], ax_size[3]])
    grp1 = np.zeros((5, 2))
    grp2 = np.zeros((5, 2))
    grps = [grp1, grp2]
    c1 = ax_lc + np.array([0.2, 0.2])*ax_len
    c2 = ax_lc + np.array([0.75, 0.75])*ax_len
    cs = [c1, c2]
    for j in range(len(grps)):
        r = rs[j]
        for i in range(grps[j].shape[0]):
            ri = r*np.random.rand()
            ti = 2*np.pi*np.random.rand()
            xi = ri*np.cos(ti)
            yi = ri*np.sin(ti)
            grps[j][i, 0] = xi + cs[j][0]
            grps[j][i, 1] = yi + cs[j][1]
    return grps, cs
        
        
def plot_grps_interaction(ax, grp1, grp2):
    ax.plot(grp1[:, 0], grp1[:, 1], color='k', marker='o', linestyle='None')
    ax.plot(grp2[:, 0], grp2[:, 1], color='k', marker='o', linestyle='None')
    for i in range(grp1.shape[0]):
        for j in range(grp2.shape[0]):
            ax.plot([grp1[i, 0], grp2[j, 0]], 
                    [grp1[i, 1], grp2[j, 1]], color='k')

            
def plot_cluster_interaction(ax, grp1, grp2, c1, r1, c2, r2, 
                             cluster1, cluster2):
    if cluster2 and not cluster1:
        ax.plot(grp1[:, 0], grp1[:, 1], color='k', marker='o', linestyle='None')
        ax.plot(grp2[:, 0], grp2[:, 1], color='gray', marker='o', linestyle='None')
        ax.plot(c2[0], c2[1], color='k', marker='*', linestyle='None')
        for i in range(grp1.shape[0]):
            ax.plot([grp1[i, 0], c2[0]], [grp1[i, 1], c2[1]], color='k')
        circ2 = mpatches.Circle((c2[0], c2[1]), radius=r2, color='k', fill=False, linestyle='--')
        ax.add_patch(circ2)
    if not cluster2 and  cluster1:
        ax.plot(grp2[:, 0], grp2[:, 1], color='k', marker='o', linestyle='None')
        ax.plot(grp1[:, 0], grp1[:, 1], color='gray', marker='o', linestyle='None')
        ax.plot(c1[0], c1[1], color='k', marker='*', linestyle='None')
        for i in range(grp2.shape[0]):
            ax.plot([grp2[i, 0], c1[0]], [grp2[i, 1], c1[1]], color='k')
        circ1 = mpatches.Circle((c1[0], c1[1]), radius=r1, color='k', fill=False, linestyle='--')
        ax.add_patch(circ1)
    if cluster1 and cluster2:
        ax.plot(grp2[:, 0], grp2[:, 1], color='gray', marker='o', linestyle='None')
        ax.plot(grp1[:, 0], grp1[:, 1], color='gray', marker='o', linestyle='None')
        ax.plot(c1[0], c1[1], color='k', marker='*', linestyle='None')
        ax.plot(c2[0], c2[1], color='k', marker='*', linestyle='None')
        ax.plot([c2[0], c1[0]], [c2[1], c1[1]], color='k')
        circ1 = mpatches.Circle((c1[0], c1[1]), radius=r2, color='k', fill=False, linestyle='--')
        circ2 = mpatches.Circle((c2[0], c2[1]), radius=r2, color='k', fill=False, linestyle='--')
        ax.add_patch(circ1)
        ax.add_patch(circ2)
        
        
def lplot_cluster_interaction(ax, grps, cs, rs, cluster1, cluster2):
    plot_cluster_interaction(ax, grps[0], grps[1], cs[0], rs[0], cs[1], rs[1], cluster1, cluster2)

def make_cluster_plot():
    plt.close('all')
    rs = [0.1, 0.1]
    fig, axs = plt.subplots(1, 3, squeeze=False, figsize=(24, 8))
    grps, cs = make_grps([0, 0, 1, 1], rs)
    plot_grps_interaction(axs[0, 0], grps[0], grps[1])
    lplot_cluster_interaction(axs[0, 1], grps, cs, rs, True, False)
    lplot_cluster_interaction(axs[0, 2], grps, cs, rs, True, True)
    titles = ['exact', 'clustered source', 'clustered source and target']
    for i in range(len(axs[0])):
        axs[0, i].set_title(titles[i])
        axs[0, i].set_xlim(0, 1)
        axs[0, i].set_ylim(0, 1)
        axs[0, i].set_axis_off()
    plt.show()