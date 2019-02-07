import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def particle_plot2d(parray, ntypes):
    ms = []
    cs = []
    labels = []
    for i in range(ntypes):
        ms.append(parray['types'] == i)
        cs.append('C%d' % i)
        labels.append('type %d' % i)
    plt.close('all')
    plt.figure(figsize=(8,8))
    for i in range(ntypes):
        plt.scatter(parray['x'][ms[i]], parray['y'][ms[i]], c=cs[i], 
        label=labels[i])
    plt.legend()
    plt.show()


def get_2dnode_corner(node, l, num):
    c = node.get_center(l, num, 2)
    c = c - (2**-(l+1))
    return c


def get_bbox_dict(tree_dict):
    bbox_dict = {}
    for l in tree_dict.keys():
        bbox_dict[l] = []
        for nk in tree_dict[l].keys():
            bbox_dict[l].append(get_2dnode_corner(tree_dict[l][nk], l, nk))
    return bbox_dict


def quadtree_plot(tree_dict):
    bbox_dict = get_bbox_dict(tree_dict)
    blist = list(bbox_dict.keys())
    blist.reverse()
    plt.close('all')
    fig, ax = plt.subplots(figsize=(8,8))
    for l in blist:
        w = 2**-l
        c = 'C%d' % l
        for box in bbox_dict[l]: 
            sqr = mpatches.Rectangle(box, w, w, fill=False,
            edgecolor=c, linewidth=.5**l)
            ax.add_patch(sqr)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    #plot particles of each node at the maximum depth
    l = len(tree_dict.keys()) - 1
    for k in tree_dict[l].keys():
        plt.scatter(tree_dict[l][k].parray['x'], tree_dict[l][k].parray['y'], 
        s=0.1, c='k')
    plt.show()






