"""Basic Quad and Octtrees."""
import numpy as np
from itertools import product
from copy import deepcopy


def quad_sort(parray, c):
    parray.sort(kind='heapsort', order='x')
    n_hemi = np.sum(parray['x'] < c[0])
    parray[:n_hemi].sort(kind='heapsort', order='y')
    parray[n_hemi:].sort(kind='heapsort', order='y')
    nq0 = np.sum(parray[:n_hemi]['y'] < c[1])
    nq2 = np.sum(parray[n_hemi:]['y'] < c[1])
    return [(0, nq0), (nq0, n_hemi), (n_hemi, n_hemi + nq2), 
            (n_hemi + nq2, parray.shape[0])]
        
    
def quad_partition(parray, c):
    ns = quad_sort(parray, c)
    plist = []
    for n in ns:
        plist.append(parray[n[0]:n[1]])
    return plist




class MemConsNode(object):
    
    def __init__(self, tree_dict, p, l=0, num=0):
        super(MemConsNode, self).__init__()
        #first entry into tree
        self.mpoles = np.zeros(p, dtype=np.complex128)
        self.lexp = np.zeros(p, dtype=np.complex128)
        tree_dict[l][num] = self

    @staticmethod
    def get_parent_num(num, d):
        return num >> d

    @staticmethod
    def get_children_nums(num, d):
        out = []
        for j in range(0, 2**d):
            out.append((2**d)*num + j)
        return out

    @staticmethod
    def _get_nums(num, d):
        bin_rep = np.binary_repr(num)
        ns = ['']*d
        k = 0
        while len(bin_rep) > 0:
            ns[k] = bin_rep[-1] + ns[k]
            bin_rep = bin_rep[:-1]
            k = (k+1)%d
        #scrub ns, change into ints 
        for i in range(d):
            if ns[i] == '':
                ns[i] = 0
            else:
                ns[i] = int(ns[i], 2)
        ns.reverse()
        return ns

    @staticmethod
    def get_center(l, num, d):
        ns = MemConsNode._get_nums(num, d)
        for i in range(len(ns)):
            ns[i] = (2**-l)*(ns[i] + 0.5)
        ns = np.array(ns)
        return ns


    @staticmethod
    def get_neighbor_list(l, num, d, c=1):
        ns = MemConsNode._get_nums(num, d)
        ns2 = deepcopy(ns)
        for i in range(len(ns)):
            ns[i] = []
            if ns2[i] >= c and ns2[i] < (2**(l*d)-1 - c):
                for j in range(-1*c, c+1, 1):
                    ns[i].append(ns2[i]+j)
            elif ns2[i] < c:
                for j in range(-1*ns2[i], c+1, 1):
                    ns[i].append(ns2[i] + j)
            else:
                #s < (2**(l*d) - c)
                for j in range(-1*c, 2**(l*d) -1 - ns2[i]):
                    ns[i].append(ns2[i] + j)
        neighs = []
        for pn in list(product(*ns)):
            nl = []
            neigh_num = ''
            for i in range(d):
                nl.append(np.binary_repr(pn[i], l+1))
            #interleave
            for j in range(l+1):
                for i in range(d):
                    neigh_num = neigh_num + nl[i][0]
                    nl[i] = nl[i][1:]
            a = int(neigh_num, 2)
            if a != num:
                neighs.append(a)
        return neighs

    @staticmethod
    def get_ilist(l, num, d, c=1):
        #get parent neighbors
        pn = MemConsNode.get_parent_num(num, d)
        pn = MemConsNode.get_neighbor_list(l-1, pn, d, c=c)
        #get parent neighbors children
        pnc = []
        for p in pn:
            ch = MemConsNode.get_children_nums(p, d)
            while(len(ch)>0):
                pnc.append(ch.pop())
        #get complement of pnc with respect to node neighbors
        nn = MemConsNode.get_neighbor_list(l, num, d, c=c)
        ilist = []
        for ch in pnc:
            if ch not in nn:
                ilist.append(ch)
        return ilist



class MemLibNode(MemConsNode):

    def __init__(self, tree_dict, p, d, max_depth, l=0, num=0):
        super(MemLibNode, self).__init__(tree_dict, p, l=l, num=num)
        if l != 0:
            self.parent = self.get_parent_num(num, d)
            self.neighs = self.get_neighbor_list(l, num, d)
            self.ilist = MemConsNode.get_ilist(l, num, d, c=1)
        if l < max_depth-1:
            self.children = self.get_children_nums(num, d)
        else:
            self.children = None
        self.center = self.get_center(l, num, d)


class Cons2dNode(MemConsNode):

    def __init__(self, tree_dict, parray, max_depth, mnum, l=0, num=0):
        super(Cons2dNode, self).__init__(tree_dict, mnum, l=l, num=num)
        if l < max_depth - 1:
            self.parray = None
            self.refine(tree_dict, parray, max_depth, mnum, l, num)
        else:
            self.parray = parray

    def refine(self, tree_dict, parray, max_depth, mnum, l, num):
        child_part = quad_partition(parray, self.get_center(l, num, 2))
        nums = self.get_children_nums(num, 2)
        for i in range(len(nums)):
            if child_part[i].shape[0] > 0:
                Cons2dNode(tree_dict, child_part[i], max_depth, mnum, 
                num=nums[i], l=l+1)


class Lib2dNode(MemLibNode):

    def __init__(self, tree_dict, parray, max_depth, mnum, l=0, num=0):
        super(Lib2dNode, self).__init__(tree_dict, mnum, 2, 
                                        max_depth, l=l, num=num)
        if l < max_depth - 1:
            self.parray = None
            self.refine(tree_dict, parray, max_depth, mnum, num, l)
        else:
            self.parray = parray
        
    def refine(self, tree_dict, parray, max_depth, mnum, num, l):
        child_part = quad_partition(parray, self.center)
        for i in range(len(self.children)):
            if child_part[i].shape[0] > 0:
                Lib2dNode(tree_dict, child_part[i], max_depth, mnum, 
                l=l+1, num=self.children[i])