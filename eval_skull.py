import os, yaml, csv
import numpy as np
from mesh_ops import sample_points, chamfer_distance, hausdorff95
from region_split import skull_regions
from summary import write_csv, barplot_means

def metric_pair(mesh_real, mesh_synth, n_pts):
    A = sample_points(mesh_real,  n_pts)
    B = sample_points(mesh_synth, n_pts)
    cd = chamfer_distance(A, B)
    hd = hausdorff95(A, B)
    regA = skull_regions(A)
    regB = skull_regions(B)
    per_region = []
    for r in range(5):
        Ar = A[regA == r]
        Br = B[regB == r]
        if len(Ar) == 0 or len(Br) == 0:
            per_region.append((r, np.nan, np.nan))
            continue
        per_region.append((r, chamfer_distance(Ar, Br), hausdorff95(Ar, Br)))
    return cd, hd, per_region

def run(cfg):
    mesh_dir = os.path.join(cfg['work_dir'], 'meshes')
    gl_rows, reg_rows = [], []
    
    for fn in os.listdir(mesh_dir):
        if not fn.endswith('_real.stl'):
            continue
        pid = fn.replace('_real.stl', '')   # e.g., CT1
        synth_pid = f"s{pid}"               # maps CT1 → sCT1
        m_real = os.path.join(mesh_dir, fn)
        m_synth = os.path.join(mesh_dir, f"{synth_pid}_synth.stl")

        if not os.path.exists(m_synth):
            print(f"[MISS] {pid} synth mesh not found")
            continue

        cd, hd, regs = metric_pair(m_real, m_synth, cfg['n_sample'])
        gl_rows.append([pid, cd, hd])
        for r, cd_r, hd_r in regs:
            reg_rows.append([pid, r, cd_r, hd_r])
        print(f"{pid}: Chamfer={cd:.3f}  HD95={hd:.3f}")

    # Write results
    out_gl  = os.path.join(cfg['work_dir'], 'global_metrics.csv')
    out_reg = os.path.join(cfg['work_dir'], 'region_metrics.csv')
    write_csv(gl_rows,  ['id', 'Chamfer_mm', 'HD95_mm'],             out_gl)
    write_csv(reg_rows, ['id', 'region', 'Chamfer_mm', 'HD95_mm'],   out_reg)

    if reg_rows:
        barplot_means(out_reg, 'Chamfer_mm', 'region',
                      'Mean Chamfer per Skull Region', 
                      os.path.join(cfg['work_dir'], 'chamfer_by_region.png'))

    # Summary
    if gl_rows:
        arr = np.asarray(gl_rows)[:, 1:].astype(float)
        mean_cd, std_cd = arr[:,0].mean(), arr[:,0].std(ddof=1)
        mean_hd, std_hd = arr[:,1].mean(), arr[:,1].std(ddof=1)
        n = len(gl_rows)
        print(f"\n=== Summary over {n} patients ===")
        print(f"Mean Chamfer  = {mean_cd:.2f} ± {std_cd:.2f} mm")
        print(f"Mean HD95     = {mean_hd:.2f} ± {std_hd:.2f} mm")

if __name__ == "__main__":
    cfg = yaml.safe_load(open(os.path.join(os.path.dirname(__file__), 'ct_config.yaml')))
    run(cfg)
