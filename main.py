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

#possibleAnswers = {}    #track which Answers are still valid in choosing
allAttributes = []      #track history of all positive Attributes
nonpossibleAnswers = {}     #track which Answers we've already decided to throw out --> do NOT attempt to add it again!

possibleAnswers = {"Peanut butter": Answer(None, "Peanut butter"),
"nutriment" : Answer(None, "nutriment"),
"chocolate" : Answer(None, "chocolate")}

userPreferences = []

MIN_POSS_ANSWERS = 3       #certain length of possibleAnswers[] necessary before able to create questions based on these probable answers.
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

#Purpose:  Given a List<String> of valid answers to add into global possibleAnswers, correctly insert it where every Answer's probability is updated + no duplicate terms
def insertUpdatePossibleAnswers(newAttribute, validPossAnswers):
    global possibleAnswers, MIN_PROBABILITY
    #1.) Iterate through possibleAnswers and update ALL probabilities of ALL possible answers based on what has and hasn't been seen this iteration
    for key in possibleAnswers.keys():
        answer = possibleAnswers.get(key)

        # if already have the answer in possibleAnswers --> increase probability, add this newAttribute it qualifies for
        if key in validPossAnswers:
            answer.addProbability()
            answer.addAttribute(newAttribute)

            # remove from validPossAnswers:
            validPossAnswers.remove(key)

        # Otherwise --> we didn't see this answer this iteration --> decrease probability
        else:
            answer.subProbability()
            # is the probability too low now? yes --> remove it and no longer consider it for future purposes
            if answer.getProbability() < MIN_PROBABILITY:
                print("possAnswers length before pop: " + str(len(possibleAnswers)))
                possibleAnswers.pop(key)
                print("possAnswers length after pop: " + str(len(possibleAnswers)))
                nonpossibleAnswers[key] = answer

    #2.) At this point, validPossAnswers should only be filled with Answer labels that are NOT yet in possibleAnswers{} --> can add it now:
    for answerLabel in validPossAnswers:
        if not (answerLabel in nonpossibleAnswers.keys()):
            possibleAnswers[answerLabel] = Answer(newAttribute, answerLabel)

    #for testing reasons:
    print("possAnswers:  ")
    for answer in possibleAnswers.items():
        print(answer[1].getLabel())

#Purpose:   Choose a random possible answer and category to ask about it. Return a tuple with (answerChosen, categoryType, list of resulting edges from query)
def generateRandomQuery(uri, randomCategory):
    global possibleAnswers, apiClient

    if randomCategory == apiClient.RELATION_PROPERTY:
        return apiClient.getPropertiesOf(uri)

    elif randomCategory == apiClient.RELATION_GET_TYPE: #Taken out of the range so don't really worry about it
        return apiClient.getTypesOf(uri)

    elif randomCategory == apiClient.RELATION_USED_FOR:
        return apiClient.getWhatUsedFor(uri)

    elif randomCategory == apiClient.RELATION_CAPABLE:
        return apiClient.getWhatCapableOf(uri)

    elif randomCategory == apiClient.RELATION_CAN_BE:
        return apiClient.getCanBe(uri)

    else:       # randomCategory == apiClient.RELATION_MADE_OF:
        return apiClient.getWhatMadeOf(uri)



#Purpose:   Choose a random possible answer and category to ask about it. Return a tuple with (answerChosen, categoryType, list of resulting edges from query)
def getThingsAboutRelation(uri, category):
    global possibleAnswers, apiClient

    if category == apiClient.RELATION_PROPERTY:
        return apiClient.thingsWithPropertiesOf(uri)

    elif category == apiClient.RELATION_GET_TYPE:       #took out of range, don't worry about this conditional for now
        return apiClient.getTypesOf(uri)

    elif category == apiClient.RELATION_USED_FOR:
        return apiClient.thingsUsedFor(uri)

    elif category == apiClient.RELATION_CAPABLE:
        return apiClient.getThingsCapableOf(uri)

    elif category == apiClient.RELATION_CAN_BE:
        return apiClient.getThingsThatCan(uri)

    else:       # randomCategory == apiClient.RELATION_MADE_OF:
        return apiClient.getThingsMadeOf(uri)



#Purpose: Use API to figure out what question to return next, format the question as a string and return it. Used by game()
def findNextQuestion():
    global apiClient, initializedAnswers, MIN_POSS_ANSWERS, possibleAnswers, allAttributes, nonpossibleAnswers

    #Because findNextQuestion() gets called many times, just update flag, initializedAnswers, whenever applicable
    if len(possibleAnswers) >= MIN_POSS_ANSWERS:
        initializedAnswers = True

    #1.) Do we have enough in our possibleAttributes to choose randomly, or choose only on general food?
    if initializedAnswers:
        #Randomly choose how we get the next question: (1) Choose question based on possible answer, (2) Choose question based on general foods (expands the possibleAnswer[])
        askedQuestion = False

        while not askedQuestion:

            randomAnswerKey = random.choice(list(possibleAnswers))
            randomAnswer = possibleAnswers[randomAnswerKey]
            allCategories = apiClient.getAllRelations()

            print("random answer: " + randomAnswer.getLabel())

            # Continue looking for validEdge if there are still categories to look for a question in
            while len(allCategories) > 0:
                randomCategory = random.choice(allCategories)
                print("random category: " + randomCategory)
                allCategories.remove(randomCategory)                #remove so we don't repeat exploring this category if we re-iterate!

                possibleEdges = generateRandomQuery(apiClient.getURI(randomAnswer.getLabel()), randomCategory)

                foundValidEdge = False
                validEdge = None
                while not foundValidEdge:
                    #Continue looking for validEdge if there are still possibleEdges
                    if len(possibleEdges) > 0:
                        #1.) Pick a random index/random edge + see if it has high enough relatedness to "food"
                        rIndex = random.randint(0, len(possibleEdges) - 1)
                        print(rIndex)

                        possibleEdge = possibleEdges[rIndex]["end"]["label"]        #"end" is correct only for our current methods
                        print(possibleEdge)
                        del possibleEdges[rIndex]  # remove this edge from dictionary to not re-do it again if it doesn't work out

                        #possibleEdge has enough relatedness to ask a question about it! --> get out of while
                        if getOverallRelatedness(possibleEdge) > 0.1:
                            foundValidEdge = True
                            validEdge = possibleEdge

                    #Otherwise --> ran out of possibleEdges
                    else:
                        break

                #If found good edge --> can ask question:
                if foundValidEdge:
                    askedQuestion = True

                    # ask question here
                    question = apiClient.getQuestionFrame(randomCategory) + validEdge + "? Enter: (1) Yes or (2) No"
                    userInput = getValidChoice(question, [1, 2])


                    # handle input here

                    if userInput == 1:
                        #1.) Create new Attribute to track in allAttributes[]
                        newAttribute = Attribute(randomCategory, validEdge)
                        allAttributes.append(newAttribute)

                        #2.) increase own probability, add attribute
                        randomAnswer.addProbability()
                        randomAnswer.addAttribute(newAttribute)

                        #Find other possibleAnswers to add to possibleAnswers{}

                        # Find all possibleAnswers:
                        # 1.) Get things that also meet this Attribute:
                        response = getThingsAboutRelation(apiClient.getURI(validEdge), randomCategory)

                        # 2.) Save only the ones that are also a food:
                        validPossAnswers = []
                        for node in response:
                            # Get the label, ensure we are using the root most form of the word
                            label = node["start"]["label"]
                            print("Before getting root:" + label)
                            label = apiClient.removeArticlesIn(label)
                            rootWord = apiClient.getRootWord(apiClient.getURI(label))
                            if rootWord is not None:
                                label = rootWord  # only ever stores ROOT words, --> easier to check, don't have to worry about any different forms
                            print('after getting root and removing articles: ' + label)

                            # If label IS a food, and NOT yet in possibleAnswers, store into validPossAnswers to incorporate into possibleAnswers later:
                            if apiClient.getIsFood(label):
                                validPossAnswers.append(label)

                        # 3.) Insert list of possible answers correcting updating old possibleAnswers:
                        insertUpdatePossibleAnswers(newAttribute, validPossAnswers)



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
                del edges[rIndex]   #remove this edge from dictionary to not re-do it again if it doesn't work out


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


                        #3.) Insert list of possible answers correcting updating old possibleAnswers:
                        insertUpdatePossibleAnswers(newAttribute, validPossAnswers)



        #Otherwise --> do NOT choose a question, instead, pick a random range and populate random interval of isA relation into possibleAnswers, + call method again to eventually ask a q
        else:
            edges = apiClient.getTypesOf(apiClient.getFoodURI())

            #Choose random sample of of random size (max of 20) of edges to look at
            section = random.sample(list(edges), random.randint(1, 20 if len(edges) > 20 else len(edges)))

            #Get the label, add a new Answer obj if its not yet in possibleAnswers AND is not banned in nonpossibleAnswers
            for node in section:
                answerLabel = node["start"]["label"]
                answerLabel = apiClient.removeArticlesIn(answerLabel)
                rootWord = apiClient.getRootWord(apiClient.getURI(answerLabel))
                if rootWord is not None:
                    answerLabel = rootWord

                if not (answerLabel in possibleAnswers.keys()) and not (answerLabel in nonpossibleAnswers.keys()):
                        possibleAnswers[answerLabel] = Answer(None, answerLabel)

            #just for testing reasons
            print("possAnswers:  ")
            for answer in possibleAnswers.items():
                print(answer[1].getLabel())

            #Call again to keep initializing possibleAnswers, and eventually actually ask question
            print("calling findNextQuestion() again")
            findNextQuestion()



while True:
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
