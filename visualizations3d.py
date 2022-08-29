import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QWidget, QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.figure import Figure
import numpy as np
import random
from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D
from sklearn import decomposition
import matplotlib.patheffects as PathEffects


def gen_tsne_3d(start=None, end=None):
    vectors = np.load("gen_data/"+"photos_faces_emb.npz")
    wektory = vectors['arr_0'][start:end]
    etykiety = vectors['arr_1'][start:end]
    etykiety = etykiety.astype(np.int)
    etykiety_unique = np.unique(etykiety)
    tsne = TSNE(n_components=3, random_state=0)
    points_reduced_tsne = tsne.fit_transform(wektory)
    np.savez_compressed("gen_data/"+'tsne_3d.npz', points_reduced_tsne, etykiety, etykiety_unique)

def gen_umap_3d(start=None, end=None):
    import umap
    vectors = np.load("gen_data/"+"photos_faces_emb.npz")
    wektory = vectors['arr_0'][start:end]
    etykiety = vectors['arr_1'][start:end]
    etykiety = etykiety.astype(np.int)
    etykiety_unique = np.unique(etykiety)
    #tsne = TSNE(n_components=3, random_state=0)
    tsne = umap.UMAP(n_components=3)
    points_reduced_tsne = tsne.fit_transform(wektory)
    np.savez_compressed("gen_data/"+'umap_3d.npz', points_reduced_tsne, etykiety, etykiety_unique)

def gen_pca_3d(start=None, end=None):
    vectors = np.load("gen_data/"+"photos_faces_emb.npz")

    wektory = vectors['arr_0'][start:end]
    etykiety = vectors['arr_1'][start:end]
    etykiety = etykiety.astype(np.int)
    etykiety_unique = np.unique(etykiety)

    pca = decomposition.PCA(n_components=3)
    points_reduced = wektory
    pca.fit(points_reduced)
    points_reduced = pca.transform(points_reduced)
    np.savez_compressed("gen_data/"+'pca_3d.npz', points_reduced, etykiety, etykiety_unique)


class Window3D(QDialog):
    def __init__(self, parent=None):
        super(Window3D, self).__init__(parent)
        self.setGeometry(400, 200, 880, 600)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas2 = MplPlot3dView(self)
        self.setWindowTitle("Face embedding visualization")
        layout = QVBoxLayout()
        layout.addWidget(self.canvas2)
        self.setLayout(layout)

    def plot(self):
        data = [[1,2,3],[4,5,6],[7,8,9]]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(data, '*-')
        self.canvas.draw()

class MplPlot3dCanvas(FigureCanvas):
    def __init__(self):
        self.surfs = [] # [{"xx":,"yy:","val:"}]
        self.fig = Figure()
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self,
            QSizePolicy.Expanding,
            QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax = Axes3D(self.fig) # Canvas figure must be created for mouse rotation
        self.format_coord_org = self.ax.format_coord
        self.ax.format_coord = self.report_pixel

    def draw_pca_3d_pre(self):
        start = None
        end = None
        data = np.load("gen_data/"+'pca_3d.npz')
        points_reduced, etykiety, etykiety_unique = data['arr_0'][start:end], data['arr_1'][start:end], data['arr_2'][
                                                                                                        start:end]
        for wt in range(1, len(etykiety_unique) + 1):
            points_tmp = points_reduced[etykiety == wt]
            xs = points_tmp[:, 0]
            ys = points_tmp[:, 1]
            zs = points_tmp[:, 2]
            self.ax.scatter(xs, ys, zs, label=etykiety_unique[wt - 1])


    def draw_pca_3d(self, tab=None, show_labels=False, start=None, end=None):
        data = np.load("gen_data/"+'pca_3d.npz')
        points_reduced_tsne = data['arr_0'][start:end]
        etykiety = data['arr_1'][start:end]
        etykiety_unique = data['arr_2'][start:end]

        # etykiety i identyfikacja
        if tab is not None:
            x2, labels2 = list(), list()
            for i in range(0, len(points_reduced_tsne)):
                if int(etykiety[i]) in tab:
                    x2.append(points_reduced_tsne[i])
                    labels2.append(etykiety[i])
            points_reduced_tsne, etykiety = np.array(x2), labels2
            etykiety_unique = np.unique(etykiety)

        vectors = np.load("gen_data/"+"photos_faces_emb.npz")
        nazwy = vectors['arr_2']
        nazwy2 = list()
        etykiety = np.array(etykiety)
        etykiety.astype(int)
        for i in nazwy:
            nazwy2.append(i[:-4])
        wskaznik = 0

        # for wt in range(1, len(etykiety_unique) + 1):
        for wt in etykiety_unique:
            points_tmp = points_reduced_tsne[etykiety == wt]
            xs = points_tmp[:, 0]
            ys = points_tmp[:, 1]
            zs = points_tmp[:, 2]
            if show_labels == True:
                for i in range(len(xs)):
                    txt1 = self.ax.text(xs[i], ys[i], zs[i], str(nazwy2[i + wskaznik]))
            wskaznik += len(xs)
            txt2 = self.ax.text(np.median(xs), np.median(ys), np.median(zs), str(wt), fontsize=16,
                                weight=1000)
            txt2.set_path_effects([
                PathEffects.Stroke(linewidth=9, foreground="w"),
                PathEffects.Normal()])
            self.ax.scatter(xs, ys, zs, label=wt)
            self.ax.legend()
            #self.ax.axis('off')
            self.ax.set_title("3D PCA")
        # plt.title('t-SNE')
        # self.ax.legend()

    def draw_pca_3d_for_comparison(self, points_reduced_f, etykiety_f, etykiety_unique_f, tab=None, show_labels=False, start=None, end=None):
        points_reduced_tsne = points_reduced_f
        etykiety = etykiety_f
        etykiety_unique = etykiety_unique_f

        # etykiety i identyfikacja
        if tab is not None:
            x2, labels2 = list(), list()
            for i in range(0, len(points_reduced_tsne)):
                if int(etykiety[i]) in tab:
                    x2.append(points_reduced_tsne[i])
                    labels2.append(etykiety[i])
            points_reduced_tsne, etykiety = np.array(x2), labels2
            etykiety_unique = np.unique(etykiety)

        for wt in etykiety_unique:
            points_tmp = points_reduced_tsne[etykiety == wt]
            xs = points_tmp[:, 0]
            ys = points_tmp[:, 1]
            zs = points_tmp[:, 2]
            txt2 = self.ax.text(np.median(xs), np.median(ys), np.median(zs), str(wt), fontsize=25,
                                weight=1000)
            txt2.set_path_effects([
                PathEffects.Stroke(linewidth=10, foreground="w"),
                PathEffects.Normal()])
            self.ax.scatter(xs, ys, zs, label=wt)

    def draw_umap_3d(self, tab=None, show_labels=False, start=None, end=None):
        data = np.load("gen_data/"+'umap_3d.npz')
        points_reduced_tsne = data['arr_0'][start:end]
        etykiety = data['arr_1'][start:end]
        etykiety_unique = data['arr_2'][start:end]
        if tab is not None:
            x2, labels2 = list(), list()
            for i in range(0, len(points_reduced_tsne)):
                if int(etykiety[i]) in tab:
                    x2.append(points_reduced_tsne[i])
                    labels2.append(etykiety[i])
            points_reduced_tsne, etykiety = np.array(x2), labels2
            etykiety_unique = np.unique(etykiety)
        vectors = np.load("gen_data/"+"photos_faces_emb.npz")
        nazwy = vectors['arr_2']
        nazwy2 = list()
        etykiety = np.array(etykiety)
        etykiety.astype(int)
        for i in nazwy:
            nazwy2.append(i[:-4])
        wskaznik = 0
        for wt in etykiety_unique:
            points_tmp = points_reduced_tsne[etykiety == wt]
            xs = points_tmp[:, 0]
            ys = points_tmp[:, 1]
            zs = points_tmp[:, 2]
            if show_labels ==True:
                for i in range(len(xs)):
                    txt1 = self.ax.text(xs[i], ys[i], zs[i], str(nazwy2[i + wskaznik]))
            wskaznik += len(xs)
            txt2 = self.ax.text(np.median(xs), np.median(ys), np.median(zs), str(wt), fontsize=16,
                            weight=1000)
            txt2.set_path_effects([
                PathEffects.Stroke(linewidth=9, foreground="w"),
                PathEffects.Normal()])
            self.ax.scatter(xs, ys, zs, label=wt)
            self.ax.legend()
            #self.ax.axis('off')
            self.ax.set_title("3D UMAP")

    def draw_tsne_3d(self, tab=None, show_labels=False, start=None, end=None):
        print(tab)
        data = np.load("gen_data/"+'tsne_3d.npz')
        points_reduced_tsne = data['arr_0'][start:end]
        etykiety = data['arr_1'][start:end]
        etykiety_unique = data['arr_2'][start:end]

        #etykiety i identyfikacja
        if tab is not None:
            x2, labels2 = list(), list()
            for i in range(0, len(points_reduced_tsne)):
                if int(etykiety[i]) in tab:
                    x2.append(points_reduced_tsne[i])
                    labels2.append(etykiety[i])
            points_reduced_tsne, etykiety = np.array(x2), labels2
            etykiety_unique = np.unique(etykiety)

        vectors = np.load("gen_data/"+"photos_faces_emb.npz")
        nazwy = vectors['arr_2']
        nazwy2 = list()
        etykiety = np.array(etykiety)
        etykiety.astype(int)
        for i in nazwy:
            nazwy2.append(i[:-4])
        wskaznik = 0

        #for wt in range(1, len(etykiety_unique) + 1):
        for wt in etykiety_unique:
            points_tmp = points_reduced_tsne[etykiety == wt]
            xs = points_tmp[:, 0]
            ys = points_tmp[:, 1]
            zs = points_tmp[:, 2]
            if show_labels ==True:
                for i in range(len(xs)):
                    txt1 = self.ax.text(xs[i], ys[i], zs[i], str(nazwy2[i + wskaznik]))
            wskaznik += len(xs)
            txt2 = self.ax.text(np.median(xs), np.median(ys), np.median(zs), str(wt), fontsize=16,
                            weight=1000)
            txt2.set_path_effects([
                PathEffects.Stroke(linewidth=9, foreground="w"),
                PathEffects.Normal()])
            self.ax.scatter(xs, ys, zs, label=wt)
            self.ax.legend()
        #self.ax.axis('off')
        self.ax.set_title("3D t-SNE")
        #plt.title('t-SNE')
        #self.ax.legend()

    def report_pixel(self, xd, yd):
        s = self.format_coord_org(xd, yd)
        s = s.replace(",", " ")
        return s


class MplPlot3dView(QWidget):
    def __init__(self, parent = None):
       super(MplPlot3dView, self).__init__(parent)
       self.canvas = MplPlot3dCanvas()
       self.toolbar = NavigationToolbar(self.canvas, self.canvas)
       self.vbox = QVBoxLayout()
       self.vbox.addWidget(self.canvas)
       self.vbox.addWidget(self.toolbar)
       self.setLayout(self.vbox)
       self.to_update = False

"""if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window3D()
    main.canvas2.canvas.draw_tsne_3d([2,3], True)
    main.show()

    sys.exit(app.exec_())"""

