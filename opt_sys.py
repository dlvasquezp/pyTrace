# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 19:29:17 2020

@author: David Vasquez
"""

class OpSysData:
    '''
    Attributes:
        SurfaceData: list of lists, (d,C,n,surfType)
        d: distance (mm)
        C: curvature (1/mm)
        n: refraction index (-)
        surfType: surface type ('standard', 'paraxial', 'grin')
    '''
    
    surfaceTypes = {'standard', 'paraxial', 'grin'}
    
    def __init__(self):                      
        self.SurfaceData=[]
        self.add_surface(10,0,1,'standard',surfIndex=0) #object
        self.add_surface( 0,0,1,'standard',surfIndex=1) #image
    
    def add_surface(self, d, C, n, surfType='standard',surfIndex=-1):
        self.check_arguments(d=d,C=C,n=n,surfType=surfType)
        surf_len= len(self.SurfaceData)
        
        if surfIndex >= 0 and surfIndex <= surf_len:
            self.SurfaceData.insert(surfIndex,[d,C,n,surfType]) 
        else:
            if surfIndex == -1:
                #if surfIndex not defined, append to the last position before 'image'
                self.SurfaceData.insert((surf_len-1),[d,C,n,surfType]) 
            else:
                raise ValueError('addSurface: invalid surface index')
                
                
    def change_surface(self, d, C, n, surfType='standard',surfIndex=-1):
        self.check_arguments(d=d,C=C,n=n,surfType=surfType)
        surf_len= len(self.SurfaceData)
        
        if surfIndex >= 0 and surfIndex <= surf_len:
            self.SurfaceData[surfIndex]=[d,C,n,surfType] 
        else:
            raise ValueError('changeSurface: invalid surface index ')
            
            
    def delete_surface(self,surfIndex=-1):
        surf_len= len(self.SurfaceData)
        
        if surfIndex >= 0 and surfIndex < surf_len:
            del self.SurfaceData[surfIndex]
        else:
            if surfIndex == -1:
                del self.SurfaceData[(surf_len-2)]    
            else:
                raise ValueError('deleteSurface: invalid surface index')
            
            
    def invert_surface_order(self, surf1, surf2):                   
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
        
    def check_arguments(self,d='nan',C='nan',n='nan',surfType='nan'):
        if d!='nan':
            assert isinstance(d,(int,float)), 'distance [d] must be either int of float'
        if C!='nan':
            assert isinstance(C,(int,float)), 'curvature [C] must be either int of float'
        if n!='nan':
            assert isinstance(C,(int,float,str)), 'refraction index [n] must be either int,float or str'
        if surfType!='nan':
            assert surfType in self.surfaceTypes, 'Surface type [surfType] not supported'
        
if __name__=='__main__':
    
    from plt_fnc import plot_system
    import matplotlib.pyplot as plt
    
    #Create system
    syst1 = OpSysData()
    syst1.change_surface(2,0,1,surfIndex=0)
    syst1.add_surface(2,1.0,2)
    syst1.add_surface(2,1/2.0,2)
    syst1.add_surface(10,1/2.0,2)
    syst1.add_surface(3,1/3.0,3)
    syst1.add_surface(4,1/4.0,1)
    print('Optical system data')
    print(syst1.SurfaceData)
    
    #Test changeSurface
    syst1.change_surface(9,1/9,4,surfIndex=3)
    print('Surface 3 changed')
    print(syst1.SurfaceData)
    
    #Test deleteSurface
    syst1.delete_surface(surfIndex=3)
    print('Surface 3 deleted')
    print(syst1.SurfaceData)
    
    #Test invert surface
    syst1.invert_surface_order(0,5)
    
    #Plot system
    arcs,line2d = plot_system(syst1)
    
    fig, ax = plt.subplots()
    for q in arcs:
        fig.gca().add_patch(q)
    for w in line2d:
        ax.add_line(w)
    
    plt.xlim([-5,+35])
    plt.ylim([-6,+6])
    plt.show()