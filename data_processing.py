
import numpy as np
import matplotlib.pyplot as plt


file_address = 'logs/2017-12-12-21-41-46-192062.txt'
file_output_address = 'np/2017-12-12-21-41-46-192062.txt'
output_file = open(file_output_address, 'w')

with open(file_address) as f:
    f.readline()
    for line in f:
        output_file.write("".join(line.split(',')[1:]))

output_file.close()

data = np.loadtxt(file_output_address)
plt.plot((data[:, 1]))
plt.show()

plt.plot(data[:, 2])
plt.show()

plt.plot(data[:, 3])
plt.show()

plt.plot(data[:, 4])
plt.show()


