import requests
obj = requests.get('http://api.conceptnet.io/c/en/example').json()
obj.keys()
dict_keys(['view', '@context', '@id', 'edges'])

len(obj['edges'])
20

obj['edges'][2]
{'@id': '/a/[/r/IsA/,/c/en/example/n/,/c/en/information/n/]',
 'dataset': '/d/wordnet/3.1',
 'end': {'@id': '/c/en/information/n',
  'label': 'information',
  'language': 'en',
  'sense_label': 'n',
  'term': '/c/en/information'},
 'license': 'cc:by/4.0',
 'rel': {'@id': '/r/IsA', 'label': 'IsA'},
 'sources': [{'@id': '/s/resource/wordnet/rdf/3.1',
   'contributor': '/s/resource/wordnet/rdf/3.1'}],
 'start': {'@id': '/c/en/example/n',
  'label': 'example',
  'language': 'en',
  'sense_label': 'n',
  'term': '/c/en/example'},
 'surfaceText': [[example]] is a type of [[information]]',
 'weight': 2.0}
