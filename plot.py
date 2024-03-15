#!/usr/bin/env python3
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

CSV_FILE = './data.csv'
TRAFFIC_TYPE = 'removed_node_uniform'

# returns a list of (x, y) tuples where x: injection rate, and y: latency
def get_points(key, traffic, k, packet_size):
    # do a full separate pass through the file for each set of points
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        return [(float(row['rate']), float(row[key])) for row in reader \
            if (
                row['traffic'] == traffic and \
                int(row['k']) == k and \
                int(row['packet_size']) == packet_size and \
                # NaN check
                not math.isnan(float(row[key]))
            )]

# make some plots for TRAFFIC_TYPE traffic
# NOTE: easier to define packet_sizes in terms of explicit multipliers
multipliers = [1, 8, 64, 512]

data = {}
for k in [4]:
    data[k] = {}
    # final element is the "multiplier" used for comparison to M3D
    # (lower packet sizes correspond to *higher* channel bandwidth)
    for multiplier in multipliers:
        packet_size = multipliers[-1] / multiplier
        data[k][multiplier] = get_points('avg_lat', TRAFFIC_TYPE, k, packet_size)


fig, ax = plt.subplots()

for k in [4]:
    line_type = '--' if k == 4 else '-'
    for multiplier in multipliers:
        print(data)
        points = data[k][multiplier]
        x, y = list(zip(*points))
        plt.plot(x, y, line_type, label=f'k={k}; {multiplier}X channel BW')

ax.set_xlabel("Flit injection rate")
ax.set_ylabel("Average packet latency (cycles)")
ax.legend(ncol=2)

# reduce margins
fig.tight_layout()


output_dir = 'render'
os.makedirs(output_dir, exist_ok=True)

plt.savefig(f'{output_dir}/latency.pdf')
plt.savefig(f'{output_dir}/latency.png', dpi=600)
plt.savefig(f'{output_dir}/latency.svg', transparent=True)

plt.close()
