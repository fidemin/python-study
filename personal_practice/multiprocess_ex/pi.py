import random
import time

def estimate_nbr_points_in_quater_circle(nbr_estimates):
    nbr_trials_in_quater_unit_circle = 0
    for step in range(int(nbr_estimates)):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        is_in_unit_circle = x * x + y * y <= 1.0
        nbr_trials_in_quater_unit_circle += is_in_unit_circle

    return nbr_trials_in_quater_unit_circle


if __name__ == "__main__":
    nbr_points = 10000000
    t1 = time.time()
    pi_estimate = estimate_nbr_points_in_quater_circle(nbr_points) / nbr_points * 4
    print("Estimaed pi", pi_estimate)
    print("Delta:", time.time() - t1)
