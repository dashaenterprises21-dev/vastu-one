"""
81 पद वास्तु ग्रिड जनरेटर
"""

class Grid81:
    def __init__(self):
        self.size = 9
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.devata_map = {}

    def load_devatas(self, devatas_json):
        for d in devatas_json["outer_devatas"] + devatas_json["inner_devatas"]:
            self.devata_map[d["pada"]] = d

    def assign_pada(self, row, col):
        return row * self.size + col + 1

    def map_devata_to_grid(self):
        for row in range(self.size):
            for col in range(self.size):
                pada = self.assign_pada(row, col)
                if pada in self.devata_map:
                    self.grid[row][col] = self.devata_map[pada]
        return self.grid

    def get_devata_at(self, row, col):
        return self.grid[row][col]

    def get_center(self):
        return self.grid[4][4]

    def get_zone(self, row, col):
        if row < 3 and col < 3: return "NE"
        if row < 3 and col > 5: return "NW"
        if row > 5 and col < 3: return "SE"
        if row > 5 and col > 5: return "SW"
        if row < 3: return "N"
        if row > 5: return "S"
        if col < 3: return "W"
        if col > 5: return "E"
        return "CENTER"
