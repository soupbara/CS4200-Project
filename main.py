#testing commit
from client import ConceptNetClient
import random
import requests

apiClient = ConceptNetClient()
apiClient.printCurrJson()
apiClient.printEdges()
userPreferences = []

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
def findNextQuestion(currentQuestion):
 category = {"breakfast":"Are you looking for breakfast? (1) Yes, (2) No", "lunch":"Are you looking for lunch? (1) Yes, (2) No", "dinner":"Are you looking for dinner? (1) Yes, (2) No", "dessert":"Are you looking for desserts? (1) Yes, (2) No"}
 portion = {"full meal":"Do you want a full meal? (1) Yes, (2) No", "snack":"Do you want a snack? (1) Yes, (2) No", "finger food":"Would you like finger food? (1) Yes, (2) No", "ready-to-eat":"Would you like ready-to-eat food? (1) Yes, (2) No"}
 type = {"beverage":"Would you like a beverage? (1) Yes, (2) No", "solid food":"Would you like solid food? (1) Yes, (2) No", "semi-solid food":"Would you like semi-solid food? (1) Yes, (2) No"}
 flavor = {"sweet":"Would you like something sweet? (1) Yes, (2) No", "savory":"Would you like something savory? (1) Yes, (2) No", "sour":"Would you like something sour? (1) Yes, (2) No", "spicy":"Would you like spicy food? (1) Yes, (2) No", "bitter":"Would you like something bitter? (1) Yes, (2) No"}
 restriction = {"vegan":"Do you want something vegan? (1) Yes, (2) No", "meat":"Are you able to eat meat? (1) Yes, (2) No", "gluten":"Are you able to eat gluten? (1) Yes, (2) No", "nuts":"Are you able to eat nuts? (1) Yes, (2) No", "dairy":"Are you able to eat dairy products? (1) Yes, (2) No"}

 #Randomly select a question to ask, however it may repeat if the user continuously answers 'no'
 if currentQuestion == 1:
     return random.choice(list(category.items()))
 if currentQuestion == 2:
     return random.choice(list(portion.items()))
 if currentQuestion == 3:
     return random.choice(list(type.items()))
 if currentQuestion == 4:
     return random.choice(list(flavor.items()))
 else:
     return random.choice(list(restriction.items()))


#Purpose: Use API to determine if we found a good enough answer! E.g. is there anything else we could ask, how confident are we in this answer, etc.
def gameFinished():
 path = 'http://api.conceptnet.io/c/en/' + userPreferences[0] #Add the user's data to the path (first item in userPreferences)
 obj = requests.get(path).json() #Get method to retrieve the data
 index = 0

 #Print out results from ConceptNet
 for i in range(len(obj['edges'])):
     print(obj['edges'][i]['end']['label'])
     #if '/r/IsA' in obj['edges'][i]['end']['label']:
         #index = i
     for key in ['rel', 'surfaceText']:
         print(obj['edges'][i][key])

 #Print suggested item to user
 print("Answer generated! You might enjoy: " + str(obj['edges'][index][key]))
 print("---------------------------------------\n")


#Purpose:  Runs one whole game of Crave! Uses findNextQuestion(), gameFinished(), and get
def game():
 currentCategory = 1
 notDone = True

 while notDone:
  #1.) Ask a question + provide choices
     #Make + call method to find a question to ask
  question = findNextQuestion(currentCategory)
  choice = getValidChoice(question[1], [1,2])

  #2.) Get validated choice
  # Only move to next question category after user has answered 'yes'
  if choice == 1:
      currentCategory = currentCategory + 1
      userPreferences.append(question[0]) #saves the attributes the user answers 'yes', to help look for a suitable food item in API

      # 3.) Check if can finish game
      # Change notDone game finished
      if currentCategory == 6:
          print("User Preferences: " + str(userPreferences))
          gameFinished() #return the suggested food
          notDone = False



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







main()
