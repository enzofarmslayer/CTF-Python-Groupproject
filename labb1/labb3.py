board = {
    (300,200):'player1'
}

def is_free(board, x, y):
    if (x,y) in board:
        return True
    else:
        return False

def place_piece(board, player, x, y):
    if is_free(board, x, y) == True:
        print('there is already a piece on that place')
        return
    else:
        boardCopy = {**board, (x,y) : player}
        board.update(boardCopy)
        print('You have placed ' + player + ' on place x= ' + str(x) + ' and y= ' + str(y))
    return

def get_piece(board, x, y):
    player = board[(x,y)]
    print(player)
    return player

def remove_piece(board, x, y):
    return

def move_piece(board, x, y):
    return

def count(board, x, y):
    return

def nearest_piece(board, x, y):
    return
place_piece(board, 'spelare1', 100, 200)
get_piece(board, 300, 200)
print(board)