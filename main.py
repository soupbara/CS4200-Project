import requests
obj = requests.get('http://api.conceptnet.io/c/en/food').json()

for i in range(len(obj['edges'])):
 print(obj['edges'][i]['end']['label'])
 for key in ['rel','surfaceText']:
  print(obj['edges'][i][key])