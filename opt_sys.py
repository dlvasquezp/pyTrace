# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 19:29:17 2020

@author: David Vasquez
"""

from numpy   import pi as pi
import matplotlib.pyplot as plt
import matplotlib.patches
import matplotlib.lines
import math

class OpSysData:
    '''
    Properties:
        SurfaceData: list of lists, (d,C,n,surfType)
            d: distance (mm)
            C: curvature (1/mm)
            n: refraction index (-)
            surfType: surface type ('object', 'surface', 'image')
        Aperture: list (surfIndex,rario)
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
        self.changeAperture(1,2)
    
    def addSurface(self, d, C, n,surfIndex):
        if surfIndex < len(self.SurfaceData) and surfIndex>0:
            self.SurfaceData.insert(surfIndex,[d,C,n,'surface']) 
        else:
            print('Surface index not valid')
    
    def changeSurface(self, d, C, n,surfIndex):
        if surfIndex < len(self.SurfaceData) and surfIndex>0:
            self.SurfaceData[surfIndex]=[d,C,n,'surface'] 
        else:
            print('Surface index not valid')
        
    def changeAperture(self, surfIndex, radio):
        if surfIndex < len(self.SurfaceData) and surfIndex>0:     #Check for vaid indices
            self.Aperture = [surfIndex, radio]
        else:
            print('Surface index not valid')
            
    def plotSystem(self):
        #Create the e vector
        z0=[]
        for q in range(len(self.SurfaceData)):
            if q == 0:
                z0.append(0)
            else:
                z0.append(z0[q-1] + self.SurfaceData[q-1][0])
        # surface center
        zR=[]
        for q in range(len(self.SurfaceData)):
            if self.SurfaceData[q][1] == 0:
                zR.append(z0[q])
            else:
                zR.append(z0[q]+(1.0/self.SurfaceData[q][1]))
        # create arc patches
        surfPatch=[]
        aperture = 5.0
        for q in range(len(self.SurfaceData)):
            if self.SurfaceData[q][1] == 0:
                #surfPatch.append(matplotlib.lines.Line2D((zR[q],zR[q])
                #                                        ,(-aperture,+aperture)))
                print ''
            else:
                #Falta los angulos theta1 y theta 2
                radius = 1.0/self.SurfaceData[q][1] 
                diam = abs(2*radius)
                if abs(aperture/radius) > 1:
                    theta = 45.0
                else:
                    theta = math.asin(abs(aperture/radius))*(180/pi)
                if radius < 0:
                    angleRot = 0
                else:
                    angleRot = 180
                    
                surfPatch.append(matplotlib.patches.Arc((zR[q],0)
                                                        ,diam
                                                        ,diam
                                                        ,angle=angleRot
                                                        ,theta1=-theta
                                                        ,theta2=+theta))
        #print(z0)
        #print(zR)
        return surfPatch
        
                
        #l1=matplotlib.patches.Arc((70,0),20,20,angle=90.0,theta1=0.0,theta2=180.0)
        

        
if __name__=='__main__':
    syst1 = OpSysData()
    syst1.addSurface(10,5,1.42,0)
    print(syst1.SurfaceData)
    syst1.addSurface(10,5,1.42,2)
    print(syst1.SurfaceData)
    syst1.changeSurface(8,4,1.22,1)
    print(syst1.SurfaceData)
    print(syst1.Aperture)
    syst1.changeAperture(2,4)
    print(syst1.Aperture)
    surfPatch=syst1.plotSystem()
    plt.gca().add_patch(surfPatch[0])