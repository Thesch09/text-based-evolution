from rich import print
colours = [260,-5,172]
print(colours)
for colour in range(len(colours)):
    if colours[colour] < 0:
        colours[colour] = 0
    if colours[colour] > 255:
        colours[colour] = 255
print(f"[rgb({colours[0]},{colours[1]},{colours[2]})] Hello")
print(f"Ay[rgb({colours[0]},{colours[1]},{colours[2]})] {colours[0]},{colours[1]},{colours[2]}")
print(f"{colours} Hello")

egg = []
eggSum = 0
for i in egg:
    eggSum += i
print(eggSum)

try:
    worthlessNum = 1/len(egg)
    print("No error")
    eggAvg = eggSum / len(egg)
except ZeroDivisionError:
    print("Error")
    eggAvg = 0

print(eggAvg)