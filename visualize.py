import matplotlib.pyplot as plt
from pathlib import Path
save_dir = Path(__file__).parent 
results = save_dir/ "results.txt"



with open(results, "r") as f:
    results = f.read()

results = [x.split(" ") for x in results.split("\n")][:-1] # [[p, n, s],[p, n, s]]
print(results)

num_steps  = [x[0] for x in results]
ps= [x[1] for x in results]
times = [float(x[2]) for x in results]

# print(ps)
# print(ns)
# print(ss)

plt.figure()
plt.title("Time per calculation")
plt.xlabel("# of steps")
plt.ylabel("Time (seconds)")
# plt.ylim(0, max(times))
plt.bar(x=[str(n) + " steps" for n in num_steps],height=times)
plt.savefig(save_dir/"performance.png")
