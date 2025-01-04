class Piece:

    def __init__(self, row, col, team, color = 'default'):
        self.row = row
        self.col = col
        self.team = team
        self.king = False

        self.color = color

    def make_king(self):
        self.king = True

    def move(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):#we can simply make our own representation of the object
        return str(self.team)

    def __str__(self):#we can simply make our own representation of the object
        return str(self.team)