#!/usr/bin/env python

import random
import sys

rnd = random.Random()

def printf(format,*args): sys.stdout.write(format%args)

class Board(object):
    def __init__(self):
        self.vals = [ ['-','-','-'],['-','-','-'],['-','-','-']]

    def add_token(self, row, col, token):
        self.vals[row][col] = token

    def print_board(self):
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
                    return True
        return False

class BadMoveException(Exception):
    pass

def get_legal_moves(board):
    moves = set()
    for r in range(0,3):
        for c in range(0,3):
            if board.vals[r][c] == '-':
                moves.add((r,c))
    return moves

def ai_move(b, side):
    moves = get_legal_moves(b)
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
        printf("Human make a move> ")
        (r, c) = getcords()
        if (r, c) not in get_legal_moves(b):
            printf("Illegal move try again\n")
            continue
        b.add_token(r,c, "X")
        b.print_board()
        legal_moves = get_legal_moves(b )
        (r, c) = rnd.choice(list(legal_moves))
        printf("Computer moves to (%d, %d)\n", r, c)
        b.add_token(r,c,"O")
        b.print_board()
        if b.is_full():
            break

if __name__ == "__main__":
    main()

