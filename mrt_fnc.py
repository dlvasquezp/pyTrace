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
    
    '''
    # arg[0] must be RaySource
    # arg[1] must be Opsysata
    # arg[2] must be int [0,1,2,3,4]
    
    #reference the values
    vector        = x0 
    RayList       = arg[0].RayList
    SurfaceData   = arg[1].SurfaceData
    ApertureRadio = arg[1].Aperture[ 0]
    ApertureIndex = arg[1].Aperture[ 1]
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
    *arg: (list) [object RaySource, object OpSysData, int indexRay]
    
    '''
    # x0 must be float
    # arg[0] must be RaySource
    # arg[1] must be Opsysata
    # arg[2] must be int [0,1,2,3,4]
    
    #Copy the values
    dist        = x0 
    RayList     = arg[0].RayList
    SurfaceData = arg[1].SurfaceData
    indexRay    = arg[2]
    
    #replace surface distance
    surf_len = len(SurfaceData)
    surf_idx = (surf_len-2) 
    arg[1].changeSurface(dist,SurfaceData[surf_idx][1],SurfaceData[surf_idx][2],surfIndex=surf_idx)

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
    from plt_fnc import plotSystem 
    import matplotlib.pyplot as plt
    
    pto1  = PointSource([0,1,0],635)
    syst1 = OpSysData()
    syst1.addSurface(10,0.05,1.42)
    syst1.changeAperture(1,surfIndex = 1)
    
    arcs,line2d = plotSystem(syst1)
    
    fig, ax = plt.subplots()
    for q in arcs:
        fig.gca().add_patch(q)
    for w in line2d:
        ax.add_line(w)
    
    plt.xlim([-5,+35])
    plt.ylim([-6,+6])
    plt.show()
    
    design1 = Trace(pto1.RayList,syst1.SurfaceData)
    
    x0  = [0,0]
    res0 = mf_ray_LMN (x0,pto1,syst1,0)
    
    x1  = 40
    res1 = mf_ray_XYZ0(x1,pto1,syst1,1)
    print(res1)
    