<<<<<<< HEAD
#import requests
# obj = requests.get('http://api.conceptnet.io/c/en/food').json()
#
# print(obj)
# for i in range(len(obj['edges'])):
#   print(obj['edges'][i]['end']['label'])
#
# #  for key in ['rel','surfaceText']:
# #   print(obj['edges'][i][key])

from client import ConceptNetClient

apiClient = ConceptNetClient()
apiClient.printCurrJson()
apiClient.printEdges()

#Purpose:  Given a list of valid options (ints), ensure user inputs one of the options. Used many time for random prompts.
def getValidChoice(prompt, options):
 while True:
  try:
   print(prompt)
   choice = int(input(""))
  except ValueError:
   print("Sorry I didn't understand that.")
   continue

  #Input was valid --> check if valid choice
  else:
   if not (choice in options):
    print("Sorry that was not a valid choice.")
   else:
    return choice


#Purpose:  Print menu prompt, return choice as int
def printMenu():
  str_menu = "Enter one of the options below:\n(1) Start! :)\n(2) Quit"
  #TODO: Add other options later

  return getValidChoice(str_menu, [1, 2])    #user must choose 1 or 2

#Purpose: Use API to figure out what question to return next, format the question as a string and return it. Used by game()
def findNextQuestion():
 pass


#Purpose: Use API to determine if we found a good enough answer! E.g. is there anything else we could ask, how confident are we in this answer, etc.
def gameFinished():
 pass


#Purpose:  Runs one whole game of Crave! Uses findNextQuestion(), gameFinished(), and get
def game():
 notDone = True

 while notDone:
  pass
  #1.) Ask a question + provide choices
     #Make + call method to find a question to ask

  #2.) Get validated choice

  #3.) Check if can finish game
     #Change notDone game finished



#Purpose:  Runs the entire program! Assembles all functions together.
def main():
 executeGame = True
 while executeGame:

  #1.) Make + call print_welcome() messages
  print("Welcome to Crave! I know you don't know what you want to eat, but I do!! Press start below so I can find out more about your belly!")
  choice = printMenu()

  #3.) Do switch statement based on choice:
   #3a.) Option 1: Play game:
  if choice == 1:
    keepPlaying = True
    while keepPlaying:
       #1.) Make + call game() to start game
       game()

       #2.) Ask to play again, get validated choice --> change keepPlaying accordingly
       strPlayAgain = "Play again? (1) Yes, (2) No";
       playAgain = getValidChoice(strPlayAgain, [1, 2])

       if playAgain == 2:
         keepPlaying = False


   #3b.) Option #2: Quit game --> change executeGame = False to end, Can assume choice = Quit since choice is validated.
  else:
   print("Okay, goodbye!! :)")
   executeGame = False







#main()
=======
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
>>>>>>> bc49aa467655f4f21ca115e9701736fffd0e695d
