# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 21:21:14 2020

@author: David Vasquez
"""

from opt_sys import OpSysData
from pto_src import PointSource
from ray_trc import Trace
from mrt_fnc import mf_ray_LMN
from scipy.optimize import minimize
from random         import uniform
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
        for rayIndex in range(5):
            LMN     = self.propagate_ray (self.pto       ,self.optSys,rayIndex)
            self.pto.ChangeCosineDir(rayIndex,LMN)
            LMN     = self.propagate_ray (self.pto_onaxis,self.optSys,rayIndex)
            self.pto_onaxis.ChangeCosineDir(rayIndex,LMN)

    def propagate_ray (self,pto,optSys,rayIndex): 
        
        #initialValue = []
        #numberStep   = 10
        #for q in  range(numberStep):
        #    if q == 0:
        #        initialValue.append([0,0]) 
        #    else:
        #        initialValue.append([0,uniform(-0.02,0.02)]) 

        #print (initialValue)        
        #for x0 in initialValue:
        x0  = [0,0]
        res = minimize(mf_ray_LMN, x0,args=(pto,optSys,rayIndex),method='Nelder-Mead')
            #print(x0,res.fun)
            #if res.fun < 1e-3:
            #    print('solved:'+ str(res.fun))
            #    break
        #Find value
        #x0  = [0,0]
        #bnds =[(-10e6,+10e6),(-10e6,+10e6)]
        #res = minimize(mf_ray_LMN, x0,args=(pto,optSys,rayIndex),method='SLSQP', bounds=bnds)
        #res = minimize(mf_ray_LMN, x0,args=(pto,optSys,rayIndex),method='Nelder-Mead')
        
        #res = minimize(mf_ray_LMN, x0,args=(pto,optSys,rayIndex),method='Newton-CG')
        #print(res.fun)
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
    syst1.changeAperture(2,3.0)
    
    # Instantiate point source
    pto1  = PointSource([0,1,0],635)
    
    design1  = OpDesign(pto1,syst1)
    RayTrace = design1.RayTrace
    Pto      = design1.pto
