# Segmention Evaluation Pipeline for CT Volumes

This repository contains a Python pipeline to evaluate synthetic CT (sCT) scans against ground-truth CT scans. It processes NIfTI (.nii.gz) files, converts them to STL meshes, and evaluates anatomical regions of the skull.

## Project Structure


- **extract_skull.py**: Converts region of interest to surface meshes (.stl).
- **eval_skull.py**: Evaluates real vs. synthetic skull meshes
- **summary.py**: Writes CSV files results and generates bar plots for metrics.
- **my_io.py**: I/O utilities for NIfTI and STL file handling.
- **mesh_ops.py**: Mesh processing utilities.
- **region_split.py**: Assigns anatomical regions to skull vertices.
- **ct_config.yaml**: Configuration 
 **Dice.py**: Computes Dice similarity coefficients between real and synthetic CT scans for more evaluation.
## Prerequisites

- **Python**: 3.8 or higher

Copy
SimpleITK==2.3.1
numpy==1.26.4
nibabel==5.2.1
trimesh==4.4.9
scikit-image==0.24.0
scipy==1.14.1
pandas==2.2.2
matplotlib==3.9.2
pyyaml==6.0.2

work_dir: /path/to/working/directory

ct_real_dir: /path/to/GT_CTs

ct_synth_dir: /path/to/s_CTs

hu_thresh: 300

n_sample: 10000

work_dir: Directory for output meshes and CSV files.

ct_real_dir: Path to real CT scans.

ct_synth_dir: Path to synthetic CT scans.

hu_thresh: Hounsfield Unit threshold for skull segmentation.

n_sample: Number of points to sample for mesh evaluation.

Prepare Input Data: Place your .nii.gz files in the directories specified in ct_config.yaml.
