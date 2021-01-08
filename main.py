from telnetlib import Telnet
import time
from Player import Player

player = Player()

with Telnet('192.168.2.38', 4000) as tn:
    player.tn = tn
    while True:
        # YO WE NEED TO LOGIN
        if not player.logged_in:
            player.login()
        else:
            # build the room im in
            player.get_room_info()

            player.check_exits()
            print(player.gm.root)
            break
