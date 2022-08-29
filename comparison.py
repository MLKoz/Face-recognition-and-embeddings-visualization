from scipy.spatial import distance
import numpy as np
from visualizations2d import Window2D
from visualizations3d import Window3D
from sklearn.preprocessing import normalize
from sklearn import decomposition

def l2_normalize(x):
    return normalize(x.reshape(1,-1), "l2", 1)


def returnDistancesForTwoGroupsEmb(wektory_os_1_arg, wektory_os_2_arg):
    wektory_os1 = wektory_os_1_arg[:]
    wektory_os2 = wektory_os_2_arg[:]
    lista_osadzen_po_norm_1 = list()
    lista_osadzen_po_norm_2 = list()
    for i in range(len(wektory_os1)):
            lista_osadzen_po_norm_1.append(l2_normalize(wektory_os1[i]))
    for i in range(len(wektory_os2)):
            lista_osadzen_po_norm_2.append(l2_normalize(wektory_os2[i]))
    lista_osadzen_po_norm_1 = np.array(lista_osadzen_po_norm_1)
    lista_osadzen_po_norm_2 = np.array(lista_osadzen_po_norm_2)
    lista_koncowa_euk = list()
    for i in lista_osadzen_po_norm_1:
        for j in lista_osadzen_po_norm_2:
            x = round(distance.euclidean(i,j), 3)
            if x!=0:
                lista_koncowa_euk.append(x)
    lista_koncowa_euk = np.array(lista_koncowa_euk)
    return lista_koncowa_euk


def gen2DAnalysisForComparison(wektory_os_1_arg : list, wektory_os_2_arg : list):
    wektory_os_1 = wektory_os_1_arg[:]
    wektory_os_2 = wektory_os_2_arg[:]
    etykiety1 = list()
    etykiety2 = list()
    for i in range(len(wektory_os_1)):
        etykiety1.append(1)
    for i in range(len(wektory_os_2)):
        etykiety2.append(2)

    etykiety1.extend(etykiety2)
    wektory_os_1.extend(wektory_os_2)
    wektory = np.asarray(wektory_os_1)
    etykiety = np.asarray(etykiety1)
    etykiety = etykiety.astype(np.int)
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
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
    return points_reduced, mediana_x, mediana_y, etykiety


def show2DAnalysisForComparison(points_reduced, mediana_x, mediana_y, etykiety):
    dialog = Window2D()
    dialog.draw_pca_2d_for_comparison(points_reduced[:, 0], points_reduced[:, 1], mediana_x, mediana_y, etykiety, [1, 2], False)
    dialog.exec_()


def gen3DAnalysisForComparison(wektory_os_1_arg : list, wektory_os_2_arg : list):
    wektory_os_1 = wektory_os_1_arg[:]
    wektory_os_2 = wektory_os_2_arg[:]
    etykiety1 = list()
    etykiety2 = list()
    for i in range(len(wektory_os_1)):
        etykiety1.append(1)
    for i in range(len(wektory_os_2)):
        etykiety2.append(2)
    etykiety1.extend(etykiety2)
    wektory_os_1.extend(wektory_os_2)
    wektory = np.array(wektory_os_1)
    etykiety = np.array(etykiety1)
    etykiety = etykiety.astype(np.int)
    etykiety_unique = np.unique(etykiety)


    pca = decomposition.PCA(n_components=3)
    points_reduced = wektory
    pca.fit(points_reduced)
    points_reduced = pca.transform(points_reduced)

    return points_reduced, etykiety, etykiety_unique


def show3DAnalysisForComparison(points_reduced, etykiety, etykiety_unique):
    dialog = Window3D()
    dialog.canvas2.canvas.draw_pca_3d_for_comparison(points_reduced, etykiety, etykiety_unique, [1,2], False)
    dialog.exec_()


def genHistDataForTwoGroups(wektory_osoby_1 : list, wektory_osoby_2 : list):
    dystanse = returnDistancesForTwoGroupsEmb(wektory_osoby_1, wektory_osoby_2)
    wszystkie_dystanse_euk = dystanse
    wszystkie_dystanse_euk.sort()
    return wszystkie_dystanse_euk


def drawHist(x):
    dialog = Window2D()
    dialog.draw_histogram(x)
    dialog.exec_()


def genDatabaseHistogramData():
    data = np.load("gen_data/"+"photos_faces_emb.npz")
    osadzenia = data['arr_0']
    etykiety = data['arr_1']
    etykiety = etykiety.astype(np.int)
    etykiety_unique = np.unique(etykiety)
    lista_osadzen = list()
    for i in range(len(etykiety)):
        lista_osadzen.append(l2_normalize(osadzenia[i]))
    lista_osadzen = np.array(lista_osadzen)
    dystanse_q = list()
    etykiety_q = list()
    for i,etykieta in enumerate(etykiety_unique, start=0):
        osadzenia_osoby_i = lista_osadzen[etykiety == etykieta]
        while len(osadzenia_osoby_i) != 0:
            for j in range(1, len(osadzenia_osoby_i)):
                dystanse_q.append(round(distance.euclidean(
                    osadzenia_osoby_i[0], osadzenia_osoby_i[j]), 4))
                etykiety_q.append(etykieta)
            osadzenia_osoby_i = osadzenia_osoby_i[1:]
    dystanse_q = np.array(dystanse_q)
    np.savez_compressed("gen_data/"+'histogramdata.npz', dystanse_q, etykiety_q)


def processingDatabaseHistogramData(tab):
    data = np.load("gen_data/"+'histogramdata.npz')
    dystanse = data['arr_0']
    print(len(dystanse))
    etykiety = data['arr_1']
    dystanse2 = list()
    if (tab is not None) and len(tab)!=1:
        return []
    if tab is not None:
        for i in range(len(etykiety)):
            if int(etykiety[i]) in tab:
                dystanse2.append(dystanse[i])
        dystanse = np.array(dystanse2)
    return dystanse