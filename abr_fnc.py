# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 09:57:31 2020

@author: David Vasquez

Function to calculate aberrations
"""
import numpy 
import math

def SeidelCoef(OptDsg):

    
    i   = 1                             # Principal Ray index
    i_b = 0                             # Chief Ray index
    j   = 5                             # 5 Aberrations
    k   = len(OptDsg.optSys.SurfaceData)# Surface k
    
    '''
    _p : sufix for prime
    _b : sufix for bar
    _pb: sufix for prime bar
    '''
    
    SeidelCoef = numpy.zeros((j,k))                            
    
    
    for k in range (1, k):                                             # k -> surface indice (start in 1)
        # Principal ray 
        n     =  OptDsg.dsgPtoTrace[i,2 ,k-1]
        U     =  OptDsg.dsgPtoTrace[i,20,k-1] 
        n_p   =  OptDsg.dsgPtoTrace[i,2 ,k]
        U_p   =  OptDsg.dsgPtoTrace[i,20,k]
        I_p   =  math.acos(OptDsg.dsgPtoTrace[i,17,k])
        # Common values
        h     =  OptDsg.dsgPtoTrace[i,9,k]
        c     =  OptDsg.dsgPtoTrace[i,1,k]
        # Chief ray
        n_pb  =  OptDsg.raySrcTrace[i_b,2 ,k]
        I_pb  =  math.acos(OptDsg.raySrcTrace[i_b,17,k])
        
        # Abreviations
        A     =  n_p*I_p
        A_b   =  n_pb*I_pb  
        H     =  1 #Still missing the definition         
            
        #Spheric aberration
        SeidelCoef[0,k] = -( (A**2)  * h * ((U_p/n_p)- (U/n) ))
        #Coma
        SeidelCoef[1,k] = -( (A*A_b) * h * ((U_p/n_p)- (U/n) ))
        #Astigmatism
        SeidelCoef[2,k] = -( (A_b**2)* h * ((U_p/n_p)- (U/n) ))
        #Petzval curvature
        SeidelCoef[3,k] = -( (H**2)  * c * (  (1/n_p)- (1/n) ))
        #Distortion
        SeidelCoef[4,k] = -( ((A_b**3)/A)     * h * ((U_p/n_p)- (U/n)  )  
                           + (A_b/A) * (H**2) * c * (  (1/n_p)- (1/n)  ))
        
    return SeidelCoef

if __name__=='__main__':
    from opt_sys import OpSysData
    from ray_src import PointSource
    from opt_dsg import OpDesign

    # Instantiate optical system
    syst1 = OpSysData()
    syst1.change_surface(10    ,0         ,1      ,surfIndex=0) 
    syst1.add_surface   (3.50  ,1/15.37   ,'N-BK7')
    syst1.add_surface   (1.50  ,1/-11.10  ,'N-SF5')
    syst1.add_surface   (5     ,1/-31.47  ,1      )
    #syst1.changeAperture(1,surfIndex=2)
    lensData=[1,5.0,5.0,5.0,1]
    syst1.plot_optical_system(lensData)
    
    # Instantiate point source
    pto1  = PointSource([0,0.5,0],635)
    
    # Instantiate optical design
    design1  = OpDesign(pto1,syst1)
    
    SCoef =  SeidelCoef(design1)
    print(SCoef)
    

    # plot design
    design1.plot_design(lensData)