#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

#BOOKSIM_EXE = './booksim2/src/booksim'
BOOKSIM_EXE = './src/booksim'
BASE_CFG = './base.cfg'
OUT_DIR = './sim-out'

def run_cmd(booksim_exe, base_cfg, out_dir, k, packet_size, traffic, rate, bad_router):
    prefix = Path(out_dir, f'K{k}-S{packet_size}-T{traffic}-R{int(rate*100):03d}')
    print(f"simulating {prefix}...")

    m_path = prefix.with_suffix('.m')
    stdout_path = prefix.with_suffix('.out')

    # run the command, making the necessary variable subsitutions from base config
    res = subprocess.run([booksim_exe, base_cfg,
                          f'k={k}',
                          f'packet_size={packet_size}',
                          f'traffic={traffic}',
                          f'injection_rate={rate}',
                          f'stats_out={m_path}'],
                          #f'bad_router={bad_router}'],
                          stdout=subprocess.PIPE, text=True)
    # save captured stdout to file
    with open(stdout_path, 'w') as f:
        f.write(res.stdout)

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # sweep over the following parameters
    for k in [4]:
        for packet_size in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]:
            # tornado exhibited some weird results; stick with 'uniform' and 'neighbor' for now
            for traffic in ['removed_node_uniform']:
                for rate in [x/100 for x in range(5, 100, 5)]:
                    run_cmd(BOOKSIM_EXE, BASE_CFG, OUT_DIR, k, packet_size, traffic, rate, 1)


if __name__ == '__main__':
    main()
