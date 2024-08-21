class Status():
    def __init__(self, min_width): 
        self.displaying_message = False
        self.min_width = min_width
        
        
    def update_message(self, player, message_win):
        if self.displaying_message:
            message_win.clear()
            self.displaying_message = False
        if player.message:
            if len(player.message) < self.min_width: message_win.addstr(0,0, player.message)
            else:
                message_win.addstr(0,0, player.message[0:self.min_width-8]+"(more)")
                message_win.getkey()
                message_win.clear()
                message_win.addstr(0,0, player.message[self.min_width-8:])
            player.message = None
            self.displaying_message = True   
        message_win.refresh()
        
    def update_attributes(self, player, att_win):
        att_win.clear()
        att_win.addstr(0,1, f"{player.name} ToHit:{player.to_hit}  DFNS:{player.defense}  \
HP:{player.hp}/{player.max_hp}  kills:{player.kills} Depth:{player.depth+1}")
        att_win.refresh()
        player.attributes_changed = False
        
