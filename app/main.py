class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        if start[0] == end[0]:
            row = start[0]
            start_col, end_col = sorted([start[1], end[1]])
            for column in range(start_col, end_col + 1):
                self.decks.append(Deck(row, column))
        else:
            col = start[1]
            start_row, end_row = sorted([start[0], end[0]])
            for row in range(start_row, end_row + 1):
                self.decks.append(Deck(row, col))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True
                return "Sunk!"
            else:
                return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships: tuple) -> None:
        self.corabels = []
        for ship in ships:
            self.corabels.append(Ship(ship[0], ship[1], True))
        self.fields = {}
        for ship in self.corabels:
            for deck in ship.decks:
                self.fields[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.fields:
            ship = self.fields[location]
            result = ship.fire(location[0], location[1])
            return result
        else:
            return "Miss!"
