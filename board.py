from random import random, sample


class Board(object):

    def __init__(self):
        figures = []

        colors = ['black', 'white']
        rows = [0, 7]

        for c in range(2):
            for i in range(8):
                figures.append({"name": 'pawn', "text": '♟' if c == 1 else '♙', "color": colors[c], "row": 1 if c == 0 else 6, "col": i})

                figures += [
                    {"name": 'rook', "text": '♜' if c == 1 else '♖', "color": colors[c], "row": rows[c], "col": 0},
                    {"name": 'knight', "text": '♞' if c == 1 else '♘', "color": colors[c], "row": rows[c], "col": 1},
                    {"name": 'bishop', "text": '♝' if c == 1 else '♗', "color": colors[c], "row": rows[c], "col": 2},
                    {"name": 'rook', "text": '♜' if c == 1 else '♖', "color": colors[c], "row": rows[c], "col": 7},
                    {"name": 'knight', "text": '♞' if c == 1 else '♘', "color": colors[c], "row": rows[c], "col": 6},
                    {"name": 'bishop', "text": '♝' if c == 1 else '♗', "color": colors[c], "row": rows[c], "col": 5},
                    {"name": 'king', "text": '♚' if c == 1 else '♔', "color": colors[c], "row": rows[c], "col": 3},
                    {"name": 'queen', "text": '♛' if c == 1 else '♕', "color": colors[c], "row": rows[c], "col": 4},
                ]

        def find_figure(i, j):
            try:
                return [f for f in figures if f["row"] == i and f["col"] == j][0]
            except IndexError:
                return None

        self.board = [[find_figure(i, j) for j in range(8)] for i in range(8)]

    def turn(self, votes):
        m = max(votes.values())
        turns = [k for k, v in votes.items() if v == m]
        turn = sample(turns, 1)[0]
        self.board[int(turn[4]) - 1][ord(turn[3]) - ord('a')] = self.board[int(turn[1]) - 1][ord(turn[0]) - ord('a')]
        self.board[int(turn[1]) - 1][ord(turn[0]) - ord('a')] = None

    def __str__(self):
        return "\n" + "-"*17 + "\n" + ("\n" + "-"*17 + "\n").join(["|" + "|".join([col["text"] if col else " " for col in row]) + "|" for row in self.board]) + "\n" + "-"*17 + "\n"
