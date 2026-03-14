from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_metrics(metrics_csv: Path, fig_dir: Path) -> None:
    fig_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(metrics_csv)
    plt.figure()
    plt.plot(df["step"], df["total_emissions_tco2e"])
    plt.title("Emissions")
    plt.savefig(fig_dir / "emissions.png")
    plt.close()
