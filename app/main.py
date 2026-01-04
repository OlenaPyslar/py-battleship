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
        self.ships = [Ship(ship[0], ship[1]) for ship in ships]

        self.fields = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.fields[(deck.row, deck.column)] = ship

        self._validate_field()

    def print_field(self) -> None:
        for row in range(10):
            row_str = ""
            for col in range(10):
                if (row, col) in self.fields:
                    deck = self.fields[(row, col)].get_deck(row, col)
                    ship = self.fields[(row, col)]
                    if deck.is_alive:
                        row_str += "□ "
                    elif ship.is_drowned:
                        row_str += "x "
                    else:
                        row_str += "* "
                else:
                    row_str += "~ "
            print(row_str)

    def _validate_field(self) -> None:
        lengths = [len(ship.decks) for ship in self.ships]
        if (lengths.count(1) != 4 or lengths.count(2) != 3
                or lengths.count(3) != 2 or lengths.count(4) != 1):
            raise ValueError("Invalid number of ships by size")

        field = [[0] * 10 for _ in range(10)]

        for ship in self.ships:
            for deck in ship.decks:
                row, col = deck.row, deck.column
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < 10 and 0 <= nc < 10:
                            if field[nr][nc] == 1:
                                if ((nr, nc) not in
                                        [
                                            (d.row, d.column)
                                            for d in ship.decks]):
                                    raise ValueError("Ships are too close")
                field[row][col] = 1

    def fire(self, location: tuple) -> str:
        if location in self.fields:
            ship = self.fields[location]
            result = ship.fire(location[0], location[1])
            return result
        return "Miss!"
