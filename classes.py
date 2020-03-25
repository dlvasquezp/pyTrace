# -*- coding: utf-8 -*-
"""
@author: vasquezpinzondavid
"""
import math
import numpy as np

def Trace(RayList,SurfaceData):
    #RayList    : [list[tuples]]
    #SurfaceData: [list[tuples]]
    i = len(RayList)                          # Ray i
    j = 23                                    # [d,c,n][X0,Y0][F,G,Delta][X,Y,Z][check1][alfa,beta,gamma][lambda][cosI,CosIp][K][L,M,N][Check2]
    k = len(SurfaceData)                      # Surface k
    RayTrace = np.zeros([i,j,k])
    RayTrace = FillFirst(RayList,SurfaceData,RayTrace,i,k)
    RayTrace = makeTrace(RayTrace,i,k)
    
    return RayTrace

def FillFirst(RayList,SurfaceData,RayTrace,i,k):
    for q in range (0,i):                                       # i -> ray indice
        RayTrace[q,8 ,0] = RayList[q][0][0]                     # X coordinate from object
        RayTrace[q,9 ,0] = RayList[q][0][1]                     # Y coordinate from object
        RayTrace[q,10,0] = RayList[q][0][2]                     # Z coordinate from object
            
        RayTrace[q,15,0] = RayList[q][2][0]                     # Wavelength in nm
            
        RayTrace[q,19,0] = RayList[q][1][0]                     # X cosine director
        RayTrace[q,20,0] = RayList[q][1][1]                     # Y cosine director
        RayTrace[q,21,0] = RayList[q][1][2]                     # Z cosine director
        
        for w in range (0,k):                                        # k -> surface indice
            RayTrace[q,0,w] = SurfaceData[w][0]                # distance in mm
            RayTrace[q,1,w] = SurfaceData[w][1]                # curvature in 1/mm
            RayTrace[q,2,w] = SurfaceData[w][2]                # refraction indice

    return RayTrace

def makeTrace(RayTrace,i,k):
    for q in range (0,i):                                                   #i -> ray indice
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
            Delta = F / (G + math.sqrt(G**2-c*F) )
            
            X = X0 + Lmin1*Delta
            Y = Y0 + Mmin1*Delta
            Z = Nmin1*Delta
            
            check1= 0                                        # The check is missing
            
            #Refraction
            
            n   = RayTrace[q,2,w-1]
            np  = RayTrace[q,2,w]
            
            alfa = -c*X
            beta = -c*Y
            gamma= 1 - c*Z
            
            
            CosI  = math.sqrt(G**2 - c*F)
            CosIp = (1/np)*math.sqrt(np**2 - (n**2)*(1-CosI**2))
            K = c*(np*CosIp - n*CosI) 
            
            L = (1/np)*(n*Lmin1 - K*X )
            M = (1/np)*(n*Mmin1 - K*Y )
            N = (1/np)*(n*Nmin1 - K*Z + np*CosIp - n*CosI)
            
            check2= L**2 + M**2 + N**2 - 1
            
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
    
class OpSysData:
    '''
    3 superficies deben ser creadas y la apertura debe ser asignada automaticamente
    listas de listas
    '''
    # Still mising a property for aperture and radious
    def __init__(self, d ,C, n):                 #d:distance mm, C: curvature (1/mm), n: refraction index, (-)
        self.SurfaceData=[tuple([d,C,n])]
    
    def addSurface(self, d, C, n):
        self.SurfaceData.append(tuple([d,C,n]))
        
class PointSource:                                     #Only for point source, for points at infinity other function is needed
    def __init__(self, XYZ, Lambda):                   #Vectors as entry
        # Initialize ray list
        self.RayList = []
        self.Position= XYZ
        # Create default rays #0,1,2
        self.NewRay([0,0,1], Lambda)
        self.NewRay([0,0,1], Lambda)
        self.NewRay([0,0,1], Lambda)
        
    def NewRay(self, LMN, Lambda):
        self.RayList.append(tuple([self.Position,LMN,Lambda]))
        
    def ReplaceRay(self, RayIndex, ReplacementRay):   
        self.RayList[RayIndex] = ReplacementRay
    
    def ReplaceRayCosineDir(self, RayIndex, CosDir):
        ModRay = tuple([self.RayList[RayIndex][0],CosDir,self.RayList[RayIndex][2]])
        self.ReplaceRay(RayIndex, ModRay)
        #self.RayList[RayIndex][1] = CosDir
        

# Merit function
def meritFun ( x0,*arg):
    # x0: (vector)[double angle,int surface]
    # *arg: (list) [object Ray, object Surface] # still missing: ApertureR, Surface
    alfa = x0[0]
    Surf = int(x0[1])
    X=[0,math.cos(alfa),math.sqrt(1-math.cos(alfa)**2)]
    arg[0].ReplaceRayCosineDir(0,X)
    RayList   = arg[0].RayList
    OpSysData = arg[1].SurfaceData
    RayTrace  = Trace(RayList,OpSysData)
    ApertureR = 4                                       # Aperdure radius [mm]
    result    = abs(ApertureR-RayTrace[0, 9 ,Surf])
    return result
  