"""
Luyu Vankerkwijk - University of Toronto Schools

Python 3.11.1

February 15th, 2023
"""

rows = int(input())

Map = [
    [],
    []
]



map_1 = input()
map_2 = input()
for i in map_1:
    if not i.isspace():
        i = int(i)
        Map[0].append(i)

for i in map_2:
    if not i.isspace():
        i = int(i)
        Map[1].append(i)



tape = 0

index = 0 
for i in Map[0]:
    if i == 1:
        tape_needed = 3
        if Map[1][index] == 1 and index%2 == 0:
            tape_needed -= 1
        if index != 0:
            if Map[0][index-1] == 1:
                tape_needed -= 1
        if index != len(Map[0])-1:
            if Map[0][index+1] == 1:
                tape_needed -=1
        #print(tape_needed,"1",index)
        tape += tape_needed

    index+= 1

index = 0
for i in Map[1]:
    if i == 1:
        tape_needed = 3
        if Map[0][index] == 1 and index%2 == 0:
            tape_needed -= 1
        if index != 0:
            if Map[1][index-1] == 1:
                tape_needed -= 1
        if index != len(Map[1])-1:
            if Map[1][index+1] == 1:
                tape_needed -=1
        tape += tape_needed
        #print(tape_needed,"2",index)
    index+= 1

print(tape)