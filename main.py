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


def askInput(generation):
    print(f"Current Generation: {generation}\n")
    print("Type FORWARD to continue to next generation")
    print("Type STATS for statistics")
    print("Type GOOBERS for goobers")
    print("If something says \"...\" press ENTER")
    print("\nInput: ", end="")


while running:
    askInput(generation)
    prompt = input("").lower().strip()

    if prompt == "forward" or prompt == "f":
        generation += 1
        print(f"Next Generation: {generation}")
        prevGoobers = len(goobList)
        for goob in goobList:
            goobList, names, deaths = goob.cycle(goobList, names, deaths)
        differenceInGoobers = prevGoobers-len(goobList)
        if differenceInGoobers == 0:
            print("[bold]Era of stillness")
        elif differenceInGoobers == prevGoobers*-1:
            print("[red][bold]CATACLYSM")
        elif differenceInGoobers < prevGoobers/10 or differenceInGoobers > prevGoobers/10*-1:
            print("[bold]Era of little change")
        input("...")
    elif prompt == "stats" or prompt == "s":
        print("--Goobers--")
        print(f"Goobers: {len(goobList)}")
        print(f"Total Goobers: {len(goobList)}")
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
            