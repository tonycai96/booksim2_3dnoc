#!/usr/bin/env python3
import csv
import os
from pathlib import Path

SIM_OUT_DIR = './sim-out'
CSV_OUT = 'data.csv'

def foo():
    pass

    '''
    res = subprocess.run(["./booksim", "base.cfg"], stdout=subprocess.PIPE, text=True)
    #print(res.stdout)

    # TODO parser
    lines = res.stdout.split('\n')
    start_idx = [i for (i, line) in enumerate(lines) if 'Overall Traffic Statistics' in line][0]

    print(lines[start_idx:])
    '''

def read_file(sim_out_dir, k, packet_size, traffic, rate):
    prefix = Path(sim_out_dir, f'K{k}-S{packet_size}-T{traffic}-R{int(rate*100):03d}')
    stdout_path = prefix.with_suffix('.out')

    with open(stdout_path, 'r') as f:
        lines = f.readlines()

    # check if simulation was unstable; if so, record a NaN for latency
    print(stdout_path)
    if 'unstable' in lines[-3]: return float('NaN')

    summary_start_idx = \
            [i for (i, line) in enumerate(lines) if 'Overall Traffic Statistics' in line][0]
    summary_lines = lines[summary_start_idx:]

    # average latency is in the summary section line 2, column 4
    return float(summary_lines[2].split()[4])


def main():
    assert(os.path.isdir(SIM_OUT_DIR))

    csv_file = open(CSV_OUT, 'w', newline='')
    fieldnames = ['k', 'packet_size', 'traffic', 'rate', 'avg_lat']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # sweep over the following parameters
    for traffic in ['removed_node_uniform']:
        for k in [4]:
            for packet_size in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]:
                for rate in [x/100 for x in range(5, 100, 5)]:
                    avg_lat = read_file(SIM_OUT_DIR, k, packet_size, traffic, rate)
                    writer.writerow({'k': k,
                                     'packet_size': packet_size,
                                     'traffic': traffic,
                                     'rate': rate,
                                     'avg_lat': avg_lat})

    csv_file.close()

if __name__ == '__main__':
    main()
