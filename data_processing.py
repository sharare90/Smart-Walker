import numpy as np
import matplotlib.pyplot as plt

file_address = 'logs/user2.txt'
file_output_address = 'np/' + file_address[file_address.index('/'):]
output_file = open(file_output_address, 'w')

with open(file_address) as f:
    titles = f.readline().replace(" ", "").split(",")[1:]
    for line in f:
        output_file.write("".join(line.split(',')[1:]))

output_file.close()

data = np.loadtxt(file_output_address)

for i in range(12):
    plt.title(titles[i])
    plt.xlabel('time')
    plt.ylabel(titles[i])

    plt.plot(data[:, i])
    plt.show()
