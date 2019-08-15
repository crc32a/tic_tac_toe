#!/usr/bin/env python

import random
import sys

rnd = random.Random()

def printf(format,*args): sys.stdout.write(format%args)

class Board(object):
    def __init__(self, vals=None):
        if not vals:
            self.vals = [ ['-','-','-'],['-','-','-'],['-','-','-']]
        else:
            self.vals = [ [vals[0],vals[1],vals[2]],
                          [vals[3],vals[4],vals[5]],
                          [vals[6],vals[7],vals[8]]]

    def add_token(self, row, col, token):
        self.vals[row][col] = token

    def display(self):
        v = self.vals
        printf("\n")
        printf("%s|%s|%s\n", v[0][0],v[0][1],v[0][2])
        printf("%s|%s|%s\n", v[1][0],v[1][1],v[1][2])
        printf("%s|%s|%s\n", v[2][0],v[2][1],v[2][2])
        printf("\n")

    def is_full(self):
        for r in range(0,3):
            for c in range(0,3):
                if self.vals[r][c] == '-':
                    return False
        return True

    def get_legal_moves(self):
        moves = set()
        for r in range(0,3):
            for c in range(0,3):
                if self.vals[r][c] == '-':
                    moves.add((r,c))
        return moves

    def can_win(self, r, c, player):
        #Can this player win up/down
        r_set = {0, 1, 2}
        r_set.remove(r) # Since we know where in this spot alreasdy
        v1 = self.vals[r_set.pop()][c]
        v2 = self.vals[r_set.pop()][c]
        if v1 == player and v2 == player:
            return True

        #can this player win left/right
        c_set = {0, 1, 2}
        c_set.remove(c) # Since we know where in this spot alreasdy
        v1 = self.vals[r][c_set.pop()]
        v2 = self.vals[r][c_set.pop()]
        if v1 == player and v2 == player:
            return True

        # Can this player win diagnally down right
        down_right = { (0,0),(1,1),(2,2) }
        if (r,c) in down_right:
            # This is on a diagnal so lets try it
            down_right.remove( (r,c) )
            (ri, ci) = down_right.pop()
            v1 = self.vals[ri][ci]
            (ri, ci) = down_right.pop()
            v2 = self.vals[ri][ci]
            if v1 == player and v2 == player:
                return True

        # Can this player win diagnally up right
        up_right = { (2,0), (1,1), (0,2) }
        if (r,c) in up_right:
            # This is on a diagnal so lets try it
            up_right.remove( (r,c) )
            (ri, ci) = up_right.pop()
            v1 = self.vals[ri][ci]
            (ri, ci) = up_right.pop()
            v2 = self.vals[ri][ci]
            if v1 == player and v2 == player:
                return True
        return False

    # This winner detector is nieve in that multiple people can win if
    # you give it a bord like for example:
    #
    # X| |O
    # X| |O
    # X| |O
    # Also instead of rewriting a variabht of can_win I just call
    # can win 9 times and list the winners. I'll optimize it later if I'm
    # bored
    def who_won(self):
        winners = set()
        for r in range(0, 3):
            for c in range(0, 3):
                player = self.vals[r][c]
                if player == "-":
                    continue
                if self.can_win(r,c,player):
                    winners.add(player)
        return winners

class BadMoveException(Exception):
    pass

def ai_move(b, ai,human):
    # Get list of legal moves
    legal_moves = b.get_legal_moves()
    
    # If no more moves then raise BadMoveException
    if len(legal_moves) <= 0:
        raise BadMoveException

    # Check if AI can win next move and win
    for (r, c) in legal_moves:
        if b.can_win(r, c, ai):
            b.add_token(r, c, ai)  # AI wins
            return (r, c)

    # Otherwise block the human player if they can win next move
    for (r, c) in legal_moves:
        if b.can_win(r, c, human):
            b.add_token(r, c, ai) #Blocked
            return (r, c)
    # Otherwise move at random
    (r, c) = rnd.choice(list(legal_moves))
    b.add_token(r, c, ai)
    return (r, c)

def getcords():
    line = sys.stdin.readline().strip()
    return [int(ch) for ch in line.strip().split(" ") if len(ch) > 0]

def play():
    b = Board()
    human = "X"
    ai = "O"
    b.display()
    printf("You can move by typing in grid cordinates for examle:\n")
    printf("0 0 or 1 1 then pressing enter\n")
    while True:
        if b.is_full():
            printf("Board full\n")
            break
        printf("Human make a move (r,c)> ")
        sys.stdout.flush()
        (r, c) = getcords()
        if (r, c) not in b.get_legal_moves():
            printf("Illegal move try again\n")
            continue
        b.add_token(r, c, human)
        b.display()
        if b.who_won():
            break
        if b.is_full():
            printf("Board full\n")
            break
        (r, c) = ai_move(b, ai, human)
        printf("Computer moves to (%d, %d)\n", r, c)
        b.display()
        if b.who_won():
            break
    if b.who_won():
        winner = b.who_won().pop()
        printf("Winner winner winner = %s\n", winner)

if __name__ == "__main__":
    play()
