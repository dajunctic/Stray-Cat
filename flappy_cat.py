import math
import random

from object import Anim
from script.settings import *
from script.text import Dialogue


class FlappyCat:
    def __init__(self, app):
        self.app = app
        self.surface = self.app.surface

        self.stage = Stage(self.app)

        self.start = False
        self.finish = False

    def load(self):
        self.start = True

    def update(self):
        self.stage.update()
        if self.stage.finished:
            self.finish = True

    def draw(self):
        self.stage.draw()

    def handle_event(self, e):
        self.stage.handle_event(e)


class Stage:
    def __init__(self, app):
        self.app = app
        self.surface = app.surface

        self.endless_bg = EndlessBackground(self.app, 'assets/img/flappy_cat/bg.jpg')

        self.rect1 = pg.Rect(800, -200, 100, 400)
        self.rect2 = pg.Rect(800, 520, 100, 400)

        self.cache_info = CACHE['flappy_cat']['obstacle']
        self.portal_info = CACHE['flappy_cat']['portal']
        self.cat_info = CACHE['flappy_cat']['cat']

        self.portal = None
        self.cat = None

        self.obstacle_img = []
        for obs in self.cache_info.keys():
            self.obstacle_img.append(pg.image.load(self.cache_info[obs]).convert_alpha())

        self.obstacles = []

        self.make_obstacles()

        self.dialogue = Dialogue(self, 'assets/text/flappy_cat.txt')

        self.finished = False

        self.loading = Anim(self.app, CACHE['loading']['path'], CACHE['loading']['num_frames'],
                            repeat=2, scale=1.6, delta=50)

        self.hack = False

    def make_obstacles(self):
        self.obstacles = []
        start_x = 500

        for i in range(5):
            if i & 1:
                self.obstacles.append(FixedObs(self.app, self, start_x))
            else:
                self.obstacles.append(MoveObs(self.app, self, start_x, 1))
            start_x += 300

        for i in range(5):
            self.obstacles.append(MoveObs(self.app, self, start_x, 0))
            start_x += 300

        for i in range(2):
            if i & 1:
                self.obstacles.append(ElevatorObs(self.app, self, start_x, False))
            else:
                self.obstacles.append(ElevatorObs(self.app, self, start_x, True))
            start_x += 500

        for i in range(2):
            if i & 1:
                self.obstacles.append(ThornObs(self.app, self, start_x))
            else:
                self.obstacles.append(ThornObs(self.app, self, start_x, True))

            start_x += 600

        start_x += 1200
        self.portal = Portal(self.app, self, start_x)
        self.obstacles.append(self.portal)

        self.cat = BotCat(self.app, self, 100)
        self.obstacles.append(self.cat)

    def update(self):

        if self.loading.is_finished():
            self.finished = True

        if self.endless_bg.stopped:
            self.dialogue.update()

        self.endless_bg.update()

        for obs in self.obstacles:
            obs.update()

        if self.cat.x >= 980 and not self.loading.is_finished():
            self.loading.update()

        if self.cat.die:
            self.make_obstacles()
            # self.cat.reset()

    def draw(self):
        self.endless_bg.draw()
        for obs in self.obstacles:
            obs.draw()

        if self.endless_bg.stopped and not self.dialogue.is_finished():
            self.dialogue.draw()

        if self.cat.x >= 980 and not self.loading.is_finished():
            self.surface.blit(self.loading.get_img(), (0, - (960 - 720) // 2))

    def handle_event(self, e):
        if self.endless_bg.stopped:
            self.dialogue.handle_event(e)
        else:
            self.cat.handle_event(e)


class BotCat:
    def __init__(self, app, stage, x):
        self.app = app
        self.surface = app.surface
        self.stage = stage

        scale = 0.25
        self.img = pg.image.load(self.stage.cat_info['path']).convert_alpha()
        self.img = pg.transform.scale(self.img, (scale * self.img.get_width(), scale * self.img.get_height()))
        self.cat_mask = pg.mask.from_surface(self.img)

        self.x = x
        self.y = 100

        self.SPEEDFLY = -500
        self.speed = 0
        self.g = 8

        self.die = False

    def reset(self):
        self.die = False

    def check_collisions(self):
        for obs in self.stage.obstacles:
            if isinstance(obs, Obstacle):

                for i in range(len(obs.masks)):
                    pos = obs.get_pos()

                    offset_x = pos[i][0] - self.x
                    offset_y = pos[i][1] - self.y

                    if self.cat_mask.overlap(obs.masks[i], (offset_x, offset_y)):
                        return True

        return False

    def update(self):
        if not self.stage.hack and self.check_collisions():
            self.die = True
        if self.y + self.img.get_height() > 720:
            self.die = True

        if self.stage.endless_bg.stopped:
            self.y = 450

            if self.stage.dialogue.is_finished() and self.x < 980:
                self.x += 400 * self.app.delta_time
        else:

            self.y += (self.speed + 0.5 * self.g) * self.app.delta_time
            self.speed += self.g

            if self.y < 0:
                self.speed = 0
                self.y = 0

    def draw(self):
        self.surface.blit(self.img, (self.x, self.y))

    def handle_event(self, e):
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_SPACE:
                self.speed = self.SPEEDFLY
            if e.key == pg.K_q:
                self.stage.hack = not self.stage.hack


class Portal:
    def __init__(self, app, stage, x):
        self.app = app
        self.surface = app.surface
        self.stage = stage
        self.path = self.stage.portal_info['path']
        self.num_frames = self.stage.portal_info['num_frames']

        self.x = x
        self.y = 270
        self.anim = Anim(app, path=self.path, num_frames=self.num_frames, scale=2)

    def update(self):
        if self.x > 800:
            self.x -= 100 * self.app.delta_time
        else:
            self.stage.endless_bg.stop()

        self.anim.update()

    def draw(self):
        self.surface.blit(self.anim.get_img(), (self.x, self.y))


class Obstacle:
    FIXED = 0
    UPDOWN = 1

    TOTAL = 2

    def __init__(self, app, stage, x):
        self.masks = None
        self.app = app
        self.surface = self.app.surface
        self.stage = stage

        self.x = x
        self.y = 0

        self.space = 0
        self.scale = 8

        self.horizontal_v = 100
        self.vertical_v = 1

        self.cur_tick = 0
        self.prev_tick = 0
        self.interval = 25

    def update(self):
        pass

    def draw(self):
        pass

    def get_pos(self):
        return [(0, 0)]


class FixedObs(Obstacle):
    def __init__(self, app, stage, x):
        super().__init__(app, stage, x)

        self.scale = 1
        self.img = self.stage.obstacle_img[3]
        self.flip_img = pg.transform.flip(self.img, False, True).convert_alpha()

        self.masks = []
        self.masks.append(pg.mask.from_surface(self.img))
        self.masks.append(pg.mask.from_surface(self.flip_img))

        self.preprocess()

    def update(self):
        self.x -= self.horizontal_v * self.app.delta_time

    def preprocess(self):
        w, h = self.img.get_width(), self.img.get_height()

        self.img = pg.transform.scale(self.img, (w * self.scale, h * self.scale))

        self.y = random.randint(200, 500)
        self.space = random.randint(200, 250)

    def draw(self):
        self.surface.blit(self.img, (self.x, self.y - self.img.get_height()))
        self.surface.blit(self.flip_img, (self.x, self.y + self.space))

    def get_pos(self):
        return [
            (self.x, self.y - self.img.get_height()),
            (self.x, self.y + self.space)
        ]


class MoveObs(Obstacle):
    def __init__(self, app, stage, x, obs_type=0):
        super().__init__(app, stage, x)
        self.max_y = None
        self.min_y = None
        self.img = self.stage.obstacle_img[3]
        self.flip_img = pg.transform.flip(self.img, False, True).convert_alpha()

        self.masks = []
        self.masks.append(pg.mask.from_surface(self.img))
        self.masks.append(pg.mask.from_surface(self.flip_img))

        self.scale = 1
        self.max_x = 600

        self.type = obs_type

        self.y1 = 0
        self.y2 = 0

        self.max_y1 = 0
        self.max_y2 = 0

        self.dist = 200

        self.vertical_v = 200 if self.type == 0 else 100
        self.horizontal_v = 100
        self.preprocess()

    def preprocess(self):
        w, h = self.img.get_width(), self.img.get_height()

        self.img = pg.transform.scale(self.img, (w * self.scale, h * self.scale))

        if self.type == 0:

            self.max_y1 = random.randint(200, 400) - self.img.get_height()
            self.space = random.randint(200, 250)
            self.max_y2 = self.max_y1 + self.img.get_height() + self.space

            self.y1 = self.max_y1 - self.dist
            self.y2 = self.max_y2 + self.dist

        else:
            self.space = 250
            self.dist = random.randint(200, 300)
            self.y = 360 - self.img.get_height() - self.space // 2
            self.min_y = self.y - self.dist // 2
            self.max_y = self.y + self.dist // 2

            self.y += random.randint(-100, 100)

    def update(self):
        self.x -= self.horizontal_v * self.app.delta_time

        if self.type == 0:
            if self.x < self.max_x:

                if self.y1 < self.max_y1:
                    self.y1 += self.vertical_v * self.app.delta_time

                if self.y2 > self.max_y2:
                    self.y2 -= self.vertical_v * self.app.delta_time

        else:
            if self.y < self.min_y or self.y > self.max_y:
                self.vertical_v = -self.vertical_v

            self.y += self.vertical_v * self.app.delta_time

    def draw(self):
        if self.type == 0:
            self.surface.blit(self.img, (self.x, self.y1))
            self.surface.blit(self.flip_img, (self.x, self.y2))
        else:
            self.surface.blit(self.img, (self.x, self.y))
            self.surface.blit(self.flip_img, (self.x, self.y + self.space + self.img.get_height()))

    def get_pos(self):
        if self.type == 0:
            return [
                (self.x, self.y1),
                (self.x, self.y2)
            ]
        else:
            return [
                (self.x, self.y),
                (self.x, self.y + self.space + self.img.get_height())
            ]


class ElevatorObs(Obstacle):
    def __init__(self, app, stage, x, down):
        super().__init__(app, stage, x)

        self.scale = 2.5
        self.img = pg.transform.rotate(self.stage.obstacle_img[1], 90).convert_alpha()
        self.down_img = pg.transform.rotate(self.stage.obstacle_img[0], 90).convert_alpha()

        self.down = down

        self.masks = []
        if not self.down:
            self.masks.append(pg.mask.from_surface(self.img))
        else:
            self.masks.append(pg.mask.from_surface(self.down_img))

        self.pos = []
        self.y = -2000
        self.space = 250

        self.vertical_v = 100
        if not down:
            self.vertical_v = -100

        self.preprocess()

    def preprocess(self):
        w, h = self.img.get_width(), self.img.get_height()

        self.img = pg.transform.scale(self.img, (w * self.scale, h * self.scale))
        self.down_img = pg.transform.scale(self.down_img, (w * self.scale, h * self.scale))

        for i in range(20):
            self.pos.append(self.y + self.space * i)

    def update(self):
        self.x -= self.horizontal_v * self.app.delta_time

        if self.x < 1280:
            for i in range(len(self.pos)):
                self.pos[i] += self.vertical_v * self.app.delta_time

    def draw(self):
        for y in self.pos:
            if y > -200:
                if self.down:
                    self.surface.blit(self.img, (self.x, y))
                else:
                    self.surface.blit(self.down_img, (self.x, y))

    def get_pos(self):
        return [(self.x, y) for y in self.pos]


class ThornObs(Obstacle):
    def __init__(self, app, stage, x, top=False):
        super().__init__(app, stage, x)
        self.img = self.stage.obstacle_img[2]
        self.flip_img = pg.transform.flip(self.img, False, True).convert_alpha()

        self.scale = 1
        self.scale_v = 1
        self.max_scale = 200

        self.cache = []
        self.height = []

        for i in range(10, self.max_scale, self.scale_v):
            sc = i / 10
            self.cache.append((pg.transform.scale(self.img, [sc * self.img.get_width(),
                                                             sc * self.img.get_height()]),
                               pg.transform.scale(self.flip_img, [sc * self.flip_img.get_width(),
                                                                  sc * self.flip_img.get_height()])))

            self.height.append((self.cache[-1][0].get_height(), self.cache[-1][1].get_height()))

        self.masks = []
        if top:
            self.masks.append(pg.mask.from_surface(self.cache[-1][0]))
        else:
            self.masks.append(pg.mask.from_surface(self.cache[-1][1]))

        self.cur = 0
        self.float_cur = 0
        self.cur_v = 40

        self.top = top

    def update(self):
        self.x -= self.horizontal_v * self.app.delta_time

        if self.x < 800:
            if self.cur < len(self.cache) - 1:
                self.float_cur += self.cur_v * self.app.delta_time
                self.cur = int(self.float_cur)

    def draw(self):

        if self.top:
            self.surface.blit(self.cache[self.cur][1], (self.x, 0))
        else:

            self.surface.blit(self.cache[self.cur][0], (self.x, HEIGHT - self.height[self.cur][0]))

    def get_pos(self):
        if self.top:
            return [(self.x, 0)]
        else:
            return [(self.x, HEIGHT - self.height[-1][0])]


class EndlessBackground:
    def __init__(self, game_app, path):
        self.app = game_app
        self.surface = self.app.surface

        self.bg = pg.image.load(path).convert()
        self.bg_width = self.bg.get_width()
        self.scroll = 0  # velocity
        self.tiles = math.ceil(WIDTH / self.bg_width) + 1

        self.scroll_v = 300  # pixel / s

        self.stopped = False

    def update(self):
        if self.stopped:
            return

        self.scroll -= self.scroll_v * self.app.delta_time

        if abs(self.scroll) > self.bg_width:
            self.scroll = 0

    def draw(self):
        for i in range(self.tiles):
            self.surface.blit(self.bg, (i * self.bg_width + self.scroll, 0))

    def stop(self):
        self.stopped = True
