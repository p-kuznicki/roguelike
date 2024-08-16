import curses
import random
import time

from .item import Item



class Weapon(Item):
    def __init__(self, name, damage, two_handed=False, attack=None, special=None):
        super().__init__(name=name, sign=")", category="weapon", appropriate_slot="weapon_hand", special=special)
        self.damage = damage
        self.two_handed = two_handed
        if attack == None: self.attack = self.animated_standard_attack
        else: self.attack = attack
        
        
    def hit_and_damage(self, monster, player):
        if random.randint(1,100) <= player.to_hit - monster.defense:
            player.message = (player.message or "") + f" You hit {monster.name}."
            monster.hp -= random.randint(1, self.damage)
            return True
        else:
            player.message = (player.message or "") + f" You miss {monster.name}."
            return False
    
    def death_check(self, level, monster, player):
        if monster.hp <= 0:
            player.message = (player.message or "") + f"\b and kill it."
            player.kills += 1
            player.attributes_changed = True
            monster.die(level)
            return True
    
    # DEPRECIATED
    def standard_attack(self, level, monster, player, map_win):
        self.hit_and_damage(monster, player)
        self.death_check(level, monster, player)

    # DEPRECIATED    
    def double_strike(self, level, monster, player, map_win):
        self.hit_and_damage(monster, player)
        if not self.death_check(level, monster, player):
            self.hit_and_damage(monster, player)
            self.death_check(level, monster, player)
        
    def hit_animation(self, level, monster, map_win):
        curses.curs_set(0)
        y, x = monster.y, monster.x
        map_win.addch(y, x, monster.sign, curses.color_pair(4))
        map_win.refresh()
        time.sleep(0.25)
        level.draw_single(y, x, map_win)
        map_win.refresh()
        curses.curs_set(1)


    def miss_animation(self, level, monster, map_win):
        curses.curs_set(0)
        y, x = monster.y, monster.x
        map_win.addch(y, x, "-")
        map_win.refresh()
        time.sleep(0.25)
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
            time.sleep(0.25)
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
                    player.message = (player.message or "") + f" You hit {level.map[iy][ix].occupied.name}."
                    level.map[iy][ix].occupied.hp -= random.randint(2,self.damage)
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
        super().__init__(name="fists", damage = 2)        

class ShortSword(Weapon):
    def __init__(self):
        super().__init__(name="short sword", damage = 6)

class HellfireStaff(Weapon):
    def __init__(self):
        super().__init__(name="hellfire staff", damage = 6, two_handed = True, attack=self.animated_hellfire)
        
class MurderMace(Weapon):
    def __init__(self):
        super().__init__(name="murder mace", damage=3, attack=self.animated_double_strike)

