import numpy as np
import matplotlib.pyplot as plt

class DynamicPlot:
    def __init__(self):
        self._fig = plt.figure()
        self._ax = self._fig.add_subplot(111)
        self._lines = {}
    def add_plot(self, x, y, name=None):
        line, = self._ax.plot(x, y)
        if name is None: name = str(len(self._lines))
        self._lines[name] = line
    def reload_plot(self, x, y, name):
        self._lines[name].set_data(x, y)
    def reflash_ax(self):
        self._ax.cla()
        self._lines = {}
    def title(self, title):
        self._ax.title(title)
    def xlabel(self, xlabel):
        self._ax.set_xlabel(r"{}".format(xlabel))
    def ylabel(self, ylabel):
        self._ax.set_ylabel(r"{}".format(ylabel))
    def xlim(self, xlim):
        self._ax.set_xlim(xlim)
    def ylim(self, ylim):
        self._ax.set_ylim(ylim)
    def xscale(self, xscale):
        self._ax.set_xscale(xscale)
    def update(self):
        plt.pause(0.01)
    
    def set_scistyle(self):
        self._ax.tick_params(which='both', direction="in", top=True, right=True)

if __name__=="__main__":
    dplt = DynamicPlot()
    x = np.arange(-2,2,0.01)
    dplt.add_plot(x, x**3-x*3)
    dplt.update()
