#Purpose:   Encapsulate a qualifying feature/attribute needed from the final answer.
class Attribute:
    
    def __init__(self, relation, value):
        self.relation = relation
        self.value = value

    def getRelation(self):
        return self.relation

    def getValue(self):
        return self.value