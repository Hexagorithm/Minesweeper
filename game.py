from abc import ABC, abstractmethod
import settings as st
import pygame as pg
from tile import Tile
from random import randint

class Screen(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def events(self):
        pass

    @abstractmethod
    def display(self):
        pass



class Game:

    def __init__(self, bomb_amount, tile_amount, screen_size):
        self.bomb_amount = bomb_amount
        self.tile_amount = tile_amount
        self.screen_size = screen_size

        self.running = True
        self.state = 'playing'
        self.clock = pg.time.Clock

    def mode(self):
        if self.state == 'playing':
            print('selected mode: playing')
            return Playing(self.bomb_amount, self.tile_amount, self.screen_size)
            #create playing screen

    def end(self):
        print('game was made to end')
        pg.quit()

    def run(self):
        print('game was made to run')
        while self.running:
            curr_mode = self.mode()
            while curr_mode.running:
                curr_mode.events()
                # print('Current mode events was run')
                curr_mode.display()
                # print('Current mode display was run')
                if curr_mode.running == 'quit':
                    self.running = False
                    break
        self.end()

class Playing(Screen):

    def __init__(self, bomb_amount, tile_amount, screen_size):
        self.bomb_amount = bomb_amount
        self.tile_amount = tile_amount
        self.screen_size = screen_size

        self.running = True
        self.screen = pg.display.set_mode(self.screen_size)
        self.map = self.create_map()
        self.render_map()

    def create_map(self):
        map = []
        for _ in range(self.tile_amount):
            map.append([['_', False, False] for _ in range(self.tile_amount)])
        for _ in range(self.bomb_amount):
            x = randint(0, self.tile_amount - 1)
            y = randint(0, self.tile_amount - 1)
            if map[y][x][0] == '_':
                map[y][x][0] = 'B'
        for y, row in enumerate(map):
            for x, item in enumerate(row):
                if item[0] == '_':
                    around = []
                    y_limit = len(map) - 1
                    x_limit = len(row) - 1
                    if y > 0 and x > 0:  # topleft
                        around.append(map[y - 1][x - 1][0])
                    if y > 0:  # top
                        around.append(map[y - 1][x][0])
                    if y > 0 and x < x_limit:  # topright
                        around.append(map[y - 1][x + 1][0])
                    if x > 0:  # left
                        around.append(map[y][x - 1][0])
                    if x < x_limit:  # right
                        around.append(map[y][x + 1][0])
                    if y < y_limit and x > 0:  # bottomleft
                        around.append(map[y + 1][x - 1][0])
                    if y < y_limit:  # midbottom
                        around.append(map[y + 1][x][0])
                    if y < y_limit and x < x_limit:  # bottomright
                        around.append(map[y + 1][x + 1][0])
                    map[y][x][0] = str(around.count('B'))

        return map # identity, if_opened, if_flagged

    def events(self):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.running = 'quit'

            if event.type == pg.MOUSEBUTTONDOWN:

                for tile in self.tiles:
                    if tile.rect.collidepoint( pg.mouse.get_pos() ):
                        if pg.mouse.get_pressed()[0]:
                            self.try_open(tile)


                        elif pg.mouse.get_pressed()[2]:

                            if tile.is_opened == False:
                                if tile.is_flagged == False:
                                    tile.flag()
                                    print('{} was flagged'.format(repr(tile)))
                                else:
                                    tile.unflag()
                                    print('{} was un-flagged'.format(repr(tile)))

    def try_open(self, tile):
        if tile.is_opened == False and tile.is_flagged == False:
            tile.open()
            if tile.identity == '0':
                x_and_y = []
                y = tile.y
                x = tile.x
                y_limit = len(self.map) - 1
                x_limit = len(self.map[0]) - 1
                if y > 0 and x > 0:  # topleft
                    x_and_y.append([y - 1,x - 1])
                if y > 0:  # top
                    x_and_y.append([y - 1,x    ])
                if y > 0 and x < x_limit:  # topright
                    x_and_y.append([y - 1,x + 1])
                if x > 0:  # left
                    x_and_y.append([y    ,x - 1])
                if x < x_limit:  # right
                    x_and_y.append([y    ,x + 1])
                if y < y_limit and x > 0:  # bottomleft
                    x_and_y.append([y + 1,x - 1])
                if y < y_limit:  # midbottom
                    x_and_y.append([y + 1,x    ])
                if y < y_limit and x < x_limit:  # bottomright
                    x_and_y.append([y + 1,x + 1])
                for tile in self.tiles:
                    if [tile.y, tile.x] in x_and_y:
                        self.try_open(tile)

            # print('{} was opened'.format(repr(tile)))

    def render_map(self):
        surface = self.screen
        self.tiles = pg.sprite.Group()
        for y, row in enumerate(self.map):
            for x , item in enumerate(row):
                tile = Tile(st.tile_multiplier,surface,x,y,*item)
                # print(repr(tile))
                self.tiles.add(tile)

    def display(self):
        self.screen.fill('black')
        for tile in self.tiles:
            tile.draw()
        pg.display.update()

    def
