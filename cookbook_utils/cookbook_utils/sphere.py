"""Classes and functions for sphere elements"""

import numpy as np
import matplotlib.pyplot as plt

from cookbook_utils.vector3d import Vector3D


def great_circle(lon, r=1, lat_range=(-90,90), density=90):
    """Returns x, y, z coordinates for a Great Circle"""
    return list(zip(*[Vector.from_geographic(phi, lon).vector for phi in np.linspace(-90., 90., 90)]))


class GreatCircle:

    def __init__(self, lon, r=1, lat_range=(-90.,90), density=90):
        # Split into hemispheres if range crosses
        if not lat_range:
            x1, y1, z1 = great_circle(lon, r=r, lat_range=(-90,90))
            x2, y2, z2 = great_circle(lon+180, r=r, lat_range=(-90,90))
            x = x1 + x2
            y = y1 + y2
            z = z1 + z2
        else:
            x, y, z = great_circle(lon, r=r, lat_range=lat_range)

        self.x = x
        self.y = y
        self.z = z

    def plot(self, ax=None, color='k', ls='-', **kwargs):
        """Plot Great Circle on existing axis"""
        if not ax:
            ax = plt.gca()
            
        ax.plot(self.x, self.y, self.z, c=color, ls=ls)
        
class Horizon:
    """Generates and plots horizon for a sphere"""

    def __init__(self, elev=None, azim=None, ax=None):
        if not ax:
            ax = plt.gca()
            
        self.tangent = Vector.from_spherical(ax.elev, 180+ax.azim, name="t", degrees=True)
        self.observation = Vector.from_geographic(ax.elev, ax.azim, name='o')

    def get_tangent_point(self, rho):
        """Returns tangent point for a given rotation"""
        return self.tangent.rotate(self.observation, rho)

    @property
    def horizon(self):
        """Returns x, y, x arrays for horizon"""
        return list(zip(*[self.get_tangent_point(rho).vector for rho in np.linspace(-2*np.pi, 2*np.pi, 180)]))

    def plot(self, ax=None, color='k', ls='-', lw=1, **kwargs):
        if not ax:
            ax = plt.gca()
            
        x, y, z = self.horizon
        ax.plot(x, y, z, color=color, ls=ls, lw=lw, **kwargs)
        
