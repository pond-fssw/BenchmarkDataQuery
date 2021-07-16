import pandas as pd

class DataParser:
    def __init__(self, fileName):
        #resultsDirectory = "adesgfwgbewigbweigb"
        resultsDirectory = "test_docs/"
        filePath = resultsDirectory + fileName + ".csv"
        print(filePath)
        self.deviceDataDict = pd.read_csv(filePath, header=None, index_col=0, squeeze=True).to_dict()

    def getFeature(self, feature):
        value = self.deviceDataDict[feature]
        return value 

    def returnDictionary(self):
        return self.deviceDataDict

if __name__ == "__main__":
    dataParser = DataParser()
    feature = "Active Dissipation"
    name = dataParser.getFeature(feature)