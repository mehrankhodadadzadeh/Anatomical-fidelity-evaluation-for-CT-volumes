"""
Mesh utilities: marching-cubes, point sampling, Chamfer, HD95.
"""
import numpy as np
from skimage.measure import marching_cubes
from scipy.spatial import cKDTree
import trimesh

# ------------------------------------------------------------------ #
# 1. binary mask --> surface mesh
# ------------------------------------------------------------------ #
def mask_to_mesh(mask: np.ndarray):
    """Run marching-cubes on a binary mask, return verts & faces."""
    verts, faces, *_ = marching_cubes(mask.astype(np.uint8), level=0)
    return verts, faces


# ------------------------------------------------------------------ #
# 2. uniform point sampling on mesh
# ------------------------------------------------------------------ #
def sample_points(mesh_file: str, n_points: int = 10_000) -> np.ndarray:
    mesh = trimesh.load_mesh(mesh_file, process=False)
    return mesh.sample(n_points)


# ------------------------------------------------------------------ #
# 3. distance metrics
# ------------------------------------------------------------------ #
def chamfer_distance(a: np.ndarray, b: np.ndarray) -> float:
    t1, t2 = cKDTree(a), cKDTree(b)
    return np.mean(t1.query(b)[0]) + np.mean(t2.query(a)[0])


def hausdorff95(a: np.ndarray, b: np.ndarray, percentile: float = 95.0) -> float:
    t1, t2 = cKDTree(a), cKDTree(b)
    d_ab = t1.query(b)[0]
    d_ba = t2.query(a)[0]
    return max(np.percentile(d_ab, percentile), np.percentile(d_ba, percentile))
