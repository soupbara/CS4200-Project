import requests

class ConceptNetClient:

    BASE_URL = 'http://api.conceptnet.io/c/en/food'

    def __init__(self):
        self.jsonResponse = requests.get(self.BASE_URL).json()

    def printEdges(self):
        for i in range(len(self.jsonResponse['edges'])):
            print(self.jsonResponse['edges'][i]['end']['label'])

        #  for key in ['rel','surfaceText']:
        #   print(obj['edges'][i][key])

    def printCurrJson(self):
        print(self.jsonResponse)