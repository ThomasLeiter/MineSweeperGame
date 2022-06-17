import pygame
from pygame import Vector2
from game_logic import MineSweeperGame, State
from os.path import join

SQUARE_WIDTH = 40

def load_sprite(sprite_name,size=None,color_key=(255,255,255)):
    """
    Load a sprite from sub_directory 'sprites/'. 

    Parameters:
    ------------
    sprite_name: str
        The name of the sprite to load.
    size: Tupel[int,int], optional
        The size of the sprite
    color_key: color, optional
        The color_key (transparent color) to be set
    Returns:
    Surface
        The loaded sprite with requested properties
    """
    path = join('sprites',f"{sprite_name}.png")
    sprite = pygame.image.load(path).convert()
    sprite.set_colorkey(color_key)
    if size:
        sprite = pygame.transform.scale(sprite,size)
    return sprite

class GUISquare:
    """
    GUISquare represents a single square of the MinesweeperGui. 
    """
    def __init__(self,x,y):
        self.sprites = {}
        for status in State:
            self.sprites[status] = load_sprite(status.value,size=(SQUARE_WIDTH-2,SQUARE_WIDTH-2))
        self.status = State.UNKNOWN
        self.position = Vector2(x*SQUARE_WIDTH+1,y*SQUARE_WIDTH+1)
    
    def draw(self,surface):
        surface.blit(self.sprites[self.status],self.position)

class MineSweeperGUI:
    """
    GUI class of the MineSweeper game. 

    Parameters:
    ------------
    width : int
        Number of squares per row
    height : int
        Number of squares per column
    mine_count : int
    Number of mines
    """
    def __init__(self,width,height,mine_count):
        self.game = MineSweeperGame(width,height,mine_count)
        self._init_pygame()

    def main_loop(self):
        while True:
            self._handle_inputs()
            self._update_game()
            self._draw()

    def _handle_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event)

    def _update_game(self):
        for (x,y) in self.game.grid:
            self.squares[x,y].status = self.game.get_square_status(x,y)

    def _handle_mouse_click(self,mouse_event):
        if self.game.game_state != 'OPEN':
            return
        x,y = mouse_event.pos
        x,y = x // SQUARE_WIDTH, y // SQUARE_WIDTH
        if mouse_event.button == 1:
            self.game.reveil_square(x,y)
        if mouse_event.button == 3:
            self.game.defuse_square(x,y)

    def _draw_game_state(self):
        msg = self.font.render(
                self.game.game_state,True,(255,0,0),(255,255,255))
        msg.set_colorkey((255,255,255))
        x,y = msg.get_size()
        _x,_y = self.screen.get_size()
        self.screen.blit(msg,Vector2((_x-x)/2,(_y-y)/2))

    def _draw(self):
        for (x,y) in self.squares:
            self.squares[x,y].draw(self.screen)
        if self.game.game_state != 'OPEN':
            self._draw_game_state()
        pygame.display.flip()
        self.clock.tick(60)

    def _init_pygame(self):
        pygame.init()
        self.font = pygame.font.Font('freesansbold.ttf', 64)
        self.clock = pygame.time.Clock()
        dim = (
            self.game.width*SQUARE_WIDTH,
            self.game.height*SQUARE_WIDTH)
        self.screen = pygame.display.set_mode(dim) 
        pygame.display.set_caption('MineSweeper')
        self.squares = {
            (x,y): GUISquare(x,y)
            for x in range(self.game.width)
            for y in range(self.game.height)
        }

