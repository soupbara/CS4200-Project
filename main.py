#testing commit
from client import ConceptNetClient
from attribute import Attribute
from answer import Answer

import random

apiClient = ConceptNetClient()
# print(apiClient.generalFoodRequest())
# uri=apiClient.getURI("breakfast")
# print(apiClient.getPropertiesOf(uri))
# print(apiClient.getTypesOf(apiClient.getURI("one_unhealthy_food")))
# print(apiClient.confirmTypeOf(apiClient.getURI("breakfast_food"), apiClient.getURI("food")))
# print(apiClient.getWhatMadeOf(apiClient.getURI("chocolate")))
# print(apiClient.getRelationTypesBw(apiClient.getURI("plate"), apiClient.getURI("food")))
# print(apiClient.getRelatednessVal(apiClient.getURI("celebration"), apiClient.getFoodURI()))
#print(apiClient.getRootWord(apiClient.getURI("pies")))

possibleAnswers = {}    #track which Answers are still valid in choosing
allAttributes = []      #track history of all positive Attributes
nonpossibleAnswers = {}     #track which Answers we've already decided to throw out --> do NOT attempt to add it again!


userPreferences = []

MIN_POSS_ANSWERS = 30       #certain length of possibleAnswers[] necessary before able to create questions based on these probable answers.
initializedAnswers = False
MIN_PROBABILITY = 0.07

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

#Purpose:   Return which Answer is the most probable (highest probability) right now, used in findNextQuestion()
def findMostProbableAnswer():
    for answer in possibleAnswers:
        pass

#Purpose:   Return the highest relatedness value from api for this phrase. Relatedness value based on this phrase and "food"
def getOverallRelatedness(phrase):
    phraseArr = phrase.split()
    max = -5        #assume no relatedness value can ever be below -5
    for word in phraseArr:
        currVal = apiClient.getRelatednessVal(apiClient.getURI(word), apiClient.getFoodURI())
        if currVal > max and word != "food":
            max = currVal
    return max

#Purpose: Use API to figure out what question to return next, format the question as a string and return it. Used by game()
def findNextQuestion():
    global initializedAnswers, MIN_POSS_ANSWERS, possibleAnswers, allAttributes, nonpossibleAnswers

    #1.) Do we have enough in our possibleAttributes to choose randomly, or choose only on general food?
    if initializedAnswers:
        #Randomly choose how we get the next question: (1) Choose question based on possible answer, (2) Choose question based on general foods (expands the possibleAnswer[])

        pass
    else:
        #Choose either to base next question on location or, choose some interval of types of food on possibleAnswers and call this method again. (purpose of this: expands the possibleAnswer[])
        choice = random.randint(0, 1)

        #do question based on locationAt relation on general food node
        if choice == 0:
            edges = apiClient.getLocationOf(apiClient.getFoodURI())

            askedQuestion = False
            while not askedQuestion:
                #Choose random edge, determine if its relatedness value to "food" is high enough, --> ask question about it if so:
                rIndex = random.randint(0, len(edges)-1)
                print(rIndex)

                edgeLabel = edges[rIndex]["end"]["label"]
                print(edgeLabel)

                if getOverallRelatedness(edgeLabel) > 0.1:
                    askedQuestion = True

                    #ask the question:
                    question = apiClient.getQuestionFrame(apiClient.RELATION_LOCATION)+edgeLabel+"? Enter: (1) Yes or (2) No"
                    userInput = getValidChoice(question, [1, 2])

                    #If said yes --> (1) create a new Attribute to track, (2) find all possible answers that satify this new Attribute + save into possibleAnswers
                    if userInput == 1:
                        newAttribute = Attribute(apiClient.RELATION_LOCATION, edgeLabel)
                        allAttributes.append(newAttribute)

                        #Find all possibleAnswers: all nodes that IsA food & is AtLocation edgeLabel:
                        #1.) Get things located at:
                        response = apiClient.getWhatIsLocatedAt(apiClient.getURI(edgeLabel), 20)

                        #2.) For each edge, save only the ones that are also a food:
                        validPossAnswers = []
                        for node in response:
                            #Get the label, ensure we are using the root most form of the word
                            label = node["start"]["label"]
                            print("Before getting root:" + label)
                            label = apiClient.removeArticlesIn(label)
                            rootWord = apiClient.getRootWord(apiClient.getURI(label))
                            if rootWord is not None:
                                label = rootWord               #only ever stores ROOT words, --> easier to check, don't have to worry about any different forms
                            print('after getting root and removing articles: '+label)
                            #If label IS a food, and NOT yet in possibleAnswers, store into validPossAnswers to incorporate into possibleAnswers later:
                            if apiClient.getIsFood(label):
                                validPossAnswers.append(label)


                                # if not (label in possibleAnswers.keys()):
                                #     possibleAnswers[label] = Answer(newAttribute, label)
                                #
                                # #If already seen this word --> increase probability, add this newAttribute it qualifies for
                                # else:
                                #     answer = Answer(possibleAnswers.get(label))
                                #     answer.addProbability()
                                #     answer.addAttribute(newAttribute)

                        #3.) Now we know what should be inside possibleAnswers bc validPossAnswers is populated
                        #           --> iterate through possibleAnswers and update ALL probabilities of ALL possible answers based on what has and hasn't been seen this iteration
                        for key in possibleAnswers.keys():
                            answer = Answer(possibleAnswers.get(key))
                            #if we already have the answer in possibleAnswers --> increase probability, add this newAttribute it qualifies for
                            if key in validPossAnswers:
                                answer.addProbability()
                                answer.addAttribute(newAttribute)

                                #remove from validPossAnswers:
                                validPossAnswers.remove(key)

                            #We didn't see this answer this iteration --> decrease probability
                            else:
                                answer.subProbability()
                                #is the probability too low now? yes --> remove it and no longer consider it for the future purposes
                                if answer.getProbability() < MIN_PROBABILITY:
                                    print("possAnswers length before pop: " + str(len(possibleAnswers)))
                                    possibleAnswers.pop(key)
                                    print("possAnswers length after pop: " + str(len(possibleAnswers)))
                                    nonpossibleAnswers[key] = answer

                        #4.) At this point, validPossAnswers should only be filled with Answer labels that are NOT yet in possibleAnswers{} --> can add it now:
                        for answerLabel in validPossAnswers:
                            if not(answerLabel in nonpossibleAnswers.keys()):
                                possibleAnswers[answerLabel] = Answer(newAttribute, answerLabel)


                        #for testing reasons:
                        print("possAnswers:  ")
                        for answer in possibleAnswers.items():
                            print(answer[1].getLabel())



        #do NOT choose a question, instead, pick a random range and populate random interval of isA relation into possibleAnswers, + call method again
        else:
            edges = apiClient.getTypesOf(apiClient.getFoodURI())

            #Choose random sample of of random size of edges to look at
            section = random.sample(list(edges), random.randint(1, 20 if len(edges) > 20 else len(edges)))


        if len(possibleAnswers) >= MIN_POSS_ANSWERS:
            initializedAnswers = True


findNextQuestion()


 # category = {"breakfast":"Are you looking for breakfast? (1) Yes, (2) No", "lunch":"Are you looking for lunch? (1) Yes, (2) No", "dinner":"Are you looking for dinner? (1) Yes, (2) No", "dessert":"Are you looking for desserts? (1) Yes, (2) No"}
 # portion = {"full meal":"Do you want a full meal? (1) Yes, (2) No", "snack":"Do you want a snack? (1) Yes, (2) No", "finger food":"Would you like finger food? (1) Yes, (2) No", "ready-to-eat":"Would you like ready-to-eat food? (1) Yes, (2) No"}
 # type = {"beverage":"Would you like a beverage? (1) Yes, (2) No", "solid food":"Would you like solid food? (1) Yes, (2) No", "semi-solid food":"Would you like semi-solid food? (1) Yes, (2) No"}
 # flavor = {"sweet":"Would you like something sweet? (1) Yes, (2) No", "savory":"Would you like something savory? (1) Yes, (2) No", "sour":"Would you like something sour? (1) Yes, (2) No", "spicy":"Would you like spicy food? (1) Yes, (2) No", "bitter":"Would you like something bitter? (1) Yes, (2) No"}
 # restriction = {"vegan":"Do you want something vegan? (1) Yes, (2) No", "meat":"Are you able to eat meat? (1) Yes, (2) No", "gluten":"Are you able to eat gluten? (1) Yes, (2) No", "nuts":"Are you able to eat nuts? (1) Yes, (2) No", "dairy":"Are you able to eat dairy products? (1) Yes, (2) No"}
 #
 # #Randomly select a question to ask, however it may repeat if the user continuously answers 'no'
 # if currentQuestion == 1:
 #     return random.choice(list(category.items()))
 # if currentQuestion == 2:
 #     return random.choice(list(portion.items()))
 # if currentQuestion == 3:
 #     return random.choice(list(type.items()))
 # if currentQuestion == 4:
 #     return random.choice(list(flavor.items()))
 # else:
 #     return random.choice(list(restriction.items()))


#Purpose: Use API to determine if we found a good enough answer! E.g. is there anything else we could ask, how confident are we in this answer, etc.
def gameFinished():
    pass
 # path = 'http://api.conceptnet.io/c/en/' + userPreferences[0] #Add the user's data to the path (first item in userPreferences)
 # obj = requests.get(path).json() #Get method to retrieve the data
 # index = 0
 #
 # #Print out results from ConceptNet
 # for i in range(len(obj['edges'])):
 #     print(obj['edges'][i]['end']['label'])
 #     #if '/r/IsA' in obj['edges'][i]['end']['label']:
 #         #index = i
 #     for key in ['rel', 'surfaceText']:
 #         print(obj['edges'][i][key])
 #
 # #Print suggested item to user
 # print("Answer generated! You might enjoy: " + str(obj['edges'][index][key]))
 # print("---------------------------------------\n")




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







#main()
