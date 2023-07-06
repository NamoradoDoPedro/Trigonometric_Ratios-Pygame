import pygame as pg
from pygame import Vector2 as v
from pygame.locals import *

from math import sin, cos, tan
from sys import exit


class Display:
    dimension = v(600, 400)
    display = pg.display.set_mode((dimension))
    title = pg.display.set_caption("Sin Graphic")


class Math:
    amplitude = 40.0000000776926
    frequency = 0.023799


class Graphic:
    def __init__(self) -> None:
        self.dimension = v(1, 1)
        self.amplitude = Math.amplitude
        self.frequency = Math.frequency
        self.toggle_sin = True
        self.toggle_cos = False
        self.toggle_tan = False
        self.toggle_info = True

    def axes(self) -> None:
        WHITE = (255, 255, 255)
        mid = v(int(Display.dimension.x/2), int(Display.dimension.y/2))
        line = pg.draw.line

        line(Display.display, WHITE, (0, mid.y), (Display.dimension.x, mid.y))
        line(Display.display, WHITE, (mid.x, 0), (mid.x, Display.dimension.x))

    def background_axes(self) -> None:
        GRAY = (100, 100, 100)
        line = pg.draw.line

        for i in range(int(Display.dimension.x/40)):
            line(Display.display, GRAY,
                 ((i*40)+20, 0), ((i*40)+20, Display.dimension.y))
        for i in range(int(Display.dimension.y/40)):
            line(Display.display, GRAY,
                 (0, (i*40)), (Display.dimension.x, (i*40)))

    def sin(self) -> None:
        WHITE = (255, 255, 255)
        mid = v(int(Display.dimension.x/2), int(Display.dimension.y/2))
        # a = 0
        for i in range(int(-mid.x), int(+mid.x)):
            center_line = self.dimension.x * (i+mid.x)
            x = sin(i*self.frequency)*-self.amplitude+mid.y
            # a = x if a < x else a
            pg.draw.rect(Display.display, WHITE,
                         ((center_line, int(x)), (self.dimension)))

    def cos(self) -> None:
        WHITE = (255, 255, 255)
        mid = v(int(Display.dimension.x/2), int(Display.dimension.y/2))
        # a = 0
        for i in range(int(-mid.x), int(+mid.x)):
            center_line = self.dimension.x * (i+mid.x)
            x = cos(i*self.frequency)*-self.amplitude+mid.y
            # a = x if a < x else a
            pg.draw.rect(Display.display, WHITE,
                         ((center_line, int(x)), (self.dimension)))

    def tan(self) -> None:
        WHITE = (255, 255, 255)
        mid = v(int(Display.dimension.x/2), int(Display.dimension.y/2))
        # a = 0
        for i in range(int(-mid.x), int(+mid.x)):
            center_line = self.dimension.x * (i+mid.x)
            x = tan(i*self.frequency)*-self.amplitude+mid.y
            # a = x if a < x else a
            pg.draw.rect(Display.display, WHITE,
                         ((center_line, int(x)), (self.dimension)))

    def show_info(self) -> None:
        FONT = pg.font.get_default_font()
        SIZE = 30
        WHITE = (255, 255, 255)

        Amplitude = round(
            ((self.amplitude-Math.amplitude)/Math.amplitude)+1, 2)
        Frequency = round(
            ((self.frequency-Math.frequency)*Math.amplitude)+1, 2)

        Amplitude_Text = fr"Amplitude: {Amplitude}"
        Frequency_Text = fr"Frequency: {Frequency}"

        f = fr"{Frequency}" if Frequency > 0 else fr"({Frequency})"

        a = fr"{Amplitude}" if Amplitude > 0 else fr"({Amplitude})"

        if Amplitude == 1 and Frequency == 1:
            sinFunction = fr"f(x) = sin(x)"
        elif Amplitude != 1 and Frequency != 1:
            sinFunction = fr"f(x) = sin(x*{f})*{a}"
        elif Frequency != 1:
            sinFunction = fr"f(x) = sin(x*{f})"
        elif Amplitude != 1:
            sinFunction = fr"f(x) = sin(x)*{a}"

        if Amplitude == 1 and Frequency == 1:
            cosFunction = fr"f(x) = cos(x)"
        elif Amplitude != 1 and Frequency != 1:
            cosFunction = fr"f(x) = cos(x*{f})*{a}"
        elif Frequency != 1:
            cosFunction = fr"f(x) = cos(x*{f})"
        elif Amplitude != 1:
            cosFunction = fr"f(x) = cos(x)*{a}"

        if Amplitude == 1 and Frequency == 1:
            tanFunction = fr"f(x) = tan(x)"
        elif Amplitude != 1 and Frequency != 1:
            tanFunction = fr"f(x) = tan(x*{f})*{a}"
        elif Frequency != 1:
            tanFunction = fr"f(x) = tan(x*{f})"
        elif Amplitude != 1:
            tanFunction = fr"f(x) = tan(x)*{a}"

        blit = Display.display.blit
        blit(pg.font.SysFont(FONT, SIZE).render(
            Amplitude_Text, True, WHITE), (10, 10))
        blit(pg.font.SysFont(FONT, SIZE).render(
            Frequency_Text, True, WHITE), (10, 30))

        if self.toggle_sin:
            blit(pg.font.SysFont(FONT, SIZE).render(
                sinFunction, True, WHITE), (Display.dimension.x-220, 10))
        elif self.toggle_cos:
            blit(pg.font.SysFont(FONT, SIZE).render(
                cosFunction, True, WHITE), (Display.dimension.x-220, 10))
        elif self.toggle_tan:
            blit(pg.font.SysFont(FONT, SIZE).render(
                tanFunction, True, WHITE), (Display.dimension.x-220, 10))

    def controller(self) -> None:
        key = pg.key.get_pressed()
        if key[K_UP]:
            self.amplitude += 1
        if key[K_DOWN]:
            self.amplitude -= 1
        if key[K_LEFT]:
            self.frequency -= 0.001
        if key[K_RIGHT]:
            self.frequency += 0.001

        if key[K_r]:
            self.reset()

    def reset(self) -> None:
        self.dimension = v(1, 1)
        self.amplitude = Math.amplitude
        self.frequency = Math.frequency

    def reset_func(self) -> None:
        self.toggle_sin = False
        self.toggle_cos = False
        self.toggle_tan = False


class Game:
    def __init__(self) -> None:
        self.graphic = Graphic()

    def update(self) -> None:
        Display.display.fill((0, 0, 0))

        self.graphic.controller()
        self.graphic.background_axes()
        self.graphic.axes()
        self.graphic.sin() if self.graphic.toggle_sin else ...
        self.graphic.cos() if self.graphic.toggle_cos else ...
        self.graphic.tan() if self.graphic.toggle_tan else ...
        self.graphic.show_info() if self.graphic.toggle_info else ...

        pg.display.update()


if __name__ == "__main__":
    pg.init()
    game = Game()
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()

            if event.type == KEYDOWN:
                key = pg.key.get_pressed()
                if key[K_s]:
                    game.graphic.reset_func()
                    game.graphic.toggle_sin = not game.graphic.toggle_sin if not game.graphic.toggle_sin else game.graphic.toggle_sin
                if key[K_c]:
                    game.graphic.reset_func()
                    game.graphic.toggle_cos = not game.graphic.toggle_cos if not game.graphic.toggle_cos else game.graphic.toggle_cos
                if key[K_t]:
                    game.graphic.reset_func()
                    game.graphic.toggle_tan = not game.graphic.toggle_tan if not game.graphic.toggle_tan else game.graphic.toggle_tan
                if key[K_i]:
                    game.graphic.toggle_info = not game.graphic.toggle_info

        game.update()
        clock.tick(60)
