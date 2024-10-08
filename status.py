from color import get_col

class Status():
    def __init__(self, min_width): 
        self.displaying_message = False
        self.min_width = min_width
        self.height = 2
        
        
    def update_message(self, player, message_win):
        if self.displaying_message:
            message_win.clear()
            self.displaying_message = False
        if player.message:
            space_left = self.min_width * self.height
            for message in player.message:
                if len(message.text) < space_left:
                    message_win.addstr(message.text, message.color)
                    space_left -= len(message.text)
                else:
                    message_win.getkey()
                    message_win.clear()
                    space_left = self.min_width * self.height
                    message_win.addstr(message.text, message.color)
            player.message = []
            self.displaying_message = True   
        message_win.refresh()
        
    def update_attributes(self, player, att_win):
        att_win.clear()
        if player.hp < player.max_hp//3:
            hp_color = get_col("red")
        elif player.hp < player.max_hp:
            hp_color = get_col("yellow")
        else:
            hp_color = get_col("white")
        att_win.addstr(f"{player.name}  HP:")
        att_win.addstr(f"{player.hp}", hp_color)
        att_win.addstr(f"/{player.max_hp}  kills:{player.kills} Depth:{player.depth+1}")
        att_win.refresh()
        player.attributes_changed = False
        
