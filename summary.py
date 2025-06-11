"""
CSV writer + simple bar plot for metrics.
"""
import csv
from collections import defaultdict
import matplotlib.pyplot as plt


def write_csv(rows, header, out_path):
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def barplot_means(csv_path, value_col, group_col, title, out_png):
    import pandas as pd
    df = pd.read_csv(csv_path)
    means = df.groupby(group_col)[value_col].mean()
    means.plot.bar(rot=0)
    plt.title(title)
    plt.ylabel(value_col)
    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.close()
