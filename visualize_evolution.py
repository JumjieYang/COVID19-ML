import pandas as pd
import numpy as np
import csv

#here is the lib for scrollbar
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

def getList():
    df = pd.read_csv("result.csv",header=None)
    list = df.values.tolist()
    return list

# this function return an array of symptom in name eg.Adrenal crisis
def  getSymptom():
    list = getList()
    symptom = []
    for item in list[0]:
        if type(item) != type('symptom'):
           continue
        if 'symptom:' in item:
            symptom.append(item[8:])
    return symptom

# this function return an array of symptom in 'symptom:'+name eg.symptom:Adrenal crisis
def  getSymptomTitle():
    list = getList()
    symptom = []
    for item in list[0]:
        if type(item) != type('symptom'):
           continue
        if 'symptom:' in item:
            symptom.append(item)
    return symptom

# this function return an array of region
def getRegion():
    list = getList()
    region = []
    for item in list:
        if item == list[0]:
            continue
        region.append(item[2])
    region = np.unique(region)
    return region

#the class for scrollbar
class ScrollableWindow(QtWidgets.QMainWindow):
    def __init__(self, fig):
        self.qapp = QtWidgets.QApplication([])

        QtWidgets.QMainWindow.__init__(self)
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QtWidgets.QVBoxLayout())
        self.widget.layout().setContentsMargins(0,0,0,0)
        self.widget.layout().setSpacing(0)

        self.fig = fig
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()
        self.scroll = QtWidgets.QScrollArea(self.widget)
        self.scroll.setWidget(self.canvas)

        self.nav = NavigationToolbar(self.canvas, self.widget)
        self.widget.layout().addWidget(self.nav)
        self.widget.layout().addWidget(self.scroll)

        self.show()
        exit(self.qapp.exec_())



df = pd.read_csv("result.csv")
list = df.values.tolist()

#here I use the data of Alaska
region = getRegion()
data = df[df['region_name']==region[0]]
time = data['date'].values.tolist()
symptom = getSymptom()
symptomTitle = getSymptomTitle()

# create a figure and some subplots
fig, axes = plt.subplots(ncols=5, nrows=25, figsize=(8,12))
plt.subplots_adjust(wspace=0.1, hspace=1)
plt.suptitle('Distribution of search frequency in '+region[0])

#draw each subpolt
#if subpolts of all symptom have been drawn
#then rest of subplots will be blank graph
i=0
for ax in axes.flatten():
    if i >= len(symptom):
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title('NA',fontsize=5)
        ax.plot([])
        continue
    search =  data[symptomTitle[i]].values.tolist()
    ax.set_ylim(0,20)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(symptom[i],fontsize=5)
    ax.bar(time,search,alpha=0.7,width=1)
    i = i + 1
# pass the figure to the custom window
ScrollableWindow(fig)
