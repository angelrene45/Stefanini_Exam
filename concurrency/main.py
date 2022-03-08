import multiprocessing as mp

num_cores = mp.cpu_count()
pool = mp.Pool( num_cores )

print( num_cores )