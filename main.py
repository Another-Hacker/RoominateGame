import random
from typing import Self

class Item:
    def __init__(self, name:str) -> None:
        self._name = name

    def get_name(self) -> str:
        return self._name

class Inventory:
    def __init__(self) -> None:
        self._inventory = {}
    
    def get_items(self) -> dict:
        return self._inventory
    
    def get_item(self,item_name:str) -> Item:
        return self._inventory[item_name]
    
    def find_item(self,item_name) -> bool:
        if item_name in self._inventory:
            return True
        else:
            return False
    
    def add_item(self,item:Item) -> None:
        if item.get_name() not in self._inventory:
            self._inventory[item.get_name()] = item
    
    def remove_item(self,item:Item) -> None:
        if item.get_name() in self._inventory:
            self._inventory.pop(item.get_name())

class Room:
    def __init__(self) -> None:
        self._inventory = Inventory()
        self._encounter = []
        self._exits = {}

    def add_exit(self,direction:str,room:Self|None=None) -> None:
        if direction not in self._exits:
            self._exits[direction] = room
    
    def update_exit(self,exit_direction:str,room:Self) -> None:
        pass
    
    def get_exits(self) -> list:
        k = list(self._exits)
        if "home" in k:
            k.pop(k.index("home"))
        return k

    def get_exit(self,direction) -> Self:
        return self._exits[direction]
            
    def enter_room(self):
        pass

class Map:
    def __init__(self,seed=random.random()) -> None:
        self._random_seed = seed
        random.seed(seed)
        self._rooms = {}
        self._room_types = {"hallway":{"exits":(2,2),"encounters":False},"chamber":{"exits":(1,4),"encounters":True}} #unused

    def get_room(self,location:tuple[int,int]) -> Room:
        if location not in self._rooms:
            self._rooms[location] = Room()
        return self._rooms[location]

    def is_wall(self,source:tuple[int,int],destination:tuple[int,int]) -> bool:
        rooms = [source,destination]
        rooms.sort()
        random.seed(str(self._random_seed)+str(rooms))
        isWall = True if random.random()<0.5 else False
        random.seed(self._random_seed)
        return isWall
            
        

class Player:
    def __init__(self, name:str, health_base:int, atk_base:int, def_base:int, starting_location:tuple[int,int]) -> None:
        self._name = name
        self._health_base = health_base
        self._atk_base = atk_base
        self._def_base = def_base
        self._statuses = []
        self._inventory = Inventory()
        self._current_location = starting_location

    def get_name(self) -> str:
        return self._name
    
    def get_location(self) -> tuple[int,int]:
        return self._current_location
    
        
class Monster:
    def __init__(self, name:str) -> None:
        self._name = name

class Door:
    pass

class Weapon(Item):
    pass

class Potion(Item):
    pass

class Armor(Item):
    pass

class Key(Item):
    pass

class Slime(Monster):
    pass

class Skeleton(Monster):
    pass

class Zombie(Monster):
    pass

class RoominateGame:
    PLAYER_BASE_HEALTH = 20
    PLAYER_BASE_ATK = 10
    PLAYER_BASE_DEF = 10

    def __init__(self) -> None:
        self._rooms = []
        self._player = None
        self._map = Map()

    def start_game(self) -> None:
        self._map.get_room((0,0))
        playername = input("Enter Player Name: ").title()
        self._player_location = (0,0)
        self._player = Player(playername,self.PLAYER_BASE_HEALTH,self.PLAYER_BASE_ATK,self.PLAYER_BASE_DEF,(0,0))
        
        while True:
            print(f"you are at {self._player_location}")
            dirc = input("where do you want to move: ")
            if dirc.lower() not in DIRECTIONS:
                print("that is not a direction")
                continue
            self.move(dirc)


    def move(self,direction:str) -> None:
        cx,cy = self._player_location# type: ignore
        if direction == "north":
            targetLocation = (cx,cy+1) 
        elif direction == "east":
            targetLocation = (cx+1,cy)
        elif direction == "south":
            targetLocation = (cx,cy-1) 
        else:
            targetLocation = (cx-1,cy) 
        
        if self._map.is_wall(self._player_location,targetLocation):
            print(f"There is no door to the {direction.title()}.")
        else:
            self._map.get_room(targetLocation)
            self._player_location = targetLocation

DIRECTIONS = ["north","east","south","west"]

if __name__ == "__main__":
    game = RoominateGame()
    game.start_game()

