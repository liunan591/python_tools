# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

"""
plt.cla() Clear an axis
plt.clf() Clear the entire figure
plt.close() Close a window
"""

def plot(x,y,save_file = None):
    #prepare data x,y
    #create plot
    fig = plt.figure()
    #plot pane
    ax = fig.add_subplot(111) #row-col-num
    #plot content
    ax.plot(x, y, color='lightblue', linewidth=3)
    ax.scatter([2,4,6],[5,15,25],color='darkgreen',marker='^')
    #set axis
    ax.set(xlim=[1, 6.5],ylim=[-1.5,30])
    ax.set(title='An Example Axes',ylabel='Y-Axis',xlabel='X-Axis')
    #save
    if save_file:
        plt.savefig(save_file)
    #show plot
    plt.show()
    



ax1 = fig.add_subplot(221) 
ax3 = fig.add_subplot(212)
lines = ax3.plot(x,y)
ax1.scatter(x,y)
#%%
fig3, axes = plt.subplots(nrows=2,ncols=2)

axes[0,0].bar([1,2,3],[3,4,5]) #Plot vertical rectangles (constant width)
axes[1,0].barh([0.5,1,2.5],[0,1,2]) #Plot horiontal rectangles (constant height)
axes[0,0].axhline(0.45) #Draw a horizontal line across axes
axes[0,1].axvline(0.65) #Draw a vertical line across axes
axes2[0].fill(x,y,color='blue') #Draw filled polygons
axes2[1].fill_between(x,y,color='yellow') #Fill between y-values and 0