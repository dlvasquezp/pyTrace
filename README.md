# pyTrace

The module pyTrace is based on two concepts:

1.1) ray: A ray is a list of elements describing the ray position, direction and 
wavelength.

    ray0 = [[X,Y,Z], [L,M,N],wvln]
    [X,Y,Z]: position in mm
    [L,M,N]: direction cosines
    wvln:    wavelength in µm
    
1.2) surface: A surface is a list of elements describing the surface distance, 
curvature, refraction index (material) and surface type.

    surf0 = [d,C,n,'type']
    d: distance to the next surface in mm
    C: curvature (1/r) in mm
    n: refraction index (float) or material name (string)
    type: (optional) surface type e.g. 'paraxial','standard','grin' 
    
From this two concepts the following classes are created:

2.1) ray_src: a ray surce is a collection of ray (lists), where their relative 
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
    ray5,6,7...: rays directed in any direction to the AP
    
    Two sub-types of ray source are supported; point source and infinity source. 
    On the point source all the rays share the same origin ([X,Y,Z]) but differ in
    the direction. On the infinity source all the rays share the same direction 
    ([L,M,N]) but differ in the origin.
    
2.2) opt_sys: a optical system is a collection of surfaces (lists), where their
              relative position (index) has a particular roll.
            
    #           roll              
    0           object
    1           surface
    ...           
    N           image (last surface) 
    
Finally with a ray source and an optical system an optical design are defined.

3.1) opt_dsg: A optical design accepts a ray source and a optical system to 
              to perform a ray trace. An important attribute of the optical 
              design is the position and size of the AP. With this information
              the optical system can calculate the rays direction and optical 
              properties of the system.
              
3.2) trace: A trace is a function where the rays are propagated through the 
            surfaces. It is based on propagation Welford's method 
       
