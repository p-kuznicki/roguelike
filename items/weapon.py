import curses
import random
import time

from message import Message
from color import get_col
from .item import Item
from helpers import d20



class Weapon(Item):
    def __init__(self, name,  min_damage, max_damage, color = "black_on_white" , full_name = None, two_handed=False, attack=None, special=None):
        super().__init__(name=name, full_name=full_name, sign=")", color = color, category="weapon", appropriate_slot="weapon_hand", special=special)
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.two_handed = two_handed
        if attack == None: self.attack = self.animated_standard_attack
        else: self.attack = attack
        
        
    def hit_and_damage(self, monster, player):
        if player.to_hit + d20() >=  monster.defense + d20():
            player.message.append(Message(f" You hit {monster.name}.", get_col("green")))
            damage = random.randint(self.min_damage, self.max_damage) - monster.armor
            if damage > 0:
                monster.hp -= damage 
            return True
        else:
            player.message.append(Message(f" You miss {monster.name}.", get_col("white")))
            return False
    
    def death_check(self, level, monster, player):
        if monster.hp <= 0:
            player.message.append(Message(f"\b and kill it.", get_col("green")))
            player.kills += 1
            player.attributes_changed = True
            monster.die(level)
            return True
        
    def hit_animation(self, level, monster, map_win):
        curses.curs_set(0)
        y, x = monster.y, monster.x
        map_win.addch(y, x, monster.sign, get_col("red"))
        map_win.refresh()
        time.sleep(0.2)
        level.draw_single(y, x, map_win)
        map_win.refresh()
        curses.curs_set(1)


    def miss_animation(self, level, monster, map_win):
        curses.curs_set(0)
        y, x = monster.y, monster.x
        map_win.addch(y, x, "-")
        map_win.refresh()
        time.sleep(0.2)
        level.draw_single(y, x, map_win)
        map_win.refresh()
        curses.curs_set(1)
    

  
    def animated_standard_attack(self, level, monster, player, map_win):
        if self.hit_and_damage(monster, player):
            self.death_check(level, monster, player)
            self.hit_animation(level, monster, map_win)
        else: self.miss_animation(level, monster, map_win)
        
        
        
    def animated_double_strike(self, level, monster, player, map_win):
        if self.hit_and_damage(monster, player):
            self.death_check(level, monster, player)
            self.hit_animation(level, monster, map_win)
        else: self.miss_animation(level, monster, map_win) 
        if monster.hp > 0:
            curses.curs_set(0)
            time.sleep(0.2)
            if self.hit_and_damage(monster, player):
                self.death_check(level, monster, player)
                self.hit_animation(level, monster, map_win)
            else: self.miss_animation(level, monster, map_win)


        
    def animated_hellfire(self, level, monster, player, map_win):   # ~+ „*❋✦✶✺
        curses.curs_set(0)
        direction_y, direction_x= monster.y-player.y, monster.x-player.x
        for i in range(1,4):
            iy = i * direction_y + player.y
            ix = i * direction_x + player.x
            if not level.is_beyond_map(iy,ix) and not level.map[iy][ix].solid:
                if level.map[iy][ix].occupied:
                    player.message.append(Message(f" You hit {level.map[iy][ix].occupied.name}.", get_col("green")))
                    level.map[iy][ix].occupied.hp -= random.randint(self.min_damage,self.max_damage)
                    self.death_check(level, level.map[iy][ix].occupied, player)
                map_win.addch(iy,ix,"✦", curses.color_pair(4))
                map_win.refresh()
                time.sleep(0.08)
                map_win.addch(iy,ix,"✶", curses.color_pair(5))
                map_win.refresh()
                time.sleep(0.08)
                map_win.addch(iy,ix,"✺", curses.color_pair(4))
                map_win.refresh()
                time.sleep(0.08)
                level.draw_single(iy,ix, map_win)
                map_win.refresh()
            else: break
        curses.curs_set(1)


      
class Fists(Weapon):
    def __init__(self):
        super().__init__(name="fists", min_damage=1, max_damage=2)        

class ShortSword(Weapon):
    def __init__(self):
        super().__init__(name="short sword", min_damage=2, max_damage=5)

class HellfireStaff(Weapon):
    def __init__(self):
        super().__init__(name="ram skull staff", full_name="Hellfire Staff",  color="magenta_on_white", min_damage=1, max_damage=7, two_handed = True, attack=self.animated_hellfire)
        
class MurderMace(Weapon):
    def __init__(self):
        super().__init__(name="bloodied mace", full_name="Murder Mace", min_damage=1, max_damage=4, attack=self.animated_double_strike)

