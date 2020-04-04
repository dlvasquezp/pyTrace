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

    surf0= [d,C,n,'type']
    d: distance to the next surface in mm
    C: curvature (1/r) in mm
    n: refraction index (float) or material name (string)
    type: (optional) surface type e.g. 'paraxial','standard','grin' 
