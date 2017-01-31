
## Libraries
import random
import sys
import pickle as pk
from math import *
import numpy as np

import matplotlib
matplotlib.use('Agg')
import pylab as pl
from matplotlib import gridspec
import subprocess

from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
from matplotlib.cbook import get_sample_data


## Properties
frameDPI = 200




print "\n\n Preparing video\n"


## Reading the video code
videoCode = sys.argv[-1]
print "Reading files in " + videoCode


## Reading files
print "Reading: " + videoCode + 'Positions.data.pk...'
POS = pk.load( open(videoCode + 'Positions.data.pk', 'rb') )
print "Reading: " + videoCode + 'Recruited.data.pk...'
REC = pk.load( open(videoCode + 'Recruited.data.pk', 'rb') )
print "Reading: " + videoCode + 'Resources.data.pk...'
RES = pk.load( open(videoCode + 'Resources.data.pk', 'rb') )
print "Reading: " + videoCode + 'AreaState.data.pk...'
ARS = pk.load( open(videoCode + 'AreaState.data.pk', 'rb') )
print "Done reading.\n"


# Number of iterations
T = len(POS)
print "Number of iterations: ", T


## Preparing plots
print "Preparing plots \n"

f = pl.figure( figsize=(8,5) )
canvas_width, canvas_height = f.canvas.get_width_height()


gs = gridspec.GridSpec(2,3) 
ax0 = pl.subplot(gs[:,:-1])

## Adding honey comb
fn = "hive.png"
arr_img = pl.imread(fn, format='png')

imagebox = OffsetImage(arr_img, zoom=0.3)
imagebox.image.axes = ax0
xy = (250, 260)
ab = AnnotationBbox(imagebox, xy,
                    xybox=(0., 0.),
                    xycoords='data',
                    boxcoords="offset points",
                    frameon=False
)
ax0.add_artist(ab)



hlA,  = ax0.plot([], [], 'o', markersize = 3,color=(0.3,1.0,0.3),
                 markeredgecolor=(0.3,1.0,0.3), zorder=0)
hl0,  = ax0.plot([], [], 's', markersize = 3, color=(1.0,0.2,0.2),
                 markeredgecolor=(1.0,0.2,0.2), zorder=5)
hle0, = ax0.plot([], [], 's', markersize = 3, color=(0.1,0.5,1.0),
                 markeredgecolor=(0.1,0.5,1.0), zorder=5)

ax0.set_xlim(0,500)
ax0.set_ylim(0,500)
ax0.set_xticks([])
ax0.set_yticks([])


maxR = np.cumsum(RES)[-1]
print maxR

ax1 = pl.subplot(gs[0,2])
rescol, = ax1.plot([], [], '-', lw=1.2, color=(0.2,0.2,0.2))
ax1.set_xlim(0,T/1000.)
ax1.set_ylim(-0.05, maxR*1.1/1000. )
ax1.set_ylabel('Resource colected (ml)')


ax2 = pl.subplot(gs[1,2])
screc, = ax2.plot([], [], '-', lw=1.2, color=(0.2,0.2,0.2))
ax2.set_xlim(0,T/1000.)
ax2.set_ylim(-5,105)
ax2.set_ylabel('Recruited bees (%)')
ax2.set_xlabel('Time')

pl.tight_layout()


print "Getting ffmpeg prepared.\n"
cmdstring = ('ffmpeg', '-y',
             '-r', '50', '-v:b', '2048',
             '-f','image2pipe',
             '-vcodec', 'png',
             '-i', 'pipe:', '-vcodec', 'libx264', 'out.avi')
p = subprocess.Popen(cmdstring, stdin=subprocess.PIPE)


print "Iterating..."


for t in range(T):

    ## Updating the position of scouts
    if POS[t][0] != [[],[]]:
        hl0.set_xdata( POS[t][0][0][0] )
        hl0.set_ydata( POS[t][0][0][1] )

    ## Updating the position of recruits
    if POS[t][1][0][0] != []:
        hle0.set_xdata( POS[t][1][0][0] )
        hle0.set_ydata( POS[t][1][0][1] )

    ## Updating resources
    hlA.set_xdata( ARS[t][0] )
    hlA.set_ydata( ARS[t][1] )
    
    uptime = np.arange(0,t)/1000.
    
    R = np.cumsum( RES[:t] )/1000.
    rescol.set_ydata(R)
    rescol.set_xdata(uptime)
    
    screc.set_ydata( REC[:t] )
    screc.set_xdata(uptime)
    
    pl.savefig(p.stdin, dpi=frameDPI, format='png')


p.communicate()
print "The end, my friend."
