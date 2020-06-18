from PySide2.QtWidgets import *
import matplotlib.pyplot as plt2
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from stl import mesh
from mpl_toolkits import mplot3d
from Calcul import *

class boatIHM(QWidget):
    def __init__(self, chemin = 'Maillage\Rectangular_HULL_Normals_Outward.stl'):
        QWidget.__init__(self)
        self.stl = chemin
        self.masse = 4000
        self.B = extractionSTL(self.stl)
        self.L1, self.L2 = self.B.extractionDesListes()
        self.bateau = operationsSurListes(self.masse, self.L1, self.L2)

        self.counter = 0
        self.setWindowTitle("Boat stabilization interface")
        self.LayoutF = QVBoxLayout()
        self.LayoutMasse = QVBoxLayout()

        self.LayoutV1 = QVBoxLayout()
        self.LayoutV2 = QVBoxLayout()
        self.LayoutH = QHBoxLayout()
        self.LayoutV3 = QVBoxLayout()
        self.LayoutH2 = QHBoxLayout()

        self.image = graph(self.stl)
        self.courbe = courbe([])
        self.boutton1 = QPushButton("Start stabilization")
        self.boutton2 = QPushButton("Change model")


        self.textA = QLabel("\tChoose a new boat mass")
        self.zoneTexte = QTextEdit("")
        self.zoneTexte.setMaximumSize(260, 30)
        self.boutton = QPushButton("Ok")

        self.LayoutMasse.addWidget(self.textA)
        self.LayoutMasse.addWidget(self.zoneTexte)
        self.LayoutMasse.addWidget(self.boutton)
        self.LayoutH.addLayout(self.LayoutMasse)
        self.text2 = QLabel("Draught (m): ")
        self.text3 = QLabel("Boat mass (Kg): ")
        self.text4 = QLabel("Weight : ")
        self.text5 = QLabel("Archimede's thrust : ")
        self.LayoutV1.addWidget(self.text2)
        self.LayoutV1.addWidget(self.text3)
        self.LayoutV1.addWidget(self.text4)
        self.LayoutV1.addWidget(self.text5)
        self.LayoutH.addLayout(self.LayoutV1)
        self.info2 = QLabel("*")
        self.info3 = QLabel(str(self.masse))
        self.info4 = QLabel(str(self.masse*9.81))
        self.info5 = QLabel("*")
        self.LayoutV2.addWidget(self.info2)
        self.LayoutV2.addWidget(self.info3)
        self.LayoutV2.addWidget(self.info4)
        self.LayoutV2.addWidget(self.info5)
        self.LayoutH.addLayout(self.LayoutV2)

        self.LayoutV3.addLayout(self.LayoutH)
        self.LayoutV3.addWidget(self.courbe)

        self.LayoutH2.addWidget(self.image)
        self.LayoutH2.addLayout(self.LayoutV3)

        self.LayoutF.addWidget(self.boutton1)
        self.LayoutF.addWidget(self.boutton2)
        self.LayoutF.addLayout(self.LayoutH2)

        self.boutton.clicked.connect(self.changerMasse)
        self.boutton2.clicked.connect(self.changerModele)
        self.boutton1.clicked.connect(self.demarrerStabilisation)

        self.setLayout(self.LayoutF)

    def changerMasse(self):
        txt = self.zoneTexte.toPlainText()
        print(txt)
        self.info3.setText(txt)
        self.info4.setText(str(float(txt)*9.81))
        self.masse = float(txt)
        self.zoneTexte.setText("")
        self.reinit()

    def changerModele(self):
            chemins = ['Maillage\Rectangular_HULL_Normals_Outward.stl', "Maillage\V_HULL_Normals_Outward.stl", "Maillage\Cylindrical_HULL_Normals_Outward.stl", "Maillage\Mini650_HULL_Normals_Outward.stl"]
            self.counter +=1
            self.stl = chemins[self.counter]
            self.image.ax.clear()
            self.image.affichageStructure(self.stl)
            self.image.canvas.draw()
            if self.counter == 3 :
                self.counter = -1
            self.reinit()

    def reinit(self):
        self.B = extractionSTL(self.stl)
        self.L1, self.L2 = self.B.extractionDesListes()
        self.bateau = operationsSurListes(self.masse, self.L1, self.L2)
        self.info2.setText("*")
        self.info5.setText("*")

        self.courbe.deleteLater()
        self.courbe = courbe([])
        self.LayoutV3.addWidget(self.courbe)

    def demarrerStabilisation(self):
        listeTirant = self.bateau.dichotomie(0.1)
        Archimede = self.bateau.getFA()
        self.info5.setText(str(Archimede))
        self.info2.setText(str(listeTirant[-2]))

        #self.courbe.ax.clear()
        #self.courbe = courbe(listeTirant)
        #self.courbe.canvas.draw()
        #self.courbe.affichageCourbe(listeTirant)

        self.courbe.canvas.deleteLater()
        self.courbe = courbe(listeTirant)
        self.LayoutV3.addWidget(self.courbe)

        #self.courbe.canvas.plot()

class graph(QWidget):
    def __init__(self, chemin):
        QWidget.__init__(self)
        self.fig = plt2.figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax = plt2.axes(projection='3d')
        self.affichageStructure(chemin)
        self.canvas.draw()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def affichageStructure(self, chemin):
        your_mesh = mesh.Mesh.from_file(chemin)
        self.ax.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten("C")
        self.ax.auto_scale_xyz(scale, scale, scale)

class courbe(QWidget):
    def __init__(self,liste):
        QWidget.__init__(self)
        self.fig = plt2.figure()
        self.canvas = FigureCanvas(self.fig)
        self.affichageCourbe(liste)
        #self.canvas.draw()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def affichageCourbe(self,l):
        if l == [] :
            plt2.xlabel("itérations")
            plt2.ylabel("tirant d'eau")
        else :
            self.xs = numpy.arange(0, l[2], 1)
            self.ys = l[0]
            plt2.xlabel("itérations")
            plt2.ylabel("tirant d'eau")
            plt2.plot(self.xs, self.ys)
        self.canvas.draw()

if __name__ == "__main__":
   app = QApplication([])
   win = boatIHM()
   win.show()
   app.exec_()
