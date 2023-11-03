import pygame as pg


class Object:
    TOP_LEFT = 0
    TOP_RIGHT = 1
    CENTER = 2
    BOT_LEFT = 3
    BOT_RIGHT = 4

    def __init__(self, app, x=0, y=0, path="", scale=1):
        self.app = app
        self.surface = app.surface
        self.x = x
        self.y = y

        self.rect = None
        self.align = Object.TOP_LEFT

        self.img = pg.image.load(path).convert_alpha()

        self.w = self.img.get_width()
        self.h = self.img.get_height()

        self.size = pg.math.Vector2(self.w, self.h)
        self.img = pg.transform.scale(self.img, self.size * scale)

        self.w, self.h = self.img.get_width(), self.img.get_height()
        self.hidden = False

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def set_img(self, img):
        self.img = img

    def get_rect(self):
        return pg.Rect(self.x, self.y, self.w, self.h)

    def update(self):
        pass

    def draw(self):
        if self.hidden:
            return

        if self.align == Object.CENTER:
            self.surface.blit(self.img, (self.x - self.w // 2, self.y - self.h // 2))
        else:
            self.surface.blit(self.img, (self.x, self.y))

    def hide(self):
        self.hidden = True

class Tile(Object):
    def __init__(self, app, x=0, y=0, path="", scale=1):
        super().__init__(app,x, y, path, scale)


class Anim:
    def __init__(self, app, path, num_frames, scale=1, delta=100, repeat=-1):
        self.app = app
        self.path = path

        self.num_frames = num_frames
        self.cur = 0
        self.cnt = 0

        self.repeat = repeat
        self.run = repeat

        self.images = []
        self.flip_images = []

        self.scale = scale
        self.delta = delta

        self.load()

    def load(self):
        img = pg.image.load(self.path).convert_alpha()
        width = img.get_width()
        height = img.get_height()

        for i in range(self.num_frames):
            x = i * width // self.num_frames
            y = 0
            w = width // self.num_frames
            h = height

            subimg = img.subsurface((x, y, w, h))
            subimg = pg.transform.scale(subimg, (self.scale * subimg.get_width(),
                                                           self.scale * subimg.get_height()))

            flip_img = pg.transform.flip(subimg, True, False)

            self.images.append(subimg)
            self.flip_images.append(flip_img)

    def reload(self):
        self.run = self.repeat

    def update(self):
        self.cnt += self.app.delta_time

        if self.cnt >= self.delta / 1000:
            self.cnt = 0

            self.cur += 1
            self.cur %= self.num_frames

            if self.cur == 0 and self.repeat > 0:
                self.run -= 1

    def get_img(self):
        return self.images[self.cur]

    def get_img_flip(self):
        return self.flip_images[self.cur]

    def is_finished(self):
        return self.run == 0
