
#Purpose:       Encapsulate a possible answer into an object, defining what qualifying Attributes it has and possibility of being chosen as a final answer.
class Answer:
    DEFAULT_PROBABILITY = 0.3
    PROBABILITY_STEP = 0.05

    def __init__(self, attribute, label):
        if attribute is not None:
            self.allAttributes = [attribute]
        else:
            self.allAttributes = []
        self.probability = self.DEFAULT_PROBABILITY
        self.label = label

    def addAttribute(self, newAttribute):
        self.allAttributes.append(newAttribute)

    def addProbability(self):
        self.probability = self.probability + self.PROBABILITY_STEP

    def subProbability(self):
        self.probability = self.probability - self.PROBABILITY_STEP

    #getters:
    def getAllAttributes(self):
        return self.allAttributes

    def getProbability(self):
        return self.probability

    def getLabel(self):
        return self.label