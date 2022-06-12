import operator
import math
import random
import numpy  as np
from matplotlib import pyplot

## X
x = np.linspace(0, 50).tolist()

## Function
func = lambda x: 50*((x*2)+(x*3)+(x*(x-1)*3))

## Y
y = np.empty(len(x))
for i in range(len(x)): y[i] = func(y[i])

## Create Graph
fig, ax = pyplot.subplots(figsize=(15,4))
ax.scatter(x, y)

## Set Labels
ax.set_xlabel('Users')
ax.set_ylabel('Requests')
ax.set_title('Data set')

pyplot.show()
