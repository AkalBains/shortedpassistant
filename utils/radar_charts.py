from __future__ import annotations
"""radar_charts.py – create PNG radar charts for slide 6
-------------------------------------------------------
`build_radar_charts()` is the public entry point used by *app.py*.
It takes the full 24‑trait ratings dictionary and an output directory,
then returns two PNG paths that match the placeholder sizes in the template.

Charts are static (matplotlib) and use the library’s default colour cycle so
we don’t need to set explicit colours.
"""

from pathlib import Path
from typing import Dict, Tuple
import tempfile
import math

import matplotlib.pyplot as plt
import numpy as np

from trait_scores import split_radar_groups


# ---------------------------------------------------------------------------
# Helper – single radar chart
# ---------------------------------------------------------------------------

def _plot_radar(ax, trait_scores: Dict[str, int]):
    labels = list(trait_scores.keys())
    values = list(trait_scores.values())

    # close the loop for radar chart
    values.append(values[0])
    angles = np.linspace(0, 2 * math.pi, len(labels), endpoint=False).tolist()
    angles.append(angles[0])

    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=8)


# ---------------------------------------------------------------------------
# Public helper – build both charts and return their paths
# ---------------------------------------------------------------------------

def build_radar_charts(detailed_ratings: Dict[str, int | str], out_dir: Path | None = None) -> Tuple[Path, Path]:
    """Generate two radar-chart PNGs and return their file paths.

    Parameters
    ----------
    detailed_ratings : dict
        Mapping of 24 trait names → rating (1‒5 int or label string).
    out_dir : Path | None
        Directory to save the PNG files (created if missing).  If *None*
        we use a temporary directory and return *Path* objects inside it.

    Returns
    -------
    (Path, Path)
        The file paths for radar_chart_1, radar_chart_2 in that order.
    """

    radar1_data, radar2_data = split_radar_groups(detailed_ratings)

    if out_dir is None:
        out_dir = Path(tempfile.mkdtemp())
    else:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

    out1 = out_dir / "radar_1.png"
    out2 = out_dir / "radar_2.png"

    # Chart #1 – personal characteristics (11 traits)
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    _plot_radar(ax, radar1_data)
    fig.tight_layout()
    fig.savefig(out1, dpi=110)
    plt.close(fig)

    # Chart #2 – leadership capabilities (13 traits)
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    _plot_radar(ax, radar2_data)
    fig.tight_layout()
    fig.savefig(out2, dpi=110)
    plt.close(fig)

    return out1, out2
