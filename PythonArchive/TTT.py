


theBoard = {'7': ' ' , '8': ' ' , '9': ' ' ,
            '4': ' ' , '5': ' ' , '6': ' ' ,
            '1': ' ' , '2': ' ' , '3': ' ' }

board_keys = []

for key in theBoard:
    board_keys.append(key)


def printBoard(board):
    def empt(slot_num):
        slot_num = str(slot_num)
        if theBoard[slot_num] == ' ':
            return str(slot_num)
        else:
            return theBoard[slot_num]
    print(empt(7) + '|' + empt(8) + '|' + empt(9))
    print('- - -')
    print(empt(4) + '|' + empt(5) + '|' + empt(6))
    print('- - -')
    print(empt(1) + '|' + empt(2) + '|' + empt(3))

def checkwin():
    if theBoard['7'] == theBoard['8'] == theBoard['9'] != ' ':
        return 1
    elif theBoard['4'] == theBoard['5'] == theBoard['6'] != ' ':
        return 1 
    elif theBoard['1'] == theBoard['2'] == theBoard['3'] != ' ':
        return 1
    elif theBoard['1'] == theBoard['4'] == theBoard['7'] != ' ':
        return 1
    elif theBoard['2'] == theBoard['5'] == theBoard['8'] != ' ':
        return 1
    elif theBoard['3'] == theBoard['6'] == theBoard['9'] != ' ':
        return 1
    elif theBoard['7'] == theBoard['5'] == theBoard['3'] != ' ':
        return 1
    elif theBoard['1'] == theBoard['5'] == theBoard['9'] != ' ':
        return 1
    else:
        return 0

def game():

    turn = 'x'
    count = 0
    machine = input("Would you like to play multiplayer? (y/n)")
    if machine == "n":
        for i in range(10):
            printBoard(theBoard)

            if turn == "x":
                print("It's your turn " + turn + ". Which place would you like to move to?")
                move = -1
                while move == -1:
                    inpu = input()
                    if inpu.isnumeric():
                        if int(inpu) <= 9 and int(inpu)>=1:
                            if theBoard[inpu] != ' ':
                                print("Filled. Move to which place?")
                            else:
                                move = inpu
                                theBoard[inpu] = turn
                                count += 1
                        else:
                            print("Invalid Input, try again. (Enter number between 1 and 9.)")
                    else:
                        print("Invalid Input, try again. (Enter number between 1 and 9.)")

                #Num(move)
            else:
                print("MACHINU TURNU")
                

            if count >= 5:
                win = checkwin()
                if win == 1:
                    printBoard(theBoard)
                    if turn =="o":
                        print("O Has won the game! Congratulations!")
                    else:
                        print("X Has won the game! Cool!")

                    break

            if count == 9:
                print("\n [Game Over.] \n")                
                print("Tie")
                break

            if turn =='x':
                turn = 'o'
            else:
                turn = 'x'        
        restart = input("Do want to play Again?(y/n)")
        if restart == "y":  
            for key in board_keys:
                theBoard[key] = " "

            game()    
    else:
        for i in range(10):
            printBoard(theBoard)
            print("It's your turn " + turn + ". Which place would you like to move to?")
            move = -1
            while move == -1:
                inpu = input()
                if inpu.isnumeric():
                    if int(inpu) <= 9 and int(inpu)>=1:
                        if theBoard[inpu] == ' ':
                            theBoard[inpu] = turn
                            move = inpu
                            count += 1
                        else:
                            print("Filled. Move to which place?")

                    else:
                        print("Invalid Input, try again. (Enter number between 1 and 9.)")

                else:
                    print("Invalid Input, try again. (Enter number between 1 and 9.)")

            #Num(move)

            if count >= 5:
                win = checkwin()
                if win == 1:
                    printBoard(theBoard)
                    if turn =="o":
                        print("O Has won the game! Congratulations!")
                    else:
                        print("X Has won the game! Cool!")

                    break
                if count > 9:
                    print("\n [Game Over.] \n")                
                    print("Tie")
                    break
            if turn =='x':
                turn = 'o'
            else:
                turn = 'x'        
        restart = input("Do want to play Again?(y/n)")
        if restart == "y":  
            for key in board_keys:
                theBoard[key] = " "

            game()

game()