
import ray
# import matplotlib.pyplot as plt
from time import time
from pathlib import Path

save_dir = Path(__file__).parent
times = []
num_steps = [1000, 1000, 10_000, 100_000, 1_000_000]
pi_estimates = []

ray.init()

@ray.remote
def step(x):
    return [(1 / (1 + val ** 2)) for val in x]

for i, N in enumerate(num_steps):
    start = time()

    x_vals = [j / (N - 1) for j in range(N)]

    num_chunks = 100
    chunk_size = len(x_vals) // num_chunks
    chunks = [x_vals[j:j + chunk_size] for j in range(0, len(x_vals), chunk_size)]

    futures = [step.remote(chunk) for chunk in chunks]
    result = sum(sum(ray.get(futures), []))

    result *= 4 / N 
    if i != 0:
        pi_estimates.append(result)
        times.append(time() - start)

num_steps.pop(0)
output_file = save_dir / "results.txt"
#Saving to a txt file because the ray workers don't have packages. I tried adding packages but it didn't work.
with open(output_file, "w") as f:
    for t, pi, n in zip(times, pi_estimates, num_steps):
        print(f"Pi estimate of {n} steps: {pi}. Took {t:.3f} seconds\n")
        f.write(f"{n} {pi} {t:.3f}\n")

# plt.figure()
# plt.title("Time per calculation")
# plt.xlabel("# of steps")
# plt.ylabel("Time (seconds)")
# plt.bar(x=[str(n) + " steps" for n in num_steps],height=times)
# plt.savefig(save_dir/"performance.png")



