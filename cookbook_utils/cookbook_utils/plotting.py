"""Plotting and helper functions"""

import matplotlib.pyplot as plt

from cookbook_utils.sphere import Horizon, Equator, Axis, GreatCircle


def add_sphere(
        ax: matplotlib.pylot.Axes=None,
        view_elevation: float=10.,
        view_azimuth: float=30.,
        show_prime_meridian=True,
        add_axes: bool=True,
        show_axis_labels=True,
        axis_length=1.5,
        return_horizon=False
):
    """Creates a three-dimensional plot of a sphere

    Arguments:
      fig : figure for plotting.  If None, then uses current figure
      view_elevation : elevation angle in degrees passed to `view_init` 
      view_azimuth : azimuth angle in degrees passed to `view_init`
      show_prime_meridian : show prime meridian - assume longitude = 0, default True
      add_axes : show x, y, z axes.  Can be True or one of "x", "y", "z". Default True
      show_axis_labels : add labels to axes, default True
      axis_length : set length of cartesian axes
      return_horizon : returns Horizon object

    Returns:
      matplotlib.axes3d

    Notes
    -----
    Current behaviour to return Horizon object is a fix in liew of creating Sphere object.
    """

    if not ax:
        fig = plt.gcf()
        ax = fig.add_subplot(
            1, 1, 1,
            projection='3d',
#            xlim=(-1.,1.),
#            ylim=(-1.,1.),
#            zlim=(-1,1),
#            xlabel='x',
#            ylabel='y',
#            zlabel='z',
            )

    ax.set_xlim(-1,1)
    ax.set_ylim(-1,1)
    ax.set_zlim(-1,1)
    ax.set_aspect('equal')
    ax.view_init(view_elevation, view_azimuth, 0.)

    # Add Horizon
    horizon = Horizon(ax=ax)
    horizon.plot(zorder=1)

    if show_prime_meridian:
        GreatCircle(0., lat_range=(-80.,90)).plot(color='r')
        #GreatCircle(180., lat_range=(-80,90)).plot(color='r', ls='--', alpha=0.5)

    if add_axes:
        
        if isinstance(add_axes, bool):
            show_axes = ["x", "y", "z"]
        elif isinstance(add_axes, str):
            show_axes = list(add_axes)
        elif isinstance(add_axes, (list, tuple)):
            show_axes = list(add_axes)
        else:
            raise ValueError(f"Expects add_axes to be one of bool, 'x', 'y', 'z', "
                             f"or list containing one or all of 'x', 'y', 'z', "
                             f"got {add_axes}")

        if "x" in show_axes:
            xaxis = Axis("x", length=axis_length)
            xaxis.plot(add_label=show_axis_labels)
        if "y" in show_axes:
            yaxis = Axis("y", length=axis_length)
            yaxis.plot(add_label=show_axis_labels)
        if "z" in show_axes:
            zaxis = Axis("z", length=axis_length)
            zaxis.plot(add_label=show_axis_labels)


    equator = Equator(horizon)
    equator.plot(ax=ax)
    
    ax.axis('off')

    if return_horizon:
        return ax, horizon
    else:
        return ax

