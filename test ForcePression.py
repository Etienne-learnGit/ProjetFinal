import numpy

def calculForcePression(N, F):
        rho = 1025
        g = 9.81
        AB = numpy.array([F[1][0]-F[0][0], F[1][1]-F[0][1], F[1][2]-F[0][2]])
        AC = numpy.array([F[2][0]-F[0][0], F[2][1]-F[0][1], F[2][2]-F[0][2]])
        normale = numpy.array(N)
        produitVectoriel = numpy.cross(AB, AC)
        dS = numpy.linalg.norm(produitVectoriel) / 2
        coordG = [(F[0][0] + F[1][0] + F[2][0]) / 3, (F[0][1] + F[1][1] + F[2][1]) / 3, (F[0][2] + F[1][2] + F[2][2]) / 3 ]
        FPression = -rho*g*dS*normale*abs(coordG[2])
        return FPression

NRectangle3 = [-0,-0,-1]
"""
FRectangle3 = [[4, -1.0, 0.0], [2, -1, 0.0], [0, 0, 0.0]]
On translate manuellement la facette pour l'immerger -->
"""
FRectangle3 = [[4, -1, -1],[2, -1, -1], [0, 0, -1]]
print("Force Pression facette Rectangle1 = ", calculForcePression(NRectangle3,FRectangle3))


NTriangle = [-0, 0.70710678118654746, -0.70710678118654746]
"""
FTriangle = [[4, 0, 0], [0, 1, 1], [4, 1, 1]]
On translate manuellement la facette pour l'immerger -->
"""
FTriangle = [[4, 0, -1], [0, 1, 0], [4, 1, 0]]
print("Force Pression facette Rectangle1 = ", calculForcePression(NTriangle,FTriangle))


NRectangle = [0, -1, -0]
"""
FRectangle = [[0, -1, 0], [2, -1, 0], [2, -1, 1]]
On translate manuellement la facette pour l'immerger -->
"""
FRectangle = [[0, -1, -1], [2, -1, -1], [2, -1, 0]]
print("Force Pression facette Triangle1 = ", calculForcePression(NRectangle,FRectangle))
