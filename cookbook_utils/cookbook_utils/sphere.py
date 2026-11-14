"""Classes and functions for sphere elements"""

import numpy as np
import matplotlib.pyplot as plt

from cookbook_utils.vector3d import Vector3D


def great_circle(lon, r=1, lat_range=(-90,90), density=90):
    """Returns x, y, z coordinates for a Great Circle"""
    return list(zip(*[Vector3D.from_geographic(phi, lon).vector for phi in np.linspace(-90., 90., 90)]))


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
            
        ax.plot(self.x, self.y, self.z, c=color, ls=ls, **kwargs)


class Horizon:
    """Generates and plots horizon for a sphere"""

    def __init__(self, elev=None, azim=None, ax=None):
        if not ax:
            ax = plt.gca()
            
        self.tangent = Vector3D.from_spherical(ax.elev, 180+ax.azim, name="t", degrees=True)
        self.observation = Vector3D.from_geographic(ax.elev, ax.azim, name='o')

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


class Axis(Vector3D):
    """Creates an axis class for plotting on a 3D projection"""

    axis_coords = {
        "x": (1, 0, 0),
        "y": (0, 1, 0),
        "z": (0, 0, 1),
        }
    
    def __init__(self, name, length=1.5):
        """Initialize an instance of the axis class

        Arguments:
          name : name of axis from "x", "y", "z"
          length : length of axis, default is 1.5

        Returns:
          Axis class object
        """
        super().__init__(*np.array(self.axis_coords[name])*length, name=name)

    def plot(self, ax=None, color='k', add_label=True, label_position='end', zorder=3):
        if not ax:
            ax = plt.gca()
            super().plot(ax, c=color, add_label=add_label,
                         label_position=label_position, zorder=zorder)


class Equator():
    """Creates an Equator object for plotting a sphere"""

    def __init__(self, horizon: Horizon):
        horizon_at_equator = horizon.get_tangent_point(np.radians(-90))

        xe0, ye0, ze0 = list(zip(*[
            horizon_at_equator.rotate('z', rho).vector for rho in np.linspace(-np.pi, 0)
        ]))
        self.x_front = xe0
        self.y_front = ye0
        self.z_front = ze0

        xe1, ye1, ze1 = list(zip(*[
            horizon_at_equator.rotate('z', rho).vector for rho in np.linspace(0,np.pi)
        ]))
        self.x_back = xe1
        self.y_back = ye1
        self.z_back = ze1

    def plot(self, ax=None, frontcolor='r', backcolor='r',
             front_linestyle='-', back_linestyle='--',
             zorder=0):
        if not ax:
            ax = plt.gca()
            
        ax.plot(
            self.x_front,
            self.y_front,
            self.z_front,
            c=frontcolor,
            ls=front_linestyle,
            zorder=zorder
        )
        
        ax.plot(
            self.x_back,
            self.y_back,
            self.z_back,
            c=backcolor,
            ls=back_linestyle,
            zorder=zorder,
            alpha=0.3
        )
