# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 21:21:14 2020

@author: David Vasquez
"""
from plt_fnc import plot_system, plot_rayTrace
from opt_sys import OpSysData
from ray_src import RaySource,PointSource,InfinitySource
from ray_trc import Trace
from mrt_fnc import LMN_apertureStop,XYZ_apertureStop,XYZ_image
from scipy.optimize import minimize
import matplotlib.pyplot as plt

class OpDesign:
    '''
    dsn_src: point source 
    opt_sys: optical system
    
    Falta: Documentacion
           check aprture index and value
    '''
    def __init__(self,usrSrc,optSys,aprRad=1.0,aprInd=1):
        #Attributes
        self.usrSrc  = usrSrc
        self.optSys  = optSys
        self.aprRad  = 1.0 
        self.aprInd  = 1
        #Assign aperture attributes
        self.change_aperture_radius(aprRad)
        self.change_aperture_index(aprInd)
        #design attributes
        self.dsgPtoSrc = PointSource([0,0,0],self.usrSrc.Wavelength) 
        self.dsgInfSrc = InfinitySource([0,0,1],self.usrSrc.Wavelength)
        #Solve attriutes
        self.dsgSolved = False
        self.dsgError  = []
        self.tolError  = 0.005
        
        # solve design
        self.solve_dsg()
        
    def change_aperture_radius(self,aprRad):
        assert isinstance(aprRad,(int,float)), 'Invalid aperture radius (aperRad) data type'
        assert aprRad > 0, 'Invalid aperture (aperRad) radius value' 
        self.aprRad=aprRad
        
    def change_aperture_index(self,aprInd):
        surf_len = len(self.optSys.SurfaceData)
        assert isinstance(aprInd,int),'Invalid aperture index (aprInd) data type'
        assert aprInd > 0 and aprInd < surf_len, 'Invalid aperture index (aprInd) value'
        self.aprInd=aprInd
        
    def solve_dsg(self):
        self.dsgSolved = False
        self.propagate_essential_rays()
        self.trace_optical_design()
        
        if max(self.dsgError)< self.tolError:
            self.dsgSolved = True
        else:
            print(self.dsgError)
            raise Warning('numerical error out of bounds, check aperture index or radius')
        
    def trace_optical_design(self):
        self.raySrcTrace = Trace(self.usrSrc.RayList   ,self.optSys.SurfaceData)
        self.dsgPtoTrace = Trace(self.dsgPtoSrc.RayList,self.optSys.SurfaceData)
        self.dsgInfTrace = Trace(self.dsgInfSrc.RayList,self.optSys.SurfaceData)
        
    def propagate_essential_rays(self):
        self.dsgError  = []
        usrSrcError=[]
        dsgPtoSrcError=[]
        dsgInfSrcError=[]
        
        for rayIndex in range(5):
            #User ray source
            LMN, rayError = self.propagate_ray (self.usrSrc   , rayIndex)
            self.usrSrc.change_LMN(LMN,rayIndex)
            usrSrcError.append(rayError)
            #Design point source
            LMN, rayError = self.propagate_ray (self.dsgPtoSrc, rayIndex)
            self.dsgPtoSrc.change_LMN(LMN,rayIndex)
            dsgPtoSrcError.append(rayError)
            #Design source at infinity
            XYZ,rayError = self.propagate_ray (self.dsgInfSrc, rayIndex)
            self.dsgInfSrc.change_XYZ(XYZ,rayIndex)
            dsgInfSrcError.append(rayError)
            
        self.dsgError.append(sum(usrSrcError))
        self.dsgError.append(sum(dsgPtoSrcError))
        self.dsgError.append(sum(dsgInfSrcError))
            
    
    def propagate_ray (self,ptoSrc,rayIndex):
        
        if isinstance(ptoSrc,PointSource):
            #Perform optimization
            x0  = [0,0]
            res = minimize(LMN_apertureStop, x0, args=(self,ptoSrc,rayIndex), method='Nelder-Mead')
            # Get result
            rayError = res.fun
            x1  = res.x
            LMN = RaySource.calc_direcCos([x1[0],x1[1],1])
            return LMN, rayError
        
        if isinstance(ptoSrc,InfinitySource):
            #Perform optimization
            x0  = [0,0]
            res = minimize(XYZ_apertureStop, x0, args=(self,ptoSrc,rayIndex), method='Nelder-Mead')
            # Get result
            rayError = res.fun
            x1  = res.x
            XYZ = [x1[0],x1[1],0]
            return XYZ, rayError
            
    def autofocus(self):
        #Perform optimization
        rayIndex = 1
        x0 = self.optSys.SurfaceData[-2][0]
        res= minimize(XYZ_image, x0,args=(self,rayIndex),method='Nelder-Mead')
        #Replace value
        x1 = res.x
        self.optSys.SurfaceData[-2][0]=x1
        #Actualize trace
        self.solve_dsg()
        
    def plot_design(self):
        fig, ax = plt.subplots()
        fig, ax = plot_system(self,fig,ax,show=True)
        fig, ax = plot_rayTrace(self.raySrcTrace,fig=fig,ax=ax)
        fig, ax = plot_rayTrace(self.dsgPtoTrace,fig=fig,ax=ax)
        

    
if __name__=='__main__':
    from plt_fnc import plot_system, plot_rayTrace
    import matplotlib.pyplot as plt
    # Instantiate optical system
    syst1 = OpSysData()
    syst1.add_surface(9,+0.5,1.42)
    syst1.add_surface(4,-0.1 ,1.5)
    
    # Instantiate point source
    pto1  = PointSource([0,0.5,0],635)
    
    design1  = OpDesign(pto1,syst1,aprRad=1,aprInd=1)
    #design1.autofocus() 
    
    RayTrace = design1.dsgPtoTrace
    Pto      = design1.usrSrc
    
    #fig, ax = plt.subplots()
    #fig, ax = plot_system(design1,fig,ax,show=True)
    #fig, ax = plot_rayTrace(design1.dsgInfTrace,fig=fig,ax=ax)
    #fig, ax = plot_rayTrace(design1.raySrcTrace,fig=fig,ax=ax)
    #fig, ax = plot_rayTrace(design1.dsgPtoTrace,fig=fig,ax=ax)
    
    design1.plot_design()
    
    
    
    
