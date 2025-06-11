"""
I/O helpers for NIfTI and STL.
"""
import os
import nibabel as nib
import numpy as np
import trimesh


def load_nifti(path: str) -> np.ndarray:
    """Return volume data as float32 numpy array."""
    return nib.load(path).get_fdata().astype(np.float32)


def save_mesh(verts: np.ndarray, faces: np.ndarray, out_path: str) -> None:
    """Write vertices/faces to an STL file."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    trimesh.Trimesh(vertices=verts, faces=faces).export(out_path)
