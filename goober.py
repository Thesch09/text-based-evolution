import random
import math
from rich import print
class goober:
    def __init__(self, name, parent1, parent2, maxHunger, forage):
        self.name = name
        self.age = 0
        self.parent1 = parent1
        self.parent2 = parent2
        self.maxHunger = maxHunger
        self.hunger = self.maxHunger/2
        self.forage = forage
        
    def procreate(self, mate, names, goobList):
        child = names[random.randint(0,len(names))]
        print(f"{self.name} and {mate.name} have given birth to {child}")
        goobList.append(goober(child, # name of new goober (will take from long list)
                       self.name, mate.name # name of parents
                       (self.maxHunger+mate.maxHunger)/2, # The size of the stomach of the child
                       (self.forage+mate.forage)/2)) # The ability to forage of the child
        return goobList
    
    def forageFood(self):
        if self.hunger <= math.ceil(self.maxHunger/3):
            chanceFail = random.randint(1,50+math.ceil(self.hunger/self.maxHunger*10))
            if chanceFail < self.forage:
                self.hunger += 10 + self.forage

    def cycle(self):
        global goobList
        global names