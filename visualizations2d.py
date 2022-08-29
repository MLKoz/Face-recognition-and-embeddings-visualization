import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import random
import os
import numpy as np
import seaborn as sns
#sns.set_style('darkgrid')
#sns.set_palette('muted')
#sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})


def gen_pca_2d(start=None, end=None):
    #czy plik istnieje
    if os.path.isfile("gen_data/"+'./photos_faces_emb.npz'):
        #plik istnieje
        vectors = np.load("gen_data/"+"photos_faces_emb.npz")
    else:
        print("Błąd podczas ładowania wektorów do t-SNE 2D")
        return
    # GENEROWANIE 2WYMIAROWYCH DANYCH t-SNE
    wektory = vectors['arr_0'][start:end]
    etykiety = vectors['arr_1'][start:end]
    etykiety = etykiety.astype(np.int)
    #from sklearn.manifold import TSNE
    from sklearn.decomposition import PCA
    #tsne = TSNE(n_components=2, random_state=0)
    #tsne_obj = tsne.fit_transform(wektory)
    pca = PCA(n_components=3)
    pca.fit(wektory)
    points_reduced = pca.transform(wektory)
    # GENEROWANIE MEDIAN
    mediana_x = list()
    mediana_y = list()
    a = 0
    for i in np.unique(etykiety):
        for p in range(a, len(etykiety)):
            if int(etykiety[p]) == i:
                # print("ok")
                if p == len(etykiety) - 1:
                    mediana_x.append(np.median(points_reduced[:, 0][a:p]))
                    mediana_y.append(np.median(points_reduced[:, 1][a:p]))
                    break
            else:
                mediana_x.append(np.median(points_reduced[:, 0][a:p]))
                mediana_y.append(np.median(points_reduced[:, 1][a:p]))
                a = p
                break
    # x -tsne , y-tsne, x- mediana, y-mediana, etykieta
    np.savez_compressed("gen_data/"+'pca_2d.npz', points_reduced[:, 0], points_reduced[:, 1], mediana_x, mediana_y, etykiety)


def gen_tsne_2d(start=None, end=None):
    #czy plik istnieje
    if os.path.isfile("gen_data/"+'./photos_faces_emb.npz'):
        #plik istnieje
        vectors = np.load("gen_data/"+"photos_faces_emb.npz")
    else:
        print("Błąd podczas ładowania wektorów do t-SNE 2D")
        return
    # GENEROWANIE 2WYMIAROWYCH DANYCH t-SNE
    wektory = vectors['arr_0'][start:end]
    etykiety = vectors['arr_1'][start:end]
    etykiety = etykiety.astype(np.int)
    from sklearn.manifold import TSNE
    tsne = TSNE(n_components=2, random_state=0)
    tsne_obj = tsne.fit_transform(wektory)
    # GENEROWANIE MEDIAN
    mediana_x = list()
    mediana_y = list()
    a = 0
    for i in np.unique(etykiety):
        for p in range(a, len(etykiety)):
            if int(etykiety[p]) == i:
                # print("ok")
                if p == len(etykiety) - 1:
                    mediana_x.append(np.median(tsne_obj[:, 0][a:p]))
                    mediana_y.append(np.median(tsne_obj[:, 1][a:p]))
                    break
            else:
                mediana_x.append(np.median(tsne_obj[:, 0][a:p]))
                mediana_y.append(np.median(tsne_obj[:, 1][a:p]))
                a = p
                break
    # x -tsne , y-tsne, x- mediana, y-mediana, etykieta
    np.savez_compressed("gen_data/"+'tsne_2d.npz', tsne_obj[:, 0], tsne_obj[:, 1], mediana_x, mediana_y, etykiety)

def gen_umap_2d(start=None, end=None):
    #czy plik istnieje
    if os.path.isfile("gen_data/"+'./photos_faces_emb.npz'):
        #plik istnieje
        vectors = np.load("gen_data/"+"photos_faces_emb.npz")
    else:
        print("Błąd podczas ładowania wektorów do UMAP 2D")
        return
    # GENEROWANIE 2WYMIAROWYCH DANYCH t-SNE
    wektory = vectors['arr_0'][start:end]
    etykiety = vectors['arr_1'][start:end]
    etykiety = etykiety.astype(np.int)
    #from sklearn.manifold import TSNE
    #tsne = TSNE(n_components=2, random_state=0)
    import umap
    tsne = umap.UMAP(n_components=2)
    tsne_obj = tsne.fit_transform(wektory)
    # GENEROWANIE MEDIAN
    mediana_x = list()
    mediana_y = list()
    a = 0
    for i in np.unique(etykiety):
        for p in range(a, len(etykiety)):
            if int(etykiety[p]) == i:
                # print("ok")
                if p == len(etykiety) - 1:
                    mediana_x.append(np.median(tsne_obj[:, 0][a:p]))
                    mediana_y.append(np.median(tsne_obj[:, 1][a:p]))
                    break
            else:
                mediana_x.append(np.median(tsne_obj[:, 0][a:p]))
                mediana_y.append(np.median(tsne_obj[:, 1][a:p]))
                a = p
                break
    # x -tsne , y-tsne, x- mediana, y-mediana, etykieta
    np.savez_compressed("gen_data/"+'umap_2d.npz', tsne_obj[:, 0], tsne_obj[:, 1], mediana_x, mediana_y, etykiety)


class Window2D(QDialog):
    def __init__(self, parent=None):
        super(Window2D, self).__init__(parent)

        self.setGeometry(400, 200, 880, 600)
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        #self.button = QPushButton('Plot')
        #self.button.clicked.connect(lambda: self.draw_tsne_2d(None,False,None,None))
        self.setWindowTitle("Face embedding visualization")
        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        #layout.addWidget(self.button)
        self.setLayout(layout)

    def draw_pca_2d(self, tab=None, show_labels=False, start=None, end=None):
        if os.path.isfile("gen_data/"+'./pca_2d.npz'):
            # plik istnieje
            vectors = np.load("gen_data/"+"pca_2d.npz")
        else:
            print("Błąd podczas ładowania danych t-SNE 2D do wyświetlania")
            return
        data = np.load("gen_data/"+'pca_2d.npz')
        x, y, m_x, m_y, labels = data['arr_0'][start:end], data['arr_1'][start:end], data['arr_2'][start:end] \
            , data['arr_3'][start:end], data['arr_4'][start:end]

        if tab is not None:
            x2, y2, m_x2, m_y2, labels2 = list(), list(), list(), list(), list()
            for i in tab:
                if i in labels:
                    m_x2.append(m_x[np.where(np.unique(labels) == i)[0][0]])
                    m_y2.append(m_y[np.where(np.unique(labels) == i)[0][0]])
            for i in range(0, len(x)):
                if labels[i] in tab:
                    x2.append(x[i])
                    y2.append(y[i])
                    labels2.append(labels[i])
            x, y, m_x, m_y, labels = x2, y2, m_x2, m_y2, labels2

        ax = self.figure.add_subplot(111)
        sc = ax.scatter(x, y, lw=0, s=20, c=tuple(labels))
        #plt.xlim(-25, 25)
        #plt.ylim(-25, 25)
        #ax.axis('off')
        #ax.axis('off')
        #ax.axis('tight')
        ax.set_title("2D PCA")

        if show_labels == True:
            vectors = np.load("gen_data/"+"photos_faces_emb.npz")
            nazwy = vectors['arr_2']
            nazwy2 = list()
            for i in nazwy:
                nazwy2.append(i[:-4])
            for i in range(len(x)):
                txt2 = ax.text(x[i], y[i], str(nazwy2[i]), fontsize=9)
                txt2.set_path_effects([
                    PathEffects.Stroke(linewidth=3, foreground="w"),
                    PathEffects.Normal()])

        listtaa = np.unique(labels)
        for i in range(len(listtaa)):
            txt = ax.text(m_x[i], m_y[i], str(listtaa[i]), fontsize=16)
            txt.set_path_effects([
                PathEffects.Stroke(linewidth=6, foreground="w"),
                PathEffects.Normal()])

        # refresh canvas
        self.canvas.draw()


    def draw_pca_2d_for_comparison(self, x, y, m_x, m_y, labels, tab=None, show_labels=False, start=None, end=None):
        if tab is not None:
            x2, y2, m_x2, m_y2, labels2 = list(), list(), list(), list(), list()
            for i in tab:
                if i in labels:
                    m_x2.append(m_x[np.where(np.unique(labels) == i)[0][0]])
                    m_y2.append(m_y[np.where(np.unique(labels) == i)[0][0]])
            for i in range(0, len(x)):
                if labels[i] in tab:
                    x2.append(x[i])
                    y2.append(y[i])
                    labels2.append(labels[i])
            x, y, m_x, m_y, labels = x2, y2, m_x2, m_y2, labels2

        ax = self.figure.add_subplot(111)
        cmap = plt.cm.get_cmap("winter")
        sc = ax.scatter(x, y, lw=0, s=30, c=tuple(labels), cmap=cmap)
        plt.xlim(-25, 25)
        plt.ylim(-25, 25)
        plt.tick_params(labelsize=20)
        ax.axis('tight')

        if show_labels == True:
            vectors = np.load("gen_data/"+"photos_faces_emb.npz")
            nazwy = vectors['arr_2']
            nazwy2 = list()
            for i in nazwy:
                nazwy2.append(i[:-4])
            for i in range(len(x)):
                txt2 = ax.text(x[i], y[i], str(nazwy2[i]), fontsize=9)
                txt2.set_path_effects([
                    PathEffects.Stroke(linewidth=3, foreground="w"),
                    PathEffects.Normal()])

        listtaa = np.unique(labels)
        for i in range(len(listtaa)):
            txt = ax.text(m_x[i], m_y[i], str(listtaa[i]), fontsize=24)
            txt.set_path_effects([
                PathEffects.Stroke(linewidth=5, foreground="w"),
                PathEffects.Normal()])
        self.canvas.draw()

    def draw_histogram(self, wszystkie_dystanse_euk, bins=50):
        fig = plt.figure()
        ax = self.figure.add_subplot(1, 1, 1)
        ax.hist(wszystkie_dystanse_euk, bins=bins, alpha=0.5, color="g")
        ax.grid(True)
        ax.set_xlabel('Euclidean distance')
        ax.set_ylabel('Number occurrences of distance')
        ax.set_title('Histogram of Euclidean distances')

    def draw_tsne_2d(self, tab=None, show_labels=False, start=None, end=None):
        if os.path.isfile("gen_data/"+'./tsne_2d.npz'):
            data = np.load("gen_data/"+"tsne_2d.npz")
        else:
            print("Błąd podczas ładowania danych t-SNE 2D do wyświetlania")
            return
        x, y, m_x, m_y, labels = data['arr_0'][start:end], data['arr_1'][start:end], data['arr_2'][start:end] \
            , data['arr_3'][start:end], data['arr_4'][start:end]
        if tab is not None:
            x2, y2, m_x2, m_y2, labels2 = list(), list(), list(), list(), list()
            for i in tab:
                if i in labels:
                    m_x2.append(m_x[np.where(np.unique(labels) == i)[0][0]])
                    m_y2.append(m_y[np.where(np.unique(labels) == i)[0][0]])
            for i in range(0, len(x)):
                if labels[i] in tab:
                    x2.append(x[i])
                    y2.append(y[i])
                    labels2.append(labels[i])
            x, y, m_x, m_y, labels = x2, y2, m_x2, m_y2, labels2
        ax = self.figure.add_subplot(111)
        sc = ax.scatter(x, y, lw=0, s=20, c=tuple(labels))
        #plt.xlim(-25, 25)
        #plt.ylim(-25, 25)
        #ax.axis('tight')
        #ax.axis('off')
        ax.set_title("2D t-SNE")
        if show_labels == True:
            vectors = np.load("gen_data/"+"photos_faces_emb.npz")
            files_names = vectors['arr_2']
            files_names2 = list()
            for i in files_names:
                files_names2.append(i[:-4])
            for i in range(len(x)):
                txt2 = ax.text(x[i], y[i], str(files_names2[i]), fontsize=9)
                txt2.set_path_effects([
                    PathEffects.Stroke(linewidth=3, foreground="w"),
                    PathEffects.Normal()])
        labels_unique = np.unique(labels)
        for i in range(len(labels_unique)):
            txt = ax.text(m_x[i], m_y[i], str(labels_unique[i]), fontsize=16)
            txt.set_path_effects([
                PathEffects.Stroke(linewidth=6, foreground="w"),
                PathEffects.Normal()])
        self.canvas.draw()

    def draw_umap_2d(self, tab=None, show_labels=False, start=None, end=None):
        if os.path.isfile("gen_data/"+'./umap_2d.npz'):
            # plik istnieje
            vectors = np.load("gen_data/"+"umap_2d.npz")
        else:
            print("Błąd podczas ładowania danych t-SNE 2D do wyświetlania")
            return
        data = np.load("gen_data/"+'umap_2d.npz')
        x, y, m_x, m_y, labels = data['arr_0'][start:end], data['arr_1'][start:end], data['arr_2'][start:end] \
            , data['arr_3'][start:end], data['arr_4'][start:end]

        if tab is not None:
            x2, y2, m_x2, m_y2, labels2 = list(), list(), list(), list(), list()
            for i in tab:
                if i in labels:
                    m_x2.append(m_x[np.where(np.unique(labels) == i)[0][0]])
                    m_y2.append(m_y[np.where(np.unique(labels) == i)[0][0]])
            for i in range(0, len(x)):
                if labels[i] in tab:
                    x2.append(x[i])
                    y2.append(y[i])
                    labels2.append(labels[i])
            x, y, m_x, m_y, labels = x2, y2, m_x2, m_y2, labels2


        ax = self.figure.add_subplot(111)
        sc = ax.scatter(x, y, lw=0, s=20, c=tuple(labels))
        #plt.xlim(-25, 25)
        #plt.ylim(-25, 25)
        #ax.axis('off')
        #ax.axis('tight')
        ax.set_title("2D UMAP")
        if show_labels == True:
            vectors = np.load("gen_data/"+"photos_faces_emb.npz")
            nazwy = vectors['arr_2']
            nazwy2 = list()
            for i in nazwy:
                nazwy2.append(i[:-4])
            for i in range(len(x)):
                txt2 = ax.text(x[i], y[i], str(nazwy2[i]), fontsize=9)
                txt2.set_path_effects([
                    PathEffects.Stroke(linewidth=3, foreground="w"),
                    PathEffects.Normal()])

        listtaa = np.unique(labels)
        for i in range(len(listtaa)):
            txt = ax.text(m_x[i], m_y[i], str(listtaa[i]), fontsize=16)
            txt.set_path_effects([
                PathEffects.Stroke(linewidth=6, foreground="w"),
                PathEffects.Normal()])

        # refresh canvas
        self.canvas.draw()