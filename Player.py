from GameMap import GameMap, Tile
import time


class Player:
    logged_in = False
    gm = GameMap()
    tn = None
    z = 0
    x = 0
    y = 0
    details = {
        "username": "Xyf",
        "password": "nope"
    }

    def __print_response(self):
        response = self.tn.read_until(b"\r\n\r\n> ", timeout=.1)
        print("---")
        for i, line in enumerate(response.decode('ascii').split("\n")):
            print(i, line)

    def get_detail(self, detail):
        return f"{self.details[detail]}\n".encode('ascii')

    def login(self):
        line = self.tn.read_very_eager()
        line = line.decode('ascii')
        # if line != "":
        #     print(line.strip())
        if not self.logged_in:
            if "what name do you wish to be known?" in line:
                self.tn.write(self.get_detail("username"))

            if "Password:" in line:
                self.tn.write(self.get_detail("password"))
            if "PRESS RETURN" in line:
                self.tn.write("\n".encode('ascii'))
            if "Make your choice:" in line:
                self.tn.write("1\n".encode('ascii'))
                self.logged_in = True
            if "Reconnecting." in line:
                self.logged_in = True

    def move_west(self):
        self.tn.write('w\n'.encode('ascii'))
        self.x -= 1

    def move_east(self):
        self.tn.write('e\n'.encode('ascii'))
        self.x += 1

    def move_south(self):
        self.tn.write('s\n'.encode('ascii'))
        self.y -= 1

    def move_north(self):
        self.tn.write('n\n'.encode('ascii'))
        self.y += 1

    def move_up(self):
        self.tn.write('u\n'.encode('ascii'))
        self.z += 1

    def move_down(self):
        self.tn.write('d\n'.encode('ascii'))
        self.z -= 1

    def get_room_info(self):
        self.tn.write('l\n'.encode('ascii'))
        response = self.tn.read_until(b"\r\n\r\n> ", timeout=.1)
        self.gm.current = Tile(response.decode('ascii').split("\n")[0], self.z, self.x, self.y)
        # for i, line in enumerate(response.decode('ascii').split("\n")):
        #     if i == 0:
        #         if self.gm.current is None:
        #             self.gm.current = Tile(line)
        #             break

    def get_tile_in_direction(self, direction):
        temp = None
        success = True
        if direction == "n":
            self.move_north()
        elif direction == "e":
            self.move_east()
        elif direction == "s":
            self.move_south()
        elif direction == "w":
            self.move_west()
        elif direction == "u":
            self.move_up()
        elif direction == "d":
            self.move_down()
        response = self.tn.read_until(b"\r\n\r\n> ", timeout=.1)
        checkmove = response.decode('ascii').split("\n")[0]
        if "Alas, you cannot" in checkmove:
            success = False
        if success:

            self.tn.write('l\n'.encode('ascii'))
            response = self.tn.read_until(b"\r\n\r\n> ", timeout=.1)
            title = response.decode('ascii').split("\n")[0]
            temp = Tile(title, self.z, self.x, self.y)

            if direction == "n":
                # print("Im trying to move south")
                self.move_south()
            if direction == "e":
                self.move_west()
            if direction == "s":
                self.move_north()
            if direction == "w":
                self.move_east()
            if direction == "u":
                self.move_down()
            if direction == "d":
                self.move_up()
            self.tn.read_until(b"\r\n\r\n> ", timeout=.1)
        return temp

    def check_exits(self):
        exits = {
            "n": None,
            "e": None,
            "s": None,
            "w": None,
            "u": None,
            "d": None
        }
        for k in exits.keys():
            temp = self.get_tile_in_direction(k)
            # print(f"MOVING {k}")
            if temp is not None:
                exits[k] = temp
        self.gm.current.exits = exits
        self.gm.add_tile(self.gm.current, self.z, self.x, self.y)
        self.gm.current = None
