# import csv
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

# instance paths
path_probe_points = r'C:\Users\nsundholm\Documents\01. My Projects\N19154.00 - CBA Tower\For SimScale\results\cba_probe_all data.csv'
path_simscale_results = r'C:\Users\nsundholm\Documents\01. My Projects\N19154.00 - CBA Tower\For SimScale\results\statisticalData.csv'
path_stories = r'C:\Users\nsundholm\Documents\01. My Projects\N19154.00 - CBA Tower\For SimScale\results\cba_stories.csv'

# function to find closest number in a list 
def closest(lst, K): 
    # k is the key value to search for
    # 1st is the list to searh in
    # returns: index of search list that matches key value
     lst = np.asarray(lst) 
     idx = (np.abs(lst - K)).argmin() 
    #  return lst[idx] 
     return idx

# read in ETABS story definitions
storyData = pd.read_csv(path_stories)
storyElev = storyData['Elevation']

# read in probe points and mesh info
probeData = pd.read_csv(path_probe_points)
x = probeData['x']
xNorm = probeData['xNorm']
y = probeData['y']
yNorm = probeData['yNorm']
z = probeData['z']
zNorm = probeData['zNorm']
areas = probeData['Area']

# read in simscale data
simscaleData = pd.read_csv(path_simscale_results)
avgPressure = simscaleData['AVG']

# create container for element force values
fx = []
fy = []
fz = []

# create container for story forces (list of zeros)
storyFx = [0] * len(storyElev)
storyFy = [0] * len(storyElev)
storyFz = [0] * len(storyElev)

# loop through and calculate forces on area elements
length = len(x)
length2 = len(avgPressure)

for i in range(length):
    fx_add = areas[i]*avgPressure[5*i+4]*xNorm[i]
    fy_add = areas[i]*avgPressure[5*i+4]*yNorm[i]
    fz_add = areas[i]*avgPressure[5*i+4]*zNorm[i]
    fx.append(fx_add)
    fy.append(fy_add)
    fz.append(fz_add)

    # find closest story to map the force to (this should work for trib area)
    ind = closest(storyElev, z[i])

    # add element force to story force
    storyFx[ind] = storyFx[ind] + fx_add
    storyFy[ind] = storyFy[ind] + fy_add
    storyFz[ind] = storyFz[ind] + fz_add

# calculate base shear
baseShearFx = sum(fx)
baseShearFy = sum(fy)
baseShearFz = sum(fz)

baseShearFxstory = sum(storyFx)
baseShearFystory = sum(storyFy)
baseShearFzstory = sum(storyFz)

print(baseShearFx)
print(baseShearFxstory)
print(baseShearFy)
print(baseShearFystory)
print(baseShearFz)
print(baseShearFzstory)

# plt.plot(storyFx,storyElev)
# plt.xlabel('Story Shear')
# plt.ylabel('Story Elevation')
# plt.show()


