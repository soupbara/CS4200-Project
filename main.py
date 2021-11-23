#Import wordnet from the NLTK

#import nltk
#nltk.download('wordnet') download wordnet
from nltk.corpus import wordnet

# syn = list()
# ant = list()
# for synset in wordnet.synsets("food"):
#    for lemma in synset.lemmas():
#       syn.append(lemma.name())
#       if lemma.antonyms():
#         ant.append(lemma.antonyms()[0].name())
# print('Synonyms: ' + str(syn))
# print('Antonyms: ' + str(ant))

synset = wordnet.synset("food.n.02")
hyponym1 = synset.hyponyms()

for hypo in hyponym1:
    print(hypo)
    print(hypo.hyponyms())
    print("")