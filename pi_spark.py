from pyspark.sql import SparkSession
import numpy as np
from pyspark.sql.functions import sum
import matplotlib.pyplot as plt
from time import time
from pathlib import Path

save_dir = Path(__file__).parent
spark = SparkSession.builder.appName("PiSim").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

times = []
num_steps = [1000,1000,10_000,100_000,1_000_000]
pi_estimates = []
spark.range(15).count()
for i, N in enumerate(num_steps):
    start = time()

    rdd = spark.sparkContext.parallelize(np.linspace(0, 1, N), numSlices=2).map(
        lambda x: 1 / (1 + x**2)
    )

    val = rdd.sum()

    val *= 4 / N

    if i != 0:  # Ignoring the dummy loop
        times.append(time() - start)
        pi_estimates.append(val)
spark.stop() #Stopping to avoid print spam
num_steps.pop(0)
for t,pi,n in zip(times,pi_estimates,num_steps):
    print(f"Pi estimate of {n} steps: {pi}. Took {t:.3f} seconds\n")

plt.figure()
plt.title("Time per calculation")
plt.xlabel("# of steps")
plt.ylabel("Time (seconds)")
plt.bar(x=[str(n) + " steps" for n in num_steps],height=times)
plt.savefig(save_dir/"performance.png")



