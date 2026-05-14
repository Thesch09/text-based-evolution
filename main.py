import random
import math
from rich import print

import os
import datetime
from console import console, saved
from goober import goober

sessionStartTime = datetime.datetime.now()
print(sessionStartTime)

running = True
generation = 0
deaths = 0
totalGoobers = 0
avgForage = 0
avgMaxHunger = 0
avgCharm = 0
avgFertility = 0
avgColour = [0,0,0]

names = ["John", "Sprunkle", "Spey", "Spob", "Goobwilliams", "Jane", "Jeff", "Carl", "Karl", "Qarl", "Jeremiah", "Goobelle", "Goobsworth", "Kasper", "Elias", "Leon", "Filip", "Jan", "Theodor", "Goobthaniel", "Gerry Man Dering", "Berry", deaths, "Todd"]
goobList = []
for i in range(10): # The original Gooberwalkers
    goobList.append(goober(names[random.randint(0,len(names)-1)], # name of new goober
                    len(goobList),
                    None, i*-1,
                    None, i*-1, # name and id of parent 2
                    random.randint(70,100), # The size of the stomach of the new goob
                    random.randint(20,50), # The ability to forage of the child
                    random.randint(2,4),
                    random.randint(30,50)/100,
                    [random.randint(200,255),random.randint(200,255),random.randint(200,255)]
                    )) 
    
    totalGoobers += 1
    avgForage += goobList[-1].forage
    avgMaxHunger += goobList[-1].maxHunger
    avgCharm += goobList[-1].charm
    avgFertility += goobList[-1].fertility
    for i in range(len(avgColour)):
        avgColour[i] += goobList[-1].colour[i]
avgForage /= len(goobList)
avgMaxHunger /= len(goobList)
avgCharm /= len(goobList)
avgFertility /= len(goobList)
for i in range(len(avgColour)):
    avgColour[i] /= len(goobList)

def askInput(generation):
    console.print(f"Current Generation: {generation}\n")
    print("Type FORWARD to continue to next generation")
    print("Type STATS for statistics")
    print("Type GOOBERS for goobers")
    print("Type NAMES to add new names")
    print("Type INSPECT to inspect a goober")
    print("Type EXIT to exit")
    console.print("If something says \"...\" press ENTER")
    print("\nInput: ", end="")

def newGeneration():
    global generation
    global goobList
    global avgForage
    global avgCharm
    global avgFertility
    global avgMaxHunger
    global avgColour
    global deaths
    global totalGoobers
    global names

    generation += 1
    saved.print(f"Next Generation: {generation}")
    saved.print(f"Goobers at start of Generation: {len(goobList)}")
    print("")

    prevGoobers = len(goobList)

    # Averages
    avgForage = 0
    avgMaxHunger = 0
    avgCharm = 0
    avgFertility = 0
    avgColour = [0,0,0]

    deathNote = {}
    for goob in goobList:
        goobList, names, deaths, totalGoobers, deathNote = goob.cycle(goobList, names, deaths, totalGoobers, deathNote, generation)

        #Averages
        avgForage += goob.forage
        avgMaxHunger += goob.maxHunger
        avgCharm += goob.charm
        avgFertility += goob.fertility
        for i in range(len(avgColour)):
            avgColour[i] += goob.colour[i]
    
    # Make the averages average
    try:
        worthlessNum = 1 / len(goobList) # If this fails then the length of goobList is 0

        avgForage /= len(goobList)
        avgMaxHunger /= len(goobList)
        avgCharm /= len(goobList)
        avgFertility /= len(goobList)
        avgColour[0] /= len(goobList)
        avgColour[1] /= len(goobList)
        avgColour[2] /= len(goobList)
    except ZeroDivisionError:
        avgForage = 0
        avgMaxHunger = 0
        avgCharm = 0
        avgFertility = 0
        avgColour[0] = 0
        avgColour[1] = 0
        avgColour[2] = 0
    
    # The goobers that died
    if len(deathNote) != 0:
        saved.print("The dead")
        for entry in deathNote:
            entry.die(deathNote[entry])
            goobList.remove(entry)
            deaths += 1
    
    differenceInGoobers = prevGoobers-len(goobList)
    if differenceInGoobers == 0:
        print("[bold]Era of stillness")
    elif differenceInGoobers == prevGoobers*-1:
        print("[red][bold]CATACLYSM")
    elif differenceInGoobers < prevGoobers/10 or differenceInGoobers > prevGoobers/10*-1:
        print("[bold]Era of little change")
    input("...")

def nameQuery():
    global names
    print("Would you like to SEE the current names, REMOVE a name or ADD a new name?")
    prompt = input("").lower().strip()
    if prompt == "see" or prompt == "s":
        for name in names:
            input(name)
    elif prompt == "remove" or prompt == "r":
        print("Which name do you want to remove? Needs proper capitilization")
        prompt = input("Remove: ")
        try:
            names.remove(prompt)
        except ValueError:
            print(f"{prompt} is already not a name")
    elif prompt == "add" or prompt == "a":
        print("Which name do you want to add?")
        print("TIP: Having multiple of the same name increases the chance of a goober getting it")
        names.append(input("Add: "))
    input("...")

def inspectGoober(goob):
    print(f"Name: [rgb({goob.colour[0]},{goob.colour[1]},{goob.colour[2]})]{goob.name}")
    print(f"Colour: [rgb({goob.colour[0]},{goob.colour[1]},{goob.colour[2]})]{goob.colour[0]},{goob.colour[1]},{goob.colour[2]}")
    console.print(f"Age: {goob.age}")
    console.print(f"ID: {goob.id}")
    input("...")
    console.print(f"Parent 1: {goob.parent1}, ID {goob.parent1Id}")
    console.print(f"Parent 2: {goob.parent2}, ID {goob.parent2Id}")
    if len(goob.children) == 0:
        print("This Goober has no kids")
    else:
        i = 1
        input("...")
        for child in goob.children:
            console.print(f"Child {i}: {child}, ID {goob.children[child]}")
            i += 1
    input("...")
    console.print(f"Hunger/Max Hunger: {goob.hunger}/{goob.maxHunger}")
    console.print(f"Forage skill: {goob.forage}")
    console.print(f"Charm: {goob.charm}")
    console.print(f"Fertility: {goob.fertility}")
    input("...")

def inspect(searchedGoobers):
    for goob in searchedGoobers:
        console.print(f"[rgb({goob.colour[0]},{goob.colour[1]},{goob.colour[2]})]{goob.name}[/rgb({goob.colour[0]},{goob.colour[1]},{goob.colour[2]})], ID {goob.id}")
    print("Which goob will you inspect? Press ENTER to return")
    prompt = input("ID: ")
    if prompt == "":
        return "break"
    try:
        prompt = int(prompt)
    except TypeError:
        console.print(f"{prompt} is not a whole number")
        return
    selectedGoob = None
    for goob in searchedGoobers:
        if goob.id == prompt:
            selectedGoob = goob
            break
    if selectedGoob == None:
        print("No Goober found with that ID")
        input("...")
    else:
        inspectGoober(selectedGoob)

def optionInspect(goobers):
    print("Select a Goober. Press ENTER to return")
    prompt = input()
    if prompt != "":
        searchedGoobers = []
        for goob in goobers:
            if goob.name == prompt:
                searchedGoobers.append(goob)
        if len(searchedGoobers) == 0:
            print(f"No living Goobers found named {prompt}...")
            input("...")
        else:
            console.print(f"{len(searchedGoobers)} Goobers named {prompt}")
            while True:
                if inspect(searchedGoobers) == "break":
                    break

while running:
    askInput(generation)
    prompt = input("").lower().strip()

    if prompt == "forward" or prompt == "f":
        years = input("How many generations? ")
        
        try:
            years = abs(int(years))
        except TypeError:
            years = 1
        except ValueError:
            years = 1
        console.print(f"Going forwards {years} generations")
        for i in range(years):
            newGeneration()
    elif prompt == "stats" or prompt == "s":
        print("--Goobers--")
        console.print(f"Goobers: {len(goobList)}")
        console.print(f"Total Goobers: {totalGoobers}")
        console.print(f"Total Deaths: {deaths}")
        input("...")
        console.print("--Colours--")
        console.print(f"Red: [rgb({round(avgColour[0])},0,0)]{avgColour[0]}")
        console.print(f"Green: [rgb(0,{round(avgColour[1])},0)]{avgColour[1]}")
        console.print(f"Blue: [rgb(0,0,{round(avgColour[2])})]{avgColour[2]}")
        print(f"Average: [rgb({round(avgColour[0])},{round(avgColour[1])},{round(avgColour[2])})]{avgColour[0]}, {avgColour[1]}, {avgColour[2]}")
        input("...")
        print("--Stats--")
        console.print(f"Average Forage Skill: {avgForage}")
        console.print(f"Average Max Hunger: {avgMaxHunger}")
        console.print(f"Average Charm: {avgCharm}")
        console.print(f"Average Fertility: {avgFertility}")
        input("...")
    elif prompt == "goobers" or prompt == "g":
        if len(goobList) > 100:
            lengthOfList = 100
        else:
            lengthOfList = len(goobList)
        print(f"Top {lengthOfList} Goobers")
        for i in range(lengthOfList):
            console.print(f"[rgb({goobList[i].colour[0]},{goobList[i].colour[1]},{goobList[i].colour[2]})]{goobList[i].name}[/rgb({goobList[i].colour[0]},{goobList[i].colour[1]},{goobList[i].colour[2]})], age {goobList[i].age}")
        input("...")
    elif prompt == "names" or prompt == "n":
        nameQuery()
    elif prompt == "inspect" or prompt == "i":
        optionInspect(goobList)
    elif prompt == "exit":
        print("Goodbye!")
        with open(f"logs/Goobers {sessionStartTime.strftime("%H-%M %d-%m-%Y")}.txt", "x") as log:
            log.write(saved.export_text())
        running = False