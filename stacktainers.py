import numpy as np
from stl import mesh

class ContainerFabric:
    """
    2x1, 2x2, 2x3, 3x3
    """

    def __init__(self, wallwidth=0.8, gap=0.1, freegap=0.2, bevel=1):
        self.wallwidth = wallwidth
        self.gap = gap
        self.freegap = freegap
        self.bevel = bevel
        self.insertionheight = 4 # Insertion height
        self.expansionheight = self.insertionheight+2 # Expansion Height
        print("Initialisation container fabric\nCommon settings: \n\twall width: %s, bevel: %s\n\tgap (tight fit): %s, freegap (free fit): %s\n\t insertion height: %s, expansion height: %s" % (self.wallwidth, self.bevel, self.gap, self.freegap, self.insertionheight, self.expansionheight))

    def ExportContainer(self, x=42, y=42, z=42, sizetype='ext', layouts=[]):
        g = self.gap
        w = self.wallwidth
        gw = g+w
        b = self.bevel # Bevel
        gwb = gw + b * 0.5
        ih = self.insertionheight
        eh = self.expansionheight
        

        print("\nCreating new container: %sx%sx%s" % (x,y,z))
        
        vertices = np.array(
            [
                [gwb,gwb,0], [gwb,y-gwb,0], [x-gwb, y-gwb,0], [x-gwb, gwb,0], # Bottom
                [gwb,gw,b], [gw, gwb,b], [gw,y-gwb,b], [gwb,y-gw,b], [x-gwb, y-gw,b], [x-gw,y-gwb,b], [x-gw,gwb,b], [x-gwb,gw,b], # Insertion
                [gwb,gw,ih], [gw, gwb,ih], [gw,y-gwb,ih], [gwb,y-gw,ih], [x-gwb, y-gw,ih], [x-gw,y-gwb,ih], [x-gw,gwb,ih], [x-gwb,gw,ih], # Insertion
                [b,0,eh], [0,b,eh], [0,y-b,eh], [b,y,eh], [x-b,y,eh], [x,y-b,eh], [x,b,eh], [x-b,0,eh], # Wall
                [b,0,z], [0,b,z], [0,y-b,z], [b,y,z], [x-b,y,z], [x,y-b,z], [x,b,z], [x-b,0,z] # Wall and top
            ]
        )
        faces = np.array(
            [
                [0,1,2], [0,2,3], # Bottom
                [5,0,4], [1,0,6], [5,6,0], [6,7,1], [8,2,1], [8,1,7], [9,2,8], [10,3,2], [10,2,9], [11,3,10], [4,0,3], [4,3,11], # Bevel
                [12,5,4], [12,13,5], [13,6,5], [13,14,6], [14,7,6], [14,15,7], [15,8,7], [15,16,8], [16,9,8], [16,17,9], [17,10,9], [17,18,10], [18,11,10], [18,19,11], [19,4,11], [19,12,4], # Insertion
                [20,13,12], [20,21,13], [21,14,13], [21,22,14], [22,15,14], [22,23,15], [23,16,15], [23,24,16], [24,17,16], [24,25,17], [25,18,17], [25,26,18], [26,19,18], [26,27,19], [27,12,19], [27,20,12], # Expansion
                [28,21,20], [28,29,21], [29,22,21], [29,30,22], [30,23,22], [30,31,23], [31,24,23], [31,32,24], [32,25,24], [32,33,25], [33,26,25], [33,34,26], [34,27,26], [34,35,27], [35,20,27], [35,28,20], # Wall
                [28,30,29], [28,31,30], [28,35,31], [35,32,31], [35,34,32], [34,33,32] # Top
            ]
        )


        container = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                container.vectors[i][j] = vertices[f[j],:]

        container.save('Stacktainer_%sx%sx%s.stl' % (x,y,z))

        if layouts:
            print("Creating subtainers %s" % layouts)
            newz = z - ih - gw
            for layout in layouts:
                xcount, ycount = layout.split('x')
                xcount = int(xcount); ycount = int(ycount)
                newx = round((x - w*2 - g*(xcount+1))/xcount,2)
                newy = round((y - w*2 - g*(ycount+1))/ycount,2)
                self.ExportContainer(newx,newy,newz)


cf = ContainerFabric()
cf.ExportContainer(84,84,46, layouts=["2x1", "2x2", "3x1", "3x2", "4x1"])