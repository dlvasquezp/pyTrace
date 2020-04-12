# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 21:21:14 2020

@author: David Vasquez
"""

from opt_sys import OpSysData
from ray_src import RaySource,PointSource,InfinitySource

from ray_trc import Trace
from mrt_fnc import mf_ray_LMN,mf_ray_XYZ0
from scipy.optimize import minimize
from random         import uniform
import math

class OpDesign:
    '''
    dsn_src: point source 
    opt_sys: optical system
    
    Falta: Documentacion
    '''
    def __init__(self,usrSrc,optSys,aprRad=1.0,aprInd=1 ):
        #Arguments
        self.usrSrc  = usrSrc
        self.optSys  = optSys
        self.aprRad  = aprRad 
        self.aprInd  = aprInd

        #Attributes
        self.dsgPtoSrc = PointSource([0,0,0],self.usrSrc.Wavelength) 
        self.dsgInfSrc = InfinitySource([0,0,1],self.usrSrc.Wavelength)
        
        #Propagate
        self.propagate_essential_rays()
        #Trace
        self.trace_optical_design()
        
    def trace_optical_design(self):
        self.raySrcTrace = Trace(self.usrSrc.RayList   ,self.optSys.SurfaceData)
        self.dsgPtoTrace = Trace(self.dsgPtoSrc.RayList,self.optSys.SurfaceData)
        
    def propagate_essential_rays(self):
        for rayIndex in range(5):
            LMN = self.propagate_ray (self.usrSrc   ,rayIndex)
            self.usrSrc.change_LMN(LMN,rayIndex)
            LMN = self.propagate_ray (self.dsgPtoSrc, rayIndex)
            self.dsgPtoSrc.change_LMN(LMN,rayIndex)
    
    def propagate_ray (self,ptoSrc,rayIndex):  
        #Perform optimization
        x0  = [0,0]
        res = minimize(mf_ray_LMN, x0, args=(self,ptoSrc,rayIndex), method='Nelder-Mead')
        
        # Replace value 
        x1 = res.x
        norm     = math.sqrt(1.0 + x1[0]**2 + x1[1]**2) 
        cosDirX  = x1[0]/norm
        cosDirY  = x1[1]/norm
        cosDirZ  = 1.0/norm 
        LMN      = [cosDirX,cosDirY,cosDirZ]
        
        return LMN
            
    def autofocus(self):
        #Perform optimization
        rayIndex = 1
        x0 = self.optSys.SurfaceData[-2][0]
        res= minimize(mf_ray_XYZ0, x0,args=(self,rayIndex),method='Nelder-Mead')
        
        #Replace value
        x1 = res.x
        self.optSys.SurfaceData[-2][0]=x1
        #Actualize trace
        self.trace_optical_design()
        

    
    
    
if __name__=='__main__':
    from plt_fnc import plot_system
    # Instantiate optical system
    syst1 = OpSysData()
    syst1.add_surface(9,0.005,1.42)
    syst1.add_surface(4,0.001 ,1.5)
    
    # Instantiate point source
    pto1  = PointSource([0,0.5,0],635)
    
    design1  = OpDesign(pto1,syst1,aprRad=1.0,aprInd=1)
    #design1.autofocus() 
    
    RayTrace = design1.dsgPtoTrace
    Pto      = design1.usrSrc
    
    plot= plot_system(design1,showplot=True)
    
    
    
    
