import sys
import os
import pandas as pd

from numpy import nan

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import Qt


from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from read_file import read_data

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


class App_ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(App_ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('./UI/App_UI_20201227.ui', self) # Load the .ui file
       
        plt.style.use('ggplot')
        self.fig = Figure()
        self.dataframe = pd.DataFrame() #Initialize an empty data frame
        self.dataframe_keys = (self.dataframe.columns)
        self.fname = ''
        self.file_size = None
        self.file_rows, self.file_cols = None, None

        self.canvas = FigureCanvas(self.fig)
        self.mplvl.addWidget(self.canvas)
        self.ax = self.fig.subplots(nrows=1, ncols=1, squeeze=False)
        self.fig.tight_layout()
        self.canvas.draw()

        self.toolbar = NavigationToolbar(self.canvas, 
                self.mplwindow, coordinates=True)
        self.mplvl.addWidget(self.toolbar)

        self.show() # Show the GUI

        btn_open_file = self.actionOpen_File
        btn_open_file.triggered.connect(self.OpenFileDialog)

        self.cmbx_x_axis_data = self.comboBox_x_axis_data
        self.cmbx_y_axis_data = self.comboBox_y_axis_data

        self.textBox_filePath    = self.textEdit_filePath
        self.textBox_fileSize    = self.textEdit_fileSize
        self.textBox_fileColumns = self.textEdit_fileColumns
        self.textBox_fileRows    = self.textEdit_fileRows

        self.spinBox_xTicksRotation = self.spinBox_x_ticks_rotation
        self.spinBox_xTicksRotation.valueChanged.connect(lambda: self.rotate_axis_ticks("x", self.spinBox_xTicksRotation.value()))
        self.spinBox_yTicksRotation = self.spinBox_y_ticks_rotation
        self.spinBox_yTicksRotation.valueChanged.connect(lambda: self.rotate_axis_ticks("y", self.spinBox_yTicksRotation.value()))

        self.table_data    = self.tableView_dataTable
        
        btn_plot_file = self.actionCreate_Plot
        btn_plot_file.triggered.connect(self.plot_mpl)

    def rotate_axis_ticks(self, plot_axis, rotation):
        self.ax[0,0].tick_params(axis=plot_axis, labelrotation=rotation)
        self.fig.canvas.draw()
        print(plot_axis, rotation)



    def add_columnNames_to_comboBox(self, combo_Box, df):
        self.dataframe_keys = (df.columns)
        combo_Box.addItem('index')
        combo_Box.addItems(self.dataframe_keys)
    
    def remove_columnNames_from_comboBox(self, combo_Box):
        combo_Box.clear()
                
    def OpenFileDialog(self):
        self.remove_columnNames_from_comboBox(self.cmbx_x_axis_data)
        self.remove_columnNames_from_comboBox(self.cmbx_y_axis_data)
        open_file_dialog = QFileDialog.getOpenFileName(self, 'Open file', "", "CSV files (*.csv)")
        if open_file_dialog == ('', ''):
            print(f'>>Info: No file was Selected: {(self.fname)}')
            # self.fname = None
            # self.dataframe = pd.DataFrame()
            
        else:
            self.fname = open_file_dialog[0]
            print(f'>>Info: Selected File: {(self.fname)}')
            self.file_size = str(os.path.getsize(self.fname)/1e6) #in MB, string
            self.dataframe = read_data(self.fname, pd.DataFrame()).data()
            self.file_rows, self.file_cols = self.dataframe.shape
            model = pandasModel(self.dataframe)
            self.table_data.setModel(model)

        self.textBox_filePath.setText(self.fname)
        self.textBox_fileSize.setText(self.file_size)

        self.add_columnNames_to_comboBox(self.cmbx_x_axis_data, self.dataframe)
        self.add_columnNames_to_comboBox(self.cmbx_y_axis_data, self.dataframe)

        self.textBox_fileColumns.setText(str(self.file_cols))
        self.textBox_fileRows.setText(str(self.file_rows))

        

        


    def set_x_data(self):
        data = self.dataframe
        if len(data)!=0:
            if self.cmbx_x_axis_data.currentText()=='index':
                self.x_axis_data = list(data.index.values)
            elif self.cmbx_x_axis_data.currentText()!='index':
                self.x_axis_data = data[self.cmbx_x_axis_data.currentText()]
        else:
            self.x_axis_data=nan


    def set_y_data(self):
        data = self.dataframe
        if len(data)!=0:
            if self.cmbx_y_axis_data.currentText()=='index':
                self.y_axis_data = list(data.index.values)
            elif self.cmbx_y_axis_data.currentText()!='index':
                self.y_axis_data = data[self.cmbx_y_axis_data.currentText()]
        else:
            self.y_axis_data=nan

    def plot_mpl(self):
        data = self.dataframe
        self.set_x_data()
        self.set_y_data()
        self.ax[0,0].cla()
        label_txt = self.cmbx_y_axis_data.currentText()
        self.ax[0,0].plot(self.x_axis_data, self.y_axis_data, 'g', label = label_txt)
        x_axis_label_txt = self.cmbx_x_axis_data.currentText()
        y_axis_label_txt = self.cmbx_y_axis_data.currentText()
        self.ax[0,0].set_xlabel(x_axis_label_txt)
        self.ax[0,0].set_ylabel(y_axis_label_txt)
        self.ax[0,0].legend(loc='best')
        self.ax[0,0].grid(True, which='both')
        # self.ax[0,0].tick_params(axis='x', labelrotation=45)
        self.fig.tight_layout()
        self.canvas.draw()
        print(f'>>Info: New plot was created')



app = QtWidgets.QApplication(sys.argv)
window = App_ui()
app.exec_()