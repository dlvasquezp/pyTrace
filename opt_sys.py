# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 19:29:17 2020

@author: David Vasquez
"""

class OpSysData:
    '''
    Properties:
        SurfaceData: list of lists, (d,C,n,surfType)
            d: distance (mm)
            C: curvature (1/mm)
            n: refraction index (-)
            surfType: surface type ('standard', 'paraxial', 'grin')
    '''
    def __init__(self):                      
        self.SurfaceData=[]
        self.SurfaceData.append([10,0,1,'standard']) #object
        self.SurfaceData.append([ 0,0,1,'standard']) #image
    
    def addSurface(self, d, C, n, surfType='standard',surfIndex=-1):
        surf_len= len(self.SurfaceData)
        
        if surfIndex >= 0 and surfIndex <= surf_len:
            self.SurfaceData.insert(surfIndex,[d,C,n,surfType]) 
        else:
            if surfIndex == -1:
                #if surfIndex not defined, append to the last position before 'image'
                self.SurfaceData.insert((surf_len-1),[d,C,n,surfType]) 
            else:
                raise ValueError('addSurface: invalid surface index')
                
                
    def changeSurface(self, d, C, n, surfType='standard',surfIndex=-1):
        surf_len= len(self.SurfaceData)
        
        if surfIndex >= 0 and surfIndex <= surf_len:
            self.SurfaceData[surfIndex]=[d,C,n,surfType] 
        else:
            raise ValueError('changeSurface: invalid surface index ')
            
            
    def deleteSurface(self,surfIndex=-1):
        surf_len= len(self.SurfaceData)
        
        if surfIndex >= 0 and surfIndex < surf_len:
            del self.SurfaceData[surfIndex]
        else:
            if surfIndex == -1:
                del self.SurfaceData[(surf_len-2)]    
            else:
                raise ValueError('deleteSurface: invalid surface index')
            
            
    def invertSurfaceOrder(self, surf1, surf2):                   
        surf_len= len(self.SurfaceData)
        
        assert surf1 >= 0       ,     'invertSurface: surf1 invalid'
        assert surf2 <  surf_len,     'invertSurface: surf2 invalid'
        assert surf1 <  surf2   ,     'invertSurface: surf1 > surf2'
        
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
    import matplotlib.pyplot as plt
    
    #Create system
    syst1 = OpSysData()
    syst1.changeSurface(0,5,1,surfIndex=0)
    syst1.addSurface(2,1.0,2)
    syst1.addSurface(2,1/2.0,2)
    syst1.addSurface(10,1/2.0,2)
    syst1.addSurface(3,1/3.0,3)
    syst1.addSurface(4,1/4.0,1)
    print('Optical system data')
    print(syst1.SurfaceData)
    
    #Test changeSurface
    syst1.changeSurface(9,1/9,4,surfIndex=3)
    print('Surface 3 changed')
    print(syst1.SurfaceData)
    
    #Test deleteSurface
    syst1.deleteSurface(surfIndex=3)
    print('Surface 3 deleted')
    print(syst1.SurfaceData)
    
    #Test invert surface
    #syst1.invertSurfaceOrder(0,5)
    
    #Plot system
    arcs,line2d = plotSystem(syst1)
    
    fig, ax = plt.subplots()
    for q in arcs:
        fig.gca().add_patch(q)
    for w in line2d:
        ax.add_line(w)
    
    plt.xlim([-5,+35])
    plt.ylim([-6,+6])
    plt.show()