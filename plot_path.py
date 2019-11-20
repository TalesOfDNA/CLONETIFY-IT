import matplotlib
from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np

def plot(Xarray, Yarray):
    #Define Plot Figure to be shown
    plt.figure('CLONETIFY-IT ~ MAPPING TRAJECTORY', figsize=(13,13))
    plt.style.use('ggplot')
    plt.suptitle('Cell Trajectory', fontsize=20)
    plt.tight_layout()

    #Convert coordinates into numpy arrays for faster processing
    Xarray = np.array(Xarray)
    Yarray = np.array(Yarray)

    #Define Trajectory to plot
    last_index = len(Xarray)
    mid_index = round(last_index/2)
    half = round(mid_index/2)
    X1 = Xarray[0:half]
    Y1 = Yarray[0:half]
    init = mid_index
    last = last_index-1
    X2 = Xarray[init:last]
    Y2 = Yarray[init:last]

    #Graph 1
    ax1 = plt.subplot(2,1,1)
    plt.plot(X1, Y1, 'bo:')
    plt.title('Segmented Trajectory')
    plt.plot(X1[0], Y1[0], marker='o', markerfacecolor='black', markersize=12)
    plt.plot(X1[half-1], Y1[half-1], marker='o', markerfacecolor='blue', markersize=12)

    #Graph 2
    ax2 = plt.subplot(2,1,2)
    plt.plot(Xarray, Yarray,  "bo:")
    plt.title('Full Trajectory')
    plt.plot(Xarray[0], Yarray[0], marker = 'o', markerfacecolor='black', markersize=12)
    plt.plot(Xarray[last_index-1], Yarray[last_index-1], markerfacecolor='blue', markersize=12, marker='o')

    plt.show()

