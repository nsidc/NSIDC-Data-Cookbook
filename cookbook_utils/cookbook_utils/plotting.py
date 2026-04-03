"""Plotting and helper functions"""

import matplotlib.pyplot as plt

from cookbook_utils.sphere import Horizon


def add_sphere(
        fig: matplotlib.pylot.Axes=None,
        view_elevation: float=10.,
        view_azimuth: float=30.,
):
    """Creates a three-dimensional plot of a sphere

    Arguments:
      fig : figure for plotting.  If None, then uses current figure
      view_elevation : elevation angle in degrees passed to `view_init` 
      view_azimuth : azimuth angle in degrees passed to `view_init`

    Returns:
      matplotlib.axes3d
    """

    if not fig:
        fig = plt.gcf()

    ax = fig.add_subplot(
        1, 1, 1,
        projection='3d',
        xlim=(-1.,1.), 
        ylim=(-1.,1.), 
        zlim=(-1,1),
        xlabel='x',
        ylabel='y',
        zlabel='z',
    )
    ax.set_aspect('equal')
    ax.view_init(10., 30., 0.)

    # Add Horizon
    horizon = Horizon(ax=ax)
    horizon.plot(zorder=1)

    return ax

