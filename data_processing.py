
import numpy as np
import matplotlib.pyplot as plt


data = np.loadtxt('logs/data1.txt')
plt.plot((data[:, 1]))
plt.show()

plt.plot(data[:, 2])
plt.show()

plt.plot(data[:, 3])
plt.show()

plt.plot(data[:, 4])
plt.show()


