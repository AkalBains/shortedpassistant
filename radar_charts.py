import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

def generate_radar_charts(trait_data):
    radar_images = []

    categories = list(trait_data.columns[1:])  # First column might be Name or ID
    N = len(categories)

    for _, row in trait_data.iterrows():
        values = row[1:].values.flatten().tolist()
        values += values[:1]  # close the circle

        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)

        ax.plot(angles, values, linewidth=2, linestyle='solid')
        ax.fill(angles, values, alpha=0.4)

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        radar_images.append(buf)

        plt.close(fig)

    return radar_images

