
import time

import numpy as np

def estimate_nbr_points_in_quater_circle(nbr_samples):
    nbr_samples = int(nbr_samples)
    np.random.seed() # important!!
    xs = np.random.uniform(0, 1, nbr_samples)
    ys = np.random.uniform(0, 1, nbr_samples)
    estimate_nbr_points_in_quater_circle = (xs * xs + ys * ys) <= 1
    nbr_trials_in_quater_unit_circle = np.sum(estimate_nbr_points_in_quater_circle)
    return nbr_trials_in_quater_unit_circle


if __name__ == "__main__":
    nbr_points = 10000000
    t1 = time.time()
    pi_estimate = estimate_nbr_points_in_quater_circle(nbr_points) / nbr_points * 4
    print("Estimaed pi", pi_estimate)
    print("Delta:", time.time() - t1)
