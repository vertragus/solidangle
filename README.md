# solidangle
calculate solid angle of a quadrangular/triangular mesh from a set of given viewpoints. 
It uses Oosterom's equation for tetrahedrons https://en.wikipedia.org/wiki/Solid_angle

Requires Python 3 and Anaconda (Numpy, Pandas, Time)

set up 3 folders 'panel','vp','output'  
the former 2 containing the input csv with the same filename as in the variable 'file'.
the latter will contain the exported computation output with the same filename as in the variable 'file'.

IMPORTANT: bring all geometry close to Origin (0,0,0) to improve quality of data output. 
Coordinates may be approximated for faraway geometries.

the input csv should be, for panels (viz. mesh faces): 'x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4', without headers. 
x,y,z are coordinates of vertexes 1,2,3,(4) respectively. 
vertex 4 should be coincident with vertex 3 in case panels are triangular.

the input csv should be, for viewpoints: 'xvp,yvp,zvp', without headers.
xvp,yvp,zvp are coordinates of viewpoints.

the standard output includes the average solid angle, for each panel, calculated over the different viewpoints.
output can be customized based on the generated dataframe, that includes all solid angles subtended by all panels from all viewpoints.

the calculation time may be elevated. It can take up to 12 hours for 1000 faces and 1000 viewpoints.
