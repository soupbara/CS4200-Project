#testing commit
from client import ConceptNetClient
import random

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
def findNextQuestion(currentQuestion):
 #TODO: change to dictionary instead of list to help with userPreferences in game()
 category = ["Are you looking for breakfast? (1) Yes, (2) No", "Are you looking for lunch? (1) Yes, (2) No", "Are you looking for dinner? (1) Yes, (2) No", "Are you looking for desserts? (1) Yes, (2) No"]
 portion = ["Do you want a full meal? (1) Yes, (2) No", "Do you want a snack? (1) Yes, (2) No", "Would you like finger food? (1) Yes, (2) No", "Would you like ready-to-eat food? (1) Yes, (2) No"]
 type = ["Would you like a beverage? (1) Yes, (2) No", "Would you like solid food? (1) Yes, (2) No", "Would you like semi-solid food? (1) Yes, (2) No"]
 flavor = ["Would you like something sweet? (1) Yes, (2) No", "Would you like something savory? (1) Yes, (2) No", "Would you like something sour? (1) Yes, (2) No", "Would you like spicy food? (1) Yes, (2) No", "Would you like something bitter? (1) Yes, (2) No"]
 restriction = ["Do you want something vegan? (1) Yes, (2) No", "Are you able to eat pork? (1) Yes, (2) No", "Are you able to eat gluten? (1) Yes, (2) No", "Are you able to eat nuts? (1) Yes, (2) No", "Are you able to eat dairy products? (1) Yes, (2) No"]

 #Randomly select a question to ask, however it may repeat if the user continuously answers 'no'
 if currentQuestion == 1:
     return category[random.randint(0,len(category)-1)]
 if currentQuestion == 2:
     return portion[random.randint(0,len(portion)-1)]
 if currentQuestion == 3:
     return type[random.randint(0,len(type)-1)]
 if currentQuestion == 4:
     return flavor[random.randint(0,len(flavor)-1)]
 else:
     return restriction[random.randint(0,len(restriction)-1)]


#Purpose: Use API to determine if we found a good enough answer! E.g. is there anything else we could ask, how confident are we in this answer, etc.
def gameFinished():
 print("Answer generated! You might enjoy: ")
 print("---------------------------------------\n")


#Purpose:  Runs one whole game of Crave! Uses findNextQuestion(), gameFinished(), and get
def game():
 currentCategory = 1
 userPreferences = []
 notDone = True

 while notDone:
  #1.) Ask a question + provide choices
     #Make + call method to find a question to ask
  question = findNextQuestion(currentCategory)
  choice = getValidChoice(question, [1,2])

  #2.) Get validated choice
  # Only move to next question category after user has answered 'yes'
  if choice == 1:
      currentCategory = currentCategory + 1

      #TODO: change questions to dictionaries to help with userPreferences
      userPreferences.append(question) #saves the questions the user answer 'yes for, to help look for a suitable food item

      # 3.) Check if can finish game
      # Change notDone game finished
      if currentCategory == 6:
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
