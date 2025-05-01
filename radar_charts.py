"""radar_charts.py – create PNG radar charts for slide 6 (Python 3.9-compatible)
--------------------------------------------------------------------------
`build_radar_charts()` generates the two static radar charts used on slide 6
and returns their file paths.
"""

from pathlib import Path
from typing import Dict, Tuple, Union, Optional
import tempfile
import math

import matplotlib.pyplot as plt
import numpy as np

from trait_scores import split_radar_groups


# ---------------------------------------------------------------------------
# Helper – single radar chart
# ---------------------------------------------------------------------------

def _plot_radar(ax, trait_scores: Dict[str, int]) -> None:
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

def build_radar_charts(
    detailed_ratings: Dict[str, Union[int, str]],
    out_dir: Optional[Union[str, Path]] = None,
) -> Tuple[Path, Path]:
    """Generate two radar-chart PNGs and return their file paths.

    Parameters
    ----------
    detailed_ratings : dict
        Mapping of 24 trait names → rating (1‒5 int or label string).
    out_dir : Path | str | None
        Directory to save the PNG files (created if missing).  If *None*
        a temporary directory is used.
    """

    radar1_data, radar2_data = split_radar_groups(detailed_ratings)

    # ensure output directory exists
    if out_dir is None:
        out_path = Path(tempfile.mkdtemp())
    else:
        out_path = Path(out_dir)
        out_path.mkdir(parents=True, exist_ok=True)

    img1 = out_path / "radar_1.png"
    img2 = out_path / "radar_2.png"

    # Chart 1 – personal characteristics (11 traits)
    fig1, ax1 = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    _plot_radar(ax1, radar1_data)
    fig1.tight_layout()
    fig1.savefig(img1, dpi=110)
    plt.close(fig1)

    # Chart 2 – leadership capabilities (13 traits)
    fig2, ax2 = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    _plot_radar(ax2, radar2_data)
    fig2.tight_layout()
    fig2.savefig(img2, dpi=110)
    plt.close(fig2)

    return img1, img2
