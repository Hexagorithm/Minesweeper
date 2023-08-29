import pygame as pg
import settings as st

class Tile(pg.sprite.Sprite):
    def __init__(self, tile_size_multiplier, surface, x, y, identity, if_opened, if_flagged):
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

    def create_tile(self):
        if (self.x + self.y) % 2 == 1:
            image_path = self.unopened_tile_light
        else:
            image_path = self.unopened_tile_dark
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, size = (self.multiplier, self.multiplier))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * self.multiplier, self.y * self.multiplier + st.menu_bar_size)
        print('Tile was created wit topleft: {}'.format((self.x * self.multiplier, self.y * self.multiplier + st.menu_bar_size)))

    def create_identity(self):
        pg.font.init()
        font = pg.font.Font(st.font_name, self.multiplier)
        self.identity_image = font.render(self.identity, True, st.font_color[self.identity])
        self.identity_image = pg.transform.scale(self.identity_image, size=(self.multiplier, self.multiplier))

    def create_flag(self):
        self.flag_image = pg.image.load(self.flag_path)
        self.flag_image = pg.transform.scale(self.flag_image, size=(self.multiplier, self.multiplier))

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
        if self.is_opened:
            self.surface.blit(self.identity_image, self.rect)

