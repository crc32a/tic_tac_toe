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



class BadMoveException(Exception):
    pass


def ai_move(b, side):
    moves = b.get_legal_moves()
    if len(moves) <= 0:
        raise BadMoveException
    (r,c) = moves.pop()
    b.add_token(r,c, side)

def getcords():
    line = sys.stdin.readline().strip()
    return [int(ch) for ch in line.strip().split(" ") if len(ch) > 0]

def main():
    b = Board()

    while True:
        if b.is_full():
            printf("Board full\n")
            break
        printf("Human make a move> ")
        (r, c) = getcords()
        if (r, c) not in b.get_legal_moves():
            printf("Illegal move try again\n")
            continue
        b.add_token(r,c, "X")
        b.display()
        if b.is_full():
            printf("Board full\n")
            break
        legal_moves = b.get_legal_moves()
        (r, c) = rnd.choice(list(legal_moves))
        printf("Computer moves to (%d, %d)\n", r, c)
        b.add_token(r,c,"O")
        b.display()

if __name__ == "__main__":
    main()

