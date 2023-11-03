import random

from script.debug import Debugger
from script.settings import *


class WhachAMole:
    def __init__(self, app):
        self.WIN_SCORE = WHACK_WIN_SCORE
        self.win_img = pg.image.load("assets/img/whach_a_mole/win.jpg").convert_alpha()
        self.initial_interval = None
        self.interval = None
        self.clock = None
        self.cycle_time = None
        self.left = None
        self.frame_num = None
        self.num = None
        self.is_down = None
        self.app = app
        self.surface = app.surface

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.FPS = 60
        self.MOLE_WIDTH = 90
        self.MOLE_HEIGHT = 81
        self.FONT_SIZE = 31
        self.FONT_TOP_MARGIN = 26
        self.LEVEL_SCORE_GAP = 4
        self.LEFT_MOUSE_BUTTON = 1

        self.GAME_TITLE = "Whack A Mole - Game Programming - Assignment 1"
        # Initialize player's score, number of missed hits and level
        self.score = 0
        self.misses = 0
        self.level = 1
        # Initialize screen
        self.screen = self.surface

        self.screen_img = pg.image.load("assets/img/whach_a_mole/screen.png").convert_alpha()
        self.background = pg.image.load("assets/img/whach_a_mole/bg.png").convert_alpha()
        self.cat_hand = pg.image.load("assets/img/whach_a_mole/hand.png").convert_alpha()
        self.cat_hand.set_alpha(100)

        # Font object for displaying text
        self.font_obj = pg.font.Font('assets/font/PixelCraft-2Odxo.otf', self.FONT_SIZE)
        # Initialize the mole's sprite sheet
        # 6 different states
        sprite_sheet = pg.image.load("assets/img/whach_a_mole/mole.png").convert_alpha()
        self.mole = []
        self.mole.append(sprite_sheet.subsurface(169, 0, 90, 81))
        self.mole.append(sprite_sheet.subsurface(309, 0, 90, 81))
        self.mole.append(sprite_sheet.subsurface(449, 0, 90, 81))
        self.mole.append(sprite_sheet.subsurface(575, 0, 116, 81))
        self.mole.append(sprite_sheet.subsurface(717, 0, 116, 81))
        self.mole.append(sprite_sheet.subsurface(853, 0, 116, 81))
        # Positions of the holes in background
        self.hole_positions = []
        self.hole_positions.append((381, 295))
        self.hole_positions.append((119, 366))
        self.hole_positions.append((179, 169))
        self.hole_positions.append((404, 479))
        self.hole_positions.append((636, 366))
        self.hole_positions.append((658, 232))
        self.hole_positions.append((464, 119))
        self.hole_positions.append((95, 43))
        self.hole_positions.append((603, 11))
        # Init debugger
        self.debugger = Debugger("debug")
        # Sound effects
        self.soundEffect = SoundEffect()

        # Offset Game Screen
        self.offsetX = (WIDTH - self.SCREEN_WIDTH) // 2
        self.offsetY = (HEIGHT - self.SCREEN_HEIGHT) // 2

        self.initial()

        self.start = False
        self.finish = False

        self.win = False
        self.tick = 0
        self._interval = 2.5

    def load(self):
        self.start = True

    def get_player_level(self):
        newLevel = 1 + int(self.score / self.LEVEL_SCORE_GAP)
        if newLevel != self.level:
            # if player get a new level play this sound
            self.soundEffect.play_level_up()
        return 1 + int(self.score / self.LEVEL_SCORE_GAP)

    def get_interval_by_level(self, initial_interval):
        new_interval = initial_interval - self.level * 0.15
        if new_interval > 0:
            return new_interval
        else:
            return 0.05

    def is_mole_hit(self, mouse_position, current_hole_position):
        mouse_x = mouse_position[0] - self.offsetX
        mouse_y = mouse_position[1] - self.offsetY
        current_hole_x = current_hole_position[0]
        current_hole_y = current_hole_position[1]

        size = 40
        rect1 = pg.Rect(mouse_x - size, mouse_y - size, 2 * size, 2 * size)
        rect2 = pg.Rect(current_hole_x, current_hole_y, self.MOLE_WIDTH, self.MOLE_HEIGHT)

        return pg.Rect.colliderect(rect1, rect2)

    def update(self):
        # Update the player's score
        current_score_string = "SCORE: " + str(self.score)
        score_text = self.font_obj.render(current_score_string, True, (255, 255, 255))
        score_text_pos = score_text.get_rect()
        score_text_pos.centerx = self.background.get_rect().centerx + self.offsetX
        score_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(score_text, score_text_pos)
        # Update the player's misses
        current_misses_string = "MISSES: " + str(self.misses)
        misses_text = self.font_obj.render(current_misses_string, True, (255, 255, 255))
        misses_text_pos = misses_text.get_rect()
        misses_text_pos.centerx = self.SCREEN_WIDTH / 5 * 4 + + self.offsetX
        misses_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(misses_text, misses_text_pos)
        # Update the player's level
        current_level_string = "LEVEL: " + str(self.level)
        level_text = self.font_obj.render(current_level_string, True, (255, 255, 255))
        level_text_pos = level_text.get_rect()
        level_text_pos.centerx = self.SCREEN_WIDTH / 5 * 1 + self.offsetX
        level_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(level_text, level_text_pos)

        if self.score == self.WIN_SCORE and not self.win:
            self.win = True
            self.soundEffect.play_you_win()
            self.tick = pg.time.get_ticks()

    def handle_event(self, e):
        if e.type == pg.MOUSEBUTTONDOWN and e.button == self.LEFT_MOUSE_BUTTON:
            self.soundEffect.play_fire()
            if (self.is_mole_hit(pg.mouse.get_pos(), self.hole_positions[self.frame_num]) and
                    self.num > 0 and self.left == 0):
                self.num = 3
                self.left = 14
                self.is_down = False
                self.interval = 0
                self.score += 1  # Increase player's score
                self.level = self.get_player_level()  # Calculate player's level
                # Stop popping sound effect
                self.soundEffect.stop_pop()
                # Play hurt sound
                self.soundEffect.play_hurt()
            else:
                self.misses += 1

    def initial(self):
        self.clock = pg.time.Clock()

        self.cycle_time = 0
        self.num = -1
        self.is_down = False
        self.interval = 0.1
        self.initial_interval = 1
        self.frame_num = 0
        self.left = 0

        for i in range(len(self.mole)):
            self.mole[i].set_colorkey((0, 0, 0))
            self.mole[i] = self.mole[i].convert_alpha()

    def draw(self):
        self.screen.fill((0, 0, 0))

        if self.win:
            self.screen.blit(self.win_img,
                             ((WIDTH - self.win_img.get_width()) // 2, (HEIGHT - self.win_img.get_height()) // 2))

            if pg.time.get_ticks() - self.tick > self._interval * 1000:
                self.finish = True

            return

        self.screen.blit(self.background, (0 + self.offsetX, 0 + self.offsetY))
        # self.screen.blit(self.screen_img, (0, 0))
        if self.num > 5:
            self.num = -1
            self.left = 0

        if self.num == -1:
            self.num = 0
            self.is_down = False
            self.interval = 0.5
            self.frame_num = random.randint(0, 8)

        mil = self.clock.tick(self.FPS)
        sec = mil / 500.0
        self.cycle_time += sec

        if self.num != -1:
            pic = self.mole[self.num]

            x = self.hole_positions[self.frame_num][0] - self.left + self.offsetX
            y = self.hole_positions[self.frame_num][1] + self.offsetY
            self.screen.blit(pic, (x, y))

        if self.cycle_time > self.interval:

            if self.is_down is False:
                self.num += 1
            else:
                self.num -= 1
            if self.num == 4:
                self.interval = 0.3
            elif self.num == 3:
                self.num -= 1
                self.is_down = True
                self.soundEffect.play_pop()
                self.interval = self.get_interval_by_level(self.initial_interval)
            else:
                self.interval = 0.1
            self.cycle_time = 0

        self.update()

        hX, hY = pg.mouse.get_pos()
        self.screen.blit(self.cat_hand, (hX - 50, hY - 20))
        size = 40
        rect1 = pg.Rect(hX - size, hY - size, 2 * size, 2 * size)
        pg.draw.rect(self.surface, (0, 255, 0), rect1, 1, 4)


class SoundEffect:
    def __init__(self):
        pg.mixer.music.load("assets/sfx/whach_a_mole/themesong.wav")
        self.fireSound = pg.mixer.Sound("assets/sfx/whach_a_mole/fire.wav")
        self.fireSound.set_volume(1.0)
        self.popSound = pg.mixer.Sound("assets/sfx/whach_a_mole/pop.wav")
        self.hurtSound = pg.mixer.Sound("assets/sfx/whach_a_mole/hurt.wav")
        self.levelSound = pg.mixer.Sound("assets/sfx/whach_a_mole/point.wav")
        self.youWin = pg.mixer.Sound("assets/sfx/whach_a_mole/youwin.mp3")

    @classmethod
    def play_bg(cls):
        pg.mixer.music.play(-1)

    def play_fire(self):
        self.fireSound.play()

    def stop_fire(self):
        self.fireSound.stop()

    def play_pop(self):
        self.popSound.play()

    def stop_pop(self):
        self.popSound.stop()

    def play_hurt(self):
        self.hurtSound.play()

    def stop_hurt(self):
        self.hurtSound.stop()

    def play_level_up(self):
        self.levelSound.play()

    def stop_level_up(self):
        self.levelSound.stop()

    def play_you_win(self):
        self.youWin.play()

    def stop_you_win(self):
        self.youWin.stop()

###############################################################
