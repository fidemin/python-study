#from multiprocessing.dummy import Pool # for thread
from multiprocessing import Pool # for parallel
import time

#from pi import estimate_nbr_points_in_quater_circle  # using loop
from pi_numpy import estimate_nbr_points_in_quater_circle # using numpy


if __name__ == "__main__":
    nbr_samples_in_total = 1e7
    nbr_parallel_blocks = 2
    pool = Pool(processes=nbr_parallel_blocks)
    nbr_samples_per_worker = nbr_samples_in_total / nbr_parallel_blocks
    print("Making {} sample per worker".format(nbr_samples_per_worker))
    nbr_trials_per_process = [nbr_samples_per_worker] * nbr_parallel_blocks
    t1 = time.time()
    nbr_in_unit_circles = pool.map(estimate_nbr_points_in_quater_circle, nbr_trials_per_process)
    pi_estimate = sum(nbr_in_unit_circles) * 4 / nbr_samples_in_total
    print("Estimaed pi", pi_estimate)
    print("Delta:", time.time() - t1)
