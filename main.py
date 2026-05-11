import random
import math
from rich import print

running = True
generation = 0
deaths = 0
goobers = 0
totalGoobers = 0
avgForage = 0

def askInput(generation):
    print(f"Current Generation: {generation}\n")
    print("Type FORWARD to continue to next generation")
    print("Type STATS for statistics")
    print("If something says \"...\", press ENTER")
    print("\nInput: ", end="")


while running:
    askInput(generation)
    prompt = input("").lower().strip()

    if prompt == "forward":
        generation += 1
        print(f"Next Generation: {generation}")
        input("...")
    elif prompt == "stats":
        print("--Goobers--")
        print(f"Goobers: {goobers}")
        print(f"Total Goobers: {goobers}")
        print(f"Total Deaths: {deaths}")
        input("...")
        print("--Stats--")
        print(f"Average Forage Skill: {avgForage}")
        input("...")