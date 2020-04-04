# pyTrace

The module pyTrace is based on two concepts:

a) ray: A ray is a list of elements describing the ray position, direction and 
wavelength.

    ray0 = [[X,Y,Z], [L,M,N],wvln]
    [X,Y,Z]: position in mm
    [L,M,N]: direction cosines
    wvln:    wavelength in µm
    
b) surface: A surface is a list of elements describing the surface distance, 
curvature, refraction index (material) and surface type.

    surf0 = [d,C,n,'type']
    d: distance to the next surface in mm
    C: curvature (1/r) in mm
    n: refraction index (float) or material name (string)
    type: (optional) surface type e.g. 'paraxial','standard','grin' 
    
From this two concepts the following classes are created:

c) ray_src: a ray surce is a collection of ray (lists), where their relative 
            position (index) has a particular roll.
            
    #           on axis                     off axis
    0           optical axis                chief ray
    1           y upper marginal ray        y upper coma ray     (y:meridional)
    2           y lower marginal ray        y lower coma ray
    3           x positive marginal ray     x positive coma ray  (x:sagital)
    4           x negative marginal ray     x negative coma ray       
    5 or >      screw ray                   screw ray  
    
    ray#index
    ray0: (or chief ray)is directed to the  sperture stop (AP) center
    ray1: (or marginal ray)is directed to the meridional upper AP boundary
    ray2: is directed to the meridional AP lower boundary
    ray3: is directed to the sagital positive AP boundary
    ray4: is directed to the sagital negative AP boundary
    ray5,6,7...: rays directed to the AP
    
d) opt_sys: a optical system is a collection of surfaces (lists), where their
            relative position (index) has a particular roll.
            
    #           roll              
    0           object
    1           surface
    ...           
    N           image (last surface) 
       
