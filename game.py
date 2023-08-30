from abc import ABC, abstractmethod
import settings as st
import pygame as pg
from tile import Tile, PlayAgainButton
from random import randint
from time import sleep

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
        icon = pg.image.load('textures\\bomb\\bomb.png')
        pg.display.set_caption('Saper')
        pg.display.set_icon(icon)

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
                elif status == 'Playing':
                    curr_mode.running = False
                    self.state = 'playing'

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
        self.force_loss = False
        self.force_win = False

    def create_map(self):
        # it should do something sbout an input where there are less avaliable tiles than bombs
        map = []
        for _ in range(self.tile_amount):
            map.append([['_', False, False] for _ in range(self.tile_amount)])
        for _ in range(self.bomb_amount):
            bomb_added = False
            while not bomb_added:
                x = randint(0, self.tile_amount - 1)
                y = randint(0, self.tile_amount - 1)
                if map[y][x][0] == '_':
                    map[y][x][0] = 'B'
                    bomb_added = True
                else:
                    continue
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
                if target_tile != None:
                    if pg.mouse.get_pressed()[0]:
                        self.try_open(target_tile)
                    elif pg.mouse.get_pressed()[2]:
                        self.try_flag(target_tile)
            # if event.type == pg.KEYDOWN:
            #     keys = pg.key.get_pressed()
            #     if keys[pg.K_l]:
            #         self.force_loss = True
            #     elif keys[pg.K_w]:
            #         self.force_win = True

    def get_tile_clicked(self):
        for tile in self.tiles:
            if tile.rect.collidepoint( pg.mouse.get_pos() ):
                return tile
        return None

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

    def display_flag_amount(self):
        pg.font.init()
        font = pg.font.Font(st.font_name,st.tile_multiplier)
        flag_amount_image = font.render('Flags left: {}'.format(self.flags),True,st.font_color['flags'])
        flag_amount_pos = (0,0)
        self.screen.blit(flag_amount_image, flag_amount_pos)

    def display(self):
        self.screen.fill('black')
        self.display_tiles()
        self.display_flag_amount()
        pg.display.update()

    def status(self):
        if self.force_loss:
            return 'EndingLoss'
        elif self.force_win:
            return 'EndingWin'
        tiles_bomb = [tile for tile in self.tiles if tile.get_identity() == 'B']
        for tile_bomb in tiles_bomb:
            if tile_bomb.get_opened():
                sleep(1)
                return 'EndingLoss'
        for tile_bomb in tiles_bomb:
            if not tile_bomb.get_flagged():
                return None
        sleep(1)
        return 'EndingWin'



class EndingWin(Screen):

    def __init__(self,screen_size):
        self.screen_size = screen_size

        self.running = True
        self.message = 'YOU WIN'
        self.go_again = False
        self.screen = pg.display.set_mode( size = self.screen_size)
        self.create_win_screen()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = 'quit'
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.play_button.rect.collidepoint(pg.mouse.get_pos()):
                    self.go_again = True

    def create_win_screen(self):
        font = pg.font.Font(st.font_name, self.screen_size[0])
        self.text_image = font.render(self.message, True, st.font_color['ending'])

        self.gj1_image = pg.image.load(st.gj1_path)
        self.gj1_image = pg.transform.scale(self.gj1_image, (
        self.gj1_image.get_size()[0] // 2, self.gj1_image.get_size()[1] // 2))
        self.gj1_rect = self.gj1_image.get_rect()
        self.gj1_rect.center = (647, 225)

        self.gj2_image = pg.image.load(st.gj2_path)
        self.gj2_image = pg.transform.scale(self.gj2_image, (
        self.gj2_image.get_size()[0] // 2, self.gj2_image.get_size()[1] // 2))
        self.gj2_rect = self.gj2_image.get_rect()
        self.gj2_rect.center = (83, 192)

        self.gj3_image = pg.image.load(st.gj3_path)
        self.gj3_image = pg.transform.scale(self.gj3_image, (
        self.gj3_image.get_size()[0] // 2, self.gj3_image.get_size()[1] // 2))
        self.gj3_rect = self.gj3_image.get_rect()
        self.gj3_rect.center = (636, 714)

        self.text_image = pg.transform.scale(self.text_image, size= (st.screen_size[0], 100))
        self.play_button = PlayAgainButton(st.screen_size[0] // 2,
                                           st.screen_size[1] // 2,
                                           64,
                                           self.screen,
                                           'Click to go again')

    def display(self):
        self.screen.fill('green')
        self.screen.blit(self.text_image,(0,0))

        self.screen.blit(self.gj1_image, self.gj1_rect)
        self.screen.blit(self.gj2_image, self.gj2_rect)
        self.screen.blit(self.gj3_image, self.gj3_rect)

        self.play_button.draw()
        pg.display.update()

    def status(self):
        if self.go_again:
            return 'Playing'
        return None



class EndingLoss(Screen):

    def __init__(self, screen_size):
        self.screen_size = screen_size

        self.running = True
        self.message = 'YOU LOST'
        self.try_again = False
        self.screen = pg.display.set_mode(size=self.screen_size)
        self.create_loss_screen()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = 'quit'
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.play_button.rect.collidepoint(pg.mouse.get_pos()):
                    self.try_again = True
                else:
                    print(pg.mouse.get_pos())

    def create_loss_screen(self):
        pg.font.init()
        font = pg.font.Font(st.font_name, self.screen_size[0])
        self.text_image = font.render(self.message, True, st.font_color['ending'])
        self.text_image = pg.transform.scale(self.text_image, size= (st.screen_size[0], 100))

        self.lmao1_image = pg.image.load(st.lmao1_path)
        self.lmao1_image = pg.transform.scale(self.lmao1_image,(self.lmao1_image.get_size()[0] // 2, self.lmao1_image.get_size()[1] // 2))
        self.lmao1_rect = self.lmao1_image.get_rect()
        self.lmao1_rect.center = (647, 225)

        self.lmao2_image = pg.image.load(st.lmao2_path)
        self.lmao2_image = pg.transform.scale(self.lmao2_image,(self.lmao2_image.get_size()[0] // 2, self.lmao2_image.get_size()[1] // 2))
        self.lmao2_rect = self.lmao2_image.get_rect()
        self.lmao2_rect.center = (83, 192)

        self.lmao3_image = pg.image.load(st.lmao3_path)
        self.lmao3_image = pg.transform.scale(self.lmao3_image, (self.lmao3_image.get_size()[0] // 2, self.lmao3_image.get_size()[1] // 2))
        self.lmao3_rect = self.lmao3_image.get_rect()
        self.lmao3_rect.center = (636, 714)

        self.play_button = PlayAgainButton(st.screen_size[0] // 2,
                                           st.screen_size[1] //2,
                                           64,
                                           self.screen,
                                           'Click to try again')

    def display(self):
        self.screen.fill('red')
        self.screen.blit(self.text_image, (0, 0))
        self.screen.blit(self.lmao1_image, self.lmao1_rect)
        self.screen.blit(self.lmao2_image, self.lmao2_rect)
        self.screen.blit(self.lmao3_image, self.lmao3_rect)
        self.play_button.draw()
        pg.display.update()

    def status(self):
        if self.try_again:
            return 'Playing'
        return None