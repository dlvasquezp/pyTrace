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

2.1) RaySource: is a class which contains collection of rays (lists) and a set 
                of methods to add modify or delete rays. 
                
Two sub-classes of ray source are supported: 

2.1.1)PointSource: all the rays share the same origin ([X,Y,Z]) but differ in 
                   the direction.
                   
2.1.2)InfinitySource: all the raysshare the same direction ([L,M,N]) but differ 
                      in the origin.

In the Point/Infinity source, the ray position (index) has a particular roll. 
The first 5 rays (0 to 4) are named "essential" because they are necessary for 
any optical design characterization.
            
    index       Name when on axis           Name when off axis
    0           optical axis                chief ray
    1           y upper marginal ray        y upper coma ray     (y:meridional)
    2           y lower marginal ray        y lower coma ray
    3           x positive marginal ray     x positive coma ray  (x:sagital)
    4           x negative marginal ray     x negative coma ray       
    5 or >      screw ray                   screw ray  
    
    ray#index
    ray0: (or chief ray)is directed to the aperture stop (AP) center
    ray1: (or marginal ray)is directed to the meridional upper AP boundary
    ray2: is directed to the meridional AP lower boundary
    ray3: is directed to the sagital positive AP boundary
    ray4: is directed to the sagital negative AP boundary
    ray5,6,7...: rays directed in any direction to the AP
    

    
2.2) opt_sys: a optical system is a collection of surfaces (lists).
            
    #           Nmae              
    0           object
    1           surface
    ...         surface  
    N           image (last surface) 
    
Finally with a ray source and an optical system a ray trace can be done,

3.1) trace: A trace is a function where the rays are propagated through the 
            surfaces. It is based on propagation Welford's method. It returns 
            a matrix called RayTrace with the propagation values.
            
For sake of simplicity an optical design is define, which will find automatically 
the values need for the design evaluation:

4.1) opt_dsg: A optical design accepts a ray source and a optical system to 
              to perform a ray trace. An important attribute of the optical 
              design is the position and size of the AP. With this information
              the optical system can calculate the rays direction and optical 
              properties of the system.
              
              Each optical design has the following attributes:
              
              Arguments passed by the user:
              ray_src: ray source
              opt_sys: optical system
              apr_rad: aperture stop radius 
              apr_ind: aperture stop index
              
              Attributes created when instantiated:
              dsg_pto: point source at position [0,0,0] 
              dsg_inf: source at infinity with direction [0,0,1]
              
              RayTrace calculated when instantiated:
              ray_src_trace -> ray source and optical system
              dsg_pto_trace -> point source and optical system
              dsg_inf_trace -> source at infinity and optical system
              
              Merit functions used in the process:
              essential_LMN: calculate the direction LMN of the point source
                             "essential" rays. It returns the difference (error) 
                             between the ray position and the aperture coordinate.
              essential_XYZ: calculate the position XYZ of a source at infiniy
                             "essential" rays. It returns the difference (error) 
                             between the ray position and the aperture coordinate.
              
              
              
              

       
