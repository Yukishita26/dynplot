import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
import os,sys

class DynamicPlot:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.lines = {}
    def add_plot(self, x, y, name=None):
        line, = self.ax.plot(x, y)
        if name is None: name = str(len(self.lines))
        self.lines[name] = line
    def reload_plot(self, x, y, name):
        self.lines[name].set_data(x, y)
    def reflash_ax(self):
        self.ax.cla()
        self.lines = {}
    def title(self, title):
        self.ax.title(title)
    def xlim(self, xlim):
        self.ax.set_xlim(xlim)
    def ylim(self, ylim):
        self.ax.set_ylim(ylim)
    def update(self):
        plt.pause(0.1)

#dp = DynamicPlot()
#lin = np.arange(-2,2,0.01)
#dp.add_plot(lin,lin**3-lin*3)
#dp.update()

class GraphAjuster:
    def __init__(self):
        # make plot area
        self.dp = DynamicPlot()
        lin = np.arange(-2,2,0.01)
        self.dp.add_plot(lin,lin**3-lin*3)
        self.dp.ax.tick_params(which='both', direction = "in", top=True, right=True)
        self.dp.update()
        #
        self.main_database = None
        #
        # make form window
        self.root = tk.Tk()
        self.root.title("test")
        self.root.geometry("400x200")
        #
        # window divide
        self.pw_main = tk.PanedWindow(self.root, orient='vertical')
        self.pw_main.pack(expand=True, fill = tk.BOTH, side="left")
        self.pw_upper = tk.PanedWindow(self.pw_main, orient='vertical')
        self.pw_main.add(self.pw_upper)
        self.pw_middle = tk.PanedWindow(self.pw_main, orient='vertical')
        self.pw_main.add(self.pw_middle)
        self.pw_lower = tk.PanedWindow(self.pw_main, orient='vertical')
        self.pw_main.add(self.pw_lower)
        self.fm_data_reader = tk.Frame(self.pw_upper, bd=2, relief="ridge")
        self.pw_upper.add(self.fm_data_reader)
        self.fm_data_setter = tk.Frame(self.pw_middle, bd=2, relief="ridge")
        self.pw_middle.add(self.fm_data_setter)
        self.fm_axis_setter = tk.Frame(self.pw_lower, bd=2, relief="ridge")
        self.pw_lower.add(self.fm_axis_setter)
        #
        # in pw_upper
        self.lbl_filename = tk.Label(self.fm_data_reader, text="file name:")
        self.lbl_filename.grid(row=0, column=0, padx=2, pady=2)
        self.txt_filename = tk.Entry(self.fm_data_reader)
        self.txt_filename.insert(0, "")
        self.txt_filename.grid(row=0, column=1, padx=2, pady=2)
        self.btn_fileref = tk.Button(self.fm_data_reader, text="file select",
                command=lambda:self.btn_fileref_pushed(self.btn_fileref))
        self.btn_fileref.grid(row=0, column=2, padx=2, pady=2)
        self.btn_loadcsv = tk.Button(self.fm_data_reader, text="load csv",
                command=lambda:self.btn_loadcsv_pushed(self.btn_loadcsv))
        self.btn_loadcsv.grid(row=0, column=3, padx=2, pady=2)
        #
        self.fm_data_reader.grid_columnconfigure(1, weight=1)
        #
        # in pe_middle
        self.lbl_xdata = tk.Label(self.fm_data_setter, text="data select; x:")
        self.lbl_xdata.grid(row=0, column=0, padx=2, pady=2)
        self.cbb_xdata = ttk.Combobox(self.fm_data_setter, state='readonly')
        self.cbb_xdata["values"] = ("load data...",)
        self.cbb_xdata.current(0)
        self.cbb_xdata.grid(row=0, column=1, padx=2, pady=2)
        self.lbl_ydata = tk.Label(self.fm_data_setter, text="y:")
        self.lbl_ydata.grid(row=0, column=2, padx=2, pady=2)
        self.cbb_ydata = ttk.Combobox(self.fm_data_setter, state='readonly')
        self.cbb_ydata["values"] = ("load data...",)
        self.cbb_ydata.current(0)
        self.cbb_ydata.grid(row=0, column=3, padx=2, pady=2)
        #
        self.lbl_xscale = tk.Label(self.fm_data_setter, text="        xscale:")
        self.lbl_xscale.grid(row=1, column=0, padx=2, pady=2)
        self.cbb_xscale = ttk.Combobox(self.fm_data_setter, state='readonly')
        self.cbb_xscale["values"] = ("linear", "log", "symlog")
        self.cbb_xscale.current(0)
        self.cbb_xscale.grid(row=1, column=1, padx=2, pady=2)
        self.lbl_yscale = tk.Label(self.fm_data_setter, text=" ")
        self.lbl_yscale.grid(row=1, column=2, padx=2, pady=2)
        self.cbb_yscale = ttk.Combobox(self.fm_data_setter, state='readonly')
        self.cbb_yscale["values"] = ("linear", "log", "symlog")
        self.cbb_yscale.current(0)
        self.cbb_yscale.grid(row=1, column=3, padx=2, pady=2)
        #        
        self.btn_plot_selected = tk.Button(self.fm_data_setter, text="plot",
                command= lambda :self.btn_plt_selected_pushed(self.btn_plot_selected))
        self.btn_plot_selected.grid(row=1, column=4, padx=2, pady=2)
        #
        self.fm_data_setter.grid_columnconfigure(1, weight=1)
        self.fm_data_setter.grid_columnconfigure(3, weight=1)
        #
        # in pw_lower
        self.lbl_xmin = tk.Label(self.fm_axis_setter, text="x min:")
        self.lbl_xmin.grid(row=0, column=0, padx=2, pady=2)
        self.txt_xmin = tk.Entry(self.fm_axis_setter)
        self.txt_xmin.insert(0, str(plt.xlim()[0]))
        self.txt_xmin.grid(row=0, column=1, padx=2, pady=2)
        self.lbl_xmax = tk.Label(self.fm_axis_setter, text=" max:")
        self.lbl_xmax.grid(row=0, column=2, padx=2, pady=2)
        self.txt_xmax = tk.Entry(self.fm_axis_setter)
        self.txt_xmax.insert(0, str(plt.xlim()[1]))
        self.txt_xmax.grid(row=0, column=3, padx=2, pady=2)
        self.btn_xapply = tk.Button(self.fm_axis_setter, text="apply",
                command= lambda :self.btn_xapply_pushed(self.btn_xapply))
        self.btn_xapply.grid(row=0, column=4, padx=2, pady=2)
        self.btn_xauto = tk.Button(self.fm_axis_setter, text="auto",
                command= lambda :self.btn_xauto_pushed(self.btn_xapply))
        self.btn_xauto.grid(row=0, column=5, padx=2, pady=2)
        #
        self.lbl_ymin = tk.Label(self.fm_axis_setter, text="y min:")
        self.lbl_ymin.grid(row=1, column=0, padx=2, pady=2)
        self.txt_ymin = tk.Entry(self.fm_axis_setter)
        self.txt_ymin.insert(0, str(plt.ylim()[0]))
        self.txt_ymin.grid(row=1, column=1, padx=2, pady=2)
        self.lbl_ymax = tk.Label(self.fm_axis_setter, text=" max:")
        self.lbl_ymax.grid(row=1, column=2, padx=2, pady=2)
        self.txt_ymax = tk.Entry(self.fm_axis_setter)
        self.txt_ymax.insert(0, str(plt.ylim()[1]))
        self.txt_ymax.grid(row=1, column=3, padx=2, pady=2)
        self.btn_yapply = tk.Button(self.fm_axis_setter, text="apply",
                command= lambda :self.btn_yapply_pushed(self.btn_yapply))
        self.btn_yapply.grid(row=1, column=4, padx=2, pady=2)
        self.btn_xauto = tk.Button(self.fm_axis_setter, text="auto",
                command= lambda :self.btn_yauto_pushed(self.btn_xapply))
        self.btn_xauto.grid(row=1, column=5, padx=2, pady=2)
        #
        self.fm_axis_setter.grid_columnconfigure(1, weight=1)
        self.fm_axis_setter.grid_columnconfigure(3, weight=1)
        #
        #
        self.root.mainloop()
    #
    # event handler
    def btn_fileref_pushed(self, button):
        #self.txt_ymin.insert(0, "pushed")
        fTyp = [("","*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        filepath = filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        self.txt_filename.delete(0, tk.END)
        self.txt_filename.insert(0, filepath)
    def btn_loadcsv_pushed(self, button):
        df = pd.read_csv(self.txt_filename.get())
        self.main_database = df
        self.cbb_xdata["values"]=tuple(self.main_database.columns)
        self.cbb_xdata.current(0)
        self.cbb_ydata["values"]=tuple(self.main_database.columns)
        self.cbb_ydata.current(1)
    def btn_xapply_pushed(self, button):
        self.set_xlim()
    def btn_xauto_pushed(self, button):
        xs = [line._x for line in self.dp.lines.values()]
        xmin = min(x.min() for x in xs)
        xmax = max(x.max() for x in xs)
        self.txt_xmin.delete(0, tk.END)
        self.txt_xmax.delete(0, tk.END)
        if self.cbb_xscale.get() == 'linear':
            self.txt_xmin.insert(0, str(xmin-(xmax-xmin)*0.05))
            self.txt_xmax.insert(0, str(xmax+(xmax-xmin)*0.05))
        else:
            self.txt_xmin.insert(0, str(10**(np.log10(xmin)-np.log10(xmax/xmin)*0.05)))
            self.txt_xmax.insert(0, str(10**(np.log10(xmax)+np.log10(xmax/xmin)*0.05)))
        self.set_xlim()
        self.setscale()
    def btn_yapply_pushed(self, button):
        self.set_ylim()
    def btn_yauto_pushed(self, button):
        ys = [line._y for line in self.dp.lines.values()]
        ymin = min(y.min() for y in ys)
        ymax = max(y.max() for y in ys)
        self.txt_ymin.delete(0, tk.END)
        self.txt_ymax.delete(0, tk.END)
        if self.cbb_yscale.get() == 'linear':
            self.txt_ymin.insert(0, str(ymin-(ymax-ymin)*0.05))
            self.txt_ymax.insert(0, str(ymax+(ymax-ymin)*0.05))
        else:
            self.txt_ymin.insert(0, str(10**(np.log10(ymin)-np.log10(ymax/ymin)*0.05)))
            self.txt_ymax.insert(0, str(10**(np.log10(ymax)+np.log10(ymax/ymin)*0.05)))
        self.set_ylim()
        self.setscale()
    def btn_plt_selected_pushed(self, button):
        if self.cbb_xdata.get()=="load data...": return
        self.reflash_plot()
        self.add_plot(self.main_database[self.cbb_xdata.get()], self.main_database[self.cbb_ydata.get()])
        self.setscale()
    #
    #
    def set_xlim(self):
        self.dp.xlim((float(self.txt_xmin.get()), float(self.txt_xmax.get())))
        self.dp.update()    
    def set_ylim(self):
        self.dp.ylim((float(self.txt_ymin.get()), float(self.txt_ymax.get())))
        self.dp.update()
    def reflash_plot(self):
        self.dp.reflash_ax()
        #self.dp.ax.cla()
    def add_plot(self,x,y,label=None):
        if label is None:
            self.dp.add_plot(x,y)
        else:
            self.dp.add_plot(x,y,name=label)
        self.dp.update()
    def setscale(self):
        if self.dp.ax.get_xscale()!=self.cbb_xscale.get()\
                or self.dp.ax.get_yscale()!=self.cbb_yscale.get():
            self.dp.ax.set_xscale(self.cbb_xscale.get())
            self.dp.ax.set_yscale(self.cbb_yscale.get())
            self.dp.update()


if __name__=="__main__":
    gg = GraphAjuster()
