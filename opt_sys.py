# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 19:29:17 2020

@author: David Vasquez
"""

from numpy   import pi
import matplotlib.pyplot as plt
import matplotlib.patches
import matplotlib.lines
import math

#missing: function to modify object distance,
#         if index not define append to the last surface,
#         Assert 

class OpSysData:
    '''
    Properties:
        SurfaceData: list of lists, (d,C,n,surfType)
            d: distance (mm)
            C: curvature (1/mm)
            n: refraction index (-)
            surfType: surface type ('object', 'surface', 'image')
        Aperture: list (surfIndex,radio)
            surfIndex: surface index where the aperture is located
            radio: aperture radio (mm)
    Falta funcion para evaluar limites y valores erroneos 
    Falta funcion para modificar plano objeto
    Falta funcion para visualizar el sistema
    '''
    def __init__(self):                      
        self.SurfaceData=[]
        self.SurfaceData.append([10,0,1,'object' ])
        self.SurfaceData.append([10,0,1,'surface'])
        self.SurfaceData.append([ 0,0,1,'image'  ])
        self.Aperture = []
        self.changeAperture(1,2.0)
    
    def addSurface(self, d, C, n,surfIndex):
        if surfIndex < len(self.SurfaceData) and surfIndex>0:
            self.SurfaceData.insert(surfIndex,[d,C,n,'surface']) 
        else:
            print('Surface index not valid')
    
    def changeSurface(self, d, C, n,surfIndex):                   #if index not define append to the last surface, missing Assert
        if surfIndex < len(self.SurfaceData) and surfIndex>0:
            self.SurfaceData[surfIndex]=[d,C,n,'surface'] 
        else:
            print('Surface index not valid')
        
    def changeAperture(self, surfIndex, radio):
        if surfIndex < len(self.SurfaceData) and surfIndex>0:     #Check for vaid indices
            self.Aperture = [surfIndex, radio]
        else:
            print('Surface index not valid')
            
    def invertSurfaceOrder(self, surf1, surf2):                   #still missing surf# validation
        #CHECK
        surfCopy_inv = self.SurfaceData[surf1:surf2+1][::-1]
        dist = [d[0] for d in surfCopy_inv]
        curv = [C[1] for C in surfCopy_inv]
        refI = [n[2] for n in surfCopy_inv]
        len_surf = len(surfCopy_inv)
        
        for q in range(len_surf):
            surfCopy_inv[q][0]= +dist[(q+1)%len_surf]
            surfCopy_inv[q][1]= -curv[q]
            surfCopy_inv[q][2]= refI[(q+1)%len_surf]
        
        self.SurfaceData[surf1:surf2+1] = surfCopy_inv

        
if __name__=='__main__':
    from plt_fnc import plotSystem
    syst1 = OpSysData()
    syst1.addSurface(10,5,1.42,0)
    #print(syst1.SurfaceData)
    syst1.addSurface(2,2,2,2)
    syst1.addSurface(3,3,3,3)
    syst1.addSurface(4,4,4,4)
    #print(syst1.SurfaceData)
    syst1.changeSurface(1,1,1,1)
    #print(syst1.SurfaceData)
    #print(syst1.Aperture)
    syst1.changeAperture(2,4)
    #print(syst1.Aperture)
    #surfPatch=syst1.plotSystem()
    #plt.gca().add_patch(surfPatch[0])
    #syst1.invertSurfaceOrder(2,4)
    print(syst1.SurfaceData)
    
    plt.figure()
    l1 = plotSystem(syst1)
    for q in l1:
        plt.gca().add_patch(q)
    
    plt.xlim([0,+25])
    plt.ylim([-2,+2])
    plt.show()