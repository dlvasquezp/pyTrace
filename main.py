# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 07:24:33 2020

@author: David Vasquez
"""
#from plt_fnc import plot_system, plot_rayTrace
from opt_sys import OpSysData
from ray_src import PointSource,InfinitySource
from opt_dsg import OpDesign
#import matplotlib.pyplot as plt



# Instantiate optical system
syst1 = OpSysData()
syst1.change_surface(4  ,0   ,1  ,surfIndex=0) 
syst1.add_surface   (2  ,0.1 ,1.0)
syst1.add_surface   (2  ,-0.5,1  )
syst1.add_surface   (4  ,0.08  ,'N-BK7')
syst1.add_surface   (2 ,0.0   ,1  )
#syst1.changeAperture(1,surfIndex=2)

# Instantiate point source
pto1  = PointSource([0,0.5,0],635)

# Instantiate optical design
design1  = OpDesign(pto1,syst1)

# autofocus
#design1.autofocus()

# plot design
design1.plot_design()

    








