# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 20:43:53 2020

@author: David Vasquez
"""
import numpy as np

class PointSource:                                     #Only for point source, for points at infinity other function is needed
    '''
    Properties:
        Position: list (x,y,z), source position in the object plane
        lambda: double, wavelength (nm)
        RayList : list of lists, ([x,y,z],[cosX,cosY,cosZ], lambda, rayType)
            x,y,z: list, position in the object plane
            LMN : list (cosX, cosY, cosZ), cosine directors for each direction, [rads]
            lambda: double, wavelength
            
            #           on axis                     off axis
            0           optical axis                chief ray
            1           y upper marginal ray        y upper coma ray          y=meridional
            2           y lower marginal ray        y lower coma ray
            3           x positive marginal ray     x positive coma ray       x=sagintal
            4           x negative marginal ray     x negative coma ray       positive/negative = pupil cartesian X sign 
            5           screw ray                   screw ray
        All the ray lists should be standard
    
    functions:  NewRay
                ChangeCosineDir
                Propagate
        falta:
        funcion para revisar valores numericos
    '''
    def __init__(self, XYZ, Lambda):                   #Vectors as entry
        # Initialize ray list
        self.Position = XYZ
        self.Lambda = Lambda
        self.RayList = []
        self.RayList.append([self.Position,[0,0,1],self.Lambda,0])    #optical axis/chiefray
        self.RayList.append([self.Position,[0,0,1],self.Lambda,1])    #y upper marginal ray/coma ray
        self.RayList.append([self.Position,[0,0,1],self.Lambda,2])    #y lower marginal ray/coma ray
        self.RayList.append([self.Position,[0,0,1],self.Lambda,3])
        self.RayList.append([self.Position,[0,0,1],self.Lambda,4])
        
    def NewRay(self,XYZ,LMN):
        assert np.isclose(np.sum(np.power(LMN,2)),1),'Not valid direction cosines'
        self.RayList.append([XYZ,LMN,self.Lambda,5])
    
    def ChangeCosineDir(self, RayIndex, LMN):
        assert np.isclose(np.sum(np.power(LMN,2)),1),'Not valid direction cosines'
        self.RayList[RayIndex][1]=LMN

        
if __name__=='__main__':
    # instantiate
    pto1=PointSource([0,4,0],635)
    print(pto1.RayList)
    # change cosine director
    LMN=[0,1,0]
    pto1.ChangeCosineDir(0,LMN)
    print(pto1.RayList)
    # New ray
    pto1.NewRay([1,1,1],[1,0.001,0])
    print(pto1.RayList)
