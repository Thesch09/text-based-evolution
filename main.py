import random
import math
from rich import print
from goober import goober

running = True
generation = 0
deaths = 0
totalGoobers = 0
avgForage = 0

names = ["John", "Sprunkle", "Spey", "Spob", "Goobwilliams", "Jane", "Jeff", "Carl", "Karl", "Qarl", "Jeremiah"]
goobList = []
for i in range(10): # The original Gooberwalkers
    goobList.append(goober(names[random.randint(0,len(names)-1)], # name of new goober
                    len(goobList),
                    None, i*-1,
                    None, i*-1, # name and id of parent 2
                    random.randint(70,100), # The size of the stomach of the new goob
                    random.randint(20,50))) # The ability to forage of the child
    totalGoobers += 1


def askInput(generation):
    print(f"Current Generation: {generation}\n")
    print("Type FORWARD to continue to next generation")
    print("Type STATS for statistics")
    print("Type GOOBERS for goobers")
    print("Type NAMES to add new names")
    print("Type INSPECT to inspect a goober")
    print("If something says \"...\" press ENTER")
    print("\nInput: ", end="")

def newGeneration():
    global generation
    global goobList
    global avgForage
    global deaths
    global totalGoobers
    global names
    generation += 1
    print(f"Next Generation: {generation}")
    print(f"Goobers at start of Generation: {len(goobList)}")
    prevGoobers = len(goobList)
    avgForage = 0
    for goob in goobList:
        goobList, names, deaths, totalGoobers = goob.cycle(goobList, names, deaths, totalGoobers)
        avgForage += goob.forage
    try:
        avgForage = avgForage/len(goobList)
    except ZeroDivisionError:
        avgForage = 0
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

while running:
    askInput(generation)
    prompt = input("").lower().strip()

    if prompt == "forward" or prompt == "f":
        newGeneration()
    elif prompt == "stats" or prompt == "s":
        print("--Goobers--")
        print(f"Goobers: {len(goobList)}")
        print(f"Total Goobers: {totalGoobers}")
        print(f"Total Deaths: {deaths}")
        input("...")
        print("--Stats--")
        print(f"Average Forage Skill: {avgForage}")
        input("...")
    elif prompt == "goobers" or prompt == "g":
        if len(goobList) > 100:
            lengthOfList = 100
        else:
            lengthOfList = len(goobList)
        print(f"Top {lengthOfList} Goobers")
        for i in range(lengthOfList):
            print(f"{goobList[i].name}, age {goobList[i].age}")
        input("...")
    elif prompt == "names" or prompt == "n":
        nameQuery()
    elif prompt == "inspect" or prompt == "i":
        print("Select a Goober. Press ENTER to return")
        prompt = input()
        if prompt != "":
            searchedGoobers = []
            for goob in goobList:
                if goob.name == prompt:
                    searchedGoobers.append(goob)
            if len(searchedGoobers) == 0:
                print("No living Goobers found with this name...")
                input("...")
            else:
                print(f"{len(searchedGoobers)} Goobers named {prompt}")
                for goob in searchedGoobers:
                    print(f"{goob.name}, ID {goob.id}")
                print("Which goob will you inspect?")
                try:
                    prompt = int(input("ID: "))
                except TypeError:
                    print(f"{prompt} is not a whole number")
                    break
                selectedGoob = None
                for goob in searchedGoobers:
                    if goob.id == prompt:
                        selectedGoob = goob
                        break
                if selectedGoob == None:
                    print("No Goober found with that ID")
                    input("...")
                else:
                    print(f"Name: {selectedGoob.name}")
                    print(f"Age: {selectedGoob.age}")
                    print(f"ID: {selectedGoob.id}")
                    input("...")
                    print(f"Parent 1: {selectedGoob.parent1}, ID {selectedGoob.parent1Id}")
                    print(f"Parent 2: {selectedGoob.parent2}, ID {selectedGoob.parent2Id}")
                    if len(goob.children) == 0:
                        print("This Goober has no kids")
                    else:
                        i = 1
                        for child in goob.children:
                            print(f"Child {i}: {child}, {child.}")
                            i += 1
                    
                    input("...")
