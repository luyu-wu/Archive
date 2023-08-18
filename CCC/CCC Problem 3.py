"""
Luyu Vankerkwijk - University of Toronto Schools

Python 3.11.1

February 15th, 2023
"""


people_interested = int(input())


days_dict = {"1":0,"2":0,"3":0,"4":0,"5":0}
for i in range(people_interested):
    days = input()
    day = "1"
    for i in days:
        if i == "Y":
            days_dict[day] += 1
        day = str(int(day)+1)


most_people = ""
highest = 0

for value in days_dict:
    if days_dict[value] > highest:
        most_people = str(value)
        highest = days_dict[value]
    elif days_dict[value]==highest:
        most_people = most_people+","+str(value)

print(most_people)