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

def pousseeArchimede(lstN, lstF):
        FA = [0,0,0]
        for i in range(0, len(lstF)):
            coordG = [(lstF[i][0][0] + lstF[i][1][0] + lstF[i][2][0]) / 3, (lstF[i][0][1] + lstF[i][1][1] + lstF[i][2][1]) / 3, (lstF[i][0][2] + lstF[i][1][2] + lstF[i][2][2]) / 3 ]
            if coordG[2] < 0:
                FA[0] = FA[0] + calculForcePression(lstN[i], lstF[i])[0]
                FA[1] = FA[1] + calculForcePression(lstN[i], lstF[i])[1]
                FA[2] = FA[2] + calculForcePression(lstN[i], lstF[i])[2]
        return numpy.vdot(FA,FA)**(1/2)

def translationDesFacette(valeurDeTranslation, lstF):
        x = valeurDeTranslation
        for elt in range(0, len(lstF)) :
            for elt2 in range(0, 3):
                lstF[elt][elt2][-1] = lstF[elt][elt2][-1] + x
        return lstF

lstNormalesR = [[0.0, -1.0, -0.0], [0.0, -1.0, -0.0], [-0.0, -1.0, 0.0], [-0.0, -1.0, 0.0], [1.0, -0.0, 0.0], [1.0, -0.0, 0.0], [1.0, 0.0, -0.0], [1.0, 0.0, -0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [-0.0, 1.0, -0.0], [-0.0, 1.0, -0.0], [-1.0, -0.0, -0.0], [-1.0, -0.0, -0.0], [-1.0, 0.0, 0.0], [-1.0, 0.0, 0.0], [-0.0, -0.0, -1.0], [-0.0, -0.0, -1.0], [0.0, 0.0, -1.0], [0.0, 0.0, -1.0], [0.0, -0.0, -1.0], [-0.0, -0.0, -1.0], [-0.0, 0.0, 1.0], [-0.0, 0.0, 1.0], [0.0, 0.0, 1.0], [0.0, -0.0, 1.0], [0.0, 0.0, 1.0], [-0.0, 0.0, 1.0]]
lstFacettesR = [[[0.0, -1.0, 0.0], [2.0, -1.0, 0.0], [2.0, -1.0, 1.0]], [[2.0, -1.0, 0.0], [4.0, -1.0, 0.0], [4.0, -1.0, 1.0]], [[4.0, -1.0, 1.0], [2.0, -1.0, 1.0], [2.0, -1.0, 0.0]], [[2.0, -1.0, 1.0], [0.0, -1.0, 1.0], [0.0, -1.0, 0.0]], [[4.0, -1.0, 0.0], [4.0, 0.0, 0.0], [4.0, 0.0, 1.0]], [[4.0, 0.0, 0.0], [4.0, 1.0, 0.0], [4.0, 1.0, 1.0]], [[4.0, 1.0, 1.0], [4.0, 0.0, 1.0], [4.0, 0.0, 0.0]], [[4.0, 0.0, 1.0], [4.0, -1.0, 1.0], [4.0, -1.0, 0.0]], [[4.0, 1.0, 0.0], [2.0, 1.0, 0.0], [2.0, 1.0, 1.0]], [[2.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 1.0]], [[0.0, 1.0, 1.0], [2.0, 1.0, 1.0], [2.0, 1.0, 0.0]], [[2.0, 1.0, 1.0], [4.0, 1.0, 1.0], [4.0, 1.0, 0.0]], [[0.0, 1.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]], [[0.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, -1.0, 1.0]], [[0.0, -1.0, 1.0], [0.0, 0.0, 1.0], [0.0, 0.0, 0.0]], [[0.0, 0.0, 1.0], [0.0, 1.0, 1.0], [0.0, 1.0, 0.0]], [[4.0, -1.0, 0.0], [2.0, -1.0, 0.0], [4.0, 0.0, 0.0]], [[2.0, -1.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 0.0]], [[4.0, 1.0, 0.0], [4.0, 0.0, 0.0], [2.0, 1.0, 0.0]], [[0.0, 1.0, 0.0], [2.0, 1.0, 0.0], [0.0, 0.0, 0.0]], [[4.0, 0.0, 0.0], [2.0, -1.0, 0.0], [2.0, 1.0, 0.0]], [[2.0, -1.0, 0.0], [0.0, 0.0, 0.0], [2.0, 1.0, 0.0]], [[0.0, -1.0, 1.0], [2.0, -1.0, 1.0], [0.0, 0.0, 1.0]], [[2.0, -1.0, 1.0], [4.0, -1.0, 1.0], [4.0, 0.0, 1.0]], [[4.0, 0.0, 1.0], [4.0, 1.0, 1.0], [2.0, 1.0, 1.0]], [[2.0, 1.0, 1.0], [0.0, 1.0, 1.0], [0.0, 0.0, 1.0]], [[0.0, 0.0, 1.0], [2.0, -1.0, 1.0], [2.0, 1.0, 1.0]], [[2.0, -1.0, 1.0], [4.0, 0.0, 1.0], [2.0, 1.0, 1.0]]]
newlstFacettesR = translationDesFacette(-0.5, lstFacettesR)

"""
On réalise le test de la poussée d'Archimede sur les facettes du rectangle
On commence par translater toute les facettes de "-0.5" car le rectangle fait "1m" en hauteur
On l'imerge de moitier 

On calcule la poussee d'Archimede avec la liste translatée,
Pour une masse de 4000 kilogrammes, le poids est de 40221 N
On est sencé trouvé une poussée d'archimede autour du poids.
"""

print("Pousse pousseeArchimede = ", pousseeArchimede(lstNormalesR, newlstFacettesR))
