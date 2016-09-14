class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __hash__(self):  # so I can use Point as a key in a dictionary
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def plus(self, other):
        return Point(self.x + other.x, self.y + other.y)


directions = {
    "NE": Point(1, -1),
    "E": Point(1, 0),
    "SE": Point(0, 1),
    "SW": Point(-1, 1),
    "W": Point(-1, 0),
    "NW": Point(0, -1)
}


class Move:
    def __init__(self, point, direction):
        self.point = point
        self.direction = direction

    def __str__(self):
        return "Move " + str(self.point) + " " + self.direction


class Board:
    def __init__(self, size):
        self.slots = {}
        for row in range(size):
            for col in range(size):
                if row + col < size:
                    self.slots[Point(row, col)] = True
        self.slots[Point(0, 0)] = False
        self.moves = []

    def __str__(self):
        string = "Pegs remaining: " + str(self.count())
        for move in self.moves:
            string += ", " + str(move)
        return string

    def clone(self):
        dup = Board(0)
        for slot in self.slots.keys():
            dup.slots[slot] = self.slots[slot]
        for move in self.moves:
            dup.moves.append(move)
        return dup

    def count(self):
        accum = 0
        for present in self.slots.values():
            if present:
                accum += 1
        return accum

    def possible_moves(self):
        moves = []
        for slot in self.slots.keys():
            for direction in directions.keys():
                move = Move(slot, direction)
                if self.is_move_valid(move):
                    moves.append(move)
        return moves

    def is_move_valid(self, move):
        source = move.point
        over = source.plus(directions[move.direction])
        destination = over.plus(directions[move.direction])
        return (source in self.slots) and (over in self.slots) and (destination in self.slots) and (self.slots[source]) and (self.slots[over]) and (not self.slots[destination])

    def perform_move(self, move):
        source = move.point
        over = source.plus(directions[move.direction])
        destination = over.plus(directions[move.direction])
        self.slots[source] = False
        self.slots[over] = False
        self.slots[destination] = True
        self.moves.append(move)

f = open('results.txt', 'w')
class ErikManager:
    def __init__(self):
        self.boards = [Board(5)]

    def run(self):
        while self.boards:
            self.step()

    def step(self):
        board = self.boards.pop(0)
        if board.count() == 1:
            f.write(str(board) + "\n")
        else:
            moves = board.possible_moves()
            for move in moves:
                new_board = board.clone()
                new_board.perform_move(move)
                self.boards.insert(0, new_board)


import datetime
print datetime.datetime.now()
ErikManager().run()
print datetime.datetime.now()
f.close()
