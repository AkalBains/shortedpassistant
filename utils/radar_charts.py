# utils/radar_charts.py

import matplotlib.pyplot as plt
import numpy as np
import os
import tempfile

def generate_radar_chart(trait_scores, title):
    labels = list(trait_scores.keys())
    values = list(trait_scores.values())

    # Complete the loop
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color='green', linewidth=2)
    ax.fill(angles, values, color='green', alpha=0.25)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_title(title, size=14, pad=20)

    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.savefig(temp_file.name, bbox_inches='tight')
    plt.close()
    return temp_file.name
