# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 06:47:46 2020

@author: David Vasquez
"""
import math
from ray_trc import Trace

def mf_ray_LMN (x0,*arg):
    '''
    Merit function to calculate the error produced by the rays propaged in the 
    x0 direction [x0[0],x0[1],1] 
    
    x0:   (list) [vector_compX, vector_comp_y] 
    *arg: (list) [object RaySource, object OpSysData, int indexRay]
    
    Note: the object is passed and modified.
    '''
    # x0 norm must be <1
    # arg[0] must be RaySource
    # arg[1] must be Opsysata
    # arg[2] must be int [0,1,2,3,4]
    
    #Copy the values
    vector        = x0 
    RayList       = arg[0].RayList
    SurfaceData   = arg[1].SurfaceData
    ApertureIndex = arg[1].Aperture[0]
    ApertureRadio = arg[1].Aperture[1]
    indexRay      = arg[2]
    
    #Calculate director cosines
    norm     = math.sqrt(1.0 + vector[0]**2 + vector[1]**2) 
    cosDirX  = vector[0]/norm
    cosDirY  = vector[1]/norm
    cosDirZ  = 1.0/norm 
    LMN      = [cosDirX,cosDirY,cosDirZ]
        
    #replace cosine director    
    arg[0].ChangeCosineDir(indexRay,LMN)
    
    #Make Raytrace
    RayTrace  = Trace(RayList,SurfaceData)
    
    #Calculate error
    error = -1
    if indexRay == 0:
        error    = (abs(RayTrace[indexRay, 9 ,ApertureIndex])
                   +abs(RayTrace[indexRay, 8 ,ApertureIndex]))
        
    if indexRay == 1:
        error    = (abs(+ApertureRadio - RayTrace[indexRay, 9 ,ApertureIndex])
                   +abs(RayTrace[indexRay, 8 ,ApertureIndex]))
                    
    if indexRay == 2:
        error    = (abs(-ApertureRadio - RayTrace[indexRay, 9 ,ApertureIndex])
                   +abs(RayTrace[indexRay, 8 ,ApertureIndex]))
                   
    if indexRay == 3:
        error    = (abs(+ApertureRadio - RayTrace[indexRay, 8 ,ApertureIndex])
                   +abs(RayTrace[indexRay, 9 ,ApertureIndex]))
        
    if indexRay == 4:
        error    = (abs(-ApertureRadio - RayTrace[indexRay, 8 ,ApertureIndex])
                   +abs(RayTrace[indexRay, 9 ,ApertureIndex]))
    
    
    return error


if __name__=='__main__':
    from pto_src import PointSource
    from opt_sys import OpSysData
    
    pto1  = PointSource([0,1,0],635)
    syst1 = OpSysData()
    syst1.addSurface(10,0.005,1.42,1)
    syst1.changeAperture(2,2)
    
    design1 = Trace(pto1.RayList,syst1.SurfaceData)
    
    x0  = [0,0]
    res0 = mf_ray_LMN (x0,pto1,syst1,0)
    