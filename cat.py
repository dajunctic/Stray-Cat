from object import Anim, Tile
from script.physics import is_collision_bottom, is_collision_top, is_collision_left, is_collision_right
from script.settings import *


class Cat:
    IDLE = 'idle'
    WALK = 'walk'
    JUMP = 'jump'
    MEOW = 'meow'

    def __init__(self, app, scene):
        self.app = app
        self.surface = app.surface
        self.scene = scene

        self.x = 100
        self.y = 440
        self.limit_y = 440
        self.gravity = 200
        self.alpha_g = 0.4

        self.is_gravity = True

        self.fixed_vx = 200
        self.vx = self.fixed_vx
        self.jump_height = 1000
        self.vy = self.jump_height

        self.move = False
        self.left = False
        self.jump = False

        self.anims = {}

        self.cache = CACHE['cat']

        for act in self.cache.keys():
            path = self.cache[act]['path']
            num_frames = self.cache[act]['num_frames']
            scale = self.cache[act]['scale']
            self.anims[act] = Anim(self.app, path, num_frames, scale=scale)

        self.act = Cat.IDLE

        self.rect = pg.Rect(self.x + 100, self.y + 120, self.get_size()[0] - 180, self.get_size()[1] - 240)

    def get_size(self):
        return self.anims[self.act].get_img().get_width(), self.anims[self.act].get_img().get_height()

    def update(self):
        prev_x = self.x
        prev_y = self.y
        if self.move:
            self.x += self.vx * self.app.delta_time

        if self.jump:
            self.y -= self.vy * self.app.delta_time
            self.vy -= 900 * self.app.delta_time
            self.vy = max(0, self.vy)

        if self.is_gravity:
            self.y += self.gravity * self.app.delta_time
            self.gravity += self.alpha_g

        if self.y > self.limit_y:
            self.jump = False
            self.y = self.limit_y
            self.gravity = 200
            self.vy = self.jump_height

        self.rect = pg.Rect(self.x + 100, self.y + 120, self.get_size()[0] - 180, self.get_size()[1] - 240)

        for obj in self.scene.objects:
            flag = True
            if isinstance(obj, Tile):
                if self.rect.colliderect(obj.get_rect()):
                    if self.jump:
                        if is_collision_bottom(rect1=self.rect, rect2=obj.get_rect()):
                            self.gravity = 200
                            self.vy = 0
                        elif is_collision_top(rect1=self.rect, rect2=obj.get_rect()):
                            self.is_gravity = False
                            self.jump = False
                            flag = False
                        elif is_collision_left(rect1=self.rect, rect2=obj.get_rect()) or \
                                is_collision_right(rect1=self.rect, rect2=obj.get_rect()):
                            self.x = prev_x
                    else:
                        if is_collision_top(rect1=self.rect, rect2=obj.get_rect()):
                            self.is_gravity = False
                            flag = False
                            self.y = prev_y
                            self.gravity = 200
            if flag:
                self.is_gravity = True

        self.rect = pg.Rect(self.x + 100, self.y + 120, self.get_size()[0] - 180, self.get_size()[1] - 240)

        self.anims[self.act].update()


    def draw(self):
        if self.left:
            self.surface.blit(self.anims[self.act].get_img_flip(), (self.x, self.y))
        else:
            self.surface.blit(self.anims[self.act].get_img(), (self.x, self.y))

        # pg.draw.rect(self.surface, (255, 255, 255), self.rect, width=2)

    def handle_event(self, e):
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_d:
                self.left = False
                self.move = True
                self.vx = self.fixed_vx
                self.act = Cat.WALK
            if e.key == pg.K_a:
                self.left = True
                self.move = True
                self.vx = -self.fixed_vx
                self.act = Cat.WALK

            if e.key == pg.K_w or e.key == pg.K_SPACE:
                if not self.jump:
                    self.vy = self.jump_height

                self.jump = True



        if e.type == pg.KEYUP:
            if e.key in (pg.K_d, pg.K_a):
                self.move = False
                self.act = Cat.IDLE

    def interact(self):
        pass


class Bot:
    IDLE = 'idle'
    LEFT = 'left'
    RIGHT = 'right'

    def __init__(self, app, scene):
        self.app = app
        self.surface = self.app.surface
        self.scene = scene

        self.x = 1100
        self.y = 600

        self.vx = 0
        self.vy = 0

        self.imgs = {}
        self.act = Bot.IDLE

        self.cache = CACHE['bot']
        for stt in self.cache.keys():
            path = self.cache[stt]['path']
            img = pg.image.load(path)
            scale = 0.25
            size = pg.math.Vector2(img.get_width(), img.get_height())

            img = pg.transform.scale(img, scale * size)

            self.imgs[stt] = img

        self.gray_img = pg.transform.grayscale(self.imgs[Bot.IDLE])
        self.w, self.h = self.gray_img.get_size()
        self.active = False

        self.question = Anim(self.app, 'assets/img/bot/question.png', num_frames=3, scale=0.08)

        self.cat = self.scene.cat

        self.interact = True

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.x += self.vx * self.app.delta_time
        self.y += self.vy * self.app.delta_time

        if self.active:
            self.x = self.cat.x + 150
            self.y = self.cat.y

            if self.cat.move:
                if self.cat.left:
                    self.act = Bot.LEFT
                else:
                    self.act = Bot.RIGHT

            else:
                self.act = Bot.IDLE

        self.question.update()

    def get_rect(self):
        return pg.Rect(self.x, self.y, self.w, self.h)

    def draw(self):
        if self.active:
            self.surface.blit(self.imgs[self.act], (self.x, self.y))
        else:
            self.surface.blit(self.gray_img, (self.x, self.y))
            self.surface.blit(self.question.get_img(), (self.x + 20, self.y - 40))

    def move(self):
        self.x = self.cat.x + 150
        self.y = self.cat.y
        self.active = True
