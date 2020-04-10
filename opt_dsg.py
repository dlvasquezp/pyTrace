# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 21:21:14 2020

@author: David Vasquez
"""

from opt_sys import OpSysData
from pto_src import PointSource
from ray_trc import Trace
from mrt_fnc import mf_ray_LMN,mf_ray_XYZ0
from scipy.optimize import minimize
from random         import uniform
import math

class OpDesign:
    '''
    pto_src: point source 
    opt_sys: optical system
    
    Falta: Documentacion
    '''
    def __init__(self,pto,optSys):
        self.pto     = pto
        self.optSys  = optSys
        #Create apeture stop
        self.apIndex = 1
        self.apRadius= 1.0 
        #Create on-axis pointsource
        self.pto_onaxis = PointSource([0,0,0],self.pto.Lambda) 
        #Propagate
        self.propagate()
        #Trace
        self.traceDesign()
        
    def traceDesign(self):
        self.RayTrace        = Trace(self.pto.RayList       ,self.optSys.SurfaceData)
        self.RayTrace_onaxis = Trace(self.pto_onaxis.RayList,self.optSys.SurfaceData)
        
    def propagate(self):
        #Propagate rays indices until 5
        for rayIndex in range(5):
            LMN     = self.propagate_ray (self.pto, rayIndex)
            self.pto.ChangeCosineDir(rayIndex,LMN)
            LMN     = self.propagate_ray (self.pto_onaxis, rayIndex)
            self.pto_onaxis.ChangeCosineDir(rayIndex,LMN)
            
    def autofocus(self):
        #Perform optimization
        rayIndex = 1
        x0 = self.optSys.SurfaceData[-2][0]
        res= minimize(mf_ray_XYZ0, x0,args=(self,rayIndex),method='Nelder-Mead')
        
        #Replace value
        x1 = res.x
        self.optSys.SurfaceData[-2][0]=x1
        #Actualize trace
        self.traceDesign()
        

    def propagate_ray (self,pto,rayIndex):  
        #Perform optimization
        x0  = [0,0]
        res = minimize(mf_ray_LMN, x0, args=(self,pto,rayIndex), method='Nelder-Mead')

        # Replace value 
        x1 = res.x
        norm     = math.sqrt(1.0 + x1[0]**2 + x1[1]**2) 
        cosDirX  = x1[0]/norm
        cosDirY  = x1[1]/norm
        cosDirZ  = 1.0/norm 
        LMN      = [cosDirX,cosDirY,cosDirZ]
        
        return LMN
    
    
if __name__=='__main__':
    # Instantiate optical system
    syst1 = OpSysData()
    syst1.addSurface(10,0.005,1.42,1)
    syst1.addSurface(4,0.001,1.5,1)
    
    # Instantiate point source
    pto1  = PointSource([0,1,0],635)
    
    design1  = OpDesign(pto1,syst1)
    design1.autofocus()
    
    RayTrace = design1.RayTrace_onaxis
    Pto      = design1.pto
