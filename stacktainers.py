import numpy as np
from stl import mesh

class ContainerFabric:

    def __init__(self, wallwidth=0.8, gap=0.1):
        self.wallwidth = wallwidth
        self.gap = gap

    def ExportContainer(self, x=42, y=42, z=42, sizetype='ext'):
        g = self.gap
        w = self.wallwidth
        gw = g+w
        i = 4 # Insertion height
        e = i+2 # Expansion Height

        vertices = np.array(
            [
                [gw,gw,0], [gw,y-gw,0], [x-gw,y-gw,0], [x-gw,gw,0], # Bottom face points
                [gw,gw,i], [gw,y-gw,i], [x-gw,y-gw,i], [x-gw,gw,i], # Insertion
                [0,0,6], [0,y,6], [x,y,6], [x,0,6], # Expansion
                [0,0,z], [0,y,z], [x,y,z], [x,0,z] # Walls
            ]
        )

        faces = np.array(
            [
                [0,1,2], [0,2,3], # Bottom
                # [1,0,4], [4,5,1], [1,5,6], [1,6,2], [6,3,2], [7,3,6], [7,0,3], [7,4,0], # Insertion
                [1,0,4], [4,5,1], [1,5,2], [6,2,5], [6,3,2], [7,3,6], [7,0,3], [7,4,0], # Insertion
                [5,4,8], [8,9,5], [5,9,6], [9,10,6], [10,7,6], [11,7,10], [11,4,7], [11,8,4], # Expansion
                [9,8,12], [12,13,9], [10,13,14], [10,9,13], [14,11,10], [15,11,14], [15,8,11], [15,12,8], # Walls
                [12,14,13], [12,15,14] # Top
            ]
        )

        container = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                container.vectors[i][j] = vertices[f[j],:]

        # Write the mesh to file "cube.stl"
        container.save('Stacktainer_%sx%sx%s.stl' % (x,y,z))


cf = ContainerFabric()
cf.ExportContainer()
cf.ExportContainer(20,20,40)
cf.ExportContainer(84,84,44)