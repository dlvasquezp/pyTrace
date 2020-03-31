# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 20:33:47 2020

@author: David Vasquez
"""
import math
import matplotlib.patches
from numpy import pi

#Missing: plot aperture position

def plotSystem(optSystem):
    #number of surfaces
    surf_len = len(optSystem.SurfaceData)
    aperture = optSystem.Aperture[1]
    
    #list the Z coordinates
    z0=[]
    for q in range(surf_len):
        if q == 0:
            z0.append(0)
        else:
            z0.append(z0[q-1] + optSystem.SurfaceData[q-1][0])
    
    #list the surface center
    zR=[]
    for q in range(surf_len):
        if optSystem.SurfaceData[q][1] == 0:
            zR.append(z0[q])
        else:
            zR.append(z0[q]+(1.0/optSystem.SurfaceData[q][1]))
    
    #List off-axis points // Only the upper point is plotted, the 2nd is mirrorred
    yP=[]
    for q in range(surf_len):
        if q == 0 or q==(surf_len-1):                          #Skipt the first and last surface
            yP.append([z0[q],+aperture])
        else:
            if optSystem.SurfaceData[q][1] == 0:               #Check curvature different from 0
                yP.append([z0[q],+aperture])
            else:
                radius = 1.0/optSystem.SurfaceData[q][1] 
                if abs(aperture/radius) > 1:                   #Check size
                    yP.append([z0[q]+radius, +abs(radius)])
                else:
                    #r**2=aperture**2+b**2, zSag = (-)r+b or [+]r-b
                    b = math.sqrt(radius**2-aperture**2)
                    if radius < 0:                             #Decide sag direction
                        yP.append([z0[q]+radius+b,+aperture])
                    else:
                        yP.append([z0[q]+radius-b,+aperture])

  
    #List additional connection points // 'NA': Not applicable
    #                                  // [0,0]: Straight line
    #                                  // [z,y]: connection point coordinate
    conP=[]
    for q in range(surf_len):
        if q == (surf_len-1):                    #Skip the last surface
            conP.append('NA')
        else:
            if optSystem.SurfaceData[q][2] == 1: #Refraction index equal to air
                conP.append('NA')
            else:
                if yP[q][1] == yP[q+1][1]:       #off axis points comparison
                    conP.append([0,0])
                else:
                    if yP[q][1] < yP[q+1][1]:    # Size comparizon
                        conP.append([yP[q][0],yP[q+1][1]])
                    else:
                        conP.append([yP[q+1][0],yP[q][1]])
   
    # create arc patches and lines 
    surfPatch= []
    lines2D  = []
    
    # Optical axis line
    lines2D.append(matplotlib.lines.Line2D((z0[0],z0[-1]),(0,0)
                                           ,c='black',lw=1.0,ls='-'))
    
    # Surfaces
    for q in range(surf_len):
        if optSystem.SurfaceData[q][1] == 0:
            lines2D.append(matplotlib.lines.Line2D((yP[q][0],yP[q][0])
                                                  ,(yP[q][1],-yP[q][1])
                                                  ,c='black',lw=1.0,ls='-'))
        else:
            radius = 1.0/optSystem.SurfaceData[q][1] 
            diam = abs(2*radius)
            if abs(aperture/radius) > 1:
                theta = 90.0
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
                                                        ,theta2=+theta
                                                        ,color='black',lw=1.0,ls='-'))
        #Connection lines
        if conP[q]!= 'NA' and q!= (surf_len-1):
            if conP[q]==[0,0]:
                lines2D.append(matplotlib.lines.Line2D((yP[q][0],yP[q+1][0])
                                                      ,(+yP[q][1],+yP[q+1][1])
                                                      ,c='black',lw=1.0,ls='-'))
                
                lines2D.append(matplotlib.lines.Line2D((yP[q][0],yP[q+1][0])
                                                      ,(-yP[q][1],-yP[q+1][1])
                                                      ,c='black',lw=1.0,ls='-')) 
            else:
                lines2D.append(matplotlib.lines.Line2D((yP[q][0],conP[q][0],yP[q+1][0])
                                                      ,(+yP[q][1],+conP[q][1],+yP[q+1][1])
                                                      ,c='black',lw=1.0,ls='-'))
                
                lines2D.append(matplotlib.lines.Line2D((yP[q][0],conP[q][0],yP[q+1][0])
                                                      ,(-yP[q][1],-conP[q][1],-yP[q+1][1])
                                                      ,c='black',lw=1.0,ls='-'))

    return surfPatch,lines2D

if __name__ == '__main__':
    from opt_sys import OpSysData
    import matplotlib.pyplot as plt
    
    syst1 = OpSysData()
    syst1.addSurface(2,0.2,1.5,1)
    syst1.addSurface(2,0.2,1.1,2)
    syst1.addSurface(3,3,1,3)
    syst1.addSurface(4,0.4,1.8,4)
    #syst1.changeSurface(1,0.1,2,1)
    #syst1.changeAperture(2,1.0)

    syst1.invertSurfaceOrder(4,5)
    syst1.invertSurfaceOrder(1,3)
   # print(syst1.SurfaceData)
    
    arcs,line2d = plotSystem(syst1)
    
    fig, ax = plt.subplots()
    for q in arcs:
        fig.gca().add_patch(q)
    for w in line2d:
        ax.add_line(w)
    
    plt.xlim([-5,+35])
    plt.ylim([-4,+4])
    plt.show()