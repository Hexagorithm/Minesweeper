import pygame as pg
import settings as st

class Tile(pg.sprite.Sprite):
    def __init__(self,
                 tile_size_multiplier,
                 surface,
                 x,
                 y,
                 identity,
                 if_opened,
                 if_flagged):
        super().__init__()
        self.multiplier = tile_size_multiplier
        self.surface = surface
        self.x = x
        self.y = y
        self.identity = identity
        self.is_opened = if_opened
        self.is_flagged = if_flagged

        self.flag_path = st.flag_path
        self.opened_tile_dark = st.opened_tile_dark
        self.opened_tile_light = st.opened_tile_light
        self.unopened_tile_dark = st.unopened_tile_dark
        self.unopened_tile_light = st.unopened_tile_light
        self.create_tile()
        self.create_flag()

    def get_position(self):
        return (self.x, self.y)

    def get_identity(self):
        return self.identity

    def get_opened(self):
        return self.is_opened

    def get_flagged(self):
        return self.is_flagged

    def create_tile(self):
        if (self.x + self.y) % 2 == 1:
            image_path = self.unopened_tile_light
        else:
            image_path = self.unopened_tile_dark
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, size = (self.multiplier, self.multiplier))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * self.multiplier, self.y * self.multiplier + st.menu_bar_size)
        print('Tile was created with topleft: {}'.format((self.x * self.multiplier, self.y * self.multiplier + st.menu_bar_size)))

    def create_identity(self):
        if self.identity == '0' :
            pass
        elif self.identity == 'B':
            self.identity_image = pg.image.load(st.bomb_path).convert_alpha()
            self.identity_image = pg.transform.scale(self.identity_image, size=(self.multiplier, self.multiplier))
        else:
            pg.font.init()
            font = pg.font.Font(st.font_name, self.multiplier)
            self.identity_image = font.render(self.identity, True, st.font_color[self.identity])
            self.identity_image = pg.transform.scale(self.identity_image, size=(self.multiplier,self.multiplier))

    def create_flag(self):
        self.flag_image = pg.image.load(self.flag_path)
        self.flag_image = pg.transform.scale(self.flag_image, size=(self.multiplier, self.multiplier))

    def if_can_open(self):
        if self.is_opened == False and self.is_flagged == False:
            return True
        else:
            return False

    def if_can_flag(self):
        if self.is_opened == False and self.is_flagged == False:
            return True
        else:
            return False

    def if_can_unflag(self):
        if self.is_opened == False and self.is_flagged == True:
            return True
        else:
            return False

    def open(self):
        if not self.is_flagged:
            self.is_opened = True
            if (self.x + self.y) % 2 == 1:
                image_path = self.opened_tile_light
            else:
                image_path = self.opened_tile_dark
            self.image = pg.image.load(image_path).convert_alpha()
            self.image = pg.transform.scale(self.image, size = (self.multiplier, self.multiplier))
            self.create_identity()

    def flag(self):
        self.is_flagged = True

    def unflag(self):
        self.is_flagged = False

    def __repr__(self):
        return 'Tile({}, {}, {}, {}, {}, {}, {})'.format(self.multiplier,
        self.surface,
        self.x,
        self.y,
        self.identity,
        self.is_opened,
        self.is_flagged,)

    def draw(self):
        self.surface.blit(self.image, self.rect)
        if self.is_flagged:
            self.surface.blit(self.flag_image, self.rect)
        if self.is_opened and self.identity != '0' :
            self.surface.blit(self.identity_image, self.rect)

class PlayAgainButton(pg.sprite.Sprite):

    def __init__(self,x,y,font_size,surface, message):
        super().__init__()
        self.x = x
        self.y = y
        self.font_size = font_size
        self.surface = surface
        self.message = message

        self.button_image_path = st.play_again_button_path
        self.size = (200, 50)
        self.font = pg.font.Font(st.font_name, self.font_size)
        self.create_button()

    def create_button(self):
        self.button_image = pg.image.load(self.button_image_path)
        self.button_image = pg.transform.scale(self.button_image,self.size)
        self.rect = self.button_image.get_rect()
        self.rect.center = (self.x, self.y)

        self.text_image = self.font.render(self.message,True,st.font_color['message'])
        self.text_image = pg.transform.scale(self.text_image, self.size)

    def draw(self):
        self.surface.blit(self.button_image,self.rect)
        self.surface.blit(self.text_image,self.rect)


