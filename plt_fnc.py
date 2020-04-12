# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 20:33:47 2020

@author: David Vasquez
"""
import math
import matplotlib.patches
import matplotlib.pyplot as plt
from numpy import pi
#from opt_sys import OpSysData
#from opt_dsg import OpDesign


def plot_system(optObj, lensData=[], fig=[], ax=[], show=False):
    '''
    plot_system accets either OpSysData or OpDesign
    '''   
    # Check class type
    if optObj.__class__.__name__=='OpSysData':
        optSystem = optObj
        apRadius  = 1.0
        apIndex   = -1
    else:
        if optObj.__class__.__name__=='OpDesign':
            optSystem = optObj.optSys
            apRadius  = optObj.aprRad
            apIndex   = optObj.aprInd
        else:
            raise TypeError ('plot_system accets either OpSysData or OpDesign')

    #number of surfaces
    surf_len = len(optSystem.SurfaceData)
    
    #Check if the lens radius are complete
    lensRadius =[]
    if len(lensData) == surf_len:
        lensRadius = lensData
    else:
        lensRadius = [apRadius for q in range(surf_len)]
    
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
            yP.append([z0[q],+lensRadius[q]])
        else:
            if optSystem.SurfaceData[q][1] == 0:               #Check curvature different from 0
                yP.append([z0[q],+lensRadius[q]])
            else:
                radius = 1.0/optSystem.SurfaceData[q][1] 
                if abs(+lensRadius[q]/radius) > 1:                   #Check size
                    yP.append([z0[q]+radius, +abs(radius)])
                else:
                    #r**2=apRadius**2+b**2, zSag = (-)r+b or [+]r-b
                    b = math.sqrt(radius**2-+lensRadius[q]**2)
                    if radius < 0:                             #Decide sag direction
                        yP.append([z0[q]+radius+b,+lensRadius[q]])
                    else:
                        yP.append([z0[q]+radius-b,+lensRadius[q]])

  
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
                                           ,c='black',lw=1.0,ls='--'))
    
    # Surfaces
    for q in range(surf_len):
        #Plot first surface, last surface and curvature equal zero as planes
        if  q == 0 or q==(surf_len-1) or optSystem.SurfaceData[q][1] == 0:
            lines2D.append(matplotlib.lines.Line2D((yP[q][0],yP[q][0])
                                                  ,(yP[q][1],-yP[q][1])
                                                  ,c='black',lw=1.0,ls='-'))
        else:
            radius = 1.0/optSystem.SurfaceData[q][1] 
            diam = abs(2*radius)
            if abs(+lensRadius[q]/radius) > 1:
                theta = 90.0
            else:
                theta = math.asin(abs(+lensRadius[q]/radius))*(180/pi)
            
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
    HIGH=1.5
    if apIndex != -1:
        # apRadius stop
        lines2D.append(matplotlib.lines.Line2D((z0[apIndex],z0[apIndex]),(apRadius,apRadius*HIGH)
                                               ,c='black',lw=2.0,ls='-'))
        lines2D.append(matplotlib.lines.Line2D((z0[apIndex],z0[apIndex]),(-apRadius,-apRadius*HIGH)
                                               ,c='black',lw=2.0,ls='-'))
    
    
    #Append arcs and lines to the figigure (fig) and axes (ax)
    for q in surfPatch:
        fig.gca().add_patch(q)
    for w in lines2D:
        ax.add_line(w)
    
    #Plot limits
    xlim =[z0[0]-1,z0[-1]+1]
    yPoints=[q[1] for q in yP]
    maxY = max(yPoints)*1.1
    ylim =[-maxY,+maxY]
    
    if show:
        #fig, ax = plt.subplots()
        plt.xlim(xlim)
        plt.ylim(ylim)
        plt.show()
    
    return fig,ax,xlim,ylim

def plotRayTrace(rayTrace,fig,ax):
    #number of surfaces
    dim = rayTrace.shape
    print dim
    lines2D  = []
    q=0
    
    for q in range(dim[0]):
        #list the Z coordinates
        z0=[]
        for w in range(dim[2]):
            if w == 0:
                z0.append(0)
            else:
                z0.append(z0[w-1] + rayTrace[q][0][w-1])
    
        for w in range(1,dim[2]):
            lines2D.append(matplotlib.lines.Line2D((z0[w-1]+ rayTrace[q][7][w-1]
                                                   ,z0[w]  + rayTrace[q][7][w])
                                                  ,(rayTrace[q][9][w-1],rayTrace[q][9][w])))    
    
    for w in lines2D:
        ax.add_line(w)
    
    return fig,ax

if __name__ == '__main__':
    from ray_src import PointSource
    from opt_sys import OpSysData
    from opt_dsg import OpDesign
    #import matplotlib.pyplot as plt
    
    syst1 = OpSysData()
    syst1.add_surface(2,+0.2,1.5)
    syst1.add_surface(4,-0.2,1.1)
    syst1.add_surface(3,-0.3,1)
    syst1.add_surface(4,+0.4,1.8)
    #syst1.changeSurface(4,1,2,surfIndex=0)
    #syst1.changeSurface(4,1,2,surfIndex=5)
    #syst1.changeapRadius(2,1.0)
    lensData=[1,2,1,1,1,1]
    
    pto1  = PointSource([0,0.5,0],635)
    
    design1  = OpDesign(pto1,syst1,aprRad=1.0,aprInd=1)

    #syst1.invertSurfaceOrder(0,5);lensData=[1,1,1,1,2,1]
    
    #syst1.invertSurfaceOrder(1,3)
    #print(syst1.SurfaceData)
    fig, ax = plt.subplots()
    fig, ax, xlim, ylim = plot_system(design1,lensData=lensData,fig=fig,ax=ax,show=True)
    fig, ax, = plotRayTrace(design1.raySrcTrace,fig,ax)
    fig, ax, = plotRayTrace(design1.dsgPtoTrace,fig,ax)
    
    #fig, ax = plt.subplots()
    #for q in arcs:
    #    fig.gca().add_patch(q)
    #for w in line2d:
    #    ax.add_line(w)
    #
    #plt.xlim([-5,+35])
    #plt.ylim([-4,+4])
    #plt.show()
    
    
    #line2d_ray = plotRayTrace(rayTrace) 