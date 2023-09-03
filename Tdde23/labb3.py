import math

board = {
    (200,200) : 'player1',
    (300,100) : 'player1',
}

def is_free(board, x, y):
    if (x,y) in board:
        return False
    else:
        return True

def place_piece(board, x, y, player):
    if is_free(board, x, y) == False:
        print('there is already a piece on that place')
        return False
    else:
        boardCopy = {**board, (x,y) : player}
        board.update(boardCopy)
        print('You have placed ' + player + ' on place x=' + str(x) + ' and y=' + str(y))
    return True

def get_piece(board, x, y):
    if is_free(board, x, y):
        return False
    player = board[(x,y)]
    print(player)
    return player

def remove_piece(board, x, y):
    player_removed = board.pop((x,y), None)
    if (player_removed != None):
        print(player_removed + ' where removed from place x=' + str(x) + ' and y=' + str(y))
        return True
    else:
        print('player not found on that position')
        return False

def move_piece(board, x, y, newX, newY):
    if is_free(board, x, y) == False:
        board[(newX,newY)] = board[(x,y)]
        board.pop((x,y), None)
        print('player was successfully moved to ' + str(newX) + ' and ' + str(newY))
        return True
    else:
        print('there are no players on these coordinates please try again')
        return False

def count(board, row, num, player):
    keyList = []
    col = 0
    total = 0

    print(board)

    if row != 'column':
        col = 1

    for key, value in board.items():
        if player == value:
            keyList.append(key)
    
    for i in keyList:
        if i[col] == num:
            total += 1
    print('the total number of players found on this ' + row + ' was ' + str(total))
    return total

def nearest_piece(board, x, y):
    keyList = list(board.keys())
    lengthList = []
    if len(board) == 0:
        print('board is empty')
        return False
    for i in keyList:
        z = (i[0] - x)**2 + (i[1] - y)**2
        totLength = math.sqrt(z)
        lengthList.append(totLength)
    itBeg = lengthList[0]
    index = 0
    for idx, num in enumerate(lengthList):
        if (itBeg > num):
            itBeg = num
            index = idx
    closest = keyList[index]
    print('the closest positioned player is positioned at ' + str(closest[0]) + ' and ' + str(closest[1]))
    return closest
# print(is_free(board, 500, 100))
# place_piece(board, 500, 100, "spelare1")
# place_piece(board, 500, 100, "spelare2")
# place_piece(board, 1, 100, "spelare2")
# place_piece(board, 500, 200, "spelare2")
# print(is_free(board, 500, 100))
# get_piece(board, 500, 100)
# get_piece(board, 666,666)
# remove_piece(board, 500, 100)
# remove_piece(board, 1, 1)
# print(is_free(board, 500, 100))
# move_piece(board,  500, 200, 500, 100)
# get_piece(board, 500, 100)
# count(board, "column", 500, "spelare2")
# count(board, "row", 100, "spelare2")
# nearest_piece(board, 500, 105)