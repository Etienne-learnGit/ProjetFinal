import numpy

class extractionSTL:
    def __init__(self, chemin):
        self.__cheminSTL = chemin
        self.__listeFacette = []
        self.__listeNormales = []

    def extractionDesListes(self):
        fileHandle = open(self.__cheminSTL,"r")
        chaine = fileHandle.read()
        lst = chaine.split("\n")
        lst.remove(lst[0])
        lst.remove(lst[-1])
        x = len(lst)
        while x > 1 :
            self.lectureBlocDeSeptLignes(lst[:7])
            x = x-7
            lst = lst[-x:]
        return self.__listeNormales, self.__listeFacette

    def lectureBlocDeSeptLignes(self, lst):
        lst.remove(lst[-1])
        lst.remove(lst[-1])
        lst.remove(lst[1])
        for elt in range(0, 4):
            lst[elt] = lst[elt].split(" ")
        self.__listeNormales.append([float(lst[0][-3]), float(lst[0][-2]), float(lst[0][-1])])
        lst.remove(lst[0])
        Vertex3 = []
        for elt2 in range(0, 3) :
            liste = [float(lst[elt2][-3]), float(lst[elt2][-2]), float(lst[elt2][-1])]
            Vertex3.append(liste)
        self.__listeFacette.append(Vertex3)
        return

class operationsSurListes:
    def __init__(self, masse, lstN, lstF):
        self.__masse = masse
        self.__lstN = lstN
        self.__lstF = lstF
        self.__FA = [0,0,0]
        self.__FP = masse*9.81
        self.__tirantEau = 10

    def getFA(self):
        return self.__FA
    def getFP(self):
        return self.__FP

    def setMasse(self, masse):
        self.__masse = masse
        self.__FP = masse * 9.81

    def calculForcePression(self, N, F):
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

    def pousseeArchimede(self):
        self.__FA = [0,0,0]
        for i in range(0, len(self.__lstF)):
            coordG = [(self.__lstF[i][0][0] + self.__lstF[i][1][0] + self.__lstF[i][2][0]) / 3, (self.__lstF[i][0][1] + self.__lstF[i][1][1] + self.__lstF[i][2][1]) / 3, (self.__lstF[i][0][2] + self.__lstF[i][1][2] + self.__lstF[i][2][2]) / 3 ]
            if coordG[2] < 0:
                self.__FA[0] = self.__FA[0] + self.calculForcePression(self.__lstN[i], self.__lstF[i])[0]
                self.__FA[1] = self.__FA[1] + self.calculForcePression(self.__lstN[i], self.__lstF[i])[1]
                self.__FA[2] = self.__FA[2] + self.calculForcePression(self.__lstN[i], self.__lstF[i])[2]
        return numpy.vdot(self.__FA,self.__FA)**(1/2)

    def translationDesFacette(self, valeurDeTranslation):
        x = valeurDeTranslation
        for elt in range(0, len(self.__lstF)) :
            for elt2 in range(0, 3):
                self.__lstF[elt][elt2][-1] = self.__lstF[elt][elt2][-1] + x
        self.__tirantEau -= x
        return self.__lstF

    def dichotomie(self,hauteurInitial):
        hauteurMaximal = 2
        precision = 10**(-3)
        debut = hauteurInitial
        fin = hauteurMaximal
        ecart = numpy.sqrt((hauteurMaximal-hauteurInitial)**2)
        n = 0
        lst1=[]
        while ecart > precision:
            m = (debut+fin)/2
            print(">> iteration num ",n)
            print("a,m,b",debut,m,fin)
            self.translationDesFacette(-debut)
            archiDebut = self.pousseeArchimede() - self.__FP
            self.translationDesFacette(debut)
            self.translationDesFacette(-m)
            archiM = self.pousseeArchimede() - self.__FP
            self.translationDesFacette(m)
            if archiM * archiDebut < 0:
                fin = m
            else:
                debut = m
                ecart = fin-debut
            lst1.append(m)
            n+=1
            self.__FA = round(archiM+self.__FP, 3)
        lst = [lst1,round(m,3),n]
        return lst

"""
La dicotomie se sert des autres methodes de la classe,
par consequent notre test se réalise sur la totalité de la classe.

On réalise le test sur un bateau de forme rectanulaire et avec une masse de 4000 Kg
"""

b1 = extractionSTL('Maillage\Rectangular_HULL_Normals_Outward.stl')
lstN , lstF = b1.extractionDesListes()

boat = operationsSurListes(4000, lstN, lstF)
tirant = boat.dichotomie(0.1)
print("Le tirant d'eau final est de : ", tirant[1], "m")
