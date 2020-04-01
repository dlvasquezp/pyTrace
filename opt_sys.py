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
            surfType: surface type ('object', 'surface', 'image')
        Aperture: list (semiradius, surfIndex)
            semiradius: aperture radio (mm)
            surfIndex: surface index where the aperture is located
    '''
    def __init__(self):                      
        self.SurfaceData=[]
        self.SurfaceData.append([10,0,1,'object'])
        self.SurfaceData.append([ 0,0,1,'image' ])
        self.Aperture = []
        self.changeAperture(2.0,surfIndex=1)
    
    def addSurface(self, d, C, n,surfIndex=-1):
        surf_len= len(self.SurfaceData)
        
        if surfIndex > 0 and surfIndex < surf_len:
            self.SurfaceData.insert(surfIndex,[d,C,n,'surface']) 
        else:
            if surfIndex == -1:
                #if surfIndex not defined, append to the last position before 'image'
                self.SurfaceData.insert((surf_len-1),[d,C,n,'surface']) 
            else:
                raise ValueError('addSurface: invalid surface index')
                
                
    def changeSurface(self, d, C, n,surfIndex=-1):
        surf_len= len(self.SurfaceData)
        
        if surfIndex > 0 and surfIndex < surf_len:
            self.SurfaceData[surfIndex]=[d,C,n,'surface'] 
        else:
            if surfIndex == 0:
                #The object plane is changed, curvature is ignored.
                self.SurfaceData[0]=[d,0,n,'object']
            else:
                raise ValueError('changeSurface: invalid surface index ')
            
            
    def deleteSurface(self,surfIndex=-1):
        surf_len= len(self.SurfaceData)
        
        if surfIndex > 0 and surfIndex < (surf_len-1):
            del self.SurfaceData[surfIndex]
        else:
            raise ValueError('deleteSurface: invalid surface index')
        
        
    def changeAperture(self,semiradius,surfIndex=-1):
        surf_len= len(self.SurfaceData)
        
        if surfIndex > 0 and surfIndex < surf_len:     #Check for vaid indices
            self.Aperture = [semiradius,surfIndex]
        else:
            raise ValueError('changeAperture: invalid surface index')
            
            
    def invertSurfaceOrder(self, surf1, surf2):                   #still missing surf# validation
        surf_len= len(self.SurfaceData)
        
        assert surf1 > 0,            'invertSurface: surf1 invalid'
        assert surf2 < (surf_len-1), 'invertSurface: surf2 invalid'
        assert surf1 < surf2,        'invertSurface: surf1 > surf2'
        
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
    syst1.changeSurface(2,5,1,surfIndex=0)
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