import random
import math
from rich import print
class goober:
    def __init__(self, name, newId, parent1, parent1Id, parent2, parent2Id, maxHunger, forage):
        self.name = name
        self.id = newId
        self.age = 0
        self.parent1 = parent1
        self.parent1Id = parent1Id
        self.parent2 = parent2
        self.parent2Id = parent2Id
        self.maxHunger = maxHunger
        self.hunger = self.maxHunger/2
        self.forage = forage
        self.lastAct = None
        
    def procreate(self, mate, names, goobList):
        child = names[random.randint(0,len(names))]
        print(f"{self.name} and {mate.name} have given birth to {child}")
        totalHunger = self.maxHunger + mate.maxHunger
        totalForage = self.forage + mate.forage
        goobList.append(goober(child, # name of new goober (will take from long list)
                        len(goobList),
                        self.name, self.id, # name and id of parent 1
                        mate.id, mate.name, # name and id of parent 2
                        totalHunger/2, # The size of the stomach of the child
                        totalForage/2)) # The ability to forage of the child
        return goobList
    
    def forageFood(self):
        if self.hunger <= math.ceil(self.maxHunger/3):
            chanceFail = random.randint(1,50+math.ceil(self.hunger/self.maxHunger*10))
            if chanceFail < self.forage:
                self.hunger += 10 + self.forage
                self.lastAct = "eat"

    def die(self, cause):
        if cause == "hunger":
            if self.lastAct == None:
                print(f"{self.name} died of hunger")
            elif self.lastAct == "eat":
                print(f"{self.name} died of hunger, even though they just ate")
            elif self.lastAct == "procreate":
                print(f"{self.name} died of hunger, next to their newborn")

    def cycle(self, goobList, names, deaths):

        self.lastAct = None
        self.age += 1

        self.forageFood()
        if self.age > 2 and self.hunger >= self.maxHunger - math.ceil(self.maxHunger/4):
            for i in range(3):
                otherGoober = goobList[random.randint(0,len(goobList)-1)]
                if otherGoober.age > 2 and otherGoober.hunger >= math.ceil(otherGoober.maxHunger/2):
                    if otherGoober.id != self.parent1Id and otherGoober.id != self.parent2Id and otherGoober.id != self.id:
                        goobList = self.procreate(otherGoober, names,goobList)
                        self.lastAct = "procrate"
                        break
        
        self.hunger -= 5+self.forage/2
        if self.hunger <= 0:
            self.die("hunger")
            goobList.remove(self)
            deaths += 1
        return goobList, names, deaths
        