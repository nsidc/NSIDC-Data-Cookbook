"""Utility functions for plotting figures in grid and projection tutorials"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection


def make_image_grid(img, fwd):

    transform = lambda l: [fwd * p for p in l]
    
    rows, cols = img.shape
    
    r = np.arange(0, rows+1)
    c = np.arange(0, cols+1)
    lines = [np.column_stack([[i,i],[r[0],r[-1]]]) for i in c]
    lines += [np.column_stack([[c[0],c[-1]], [j, j]]) for j in r]
    return [transform(line) for line in lines]


def add_image_grid(img, fwd, ax=None, color=None):
    """Add grid lines around image"""

    if not ax:
        ax = plt.gca()
        
    lines = make_image_grid(img, fwd)    
    ax.add_collection(LineCollection(lines, colors=color))
    return
    
def cell_width_marker(rc, fwd, dimension="width", color="0.7"):
    transform = lambda l: [fwd * p for p in l]

    r, c = rc
    if dimension == "width":
        lines = [np.column_stack([[i,i],[c,c+1]]) for i in [r-1, r]]
    elif dimension == "height":
        lines = [np.column_stack([[r,r+1],[j,j]]) for j in [c-1, c]]
    else:
        raise ValueError
        
    return LineCollection([transform(line) for line in lines], color=color)


def make_width_arrow(rc, fwd, position="left", **kwargs):
    """Define a FancyArrwPatch depending on position"""
    r, c = rc
    if position == "left":
        head_x, head_y = fwd * (r-1,c+.5)
        tail_x, tail_y = fwd * (r-2,c+.5)
    elif position == "right":
        head_x, head_y = fwd * (r,c+.5)
        tail_x, tail_y = fwd * (r+1,c+.5)
    elif position == "top":
        head_x, head_y = fwd * (r+.5,c-1)
        tail_x, tail_y = fwd * (r+.5,c-2)        
    elif position == "bottom":
        head_x, head_y = fwd * (r+.5,c)
        tail_x, tail_y = fwd * (r+.5,c+1)
    else:
        raise ValueError(f"Expected position to be one of 'left', 'right', 'top', 'bottom', "
                         f"got {position} instead")
        
    return mpatches.FancyArrowPatch((tail_x, tail_y), (head_x, head_y), **kwargs)

    
def add_cell_width_marker(rc, fwd, ax=None, dimension="width", color=None, label=None):
    """Adds symbols and text to define cell dimension"""
    if not ax:
        ax = plt.gca()

    r, c = rc
    
    ax.add_collection(cell_width_marker(rc, fwd, dimension=dimension, color="k"))
    if dimension == "width":
        for arrow_position in ["left", "right"]:
            ax.add_artist(
                make_width_arrow(
                    rc, fwd, position=arrow_position, 
                    mutation_scale=10, color="k"
                )
            )
        text_x, text_y = fwd * (r-.5, c+1.5)
        if not label:
            label = r"$\Delta x$"
        ax.text(text_x, text_y, label, va="top", ha="center")
    else:
        for arrow_position in ["top", "bottom"]:
            ax.add_artist(
                make_width_arrow(
                    rc, fwd, position=arrow_position, 
                    mutation_scale=10, color="k"
                )
            )
        text_x, text_y = fwd * (r+1.5, c-.5)
        if not label:
            label = r"$\Delta y$"
        ax.text(text_x, text_y, label, va="center", ha="left")