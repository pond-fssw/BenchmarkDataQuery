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
        self.setWindowTitle("CE Hardware Benchmarking")
        self.devicesToCompare = []
        self.summaryFilesPath = "test_docs/"
        self.tempFile = "Comparison_Table.csv" 
        self.benchmarkInputs = [[self.b1_1, self.b1_2],
                                [self.b2_1, self.b2_2],
                                [self.b3_1, self.b3_2],
                                [self.b4_1, self.b4_2]]
        self.benchmarkInputsNames = [["a", "swd"],
                                    ["asd", "asd"],
                                    ["sa", "asd"],
                                    ["s", "asd"]]

    def init_ui(self):
        self.generateCompareDropdown()
        self.genTable.clicked.connect(self.generateTable)
        self.addDevice.clicked.connect(self.addThisDevice)
        self.clearDevices.clicked.connect(self.clearAllDevices)
        self.exportTable.clicked.connect(self.exportCompTable)
        self.queryButton.clicked.connect(self.generateQuery)
        self.benchmarkRun.clicked.connect(self.benchmarkSaveSelection)
        self.benchmarkClear.clicked.connect(self.benchmarkClearSelection)
    
    def benchmarkSaveSelection(self):
        fileName = self.summaryFilesPath + self.benchmarkDevice.text() + ".csv"

        for input_group, input_label_group in zip(self.benchmarkInputs, self.benchmarkInputsNames):
            for property_value, property_label in zip(input_group, input_label_group):
                pass

    def benchmarkClearSelection(self):
        for input_group in self.benchmarkInputs:
            for property_value in input_group:
                property_value.setText("")

    def generateQuery(self):
        deviceToQuery = self.toQuery.currentText()

        deviceDataParsed = DataParser(deviceToQuery)
        self.queriedDevice.setText("Device: " + self.byeDotCSV(deviceToQuery))
        self.qPassiveTotal.setText("Passive Total: " + deviceDataParsed.getFeature("Passive Total"))
        self.qActiveTotal.setText("Active Total: " + deviceDataParsed.getFeature("Active Total"))
        self.qActiveDissipation.setText("Active Dissipation: " + deviceDataParsed.getFeature("Active Dissipation"))

    def exportCompTable(self):
        tempFile = self.tempFile
        df = pd.read_csv(tempFile)

        if not df.empty:
            folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
            filename = self.exportfile.text()
            filepath = folderpath + "/" + filename + ".csv"

            df.to_csv(filepath)

    def byeDotCSV(self, fileName):
        return fileName.strip(".csv")

    def generateCompareDropdown(self):
        for deviceFile in os.listdir(self.summaryFilesPath):
            deviceName = self.byeDotCSV(deviceFile)
            self.toCompare.addItem(deviceName)
            self.toQuery.addItem(deviceName)

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
            labelName = self.byeDotCSV(labelName)
            newLabel = "Device " + str(counter) + ": " + labelName
            labelItem.setText(newLabel) 
            counter += 1

    def generateTable(self):
        tempFile = self.tempFile
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

            self.embedTable()

    def embedTable(self):
        tempFile = self.tempFile
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