from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)
    return my_autopct


class Canvas(FigureCanvas):
    def __init__(self, parent=None, width=2.5, height=2.5,
                 dpi=110, title="Title"):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_title(title, fontsize=16)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)


    def plot(self, array, labels):
        ax = self.figure.add_subplot(111)
        patches, texts, z = \
            ax.pie(array, autopct=make_autopct(array),
                   textprops=dict(color="w"),
        shadow=True)
        ax.legend(patches, labels, loc="best")


class Canvas2(FigureCanvas):
    def __init__(self, parent=None, width=3, height=3,
                 dpi=130, title='Title', ylabel="YLabel"):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_title(title, fontsize=16)
        self.axes.set_ylabel(ylabel, fontsize=16)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)


    def plot(self, array, labels):
        N = len(array)
        ind = np.arange(N)
        width = 0.5
        ax = self.figure.add_subplot(111)
        ax.bar(ind, array, width)
        ax.set_xticks(ind)
        ax.set_xticklabels(labels, fontsize=7)


class Canvas3(FigureCanvas):
    def __init__(self, parent=None, width=2.5, height=2.5, dpi=120, title='Title', ylabel="YLabel", xlabel="XLabel"):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_title(title, fontsize=16)
        self.axes.set_ylabel(ylabel, fontsize=16)
        self.axes.set_xlabel(xlabel, fontsize=16)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)


    def plot(self, array, labels):
        N = len(array)
        ind = np.arange(N)
        width = 0.5
        ax = self.figure.add_subplot(111)
        ax.bar(ind, array, width)
        ax.set_xticks(ind)
        ax.set_xticklabels(labels, fontsize=8)

