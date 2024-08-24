import random, curses
from items import Corpse
from message import Message
from color import get_col
from helpers import d20

class Monster():
    def __init__(self, name, sign, hp, min_damage, max_damage,  initiative=100, to_hit=0, defense=0, armor=0):
        self.name = name
        self.sign = sign
        self.to_hit = to_hit
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.defense = defense
        self.armor = armor
        self.hp = hp
        self.max_hp = hp
        self.initiative_increment = initiative
        self.current_initiative = 0
        self.y = None
        self.x = None
        
    def die(self, level):
            #new_item = Corpse(name=f"{self.name} corpse", y=self.y, x=self.x)
            #level.map[self.y][self.x].loot.append(new_item)
            #level.items.append(new_item)
            level.monsters.remove(self)
            level.map[self.y][self.x].occupied = False
        
    def action(self, level, player):
            self.current_initiative += self.initiative_increment
            while self.current_initiative >= player.initiative:
                if abs(self.x - player.x) + abs(self.y - player.y) > 4: self.move_random(level)
                else: self.move_closer(level, player)
                self.current_initiative -= player.initiative


    def complete_movement(self, level, ny, nx):          
            level.map[self.y][self.x].occupied = False
            level.map[ny][nx].occupied = self
            self.y = ny
            self.x = nx
            
    def move_random(self, level):
            ny = self.y + random.randint(-1,1)
            nx = self.x + random.randint(-1,1)
            if not level.is_space_unavaible(ny,nx): self.complete_movement(level,ny,nx)
            
    def move_closer(self, level, player):
            nx = self.x                         # create direction and assume monster is on the same row as player
            if self.x > player.x: nx -=1        # if player has lower x adjust nx by x-1
            elif self.x < player.x: nx +=1      # if player has higher x adjust nx by x+1
            ny = self.y                 	# create direction and assume monster is on the same column as player
            if self.y > player.y: ny -=1        # if player has lower y adjust ny by y-1
            elif self.y < player.y: ny +=1      # if player has higher y adjust ny by y+1
            
            if ny == player.y and  nx == player.x:      # if tries to go into player - attack
                if self.to_hit + d20() >=  player.defense + d20():
                    damage = random.randint(self.min_damage, self.max_damage) - player.calculate_armor()
                    if damage > 0:
                        player.hp -= damage
                        player.message.append(Message(f" {self.name} hits you for {damage}.", get_col("red")))
                        player.attributes_changed = True
                        player.hit = True
                    else:
                        player.message.append(Message(f" {self.name} hits you but doesn't manage to wound.", get_col("white")))
                else: player.message.append(Message(f" {self.name} misses you.", get_col("white")))
                return   	
            
            if level.is_space_unavaible(ny, nx):					# if direct path unavaible try other:
                if player.x == nx and not level.is_space_unavaible(ny, nx+1): nx +=1          # if is in the same column as player and diagonal right is open, go diag-right   
                elif player.x == nx and not level.is_space_unavaible(ny, nx-1): nx -=1        # if is in the same column as player and diagonal left is open, go diag-left
                elif player.y == ny and not level.is_space_unavaible(ny+1, nx): ny +=1        # if is in the same row as player and diagonal down is open, go diag-down
                elif player.y == ny and not level.is_space_unavaible(ny-1, nx): ny -=1        # if is in the same row as player and diagonal up is open, go diag-up
                elif nx != player.x and ny !=player.y and not level.is_space_unavaible(ny,self.x): nx = self.x # if tries to go diagonal, and path along x axis is open go along x
                elif nx != player.x and ny !=player.y and not level.is_space_unavaible(self.y,nx): ny = self.y # if tries to go diagonal, and path along y axis is open go along y
                else: return								                                    # if non apply, do nothing	
            self.complete_movement(level, ny, nx)


class Kobold(Monster):
    def __init__(self):
        super().__init__(name='kobold', sign='k', hp=5, min_damage=1, max_damage=3 )
