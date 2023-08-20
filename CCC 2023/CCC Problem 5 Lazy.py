"""
Luyu Vankerkwijk - University of Toronto Schools

Python 3.11.1

February 15th, 2023
"""


map = []


word = input()
word_r = ""
for i in range(len(word)):
    word_r = word_r+word[len(word)-1-i]

rows = int(input())

columns = int(input())


for i in range(rows):
    list = []
    for i in input():
        if not i.isspace():
            list.append(i)
    map.append(list)

matches = 0

# Horizontal Word Search

# Correct Word search
for i in map:
    letter_matches = 0

    for letter in i:
        if letter == word[letter_matches]:
            letter_matches += 1
            if letter_matches == len(word):
                matches+=1
                letter_matches = 0


# Reversed Word Search
for i in map:
    letter_matches = 0

    for letter in i:
        if letter == word_r[letter_matches]:
            letter_matches += 1
            if letter_matches == len(word):
                matches+=1
                letter_matches = 0


# Vertical Searches

# Make Map Vertical
map_v = []
for i in range(columns):
    column_list = []
    for v in map:
        column_list.append(v[i])
    map_v.append(column_list)

# Normal Search
for i in map_v:
    letter_matches = 0

    for letter in i:
        if letter == word[letter_matches]:
            letter_matches += 1
            if letter_matches == len(word):
                matches+=1
                letter_matches = 0

# Reversed Word Search
for i in map_v:
    letter_matches = 0

    for letter in i:
        if letter == word_r[letter_matches]:
            letter_matches += 1
            if letter_matches == len(word):
                matches+=1
                letter_matches = 0




# Diagonal
"""
Only search diagonal downwards in both directions

Go through rows, if less rows below and including itself cancel search of row.

ROW_NUMBER is the starting verticle position of the search

COL_NUMBER is the starting horizontal position of the search.
"""
highest_col_ind = columns-1


def GreedyCheck(row,col,letter,direction,word_here,has_switched): # Row and Col is the location of the previous box checked.
    looking_for = word_here[letter]
    global matches
    lastletter = letter == len(word_here)-1

    if not has_switched or direction == -1: # Check the lower left
        if col-1>=0:
            if map[row+1][col-1] == looking_for:

                if has_switched and direction != -1:
                    has_switched = True
                    direction = -1


                if lastletter:
                    matches += 1
                else:
                    GreedyCheck(row+1,col+1,letter+1,has_switched=has_switched,word_here=word_here,direction=direction)
    if not has_switched or direction == 1: # Check the lower right
        if col+1<=highest_col_ind:
            if map[row+1][col+1] == looking_for:
                if has_switched and direction != 1:
                    has_switched = True
                    direction = 1
                if lastletter:
                    matches += 1
                else:
                    GreedyCheck(row+1,col+1,letter+1,has_switched=has_switched,word_here=word_here,direction=direction)


for row_number in range(rows):
    if rows-row_number >= len(word): # If there aren't enough rows below it dont even bother.
        col_number = 0

        for i in map[row_number]:
            if i == word[0]:
                GreedyCheck(row_number,col_number,1,0,word,False)
            if i == word_r[0]:
                GreedyCheck(row_number,col_number,1,0,word_r,False)


            col_number+=1
                    
                

print(matches)
