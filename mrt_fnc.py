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
    *arg: (list) [object Optical desing, object ray source, int indexRay]
    
    '''
    # arg[0] must be Optical design
    # arg[1] must be ray source
    # arg[2] must be int [0,1,2,3,4]
    
    #reference the values
    vector        = x0 
    SurfaceData   = arg[0].optSys.SurfaceData
    ApertureRadio = arg[0].apRadius
    ApertureIndex = arg[0].apIndex
    RayList       = arg[1].RayList
    indexRay      = arg[2]
    
    #Calculate director cosines
    norm     = math.sqrt(1.0 + vector[0]**2 + vector[1]**2) 
    cosDirX  = vector[0]/norm
    cosDirY  = vector[1]/norm
    cosDirZ  = 1.0/norm 
    LMN      = [cosDirX,cosDirY,cosDirZ]
        
    #replace cosine director    
    arg[1].ChangeCosineDir(indexRay,LMN)
    
    #Make Raytrace
    RayTrace  = Trace(RayList,SurfaceData)
    
    #Calculate error
    error = -1
    if indexRay == 0:
        error    = (abs(RayTrace[indexRay, 9 ,ApertureIndex])
                   +abs(RayTrace[indexRay, 8 ,ApertureIndex])
                   +abs(RayTrace[indexRay, 7 ,ApertureIndex]))
        
    if indexRay == 1:
        error    = (abs(+ApertureRadio - RayTrace[indexRay, 9 ,ApertureIndex])
                   +abs(RayTrace[indexRay, 8 ,ApertureIndex])
                   +abs(RayTrace[indexRay, 7 ,ApertureIndex]))
                    
    if indexRay == 2:
        error    = (abs(-ApertureRadio - RayTrace[indexRay, 9 ,ApertureIndex])
                   +abs(RayTrace[indexRay, 8 ,ApertureIndex])
                   +abs(RayTrace[indexRay, 7 ,ApertureIndex]))
                   
    if indexRay == 3:
        error    = (abs(+ApertureRadio - RayTrace[indexRay, 8 ,ApertureIndex])
                   +abs(RayTrace[indexRay, 9 ,ApertureIndex])
                   +abs(RayTrace[indexRay, 7 ,ApertureIndex]))
        
    if indexRay == 4:
        error    = (abs(-ApertureRadio - RayTrace[indexRay, 8 ,ApertureIndex])
                   +abs(RayTrace[indexRay, 9 ,ApertureIndex])
                   +abs(RayTrace[indexRay, 7 ,ApertureIndex]))
    
    
    return error

def mf_ray_XYZ0 (x0,*arg):
    '''
    Merit function to calculate the error produced by the ray 0 propaged in the 
    last surface (image) 
    
    x0:   (float) distance
    *arg: (list) [object optical design, int indexRay]
    
    '''
    # x0 must be float
    # arg[0] must be Optical design
    # arg[1] must be int [0,1,2,3,4]
    
    #Copy the values
    dist        = x0 
    RayList     = arg[0].pto_onaxis.RayList
    SurfaceData = arg[0].optSys.SurfaceData
    indexRay    = arg[1]
    
    #replace surface distance
    surf_len = len(SurfaceData)
    surf_idx = (surf_len-2) 
    arg[0].optSys.changeSurface(dist,SurfaceData[surf_idx][1],SurfaceData[surf_idx][2],surfIndex=surf_idx)
    
    #Make Raytrace
    RayTrace  = Trace(RayList,SurfaceData)
    
    #Calculate error
    error = (abs(RayTrace[indexRay, 7 ,-1])
            +abs(RayTrace[indexRay, 8 ,-1])
            +abs(RayTrace[indexRay, 9 ,-1]))
    
    return error



if __name__=='__main__':
    from pto_src import PointSource
    from opt_sys import OpSysData
    from plt_fnc import plotSystem,plotRayTrace 
    from opt_dsg import OpDesign
    import matplotlib.pyplot as plt
    
    pto1  = PointSource([0,1,0],635)
    syst1 = OpSysData()
    syst1.addSurface(2,0.05,1.7)
    syst1.addSurface(10,-0.5,1.4)
    #syst1.changeAperture(1,surfIndex = 1)
    
    design1  = OpDesign(pto1,syst1)
    design1.autofocus()
    
    arcs,line2d = plotSystem(syst1)
    
    fig, ax = plt.subplots()
    for q in arcs:
        fig.gca().add_patch(q)
    for w in line2d:
        ax.add_line(w)
    
    
    #design1 = Trace(pto1.RayList,syst1.SurfaceData)
    
    x0  = [0,0]
    res0 = mf_ray_LMN (x0,design1,pto1,1)
    
    x1  = 40
    res1 = mf_ray_XYZ0(x1,design1,1)
    print(res1)
    
    line2d_ray = plotRayTrace(design1.RayTrace) 
    for w in line2d_ray:
        ax.add_line(w)
        
    plt.xlim([-5,+50])
    plt.ylim([-6,+6])
    plt.show()
    