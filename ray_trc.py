# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 05:44:55 2020

@author: David Vasquez
"""
from catalog import OPT_GLASS, sellmeierDispForm
import math
import numpy

def Trace(RayList,SurfaceData):
    '''
    RayList    : list of lists, ([x,y,z],[cosX,cosY,cosZ], lambda, rayType)
    SurfaceData: list of lists, (d,C,n,surfType)
    RayTrace: numpy.ndarray  [d,c,n]            distance,curvature,refraction index
                             [X0,Y0]            last position X,Y
                             [F,G,Delta]        -
                             [X,Y,Z]            new position X,Y,Z
                             [check1]           -
                             [alfa,beta,gamma]  last direction cosines 
                             [lambda]           Wavelength
                             [cosI,CosIp]       -
                             [K]                -
                             [L,M,N]            new direction cosines
                             [Check2]           -
                         
            The position is represented by the index.
            In the array, i represent the ray, j the data and k the surface
            
    When the rays are not propagated, the values are NaN
    Missing: scale the function to list of points and surfaces Data
    '''
    i = len(RayList)                          # Ray i
    j = 23                                    # [d,c,n][X0,Y0][F,G,Delta][X,Y,Z][check1][alfa,beta,gamma][lambda][cosI,CosIp][K][L,M,N][Check2]
    k = len(SurfaceData)                      # Surface k
    RayTrace = numpy.zeros([i,j,k])
    RayTrace = FillFirst(RayList,SurfaceData,RayTrace,i,k)
    RayTrace = makeTrace(RayTrace,i,k)
    
    return RayTrace

def FillFirst(RayList,SurfaceData,RayTrace,i,k):
    for q in range (0,i):                                       # i -> ray indice
        RayTrace[q,8 ,0] = RayList[q][0][0]                     # X coordinate from object
        RayTrace[q,9 ,0] = RayList[q][0][1]                     # Y coordinate from object
        RayTrace[q,10,0] = RayList[q][0][2]                     # Z coordinate from object
        
        RayTrace[q,11,0] = 1                                    # Chech 1 -> true
        RayTrace[q,15,:] = RayList[q][2]                        # Wavelength in nm
        
        RayTrace[q,19,0] = RayList[q][1][0]                     # X cosine director
        RayTrace[q,20,0] = RayList[q][1][1]                     # Y cosine director
        RayTrace[q,21,0] = RayList[q][1][2]                     # Z cosine director 
        
        RayTrace[q,22,0] = 1                                    # Chech 2 -> true
        
        for w in range (0,k):                                  # k -> surface indice
            RayTrace[q,0,w] = SurfaceData[w][0]                # distance in mm
            RayTrace[q,1,w] = SurfaceData[w][1]                # curvature in 1/mm
            # refraction indice 
            if isinstance(SurfaceData[w][2],basestring):
                try:
                    RayTrace[q,2,w] = sellmeierDispForm (OPT_GLASS[SurfaceData[w][2]]
                                                        ,RayList[q][2])
                except KeyError:
                    raise ValueError('%s, non existent glass material' % SurfaceData[w][2])
            else:
                RayTrace[q,2,w] = SurfaceData[w][2]                 
            
        
            
    return RayTrace

def makeTrace(RayTrace,i,k):
    for q in range (0,i):                                             #i -> ray indice
        for w in range (1,k):                                         #k -> surface indice, start in 1
                
            #Transfer part1
            dmin1 = RayTrace[q,0 ,w-1]
            
            Xmin1 = RayTrace[q,8 ,w-1]
            Ymin1 = RayTrace[q,9 ,w-1]
            Zmin1 = RayTrace[q,10,w-1]
            
            Lmin1 = RayTrace[q,19,w-1]
            Mmin1 = RayTrace[q,20,w-1]
            Nmin1 = RayTrace[q,21,w-1]
            
            X0 = Xmin1 + (Lmin1/Nmin1)*(dmin1-Zmin1)
            Y0 = Ymin1 + (Mmin1/Nmin1)*(dmin1-Zmin1)
            
            #Transfer part2
            
            c = RayTrace[q,1,w]
            
            F = c*(X0**2+Y0**2)
            G = Nmin1 - c*(Lmin1*X0+Mmin1*Y0)
            
            try:
                Delta = F / (G + math.sqrt(G**2-c*F) )
            except ValueError:
                #Surface not found
                RayTrace[q,3:11,w:]  = numpy.NaN
                RayTrace[q,12:15,w:] = numpy.NaN
                RayTrace[q,16:22,w:] = numpy.NaN
                break 
            
            X = X0 + Lmin1*Delta
            Y = Y0 + Mmin1*Delta
            Z = Nmin1*Delta
            
            # The ray i meet the surface k
            check1 = 1
            
            #Refraction
            
            n   = RayTrace[q,2,w-1]
            np  = RayTrace[q,2,w]
            
            alfa = -c*X
            beta = -c*Y
            gamma= 1 - c*Z
            
            
            CosI  = math.sqrt(G**2 - c*F)
            
            try:
                CosIp = (1/np)*math.sqrt(np**2 - (n**2)*(1-CosI**2))
            except ValueError:
                #ray reflected instead of refracted
                RayTrace[q,3:11,w:]  = numpy.NaN
                RayTrace[q,12:15,w:] = numpy.NaN
                RayTrace[q,16:22,w:] = numpy.NaN
                break
            
            K = c*(np*CosIp - n*CosI) 
            
            L = (1/np)*(n*Lmin1 - K*X )
            M = (1/np)*(n*Mmin1 - K*Y )
            N = (1/np)*(n*Nmin1 - K*Z + np*CosIp - n*CosI)
            
            #Check1 and Check for direction cosines
            check2 = int(check1 and numpy.isclose((L**2+M**2+N**2),1))
            
            # Replace
            
            #RayTrace[q,0 ,w] = d                        # From SysData in function "Fillfirst"
            #RayTrace[q,1 ,w] = c                        # From SysData in function "Fillfirst"
            #RayTrace[q,2 ,w] = np                       # From SysData in function "Fillfirst"
            RayTrace[q,3 ,w] = X0
            RayTrace[q,4 ,w] = Y0
            RayTrace[q,5 ,w] = F
            RayTrace[q,6 ,w] = G
            RayTrace[q,7 ,w] = Delta
            RayTrace[q,8 ,w] = X
            RayTrace[q,9 ,w] = Y
            RayTrace[q,10,w] = Z
            RayTrace[q,11,w] = check1
            RayTrace[q,12,w] = alfa
            RayTrace[q,13,w] = beta
            RayTrace[q,14,w] = gamma
            #RayTrace[q,15,w] = Lambda                   # From sysData in function "Fillfirst"
            RayTrace[q,16,w] = CosI
            RayTrace[q,17,w] = CosIp
            RayTrace[q,18,w] = K
            RayTrace[q,19,w] = L
            RayTrace[q,20,w] = M
            RayTrace[q,21,w] = N
            RayTrace[q,22,w] = check2
                
    
    return RayTrace
    

    
#def SeidelCoef(self):
#    self.SeidelCoef = numpy.zeros((self.i,5,self.k))                            # 5 Aberrations
#    
#    for i in range (0,self.i):                                                  # i -> ray indice
#        for k in range (1, self.k):                                             # k -> surface indice (start in 1)
#             
#            n     =  self.RayTrace[i,2,k-1]
#            np    =  self.RayTrace[i,2,k]
#            Ip    =  math.acos(self.RayTrace[i,17,k])
#            h     =  self.RayTrace[i,9,k]
#            U     =  self.RayTrace[i,20,k]
#            Umin1 =  self.RayTrace[i,20,k-1]
#            
#            self.SeidelCoef[i,0,k] = -( (np*Ip)**2 * h * ((U/np)- (Umin1/n) ))
#               
#    print self.SeidelCoef 
#    return 0
 
if __name__ == '__main__':
    from pto_src import PointSource
    from opt_sys import OpSysData
    
    pto1  = PointSource([0,1,0],1040)
    syst1 = OpSysData()
    syst1.addSurface(10,0.005,'N-BK7')
    syst1.addSurface(10,5,1.42)
    syst1.addSurface(10,0.005,'N-K5')
    
    design1 = Trace(pto1.RayList,syst1.SurfaceData)
    
    