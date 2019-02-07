"""A set of classes for storing MD data."""
import numpy as np 

parray2d_dtype = [('ids', np.uint16), ('types', np.uint8),
                  ('x', np.float64), ('y', np.float64),
                  ('vx', np.float64), ('vy', np.float64),
                  ('fx', np.float64), ('fy', np.float64)]

p2d = ('x', 'y')
v2d = ('vx', 'vy')
f2d = ('fx', 'fy')

parray3d_dtype = [('ids', np.uint16), ('types', np.uint8),
                  ('x', np.float64), ('y', np.float64), ('z', np.float64),
                  ('vx', np.float64), ('vy', np.float64), ('vz', np.float64),
                  ('fx', np.float64), ('fy', np.float64), ('fz', np.float64)]

p3d = ('x', 'y', 'z')
v3d = ('vx', 'vy', 'vz')
f3d = ('fx', 'fy', 'fz')

class Particles2D(object):

    def __init__(self, bbox, charges, masses, parray, dt):
        super(Particles2D, self).__init__()
        self.dt = dt
        self.charges = charges
        self.masses = masses
        self.parray = parray
        self._scale_coords(bbox)

    @classmethod
    def from_vecs(cls, bbox, charges, masses, ids, types, rs, vs, dt, fs=None):
        if rs.shape[1] == 2:
            parray = np.zeros(ids.shape[0], dtype=parray2d_dtype)
        elif rs.shape[1] == 3:
            parray = np.zeros(ids.shape[0], dtype=parray3d_dtype)
        parray['ids'] = ids
        parray['types'] = types
        parray['x'] = rs[:, 0]
        parray['y'] = rs[:, 1]
        parray['vx'] = vs[:, 0]
        parray['vy'] = vs[:, 1]
        if fs is not None:
            parray['fx'] = fs[:, 0]
            parray['fy'] = fs[:, 0]
        return cls(bbox, charges, masses, parray, dt)

    def _scale_coords(self, bbox):
        ds = bbox[1] - bbox[0]
        for i in range(len(p2d)):
            self.parray[p2d[i]] = (self.parray[p2d[i]] - bbox[0][i])/ds[i]
            self.parray[v2d[i]] = self.parray[v2d[i]]/ds[i]

    def half_step_v(self):
        for t in range(len(self.charges)):
            m = self.parray['types'] == t
            for i in range(len(v2d)):
                self.parray[v2d[i]][m] += 0.5*self.dt*self.parray[f2d[i]][m]/self.masses[t]

    def step_r(self):
        for i in range(len(p2d)):
            self.parray[p2d[i]] = self.parray[p2d[i]] + self.dt*self.parray[v2d[i]]




class Particles3D(object):

    def __init__(self, charges, masses, parray, dt):
        super(Particles3D, self).__init__()
        self.dt = dt
        self.charges = charges
        self.masses = masses
        self.parray = parray

    @classmethod
    def from_vecs(cls, charges, masses, dt, ids, types, rs, vs, fs=None):
        if rs.shape[1] == 2:
            parray = np.zeros(ids.shape[0], dtype=parray2d_dtype)
        elif rs.shape[1] == 3:
            parray = np.zeros(ids.shape[0], dtype=parray3d_dtype)
        parray['ids'] = ids
        parray['types'] = types
        for i in range(len(p3d)):
            parray[p3d[i]] = rs[:, i]
            parray[v3d[i]] = vs[:, i]
        if fs is not None:
            for i in range(len(f3d)):
                parray[f3d[i]] = fs[:, i]
        return cls(charges, masses, parray, dt)

    def _scale_coords(self, bbox):
        ds = bbox[1] - bbox[0]
        for i in range(len(p3d)):
            self.parray[p3d[i]] = (self.parray[p3d[i]] - bbox[0][i])/ds[i]
            self.parray[v3d[i]] = self.parray[v3d[i]]/ds[i]

    def half_step_v(self):
        for t in range(len(self.charges)):
            m = self.parray['types'] == t
            for i in range(len(v3d)):
                self.parray[v3d[i]][m] += 0.5*self.dt*self.parray[f3d[i]][m]/self.masses[t]

    def step_r(self):
        for i in range(len(p3d)):
            self.parray[p3d[i]] = self.parray[p3d[i]] + self.dt*self.parray[v3d[i]]
