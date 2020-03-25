# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 21:21:14 2020

@author: David Vasquez
"""
from opt_sys import OpSysData
from pto_src import PointSource
from ray_trc import Trace
from mrt_fnc import mf_ray_LMN
from numpy   import pi as pi
from scipy.optimize import minimize
import math

class OpDesign:
    '''
    pto_src: point source 
    opt_sys: optical system
    
    Falta: Documentacion
           Plot rays
    '''
    def __init__(self,pto,optSys):
        self.pto    = pto
        self.optSys = optSys
        #Create on-axis pointsource
        self.pto_onaxis = PointSource([0,0,0],self.pto.Lambda) 
        #Propagate
        self.propagate()
        #Trace
        self.RayTrace        = Trace(self.pto.RayList       ,self.optSys.SurfaceData)
        self.RayTrace_onaxis = Trace(self.pto_onaxis.RayList,self.optSys.SurfaceData)
     
    def propagate(self):
        #Propagate rays indices until 2
        for rayIndex in range(3):
            LMN     = self.propagate_ray (self.pto       ,self.optSys,rayIndex)
            self.pto.ChangeCosineDir(rayIndex,LMN)
            LMN     = self.propagate_ray (self.pto_onaxis,self.optSys,rayIndex)
            self.pto_onaxis.ChangeCosineDir(rayIndex,LMN)

    def propagate_ray (self,pto,optSys,rayIndex):                     
        #Find value
        x0  = pi/2
        bnds =[(0,+pi)]
        res = minimize(mf_ray_LMN, x0,args=(pto,optSys,rayIndex),method='SLSQP', bounds=bnds)
        
        # Replace value 
        x1 = res.x[0]
        LMN  = [0,math.cos(x1),math.sqrt(1-math.cos(x1)**2)]
        
        return LMN
    
    
if __name__=='__main__':
    # Instantiate optical system
    syst1 = OpSysData()
    syst1.addSurface(10,0.005,1.42,1)
    syst1.changeAperture(2,3.0)
    
    # Instantiate point source
    pto1  = PointSource([0,1,0],635)
    
    design1  = OpDesign(pto1,syst1)
    RayTrace = design1.RayTrace
    Pto      = design1.pto
