"""
Luyu Vankerkwijk - University of Toronto Schools

Python 3.11.1

February 15th, 2023
"""

peppers_dict = {"Poblano":1500,"Mirasol":6000,"Serrano":15500,"Cayenne":40000,"Thai":75000,"Habanero":125000}

amountofpeppers = int(input())

peppers = []
for i in range(amountofpeppers):
    peppers.append(input())

spice = 0

for i in peppers:
    spice+= peppers_dict[i]

print(spice)