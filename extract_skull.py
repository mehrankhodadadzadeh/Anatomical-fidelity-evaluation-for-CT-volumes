"""
Convert every CT / sCT in the folders to skull surface meshes (.stl).
"""
import os, yaml
import numpy as np
from my_io       import load_nifti, save_mesh
from mesh_ops import mask_to_mesh

def run(cfg):
    for folder, tag in [(cfg['ct_real_dir'], 'real'), (cfg['ct_synth_dir'], 'synth')]:
        for fn in os.listdir(folder):
            if not fn.lower().endswith('.nii.gz'):
                continue
            vol = load_nifti(os.path.join(folder, fn))
            mask = vol > cfg['hu_thresh']
            if mask.sum() == 0:
                print(f"[WARN] empty mask for {fn}")
                continue
            v, f = mask_to_mesh(mask)
            out_name = fn.replace('.nii.gz', f'_{tag}.stl')
            out_path = os.path.join(cfg['work_dir'], 'meshes', out_name)
            save_mesh(v, f, out_path)
            print("✓", out_name)

if __name__ == "__main__":
    cfg = yaml.safe_load(open(os.path.join(os.path.dirname(__file__), 'ct_config.yaml')))
    os.makedirs(os.path.join(cfg['work_dir'], 'meshes'), exist_ok=True)
    run(cfg)
