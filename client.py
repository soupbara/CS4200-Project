import random

import requests

class ConceptNetClient:

    BASE_URL = 'http://api.conceptnet.io'
    # ---static Relation constants----
    RELATION_LOCATION = "AtLocation"
    RELATION_GET_TYPE = "IsA"
    RELATION_PROPERTY = "HasProperty"
    RELATION_USED_FOR = "UsedFor"
    RELATION_MADE_OF = "MadeOf"
    RELATION_CAN_BE = "ReceivesAction"
    RELATION_CAPABLE = "CapableOf"

    RELATE_TO_ENG = {RELATION_LOCATION:"Do you want something from ",
                     RELATION_GET_TYPE: "Do you want ",
                     RELATION_PROPERTY: "Do you want something that is ",
                     RELATION_USED_FOR: "Do you want a food that is used for ",
                     RELATION_MADE_OF: "Do you want something that is made of ",
                     RELATION_CAN_BE: "Do you want something that can be ",
                     RELATION_CAPABLE: "Do you want something that is able to "}


    def __init__(self):
        pass
        #self.jsonResponse = requests.get(self.BASE_URL).json()

    def printEdges(self):
        for i in range(len(self.jsonResponse['edges'])):
            print(self.jsonResponse['edges'][i]['end']['label'])

        #  for key in ['rel','surfaceText']:
        #   print(obj['edges'][i][key])

    def printCurrJson(self):
        print(self.jsonResponse)

    def generalFoodRequest(self):
        return requests.get(self.BASE_URL+"/c/en/food").json()

    def getFoodURI(self):
        return "/c/en/food"

    def makeRequest(self, queryString):
        print(self.BASE_URL + queryString)
        jsonResponse = requests.get(self.BASE_URL + queryString).json()

        # if the id of jsonResponse isn't our queryString, our response is wrong
        if jsonResponse.get("@id") != queryString:
            print("Got the wrong response..")
            return None
        else:
            return jsonResponse

    def getQuestionFrame(self, code):
        try:
            return self.RELATE_TO_ENG.get(code)
        except TypeError:
             print("your code didn't match anything")
             return None

    def getRandomCategory(self):
        arbitraryInt = random.randint(1, 5)
        if arbitraryInt == 0:           #I took this out of the range b/c I don't think its gonna work.
            return self.RELATION_GET_TYPE
        elif arbitraryInt == 1:
            return self.RELATION_PROPERTY
        elif arbitraryInt == 2:
            return self.RELATION_USED_FOR
        elif arbitraryInt == 3:
            return self.RELATION_MADE_OF
        elif arbitraryInt == 4:
            return self.RELATION_CAN_BE
        else:
            return self.RELATION_CAPABLE

    def getAllRelations(self):
        # return [self.RELATION_GET_TYPE, self.RELATION_PROPERTY, self.RELATION_USED_FOR, self.RELATION_MADE_OF, self.RELATION_CAN_BE, self.RELATION_CAPABLE]
        return [self.RELATION_PROPERTY, self.RELATION_USED_FOR, self.RELATION_MADE_OF, self.RELATION_CAN_BE, self.RELATION_CAPABLE]

    def removeArticlesIn(self, word):
        if "the " in word:
            word = word.removeprefix("the ")
        if "a " in word:
            word = word.removeprefix("a ")
        if "an " in word:
            word = word.removeprefix("an ")

        return word
    #Purpose:      Get correct URI endpoint for the given word.
    def getURI(self, word):
        #queryString = "/uri?language=en&text="+word
        #return requests.get(self.BASE_URL + queryString).json().get("@id")
        word = self.removeArticlesIn(word)
        if word.find(' ') != -1:
            word = word.replace(' ', '_')
            print("new edgeLabel: " + word)
        return "/c/en/"+word

    def getRelatednessVal(self, startUri, endUri):
        return self.makeRequest("/relatedness?node1="+startUri+"&node2="+endUri)["value"]

    #----------Relation queries-------------------------------:

    #Purpose:     Get all possible relations between these two uris
    def getRelationTypesBw(self, uri1, uri2):
        return self.makeRequest("/query?node=" + uri1 + "&other=" + uri2)


    #Purpose:     Get all properties of this things
    def getPropertiesOf(self, startUri):
        return self.makeRequest("/query?start="+startUri+"&rel=/r/HasProperty").get("edges")
    def thingsWithPropertiesOf(self, endUri):
        return self.makeRequest("/query?end=" + endUri + "&rel=/r/HasProperty").get("edges")


    #Properties:     Get all words that are types of this uri
    def getTypesOf(self, endUri):
        return self.makeRequest("/query?end=" + endUri + "&rel=/r/IsA").get("edges")

    #Purpose:   Get the specific edge if this startUri IS a type of this endUri
    def confirmTypeOf(self, startUri, endUri):
        return self.makeRequest("/query?start=" + startUri + "&end="+endUri + "&rel=/r/IsA").get("edges")


    def getWhatMadeOf(self, startUri):
        return self.makeRequest("/query?start="+startUri+"&rel=/r/MadeOf").get("edges")
    def getThingsMadeOf(self, endUri):
        return self.makeRequest("/query?end=" + endUri + "&rel=/r/MadeOf").get("edges")

    def getLocationOf(self, startUri):
        return self.makeRequest(("/query?start="+startUri+"&rel=/r/AtLocation")).get("edges")
    def getWhatIsLocatedAt(self, endUri, limitCount):
        return requests.get(self.BASE_URL + "/query?end="+endUri+"&rel=/r/AtLocation&limit="+str(limitCount)).json().get("edges")
        #return self.makeRequest(("/query?end="+endUri+"&rel=/r/AtLocation&limit="+str(limitCount))).get("edges")


    def getCanBe(self, startUri):
        return self.makeRequest(("/query?start=" + startUri + "&rel=/r/ReceivesAction")).get("edges")
    def getThingsThatCan(self, endUri):
        return self.makeRequest(("/query?end=" + endUri + "&rel=/r/ReceivesAction")).get("edges")

    def getWhatUsedFor(self, startUri):
        return self.makeRequest(("/query?start=" + startUri + "&rel=/r/UsedFor")).get("edges")
    def thingsUsedFor(self, endUri):
        return self.makeRequest(("/query?end=" + endUri + "&rel=/r/UsedFor")).get("edges")


    def getWhatCapableOf(self, startUri):
        return self.makeRequest(("/query?start=" + startUri + "&rel=/r/CapableOf")).get("edges")
    def getThingsCapableOf(self, endUri):
        return self.makeRequest(("/query?end=" + endUri + "&rel=/r/CapableOf")).get("edges")


    #Purpose:   Returns the actual root word as a string. Just chooses the first result (highest weight) though, which may be buggy
    def getRootWord(self, startUri):
        response = self.makeRequest(("/query?start=" + startUri + "&rel=/r/FormOf")).get("edges")
        if len(response) > 0:
            return response[0]["end"]["label"]
        return None

    def getAllForms(self, startUri):
        response = self.makeRequest(("/query?start=" + startUri + "&rel=/r/FormOf")).get("edges")
        allForms = []
        for node in response:
            newForm = node["end"]["label"]
            if not(newForm in allForms):
                allForms.append(newForm)
        print(str(allForms))
        return allForms

    #Purpose:   Return whether or not the given phrase is a food
    def getIsFood(self, phrase):
        if phrase != "food":
            phraseUri = self.getURI(phrase)
            # rootWord = self.getRootWord(self.getURI(phrase))
            # if rootWord is not None:
            #     phraseUri = self.getURI(rootWord)

            # Case 1: Some words in ConceptNet don't register as "food" for some reason but do when you find the word sense_label:
            case1 = self.makeRequest(phraseUri + "/n/wn/food").get("edges")
            if len(case1) > 0:
                return True

            #Case 2: isA "food" returns an edge
            case2 = self.confirmTypeOf(phraseUri, self.getFoodURI())
            #If there is an edge & not actually the term "food", --> return true
            if len(case2) > 0 and case2[0]["start"]["label"] != "food":
                return True

            #Case 3: if the typesOf this phrase are foods
            typesOfPhrase = self.getTypesOf(phraseUri)
            counter = 1
            for node in typesOfPhrase:
                if counter < 2:         #let's say if the first 2 aren't foods, let's not bother checking the rest.
                    isAFood = self.confirmTypeOf(self.getURI(node["start"]["label"]), self.getFoodURI())

                    # If there is an edge & not actually the term "food", --> return true
                    if len(isAFood) > 0 and isAFood[0]["start"]["label"] != "food":
                        return True
                    counter = counter + 1
                else:
                    break

        #All else fails
        return False




#Interest:
#- relatedness value between pairs of terms
# - f(F)eature(s)
# - possible relations: /query?node=/c/en/dog&other=/c/en/bark
#- relations:
# #   - properties of /r/HasProperty
#     - location of   /r/AtLocation
#     - is a type of:  /r/IsA
#     - made of

# Questions:
# - breakfast food is a type of food (/query?start=/c/en/breakfast_food&end=/c/en/food&rel=/r/IsA)
#     - what are the types of breakfast foods? (bc then they must also be foods) (query?start=/c/en/breakfast_food&rel=/r/IsA)
