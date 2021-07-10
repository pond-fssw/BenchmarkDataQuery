import sys
import os
import csv
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

from BenchmarkDataParser import DataParser

class BenchmarkDataQuery(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/BenchmarkDataQuery.ui", self)
        self.init_vars()
        self.init_ui()

    def init_vars(self):
        self.devicesToCompare = []
        self.summaryFilesPath = "test_docs"

    def init_ui(self):
        self.generateCompareDropdown()
        self.genTable.clicked.connect(self.generateTable)
        self.addDevice.clicked.connect(self.addThisDevice)
        self.clearDevices.clicked.connect(self.clearAllDevices)

    def generateCompareDropdown(self):
        for deviceFile in os.listdir(self.summaryFilesPath):
            self.toCompare.addItem(deviceFile)
            self.toQuery.addItem(deviceFile)

    def addThisDevice(self):
        deviceFile = self.toCompare.currentText()
        self.devicesToCompare.append(deviceFile)
        self.updateCompareLabels()

    def clearAllDevices(self):
        self.devicesToCompare = []
        self.updateCompareLabels()

    def updateCompareLabels(self):
        labelItems = [self.dev1, self.dev2, self.dev3]
        labelNames = self.devicesToCompare.copy()
        print(labelNames)
        if len(self.devicesToCompare) < 3:
            labelNames.extend([" ", " ", " "])

        counter = 1
        for labelItem, labelName in zip(labelItems, labelNames):
            newLabel = "Device " + str(counter) + ": " + labelName
            labelItem.setText(newLabel) 
            counter += 1

    def generateTable(self):
        tempFile = "Comparison_Table.csv" 
        f = open(tempFile, "w+")
        f.close()

        if (len(self.devicesToCompare) == 0):
            self.compTable.clear()
        else:
            deviceInfoDicts = []
            for device in self.devicesToCompare:
                deviceInfo = DataParser(device)
                deviceInfoDicts.append(deviceInfo.returnDictionary())
        
            with open(tempFile, "a") as f:
                writer = csv.writer(f)
                for featureKey in deviceInfoDicts[0]:
                    row = [featureKey]
                    for deviceInfoDict in deviceInfoDicts:
                        row.append(deviceInfoDict[featureKey])
                    
                    writer.writerow(row)

            self.embedTable(tempFile)

    def embedTable(self, tempFile):
        table = self.compTable
        df = pd.read_csv(tempFile, skiprows=4)

        df.fillna('', inplace= True)
        table.setRowCount(df.shape[0])
        table.setColumnCount(df.shape[1])
        table.setHorizontalHeaderLabels(df.columns)

        # Returns pandas array object
        for row in df.iterrows():
            values = row[1]
            for col_index, value in enumerate(values):
                if isinstance(value, (float, int)):
                    value = '{0:0,.0f}'.format(value)
                tableItem = QtWidgets.QTableWidgetItem(str(value))
                table.setItem(row[0], col_index, tableItem)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = BenchmarkDataQuery()
    window.show()
    app.exec_()