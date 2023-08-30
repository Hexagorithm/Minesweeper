from abc import ABC, abstractmethod
import settings as st
import pygame as pg
from tile import Tile, Pause_button
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

    @abstractmethod
    def status(self):
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
        elif self.state == 'endingloss':
            print('selected mode: ending with loss')
            return EndingLoss(self.screen_size)
        elif self.state == 'endingwin':
            print('selected mode: ending with win')
            return EndingWin(self.screen_size)

    def end(self):
        print('game was made to end')
        pg.quit()

    def run(self):
        print('game was made to run')
        while self.running:
            curr_mode = self.mode()
            while curr_mode.running:
                curr_mode.events()
                curr_mode.display()
                status = curr_mode.status()
                if curr_mode.running == 'quit':
                    self.running = False
                    break
                if status == None:
                    continue
                elif status == 'EndingLoss':
                    curr_mode.running = False
                    self.state = 'endingloss'
                elif status == 'EndingWin':
                    curr_mode.running = False
                    self.state = 'endingwin'

        self.end()

class Playing(Screen):

    def __init__(self, bomb_amount, tile_amount, screen_size):
        self.bomb_amount = bomb_amount
        self.tile_amount = tile_amount
        self.screen_size = screen_size

        self.running = True
        self.flags = self.bomb_amount
        self.screen = pg.display.set_mode(self.screen_size)
        self.map = self.create_map()
        self.render_tiles()
        # self.render_pause()

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

                target_tile = self.get_tile_clicked()
                if pg.mouse.get_pressed()[0]:
                    self.try_open(target_tile)
                elif pg.mouse.get_pressed()[2]:
                    self.try_flag(target_tile)

    def get_tile_clicked(self):
        for tile in self.tiles:
            if tile.rect.collidepoint( pg.mouse.get_pos() ):
                return tile

    def try_nuke(self,tile):
        if tile.get_identity() == '0':
            x_and_y = []
            y = tile.y
            x = tile.x
            y_limit = len(self.map) - 1
            x_limit = len(self.map[0]) - 1
            if y > 0 and x > 0:  # topleft
                x_and_y.append([y - 1, x - 1])
            if y > 0:  # top
                x_and_y.append([y - 1, x])
            if y > 0 and x < x_limit:  # topright
                x_and_y.append([y - 1, x + 1])
            if x > 0:  # left
                x_and_y.append([y, x - 1])
            if x < x_limit:  # right
                x_and_y.append([y, x + 1])
            if y < y_limit and x > 0:  # bottomleft
                x_and_y.append([y + 1, x - 1])
            if y < y_limit:  # midbottom
                x_and_y.append([y + 1, x])
            if y < y_limit and x < x_limit:  # bottomright
                x_and_y.append([y + 1, x + 1])
            for tile in self.tiles:
                if [tile.y, tile.x] in x_and_y:
                    self.try_open(tile)

    def try_open(self, tile):
        if tile.if_can_open():
            tile.open()
            self.try_nuke(tile)

    def try_flag(self,tile):
        if tile.if_can_flag() and self.flags != 0:
            tile.flag()
            self.flags -= 1
        elif tile.if_can_unflag():
            tile.unflag()
            self.flags += 1

    def render_tiles(self):
        self.tiles = pg.sprite.Group()

        for y, row in enumerate(self.map):
            for x , item in enumerate(row):

                tile = Tile(st.tile_multiplier,self.screen,x,y,*item)
                self.tiles.add(tile)

    def display_tiles(self):
        for tile in self.tiles:
            tile.draw()

    def render_pause(self):
        self.pause = Pause_button(st.tile_multiplier, self.screen, 0, 0)

    def display_pause(self):
        self.pause.draw()

    def pause_game(self):
        self.running = False

    def display(self):
        self.screen.fill('black')
        self.display_tiles()
        # self.display_pause()
        pg.display.update()

    def status(self):
        tiles_bomb = [tile for tile in self.tiles if tile.get_identity() == 'B']
        for tile_bomb in tiles_bomb:
            if tile_bomb.get_opened():
                return 'EndingLoss'
        for tile_bomb in tiles_bomb:
            if not tile_bomb.get_flagged():
                return None
        return 'EndingWin'


class EndingWin(Screen):

    def __init__(self,screen_size):
        self.screen_size = screen_size

        self.running = True
        self.message = 'YOU WIN'
        self.screen = pg.display.set_mode( size = self.screen_size)
        self.create_win_screen()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = 'quit'

    def create_win_screen(self):
        font = pg.font.Font(st.font_name, self.screen_size[0])
        self.text_image = font.render(self.message, True, st.font_color['ending'])
        self.text_image = pg.transform.scale(self.text_image, size= self.screen_size)

    def display(self):
        self.screen.fill('green')
        self.screen.blit(self.text_image,(0,0))
        pg.display.update()

    def status(self):
        return None


class EndingLoss(Screen):

    def __init__(self, screen_size):
        self.screen_size = screen_size

        self.running = True
        self.message = 'YOU LOST'
        self.screen = pg.display.set_mode(size=self.screen_size)
        self.create_loss_screen()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = 'quit'

    def create_loss_screen(self):
        pg.font.init()
        font = pg.font.Font(st.font_name, self.screen_size[0])
        self.text_image = font.render(self.message, True, st.font_color['ending'])
        self.text_image = pg.transform.scale(self.text_image, size=self.screen_size)

    def display(self):
        self.screen.fill('red')
        self.screen.blit(self.text_image, (0, 0))
        pg.display.update()

    def status(self):
        return None

class Pause(Screen):

    def __init__(self, screen_size):
        self.screen_size = screen_size

        self.screen = pg.display.set_mode(self.screen_size)
        self.running = True

    def events(self):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.running = 'quit'

            if event.type == pg.MOUSEBUTTONDOWN:
                pass

    def display(self):
        self.screen.fill('black')