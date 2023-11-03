from script.settings import *


class Menu:
    def __init__(self, app):
        self.app = app
        # self.manager = self.app.manager
        self.surface = self.app.surface

        self.bg = pg.transform.scale(pg.image.load(MENU_BG_IMG), RESOLUTION)

        self.font = pg.font.Font(filename="assets/font/DebugFreeTrial-MVdYB.otf", size=200)
        self.name = self.font.render(GAME_NAME, True, (255, 255, 255))

        self.font2 = pg.font.Font(filename="assets/font/DebugFreeTrial-MVdYB.otf", size=60)
        self.press = self.font2.render("PRESS ENTER", True, (255, 255, 255))

        self.name_pos = [520, 415]
        self.V = 1
        self.v = -self.V

        self.prev_tick = pg.time.get_ticks()

    def update(self):
        tick = pg.time.get_ticks()
        if tick - self.prev_tick > 10:
            self.prev_tick = tick

            self.name_pos[1] += self.v

            if self.name_pos[1] < 400:
                self.v = self.V / 2
            elif self.name_pos[1] > 415:
                self.v = -self.V

    def draw(self):
        self.surface.blit(self.bg, (0, 0))

        self.surface.blit(self.name, (300, 150))
        self.surface.blit(self.press, self.name_pos)

    def handle_event(self, e):
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_RETURN:
                self.app.manager.set_scene(1) # Gameplay
