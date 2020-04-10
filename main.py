# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 07:24:33 2020

@author: David Vasquez
"""
from plt_fnc import plotSystem, plotRayTrace
from opt_sys import OpSysData
from pto_src import PointSource
from opt_dsg import OpDesign
from numpy   import pi as pi
from scipy.optimize import minimize
import math
import matplotlib.pyplot as plt
import matplotlib.patches
import matplotlib.lines


# Instantiate optical system
syst1 = OpSysData()
syst1.changeSurface(4,0,1,surfIndex=0) 
syst1.addSurface(8,1 ,1.0)
syst1.addSurface(8 ,-0.5,1  )
syst1.addSurface(4 ,0.08  ,'N-BK7')
syst1.addSurface(10,0.0   ,1  )
#syst1.changeAperture(1,surfIndex=2)


# Instantiate point source
pto1  = PointSource([0,0.5,0],635)

# Instantiate optical design
design1  = OpDesign(pto1,syst1)

# autofocus
#design1.autofocus()


arcs,line2d = plotSystem(design1.optSys)
    
fig, ax = plt.subplots()
for q in arcs:
    fig.gca().add_patch(q)
for w in line2d:
    ax.add_line(w)
    
line2d_ray = plotRayTrace(design1.RayTrace) 
for w in line2d_ray:
    ax.add_line(w)

plt.xlim([-5,+50])
plt.ylim([-6,+6])
plt.show()






