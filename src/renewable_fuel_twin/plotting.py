from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_metrics(metrics_csv: Path, fig_dir: Path) -> None:
    """
    Create and save a line plot of total emissions over training steps.
    
    Reads metrics from the CSV at `metrics_csv`, ensures `fig_dir` exists, plots the DataFrame's "total_emissions_tco2e" against "step", and writes the figure to `emissions.png` inside `fig_dir`.
    
    Parameters:
        metrics_csv (Path): Path to the CSV file containing at least "step" and "total_emissions_tco2e" columns.
        fig_dir (Path): Directory where the plot image will be saved; created if it does not exist.
    """
    fig_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(metrics_csv)
    plt.figure()
    plt.plot(df["step"], df["total_emissions_tco2e"])
    plt.title("Emissions")
    plt.savefig(fig_dir / "emissions.png")
    plt.close()
