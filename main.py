# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 07:24:33 2020

@author: David Vasquez
"""

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
syst1.changeSurface(10,0,1,1) 
syst1.addSurface(10,0.2,1.5,2)
syst1.addSurface(10,-0.005,1,3)
syst1.addSurface(40,0.08,1.7,4)
syst1.changeAperture(2,1.0)

# Instantiate point source
pto1  = PointSource([0,2,0],635)

# Instantiate optical design
design1  = OpDesign(pto1,syst1)

#Copy Ray trace and plot it
RayTrace1 = design1.RayTrace
RayTrace2 = design1.RayTrace_onaxis

#[rayIndex][d][all surfaces] + [rayIndex][Z][all surfaces]
z10 = RayTrace1[0][0][:] #+ RayTrace1[0][10][:]  
z11 = RayTrace1[1][0][:] #+ RayTrace1[1][10][:]
z12 = RayTrace1[2][0][:] #+ RayTrace1[2][10][:]

zz10 = []
zz11 = []
zz12 = []
for q in range(len(z10)):
    if q == 0:
        zz10.append(0)
        zz11.append(0)
        zz12.append(0)
    else:
        zz10.append(z10[0:q].sum()+ RayTrace1[0][10][q])
        zz11.append(z11[0:q].sum()+ RayTrace1[1][10][q])
        zz12.append(z12[0:q].sum()+ RayTrace1[2][10][q])

y10 = RayTrace1[0][9][:]
y11 = RayTrace1[1][9][:]
y12 = RayTrace1[2][9][:]

############################################################
zzz10 = []
zzz11 = []
zzz12 = []
for q in range(len(z10)):
    if q == 0:
        zzz10.append(0)
        zzz11.append(0)
        zzz12.append(0)
    else:
        zzz10.append(z10[0:q].sum()+ RayTrace2[0][10][q])
        zzz11.append(z11[0:q].sum()+ RayTrace2[1][10][q])
        zzz12.append(z12[0:q].sum()+ RayTrace2[2][10][q])

yyy10 = RayTrace2[0][9][:]
yyy11 = RayTrace2[1][9][:]
yyy12 = RayTrace2[2][9][:]
#############################################################
#l1=matplotlib.patches.Arc((70,0),20,20,angle=90.0,theta1=0.0,theta2=180.0)
plt.figure()
l1 = syst1.plotSystem()
for q in l1:
    plt.gca().add_patch(q)
plt.plot(zz10,y10,'b',zz11,y11,'b',zz12,y12,'b')
plt.plot(zzz10,yyy10,'g',zzz11,yyy11,'g',zzz12,yyy12,'g')
plt.xlim([zz10[0]-10,zz10[-1]+10])
plt.ylim([y10[0]-10,y10[-1]+10])
plt.show()






