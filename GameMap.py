class Tile:
    title = None
    exits = {
        "n": None,
        "e": None,
        "s": None,
        "w": None,
        "u": None,
        "d": None
    }

    def __init__(self, title, z, x, y):
        self.title = title

    def add_exit(self, direction, tile):

        assert direction in ["n", "e", "s", "w", "u", "d"]
        # exits = list(self.exits).copy()
        # i = 0
        # if direction == "n":
        #     exits[i] = tile
        #
        # i += 1
        # if direction == "e":
        #     exits[i] = tile
        # i += 1
        # if direction == "s":
        #     exits[i] = tile
        # i += 1
        # if direction == "w":
        #     exits[i] = tile
        # i += 1
        # if direction == "u":
        #     exits[i] = tile
        # i += 1
        # if direction == "d":
        #     exits[i] = tile
        # self.exits = tuple(exits)
        self.exits[direction] = tile

    def __str__(self):
        ret = self.title
        for dir, tile in self.exits.items():
            if tile is not None:
                ret += f"\n{dir} {tile.title}"
        return ret

    def __repr__(self):
        return str(self)

    def __hash__(self):


class GameMap:
    gamemap = dict()
    root = None
    current = None
    minx = 0
    maxx = 0
    miny = 0
    maxy = 0
    minz = 0
    maxz = 0

    def add_tile(self, tile, z, x, y):
        if x > self.maxx:
            self.maxx = x
        if x < self.minx:
            self.minx = x

        if y > self.maxy:
            self.maxy = y
        if y < self.miny:
            self.miny = y

        if z > self.maxz:
            self.maxz = z
        if z < self.minz:
            self.minz = z
        if self.root is None:
            self.root = tile
        if (z, x, y) not in self.gamemap.keys():
            self.gamemap[(z, x, y)] = tile
        else:
            curr = self.gamemap[(z, x, y)]
            if curr.title is None:
                curr.title = tile.title
            for k, v in curr.exits.items():
                if v is None:
                    curr.exits[k] = tile.exits[k]


if __name__ == "__main__":
    z = 0
    x = 0
    y = 0
    tile = Tile("Test title", z, x, y)
    x += 1
    east = Tile("to the east", z, x, y)
    tile.add_exit("e", east)
    print(tile)
