import numpy as np
import matplotlib.pyplot as plt 

if __name__ == "__main__":
    # FRAC_THROTTLED = [0.0, 0.2, 0.4, 0.6, 0.8]

    # UNIFORM_AVG_LATENCY_DOR = [44.55, 68.4657, 75.9165, 80.818, 87.9356]
    # UNIFORM_AVG_LATENCY_ADAPTIVE = [44.3853, 67.072, 77.0165, 86.8438, 95.8693]

    # BITCOMP_AVG_LATENCY_DOR = [61.4582, 109.35, 138.744, 153.822, 169.749]
    # BITCOMP_AVG_LATENCY_ADAPTIVE = [62.8725, 114.07, 151.061, 174.312, 197.364]

    # plt.plot(FRAC_THROTTLED, UNIFORM_AVG_LATENCY_DOR, label='DOR (uniform)', color='red', marker='o', linestyle='dashed')
    # plt.plot(FRAC_THROTTLED, UNIFORM_AVG_LATENCY_ADAPTIVE, label='MIN-ADAPT (uniform)', color='red', marker='x', linestyle='solid')

    # plt.plot(FRAC_THROTTLED, BITCOMP_AVG_LATENCY_DOR, label='DOR (bitcomp)', color='green', marker='o', linestyle='dashed')
    # plt.plot(FRAC_THROTTLED, BITCOMP_AVG_LATENCY_ADAPTIVE, label='MIN-ADAPT (bitcomp)', color='green', marker='x', linestyle='solid')

    # plt.legend()
    # plt.xlabel('Fraction of throttled nodes')
    # plt.ylabel('Average Latency')
    # plt.savefig('throttleRate_vs_latency.png')
    INJECTION_RATE = [0.10, 0.20, 0.30, 0.40, 0.50]
    UNIFORM_DETERMINISTIC_LATENCY_AVG = [40.3821, 46.8471, 57.9138, 77.9185, 183.211]
    UNIFORM_ADAPTIVE_LATENCY_AVG = [40.6485, 47.3605, 60.6008, 140.438, 1049.06]

    INJECTION_RATE2 = [0.10, 0.20, 0.30]
    BITCOMP_ADAPTIVE_LATENCY_AVG = [48.3697, 77.2004, 422.473]
    BITCOMP_DETERMINISTIC_LATENCY_AVG = [47.1191, 95.007, 750.382]

    plt.plot(INJECTION_RATE, UNIFORM_ADAPTIVE_LATENCY_AVG, label='adaptive (uniform)', color='red', marker='x', linestyle='solid')
    plt.plot(INJECTION_RATE, UNIFORM_DETERMINISTIC_LATENCY_AVG, label='deterministic (uniform)', color='red', marker='o', linestyle='dashed')

    plt.plot(INJECTION_RATE2, BITCOMP_ADAPTIVE_LATENCY_AVG, label='adaptive (bitcomp)', color='green', marker='x', linestyle='solid')
    plt.plot(INJECTION_RATE2, BITCOMP_DETERMINISTIC_LATENCY_AVG, label='deterministic (bitcomp)', color='green', marker='o', linestyle='dashed')
    plt.legend()
    plt.xlabel('Flit injection rate')
    plt.ylabel('Average latency')
    plt.savefig('injectionRate_vs_latency.png')