import pandas as pd

class DataParser:
    def __init__(self, fileName=0):
        fileName = "test_docs/template-ex.csv"
        self.deviceDataDict = pd.read_csv(fileName, header=None, index_col=0, squeeze=True).to_dict()

    def getFeature(self, feature):
        value = self.deviceDataDict[feature]
        return value 

    def returnDictionary(self):
        return self.deviceDataDict

if __name__ == "__main__":
    dataParser = DataParser()
    feature = "Active Dissipation"
    name = dataParser.getFeature(feature)