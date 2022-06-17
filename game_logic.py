from random import shuffle

from enum import Enum

class State(Enum):
    ZERO = '0'
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    MINE = 'mine'
    DEFUSED_MINE = 'defused_mine'
    UNKNOWN = 'unknown'
    def get(value):
        for item in State:
            if item.value == value:
                return item
        return None


class MineSweeperGame:

    def __init__(self,height,width,mine_count):
        self.height = height
        self.width = width
        self.mine_count = mine_count
        self.defused_count = 0
        self.reveiled_count = 0
        self.grid = {}
        self._lay_mines()
        self.game_state = 'OPEN'
    
    def _lay_mines(self):
        loC = [
            (x,y)
            for x in range(self.width)
            for y in range(self.height)
        ]
        shuffle(loC)
        for (x,y) in loC[:self.mine_count]:
            self.grid[x,y] = (State.MINE,State.UNKNOWN)
        for (x,y) in loC[self.mine_count:]:
            neighboring_mines = self._count_neighboring_mines(x,y)
            self.grid[x,y] = (State.get(str(neighboring_mines)),State.UNKNOWN)
    
    def _count_neighboring_mines(self,x,y):
        mine_count = 0
        for (_x,_y) in self._neighborhood(x,y):
            if self.grid[_x,_y][0] == State.MINE:
                mine_count += 1
        return mine_count
    
    def _neighborhood(self,x,y):
        for dx,dy in [
            (1,0),(1,1),(0,1),(-1,1),
            (-1,0),(-1,-1),(0,-1),(1,-1)]:
            if (x+dx,y+dy) in self.grid:
                yield (x+dx,y+dy)
            
    def reveil_square(self,x,y):
        _type,_state = self.grid[x,y]
        if _type == _state:
            return
        self.reveiled_count += 1
        self.grid[x,y] = _type,_type
        if _type == State.MINE:
            self.game_state = 'LOST'
        if _type == State.ZERO:
            for (_x,_y) in self._neighborhood(x,y):
                self.reveil_square(_x,_y)
        self.update_game_state()

    def defuse_square(self,x,y):
        _type,_state = self.grid[x,y]
        self.grid[x,y] = _type,State.DEFUSED_MINE
        self.defused_count += 1
        self.update_game_state()

    def get_square_status(self,x,y):
        _type,_state = self.grid[x,y]
        return _state

    def update_game_state(self):
        if self.defused_count + self.reveiled_count == self.width * self.height:
            self.game_state = 'WON'
