import math

from gameplay import Gameplay
from menu import Menu
from script.settings import *


class Manager:
    MENU = 0
    GAMEPLAY = 1

    def __init__(self):
        self.scene = Manager.GAMEPLAY
        self.functions = {}

    def add(self, scene, function):
        self.functions[scene] = function

    def get(self):
        return self.functions[self.scene]

    def set_scene(self, scene):
        self.scene = scene


class App:
    def __init__(self):
        pg.init()
        pg.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

        self.surface = pg.display.set_mode(RESOLUTION)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.delta_time = 0

        self.manager = Manager()

        self.menu = Menu(self)
        self.manager.add(Manager.MENU, self.menu)

        self.gameplay = Gameplay(self)
        self.manager.add(Manager.GAMEPLAY, self.gameplay)

    def run(self):
        loop = True
        tick_last_frame = 0

        while loop:
            t = pg.time.get_ticks()
            self.delta_time = (t - tick_last_frame) / 1000.0
            tick_last_frame = t

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    loop = False

                self.manager.get().handle_event(e)

            self.update()
            self.draw()

            self.clock.tick()
            pg.display.flip()

        pg.quit()

    def update(self):
        pg.display.set_caption(TITLE + " " + str(int(self.clock.get_fps())))
        self.manager.get().update()
        pass

    def draw(self):
        self.surface.fill((0, 0, 0))

        self.manager.get().draw()


if __name__ == '__main__':
    app = App()
    app.run()
