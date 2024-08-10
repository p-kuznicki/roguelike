class Status():
    def __init__(self, player, message_win, attributes_win):
        self.mess_win = message_win
        self.att_win = attributes_win
        self.player = player 
        self.displaying_message = False
        
        
    def update_message(self):
        if self.displaying_message:
            self.mess_win.clear()
            self.displaying_message = False
        if self.player.message:
            self.mess_win.addstr(0,1, self.player.message)
            self.player.message = None
            self.displaying_message = True
        self.mess_win.refresh()
        
    def update_attributes(self):
        self.att_win.addstr(0,1, f"{self.player.name} ToHit:{self.player.to_hit}  DMG:1-{self.player.damage}  DFNS:{self.player.defense}  \
HP:{self.player.hp}  kills:{self.player.kills}")
        self.att_win.refresh()
        self.player.attributes_changed = False
        
