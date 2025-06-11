"""
Assign coarse anatomical regions to skull vertices.
Regions: 0=Top, 1=Front, 2=Back, 3=Left, 4=Right
"""

import numpy as np


def skull_regions(points: np.ndarray) -> np.ndarray:
    """
    Parameters
    ----------
    points : (N, 3) array of XYZ coordinates (in mm).

    Returns
    -------
    labels : (N,) int array with values 0-4.
    """
    # centre points and scale to unit cube
    ctr = points.mean(axis=0)
    rel = points - ctr
    rel /= np.max(np.abs(rel), axis=0) + 1e-6  # scale to [-1,1]

    labels = np.empty(len(points), dtype=np.int8)
    for i, (x, y, z) in enumerate(rel):
        if z > 0.33:                 # superior part
            labels[i] = 0            # Top
        elif abs(x) >= abs(y):       # left/right dominate
            labels[i] = 3 if x < 0 else 4
        else:                        # anterior/posterior dominate
            labels[i] = 1 if y > 0 else 2
    return labels
