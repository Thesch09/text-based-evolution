import random
import math
from rich import print
from console import saved
class goober:
    def __init__(self, name, newId, parent1, parent1Id, parent2, parent2Id, maxHunger, forage, charm, fertility, colour):
        self.name = name
        self.id = newId
        self.age = 0
        self.parent1 = parent1
        self.parent1Id = parent1Id
        self.parent2 = parent2
        self.parent2Id = parent2Id
        self.maxHunger = maxHunger # How much food a goober can have
        self.hunger = self.maxHunger/2
        self.forage = forage # The chance of a successful forage
        self.charm = charm # The rolls a goober has to successfully procreate
        self.fertility = fertility # How many kids a goober can get, only from 1 parent
        self.colour = colour
        self.lastAct = None
        self.children = {}
        
    def procreate(self, mate, names, goobList, totalGoobers, generation):
        parentsFertility = self.fertility + mate.fertility
        if parentsFertility < 1:
            parentsFertility = 1
        else:
            parentsFertility = round(parentsFertility)
        for kids in range(parentsFertility):
            # Name and colour of the child
            child = names[random.randint(0,len(names)-1)]
            totalColour = [self.colour[0] + mate.colour[0] + random.randint(-10,10),
                            self.colour[1] + mate.colour[1] + random.randint(-10,10),
                            self.colour[2] + mate.colour[2] + random.randint(-10,10)]
            for colour in range(len(totalColour)):
                if totalColour[colour] < 0:
                    totalColour[colour] = 0
                if totalColour[colour] > 255:
                    totalColour[colour] = 255
            
            saved.print(f"[rgb({self.colour[0]},{self.colour[1]},{self.colour[2]})]{self.name}[/rgb({self.colour[0]},{self.colour[1]},{self.colour[2]})] and [rgb({mate.colour[0]},{mate.colour[1]},{mate.colour[2]})]{mate.name}[/rgb({mate.colour[0]},{mate.colour[1]},{mate.colour[2]})] have given birth to [rgb({totalColour[0]},{totalColour[1]},{totalColour[2]})]{child}[/rgb({totalColour[0]},{totalColour[1]},{totalColour[2]})]")
            # There must be a better way to do that, but it's the colour of the parent, name, remove the colour, colour of the other parent, name, remove the colour, colour of the child, name and remove the colour

            self.children.update({child:totalGoobers})
            mate.children.update({child:totalGoobers})

            # Stat totals
            totalHunger = self.maxHunger + mate.maxHunger + random.randint(-5,10)
            totalForage = self.forage + mate.forage + random.randint(-5,10)
            totalCharm = self.charm + mate.charm + random.randint(-5,5)/10
            totalFertility = self.fertility + random.randint(-5,5)/10

            totalGoobers += 1
            goobList.append(goober(child, # name of new goober (will take from long list)
                            totalGoobers + generation, # ID of the child
                            self.name, self.id, # name and id of parent 1
                            mate.name, mate.id, # name and id of parent 2
                            totalHunger/2, # The size of the stomach of the child
                            totalForage/2, # The ability to forage of the child
                            math.floor(totalCharm/2),
                            totalFertility/2,
                            totalColour
                            ))
        return goobList
    
    def forageFood(self):
        if self.hunger <= math.ceil(self.maxHunger/3):
            chanceFail = random.randint(1,50+math.ceil(self.hunger/self.maxHunger*10))
            if chanceFail < self.forage:
                self.hunger += 10 + self.forage
                self.lastAct = "eat"
                saved.print(f"[rgb({self.colour[0]},{self.colour[1]},{self.colour[2]})]{self.name}[/rgb({self.colour[0]},{self.colour[1]},{self.colour[2]})] ate some food")

    def die(self, cause):
        if cause == "hunger":
            if self.lastAct == None:
                saved.print(f"[rgb({self.colour[0]},{self.colour[1]},{self.colour[2]})]{self.name}[/rgb({self.colour[0]},{self.colour[1]},{self.colour[2]})] died of hunger")
            elif self.lastAct == "eat":
                saved.print(f"[rgb({self.colour[0]},{self.colour[1]},{self.colour[2]})]{self.name}[/rgb({self.colour[0]},{self.colour[1]},{self.colour[2]})] died of hunger, even though they just ate")
            elif self.lastAct == "procreate":
                saved.print(f"[rgb({self.colour[0]},{self.colour[1]},{self.colour[2]})]{self.name}[/rgb({self.colour[0]},{self.colour[1]},{self.colour[2]})] died of hunger, next to their newborn")
            elif self.lastAct == "rejection":
                saved.print(f"[rgb({self.colour[0]},{self.colour[1]},{self.colour[2]})]{self.name}[/rgb({self.colour[0]},{self.colour[1]},{self.colour[2]})] died of hunger, and sadness")

    def thinker(self):
        if random.randint(1,10) == 1:
            if self.lastAct == "procreate":
                return "I love my child"
            if self.lastAct == "eat":
                return "Yummy food!"
            if self.hunger < self.maxHunger/2:
                return "I'm getting kinda hungy"
            if self.hunger < self.maxHunger/4 and self.lastAct == "procreate":
                return "Times are dire. Why do I want to consume my own child?"
            if self.lastAct == "rejection":
                return "No one wanted to hang with me..."
            return ""
        else:
            return ""

    def cycle(self, goobList, names, deaths, totalGoobers, deathNote, generation):

        self.lastAct = None
        self.age += 1

        self.forageFood()
        if self.age > 2 and self.hunger >= self.maxHunger - math.ceil(self.maxHunger/4):
            for i in range(self.charm):
                otherGoober = goobList[random.randint(0,len(goobList)-1)]
                if otherGoober.age > 2 and otherGoober.hunger >= math.ceil(otherGoober.maxHunger/2):
                    if otherGoober.id != self.parent1Id and otherGoober.id != self.parent2Id and otherGoober.id != self.id:
                        goobList = self.procreate(otherGoober, names,goobList, totalGoobers, generation)
                        self.lastAct = "procrate"
                        break
            else:
                if random.randint(1,2) == 2:
                    self.lastAct = "rejection"
        
        thought = self.thinker()
        if thought != "":
            saved.print(f"[rgb({self.colour[0]},{self.colour[1]},{self.colour[2]})]{self.name}[/rgb({self.colour[0]},{self.colour[1]},{self.colour[2]})] thought: [rgb({self.colour[0]},{self.colour[1]},{self.colour[2]})]{thought}")

        self.hunger -= 5+self.fertility*10
        if self.hunger <= 0:
            deathNote.update({self:"hunger"})
        return goobList, names, deaths, totalGoobers, deathNote
        