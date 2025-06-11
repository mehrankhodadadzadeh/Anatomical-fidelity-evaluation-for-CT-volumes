import os
import SimpleITK as sitk
import numpy as np
import csv

def compute_dice(real_path, synth_path, threshold=300):
    real_img = sitk.ReadImage(real_path)
    synth_img = sitk.ReadImage(synth_path)

    real_np = sitk.GetArrayFromImage(real_img)
    synth_np = sitk.GetArrayFromImage(synth_img)

    real_mask = (real_np > threshold).astype(np.uint8)
    synth_mask = (synth_np > threshold).astype(np.uint8)

    intersection = np.sum(real_mask * synth_mask)
    volume_sum = np.sum(real_mask) + np.sum(synth_mask)

    if volume_sum == 0:
        return 0.0
    return (2.0 * intersection) / volume_sum

# ---- Your test data folders ----
real_dir = r"C:\Users\MK000025\Desktop\CTs_output\novel_eval\GT_CTs"
synth_dir = r"C:\Users\MK000025\Desktop\CTs_output\novel_eval\s_CTs"

output_csv = os.path.join(real_dir, "dice_scores.csv")
rows = []

for file in os.listdir(real_dir):
    if file.endswith(".nii.gz"):
        pid = file.replace(".nii.gz", "")  # e.g., CT1
        real_path = os.path.join(real_dir, file)
        synth_path = os.path.join(synth_dir, f"s{pid}.nii.gz")  # matches sCT1.nii.gz

        if not os.path.exists(synth_path):
            print(f"[MISS] {pid} - synthetic CT not found")
            continue

        dice = compute_dice(real_path, synth_path)
        rows.append([pid, dice])
        print(f"{pid}: Dice = {dice:.4f}")

# Save to CSV
with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "Dice"])
    writer.writerows(rows)

print(f"✅ Dice scores saved to {output_csv}")
