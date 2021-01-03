import pandas as pd
import os


import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog

import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Qt5Agg')






dir_icons = "./icons/fugue-icons-3.5.6/icons-shadowless"


# app = QtGui.QApplication([])
# import pyqtgraph.parametertree.parameterTypes as pTypes
# from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType


class read_data:
    def __init__(self, filepath, dataframe):
        
        if filepath:
            self.df = dataframe
            self.filepath = filepath
            self.filename = os.path.basename(self.filepath)
            self.filename_no_ext, self.file_ext = os.path.splitext(self.filename)
        elif not filepath:
            self.df = dataframe
            self.filepath = ''
            self.filename = 'os.path.basename(self.filepath)'
            self.filename_no_ext, self.file_ext = '', ''


    def data_from_file(self):
        try:
            if self.file_ext == '.csv':
                data_set = pd.read_csv(self.filepath)
                # print(f'>>Info: dataset was created from file')
            return (data_set)
        except:
            # print(f'>>Info: Could not load data from {self.filepath}')
            # print(f'>>Info: Empty dataset was created')
            data_set = pd.DataFrame()
            return (data_set)

    def data_from_df(self):
        data_set = self.df
        # print(f'>>Info: dataset was created from pandas dataframe')
        return (data_set) 


    def data(self):
        df_is_empty = (self.df).empty
        if self.filepath and df_is_empty:
            data = self.data_from_file()
        if not self.filepath and not df_is_empty:
            data = self.data_from_df()
        if not self.filepath and df_is_empty:
            data = pd.DataFrame()
            # f'>>Info: empty dataset was created'
            # f'>>Info: filename argument and  dataframe argument were both empty'
        if self.filepath and not df_is_empty:
            data = pd.DataFrame()
            # f'>>Info: empty dataset was created'
            # f'>>Info: give either non empty filename argument or non empty dataframe argument'
        return data

# class plot_data(QMainWindow):

#     def __init__(self, *args, **kwargs):
#         super(plot_data, self).__init__(*args, **kwargs)

#         self.setWindowTitle("Application to Plot of data")

#         label = QLabel("This is a PyQt5 window!")
#         label.setAlignment(Qt.AlignCenter)
#         self.setCentralWidget(label) 

#         fig = Figure()
#         self.axes = fig.add_subplot(111)  

#         toolbar = QToolBar("My main toolbar")
#         toolbar.setIconSize(QSize(16,16))
#         self.addToolBar(toolbar)
#         fig.tight_layout()

#         btn_open_file = QAction(QIcon(dir_icons+"/folder-open-document.png"), "button open file", self)
#         btn_open_file.setStatusTip("Button to open file")
#         btn_open_file.triggered.connect(self.FileDialog)
#         toolbar.addAction(btn_open_file)

#         btn_plot_file = QAction(QIcon(dir_icons+"/chart.png"), "button make plot", self)
#         btn_plot_file.setStatusTip("Button to plot data")
#         btn_plot_file.triggered.connect(self.plot_mpl)
#         toolbar.addAction(btn_plot_file)

#     def FileDialog(self):
#         fname = QFileDialog.getOpenFileName(self, 'Open file')[0]
#         print(f'>>Info: Selected File: {(fname)}')
#         self.dataframe = read_data(fname, pd.DataFrame()).data()
#         print(self.dataframe)

#     def plot_mpl(self):
#         data = self.dataframe
#         plt.cla()
#         ax = self.figure.add_subplot(111)
#         ax.plot(data.iloc[:,1], 'g', label = "Pred on data with Model")
#         self.canvas.draw()





# app = QApplication(sys.argv)
# window = plot_data()
# window.show()

# app.exec_()



        
        
        
        
# # df_test = pd.DataFrame(); path = "./sample_data/data-master/us-weather-history/KCLT.csv";
# # # df_test = pd.DataFrame([['tom', 10], ['nick', 15], ['juli', 14]] , columns = ['Name', 'Age']); path = ''
# # data_test = read_data(path, df_test).data()

# # print(data_test.index.name)
# # plot_data(data_test)



