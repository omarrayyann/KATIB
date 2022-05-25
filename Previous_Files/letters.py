from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import csv

x = []
y = []
z = []
letter =raw_input("Give a letter:")
print letter
with open(letter+'.csv','r') as csvfile:
	plots = csv.reader(csvfile, delimiter=' ')
	header = next(plots)
	for row in plots:
		if (float(row[2])>-0.001 and float(row[2])<0.001):
		
			x.append(float(row[1]))
			y.append(-float(row[3]))
		
xmin=np.min(x)
xmax=np.max(x)
ymin=np.min(y)
ymax=np.max(y)
gmax=max((xmax-xmin),(ymax-ymin))
plt.plot((x-xmin)/gmax,(y-ymin)/gmax, label='Loaded from file!')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim([0,1])
plt.ylim([0,1])
plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.show()