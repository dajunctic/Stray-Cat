from script.settings import *


class Text:
    STATIC = 0
    DYNAMIC = 1

    def __init__(self, app, text, status=DYNAMIC):
        self.app = app
        self.surface = app.surface

        self.font_size = DIALOGUE_FONT_SIZE
        self.font = pg.font.Font(DEFAULT_TEXT_FONT, self.font_size)
        self.color = DIALOGUE_TEXT_COLOR
        self.text = text
        self.status = status
        self.text_length = len(text)

        self.text_rect = []
        self.text_surf = []
        self.cur_line = 0

        self.line_width = 800
        self.line_height = 40

        self.x = (WIDTH - self.line_width) // 2
        self.y = 610

        self.cur_text = ""
        self.cur = 0

        self.prev_tick = 0
        self.cur_tick = 0
        self.interval = 25  # millisecond

        if self.status == Text.STATIC:
            self.finish()

    def set_font(self, font):
        self.font = pg.font.Font(font)

    def set_pos(self, x, y):
        self.x = x
        self.y = y

        for i in range(len(self.text_rect)):
            self.text_rect[i].bottomleft = (self.x, self.y + i * self.line_height)

    def set_text(self, text):
        self.text = text
        self.text_length = len(text)

    def set_line_width(self, width):
        self.line_width = width

    def set_line_height(self, height):
        self.line_height = height

    def get_rect(self):
        return self.text_rect[0]

    def update(self):
        self.cur_tick = pg.time.get_ticks()

        if self.cur_tick - self.prev_tick > self.interval and self.cur < self.text_length:
            self.generate()
            self.prev_tick = self.cur_tick

    def generate(self):
        self.cur_text += self.text[self.cur]
        self.cur += 1

        self.render()
        if self.text_rect[self.cur_line].width > self.line_width:
            self.cur_text = self.cur_text[:-1]

            if self.text[self.cur - 2] != ' ' and self.cur < self.text_length and self.text[self.cur - 1] != ' ':
                self.cur_text += '-'

            self.render()

            self.cur_text = "" + self.text[self.cur - 1]
            self.cur_line += 1
            self.render()

    def render(self):
        if self.cur_line >= len(self.text_surf):
            self.text_surf.append(None)
            self.text_rect.append(None)

        self.text_surf[self.cur_line] = self.font.render(self.cur_text, True, self.color)
        self.text_rect[self.cur_line] = self.text_surf[self.cur_line].get_rect()
        self.text_rect[self.cur_line].bottomleft = (self.x, self.y + self.cur_line * self.line_height)

    def reset(self):
        self.cur = 0
        self.cur_text = ""

    def draw(self):
        for i, surf in enumerate(self.text_surf):
            self.surface.blit(surf, self.text_rect[i])

    def finish(self):
        while self.cur < self.text_length:
            self.generate()

    def is_finished(self):
        return self.cur == self.text_length

class Dialogue:
    def __init__(self, app,  path=""):
        self.app = app
        self.surface = app.surface
        self.path = path
        self.textbox = pg.image.load(TEXT_BOX_IMG)
        self.message_line = pg.image.load(MESSAGE_LINE_IMG)
        self.message_line_y = 520

        self.speech_info = []
        self.speech_text = []
        self.cur = 0

        self.finished = False

        self.read()

    def is_finished(self):
        return self.finished

    def read(self):
        with open(self.path, 'r', encoding="utf8") as file:
            for line in file.readlines():
                line = [x.replace("\"", "") for x in line.replace("\n", "").split("\" \"")]
                self.speech_info.append(line)

                name = Text(self.app, self.speech_info[-1][0], Text.STATIC)
                name.set_pos((WIDTH - name.get_rect().width) // 2, self.message_line_y + 20)
                self.speech_text.append(
                    {
                    'character': name,
                    'text': Text(self.app, self.speech_info[-1][2]),
                    }
                )

    def draw(self):
        self.surface.blit(self.textbox, (0, 0))
        self.surface.blit(self.message_line, ((WIDTH - 324) // 2, self.message_line_y))

        self.speech_text[self.cur]['character'].draw()
        self.speech_text[self.cur]['text'].draw()

    def update(self):
        self.speech_text[self.cur]['text'].update()

    def handle_event(self, e):
        if e.type == pg.MOUSEBUTTONUP:
            if self.speech_text[self.cur]['text'].is_finished():
                self.cur += 1

                if self.cur == len(self.speech_text):
                    self.cur -= 1
                    self.finished = True
            else:
                self.speech_text[self.cur]['text'].finish()
