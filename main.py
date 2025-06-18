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

    def enter_room(self):
        pass

class Map:
    def __init__(self,seed=random.random()) -> None:
        self._random_seed = seed
        random.seed(seed)
        self._rooms = {}
        self._walls = {}
        self._room_types = {"hallway":{"exits":(2,2),"encounters":False},"chamber":{"exits":(1,4),"encounters":True}} #unused

    def get_room(self,location:tuple[int,int]) -> Room:
        if location not in self._rooms:
            self._rooms[location] = Room()
        return self._rooms[location]

    def is_wall(self,source:tuple[int,int],destination:tuple[int,int]) -> bool:
        rooms = [source,destination]
        rooms.sort()

        rng = random.Random(str(self._random_seed)+str(rooms))

        # check cache for prior set up
        if str(self._random_seed)+str(rooms) in self._walls:
            return self._walls[str(self._random_seed)+str(rooms)]
        
        isWall = True if rng.random()<0.5 else False

        self._walls[str(self._random_seed)+str(rooms)] = isWall

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
    
    def set_location(self,location:tuple[int,int]) -> None:
        self._current_location = location
    
        
class Monster:
    def __init__(self, name:str, health_base:int, atk_base:int, def_base:int) -> None:
        self._name = name
        self._health_base = health_base
        self._atk_base = atk_base
        self._def_base = def_base
        self._statuses = []
        self._inventory = Inventory()


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
    DIRECTIONS = ["north","east","south","west"]
    COMMAND_SETS = {"move":[d for d in DIRECTIONS],
                    "go":[d for d in DIRECTIONS],
                    "look":[d for d in DIRECTIONS]+["around"]}

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
        self._player = Player(playername,self.PLAYER_BASE_HEALTH,self.PLAYER_BASE_ATK,self.PLAYER_BASE_DEF,(0,0))
        
        while True:
            action = self.get_player_action()

            # look action
            if action[0] == "look":
                if action[1] == "around":
                    for d in self.DIRECTIONS:
                        print(f"There is {'a wall' if self.look(d) else 'door'} to the {d.title()}.")
                else:
                    print(f"There is {'' if self.look(action[1]) else 'not '}a wall to the {action[1].title()}.")

            # move action
            if action[0] == "move" or action[0] == "go":
                self.move(action[1])
            
    
    def get_player_action(self) -> list:
        while True:
            action = input("What do you do?: ").lower()

            try:
                actionList = action.split()
                if actionList[0] in self.COMMAND_SETS:
                    if actionList[1] in self.COMMAND_SETS[actionList[0]]:
                        return actionList
                    else:
                        raise(Exception)
            except:
                if action == '':
                    print(f"No command given. You can '{'\', \''.join(self.COMMAND_SETS.keys())}'.")
                elif actionList[0] not in self.COMMAND_SETS:
                    print(f"'{actionList}' is not a valid command. You can '{'\', \''.join(self.COMMAND_SETS.keys())}'.")
                elif actionList[1] not in self.COMMAND_SETS[actionList[0]]:
                    print(f"'{' '.join(actionList)}' is not a valid command. You can '{actionList[0]}' '{'/'.join(self.COMMAND_SETS[actionList[0]])}'.")


    def look(self, direction) -> bool:
        cx,cy = self._player.get_location()# type: ignore
        if direction == "north":
            targetLocation = (cx,cy+1) 
        elif direction == "east":
            targetLocation = (cx+1,cy)
        elif direction == "south":
            targetLocation = (cx,cy-1) 
        else:
            targetLocation = (cx-1,cy) 
        
        if self._map.is_wall(self._player.get_location(),targetLocation):
            return True
        else:
            return False

    def move(self,direction:str) -> None:
        cx,cy = self._player.get_location()# type: ignore
        if direction == "north":
            targetLocation = (cx,cy+1) 
        elif direction == "east":
            targetLocation = (cx+1,cy)
        elif direction == "south":
            targetLocation = (cx,cy-1) 
        else:
            targetLocation = (cx-1,cy) 
        
        if self._map.is_wall((cx,cy),targetLocation):
            print(f"There is no door to the {direction.title()}.")
        else:
            print(f"You go {direction.title()}.")
            self._map.get_room(targetLocation)
            self._player.set_location(targetLocation)



if __name__ == "__main__":
    game = RoominateGame()
    game.start_game()

