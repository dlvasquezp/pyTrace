# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 06:47:46 2020

@author: David Vasquez
"""
import math
from ray_trc import Trace

def mf_ray_LMN ( x0,*arg):
    '''
    Ray index 0: it goes to the center of the pupil; also chief ray
    x0: (double) angle [radians]
    *arg: (list) [object RaySource, object OpSysData, int indexRay] # still missing: ApertureR, Surface
    
    Falta extenderlo a X
    '''
    #Merit function constant values
    #indexRay = 0
    surfProp = 9 # Y position
    
    #Copy the values
    alfa    = x0 
    RayList = arg[0].RayList
    SurfaceData   = arg[1].SurfaceData
    ApertureIndex = arg[1].Aperture[0]
    ApertureRadio = arg[1].Aperture[1]
    indexRay = arg[2]
    
    #Replace the YZ cosine director in the object plane
    LMN=[0,math.cos(alfa),math.sqrt(1-math.cos(alfa)**2)]
    arg[0].ChangeCosineDir(indexRay,LMN)
    
    #Make Raytrace
    RayTrace  = Trace(RayList,SurfaceData)
    
    #Calculate error                THIS PART NEED TO BE IMPROVED
    error = -1
    if indexRay == 0:
        error    = abs(RayTrace[indexRay, surfProp ,ApertureIndex])
    if indexRay == 1:
        error    = abs(+ApertureRadio - RayTrace[indexRay, surfProp ,ApertureIndex])
    if indexRay == 2:
        error    = abs(-ApertureRadio - RayTrace[indexRay, surfProp ,ApertureIndex])
    
    return error


def mf_ray0_LMN ( x0,*arg):
    '''
    Ray index 0: it goes to the center of the pupil; also chief ray
    x0: (double) angle [radians]
    *arg: (list) [object RaySource, object OpSysData] # still missing: ApertureR, Surface
    '''
    #Merit function constant values
    indexRay = 0
    surfProp = 9 # Y position
    
    #Copy the values
    alfa    = x0 
    RayList = arg[0].RayList
    SurfaceData   = arg[1].SurfaceData
    ApertureIndex = arg[1].Aperture[0]
    ApertureRadio = arg[1].Aperture[1]
    
    #Replace the YZ cosine director in the object plane
    LMN=[0,math.cos(alfa),math.sqrt(1-math.cos(alfa)**2)]
    arg[0].ChangeCosineDir(0,LMN)
    
    #Make Raytrace
    RayTrace  = Trace(RayList,SurfaceData)
    
    #Calculate error
    error    = abs(RayTrace[indexRay, surfProp ,ApertureIndex])
    
    return error

def mf_ray1_LMN ( x0,*arg):
    '''
    Ray index 1: it goes to the + rim of the pupil; also marginal/coma ray
    x0: (double) angle [radians]
    *arg: (list) [object RaySource, object OpSysData] # still missing: ApertureR, Surface
    '''
    #Merit function constant values
    indexRay = 1
    surfProp = 9 # Y position
    
    #Copy the values
    alfa    = x0 
    RayList = arg[0].RayList
    SurfaceData   = arg[1].SurfaceData
    ApertureIndex = arg[1].Aperture[0]
    ApertureRadio = arg[1].Aperture[1]
    
    #Replace the YZ cosine director in the object plane
    LMN=[0,math.cos(alfa),math.sqrt(1-math.cos(alfa)**2)]
    arg[0].ChangeCosineDir(indexRay,LMN)
    
    #Make Raytrace
    RayTrace  = Trace(RayList,SurfaceData)
    
    #Calculate error
    error    = abs(ApertureRadio - RayTrace[indexRay, surfProp ,ApertureIndex])
    
    return error

def mf_ray2_LMN ( x0,*arg):
    '''
    Ray index 2: it goes to the - rim of the pupil; also marginal/coma ray
    x0: (double) angle [radians]
    *arg: (list) [object RaySource, object OpSysData] # still missing: ApertureR, Surface
    '''
    #Merit function constant values
    indexRay = 2
    surfProp = 9 # Y position
    
    #Copy the values
    alfa    = x0 
    RayList = arg[0].RayList
    SurfaceData   = arg[1].SurfaceData
    ApertureIndex = arg[1].Aperture[0]
    ApertureRadio = arg[1].Aperture[1]
    
    #Replace the YZ cosine director in the object plane
    LMN=[0,math.cos(alfa),math.sqrt(1-math.cos(alfa)**2)]
    arg[0].ChangeCosineDir(indexRay,LMN)
    
    #Make Raytrace
    RayTrace  = Trace(RayList,SurfaceData)
    
    #Calculate error
    error    = abs(-ApertureRadio - RayTrace[indexRay, surfProp ,ApertureIndex])
    
    return error

if __name__=='__main__':
    from pto_src import PointSource
    from opt_sys import OpSysData
    
    pto1  = PointSource([0,1,0],635)
    syst1 = OpSysData()
    syst1.addSurface(10,0.005,1.42,1)
    syst1.changeAperture(2,2)
    
    design1 = Trace(pto1.RayList,syst1.SurfaceData)
    
    x0  = 1.4
    res0 = mf_ray2_LMN (x0,pto1,syst1)
    res1 = mf_ray_LMN (x0,pto1,syst1,2)