from cat import Cat, Bot
from flappy_cat import FlappyCat
from object import Object, Anim, Tile
from script.text import Dialogue
from whach_a_mole import WhachAMole
from script.settings import *


class Gameplay:
    def __init__(self, app):
        self.app = app
        self.surface = self.app.surface

        self.cat = Cat(app, self)
        self.bot = Bot(app, self)

        self.game_box = Object(self.app, 50, 380, "assets/img/obj/game_machine.png")
        self.battery = Object(self.app, 50, 100, 'assets/img/obj/pin.png',scale=0.2)

        self.objects = [
            Tile(self.app, 900, 400, 'assets/img/obj/obj.png', scale=0.3),
            Tile(self.app, 450, 300, 'assets/img/obj/obj1.png', scale=0.6),
            Tile(self.app, 0, 200, 'assets/img/obj/obj2.png', scale=0.3),
            self.battery,
            self.game_box
        ]

        self.whach = WhachAMole(self.app)
        self.flappy = FlappyCat(self.app)

        self.bg_img = [
            pg.image.load('assets/img/bg/street.jpg').convert_alpha(),
            pg.image.load('assets/img/bg/forest.jpg').convert_alpha(),
            pg.image.load('assets/img/bg/end.png').convert_alpha(),
        ]
        self.cur_bg = 0

        self.dialogues = [
            Dialogue(self, 'assets/text/1.txt'),
            Dialogue(self, 'assets/text/2.txt'),
            Dialogue(self, 'assets/text/3.txt'),
            Dialogue(self, 'assets/text/4.txt')
        ]

        self.cur_dlg = 0
        self.dlg_active = False

        # self.whach.load()
        # self.flappy.load()
        self.mng_active = False
        self.minigame = [self.whach, self.flappy]

        self.duty = Duty(app, self)

        self.ending = False

    def update(self):
        if self.duty.is_ready():
            self.duty.start_task()
        elif self.duty.check_task():
            self.duty.finish_task()

        if self.mng_active:
            for g in self.minigame:
                if g.start and not g.finish:
                    g.update()
        else:
            self.bot.update()
            self.cat.update()

            for obj in self.objects:
                obj.update()

            if self.dlg_active:
                self.dialogues[self.cur_dlg].update()

    def draw(self):
        if self.mng_active:
            for g in self.minigame:
                if g.start and not g.finish:
                    g.draw()
        else:
            self.surface.blit(self.bg_img[self.cur_bg], (0, 0))

            for obj in self.objects:
                obj.draw()

            self.bot.draw()
            self.cat.draw()

            if self.dlg_active:
                self.dialogues[self.cur_dlg].draw()

            if self.ending:
                self.surface.blit(self.bg_img[2], (0, 0))

    def handle_event(self, e):
        if self.mng_active:
            for g in self.minigame:
                if g.start and not g.finish:
                    g.handle_event(e)
        else:

            self.cat.handle_event(e)

            if self.dlg_active:
                self.dialogues[self.cur_dlg].handle_event(e)

            if self.ending:
                if e.type == pg.MOUSEBUTTONDOWN:
                    self.app.manager.set_scene(self.app.manager.MENU)


class Duty:
    def __init__(self, app, scene):
        self.app = app
        self.scene = scene
        self.cur_task = 0
        self.ready = True

    def start_task(self):
        self.ready = False

        match self.cur_task:

            # Hiện thị đoạn text thứ nhất - Robot kêu cứu
            case 0:
                self.scene.dlg_active = True
                return

            # Lấy cục pin
            case 1:
                pass

            # Đưa con robot
            case 2:
                self.scene.cur_dlg = 1
                self.scene.bot.interact = True

            # Trò chuyện và đưa vào minigame 1, tiếp xúc với máy trò chơi
            case 3:
                self.scene.dlg_active = True
                self.scene.cur_dlg = 2

            case 4:
                self.scene.dlg_active = True
                self.scene.cur_dlg = 3

            case 5:
                for obj in self.scene.objects:
                    obj.hide()
                self.scene.cur_bg = 1
                self.scene.ending = True

    def check_task(self):
        match self.cur_task:

            case 0:
                return self.scene.dialogues[0].is_finished()

            case 1:
                return self.scene.cat.rect.colliderect(self.scene.battery.get_rect())

            case 2:
                if self.scene.cat.rect.colliderect(self.scene.bot.get_rect()):
                    self.scene.dlg_active = True

                if self.scene.dialogues[1].is_finished():
                    self.scene.dlg_active = False
                    self.scene.bot.move()

                return self.scene.bot.active

            case 3:
                if self.scene.dialogues[2].is_finished():
                    self.scene.dlg_active = False

                if self.scene.cat.rect.colliderect(self.scene.game_box.get_rect()):
                    self.scene.mng_active = True
                    self.scene.cat.move = False
                    self.scene.whach.load()

                if self.scene.whach.finish:
                    self.scene.mng_active = False

                return self.scene.whach.finish

            case 4:
                if self.scene.dialogues[3].is_finished():
                    self.scene.dlg_active = False

                    self.scene.mng_active = True
                    self.scene.flappy.load()

                if self.scene.flappy.finish:

                    self.scene.mng_active = False

                return self.scene.flappy.finish

    def finish_task(self):
        match self.cur_task:

            case 0:
                self.scene.dlg_active = False
                self.scene.cur_dlg += 1

            case 1:
                self.scene.battery.hide()

            case 2:
                pass

            case 3:
                pass

            case 4:
                pass

        self.cur_task += 1
        self.ready = True

    def is_ready(self):
        return self.ready
