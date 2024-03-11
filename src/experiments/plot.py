import numpy as np
import matplotlib.pyplot as plt 

if __name__ == "__main__":
    CHANNEL_WIDTHS = [320, 384, 448, 512, 576, 640, 704]
    AVG_LATENCY_DOR = [119.174, 101.207, 89.6132, 80.156, 76.5802, 85.822, 131.057]
    AVG_LATENCY_ADAPTIVE = [118.635, 103.495, 94.7429, 82.9253, 80.2566, 82.593, 100.237]
    plt.plot(CHANNEL_WIDTHS, AVG_LATENCY_DOR, label='DOR')
    plt.plot(CHANNEL_WIDTHS, AVG_LATENCY_ADAPTIVE, label='Adaptive XY')
    plt.legend()
    plt.xlabel('Channel Width')
    plt.ylabel('Average Latency')
    plt.savefig('channelWidth_vs_latency.png')