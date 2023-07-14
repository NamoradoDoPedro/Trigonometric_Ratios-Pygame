import pygame as pg
from pygame import Vector2 as v
from pygame.locals import *

from math import sin, cos, tan, radians, degrees
from sys import exit


class Display:
    dimension = v(600, 400)
    display = pg.display.set_mode((dimension))
    title = pg.display.set_caption("Graphic")


class Math:
    amplitude = 40
    frequency = 0.02379
    angle_ajust = 0.73333333333333333333333333333333


class Graphic:
    def __init__(self) -> None:
        self.reset()
        self.circle_color = (255, 255, 255)
        self.sin_color = (0, 0, 255)
        self.cos_color = (255, 0, 0)
        self.tan_color = (255, 0, 255)

    def reset(self) -> None:
        self.dimension = v(1, 1)
        self.amplitude = Math.amplitude
        self.frequency = Math.frequency
        self.e = 0
        self.circle_size = 1
        self.cos_size = 1
        self.sin_size = 1
        self.tan_size = 1

        self.toggle_sin = False
        self.toggle_cos = False
        self.toggle_tan = False
        self.toggle_circle = True
        self.toggle_info = True

    def change_size(self, x):
        self.circle_size = x
        self.cos_size = x
        self.sin_size = x
        self.tan_size = x

    @staticmethod
    def axes() -> None:
        WHITE = (255, 255, 255)
        mid = v(int(Display.dimension.x/2), int(Display.dimension.y/2))
        line = pg.draw.line

        # Axes X
        line(Display.display, WHITE, (mid.x, 0), (mid.x, Display.dimension.x))
        # Axes Y
        line(Display.display, WHITE, (0, mid.y), (Display.dimension.x, mid.y))

    @staticmethod
    def background_axes() -> None:
        GRAY = (100, 100, 100)
        line = pg.draw.line

        for i in range(int(Display.dimension.x/40)):
            line(Display.display, GRAY,
                 ((i*40)+20, 0), ((i*40)+20, Display.dimension.y))

        for i in range(int(Display.dimension.y/40)):
            line(Display.display, GRAY,
                 (0, (i*40)), (Display.dimension.x, (i*40)))

    def sin(self, ag: int = None) -> None:
        mid = v(int(Display.dimension.x/2), int(Display.dimension.y/2))

        for i in range(-int(Display.dimension.x*self.sin_size), int(Display.dimension.x*self.sin_size)):
            center_line = self.dimension.x * (i+mid.x)

            x = sin(i*self.frequency/self.sin_size) * \
                -(self.amplitude*self.sin_size)+mid.y

            if ag is None:
                if not self.toggle_circle:
                    pg.draw.rect(Display.display, self.sin_color,
                                 ((center_line, int(x)), (self.dimension)))
            else:
                pg.draw.rect(Display.display, self.sin_color,
                             ((center_line+ag, int(x)), (self.dimension)))

    def cos(self, ag: int = None) -> None:
        mid = v(int(Display.dimension.x/2), int(Display.dimension.y/2))

        for i in range(-int(Display.dimension.x*self.cos_size), int(Display.dimension.x*self.cos_size)):
            center_line = self.dimension.x * (i+mid.x)

            x = cos(i*self.frequency/self.cos_size) * \
                -(self.amplitude*self.cos_size)+mid.y

            if ag is None:
                if not self.toggle_circle:
                    pg.draw.rect(Display.display, self.cos_color,
                                 ((center_line, int(x)), (self.dimension)))
            else:
                pg.draw.rect(Display.display, self.cos_color,
                             ((center_line+ag, int(x)), (self.dimension)))

    def tan(self) -> None:
        mid = v(int(Display.dimension.x/2), int(Display.dimension.y/2))

        for i in range(int(-mid.x), int(+mid.x)):
            center_line = self.dimension.x * (i+mid.x)

            x = tan(i*self.frequency/self.tan_size)*- \
                (self.amplitude*self.tan_size)+mid.y

            pg.draw.rect(Display.display, self.tan_color,
                         ((center_line, int(x)), (self.dimension)))

    def circle(self) -> None:
        mid = v(int(Display.dimension.x/2), int(Display.dimension.y/2))
        arc_size = v(30*self.circle_size, 30*self.circle_size)

        _sin = self.circle_size * \
            sin(self.e*Math.frequency)*-Math.amplitude+mid.y
        _cos = -self.circle_size * \
            cos(self.e*Math.frequency)*-Math.amplitude+mid.x

        self.angle = degrees(radians(self.e/Math.angle_ajust))

        if self.angle > 360:
            self.e = 0
        if self.angle < 0:
            self.e = 360*Math.angle_ajust

        pg.draw.circle(Display.display, self.circle_color, mid,
                       self.circle_size*Math.amplitude, 1)

        # hypotenuse
        pg.draw.line(Display.display, self.circle_color, mid,
                     (_cos, _sin), 2)

        # sin
        pg.draw.line(Display.display, self.sin_color, (_cos, mid.y),
                     (_cos, _sin), 2)

        # cos
        pg.draw.line(Display.display, self.cos_color, mid,
                     (_cos, mid.y), 2)

        # angle arc
        pg.draw.arc(Display.display, self.circle_color,
                    ((mid.x-arc_size.x/2, mid.y-arc_size.y/2), arc_size), 0, radians(self.angle), 1)

        if self.toggle_sin:
            self.sin(-int(self.e*self.circle_size))
        if self.toggle_cos:
            self.cos(-int(self.e*self.circle_size))

    def show_info(self) -> None:
        FONT = pg.font.get_default_font()
        SIZE = 30
        WHITE = (255, 255, 255)

        Amplitude = round(
            ((self.amplitude-Math.amplitude)/Math.amplitude)+1, 2)
        Frequency = round(
            ((self.frequency-Math.frequency)*Math.amplitude)+1, 2)

        Amplitude_Text = f"Amplitude: {Amplitude}"
        Frequency_Text = f"Frequency: {Frequency}"

        f = f"{Frequency}" if Frequency > 0 else f"({Frequency})"
        a = f"{Amplitude}" if Amplitude > 0 else f"({Amplitude})"

        if Amplitude == 1 and Frequency == 1:
            sinInfos = f"f(x) = sin(x)"
            cosInfos = f"f(x) = cos(x)"
            tanInfos = f"f(x) = tan(x)"
        elif Amplitude != 1 and Frequency != 1:
            sinInfos = f"f(x) = sin(x*{f})*{a}"
            cosInfos = f"f(x) = cos(x*{f})*{a}"
            tanInfos = f"f(x) = tan(x*{f})*{a}"
        elif Frequency != 1:
            sinInfos = f"f(x) = sin(x*{f})"
            cosInfos = f"f(x) = cos(x*{f})"
            tanInfos = f"f(x) = tan(x*{f})"
        elif Amplitude != 1:
            sinInfos = f"f(x) = sin(x)*{a}"
            cosInfos = f"f(x) = cos(x)*{a}"
            tanInfos = f"f(x) = tan(x)*{a}"

        circleInfos = [
            f"Angle: {round(self.angle, 2)}°",
            f"sin({round(radians(self.angle), 2)}rad) = {round(sin(radians(self.angle)), 2)}",
            f"cos({round(radians(self.angle), 2)}rad) = {round(cos(radians(self.angle)), 2)}"
        ]

        if self.circle_size != 1:
            circleSinInfo = f"f(x) = {self.circle_size}sin((x+{round((self.e)/66, 2)})/{self.circle_size})"
            circleCosInfo = f"f(x) = {self.circle_size}cos((x+{round((self.e)/66, 2)})/{self.circle_size})"
        else:
            circleSinInfo = f"f(x) = sin(x+{round((self.e)/66, 2)})"
            circleCosInfo = f"f(x) = cos(x+{round((self.e)/66, 2)})"

        blit = Display.display.blit
        render_text = pg.font.SysFont(FONT, SIZE).render

        if not self.toggle_circle:
            if self.toggle_sin or self.toggle_cos or self.toggle_tan:
                blit(render_text(Amplitude_Text, True, WHITE), (10, 10))
                blit(render_text(Frequency_Text, True, WHITE), (10, 30))

        if self.toggle_circle:
            if self.toggle_sin and self.toggle_cos:
                blit(render_text(
                    circleInfos[0], True, WHITE), (10, 22))
                blit(render_text(
                    circleInfos[1], True, WHITE), (10, 44))
                blit(render_text(
                    circleInfos[2], True, WHITE), (10, 66))

                # Default
                blit(render_text(circleSinInfo, True, WHITE),
                     (Display.dimension.x-220, 10))
                blit(render_text(circleCosInfo, True, WHITE),
                     (Display.dimension.x-220, 35))

            elif self.toggle_sin:
                blit(render_text(
                    circleInfos[0], True, WHITE), (10, 22))
                blit(render_text(
                    circleInfos[1], True, WHITE), (10, 44))

                # Default
                blit(render_text(circleSinInfo, True, WHITE),
                     (Display.dimension.x-220, 10))

            elif self.toggle_cos:
                blit(render_text(
                    circleInfos[0], True, WHITE), (10, 22))
                blit(render_text(
                    circleInfos[2], True, WHITE), (10, 44))

                # Default
                blit(render_text(circleCosInfo, True, WHITE),
                     (Display.dimension.x-220, 10))

            else:
                blit(render_text(
                    circleInfos[0], True, WHITE), (10, 22))

        elif self.toggle_sin:
            blit(render_text(sinInfos, True, WHITE),
                 (Display.dimension.x-220, 10))
        elif self.toggle_cos:
            blit(render_text(cosInfos, True, WHITE),
                 (Display.dimension.x-220, 10))
        elif self.toggle_tan:
            blit(render_text(tanInfos, True, WHITE),
                 (Display.dimension.x-220, 10))

    def controller(self) -> None:
        key = pg.key.get_pressed()
        if not self.toggle_circle:
            if key[K_UP]:
                self.amplitude += 1
            if key[K_DOWN]:
                self.amplitude -= 1
            if key[K_LEFT]:
                self.frequency -= 0.001
            if key[K_RIGHT]:
                self.frequency += 0.001

        elif self.toggle_circle:
            if key[K_UP]:
                self.e += 1
            if key[K_DOWN]:
                self.e -= 1

        for i, K in enumerate([K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]):
            if key[K]:
                self.change_size(i+1)

        if key[K_r]:
            self.reset()

    def reset_func(self) -> None:
        self.toggle_sin = False
        self.toggle_cos = False
        self.toggle_tan = False
        self.toggle_circle = False


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
        self.graphic.circle() if self.graphic.toggle_circle else ...
        self.graphic.show_info() if self.graphic.toggle_info else ...

        pg.display.update()

    def controller(self) -> None:
        key = pg.key.get_pressed()
        if key[K_s]:
            # self.graphic.reset_func()
            # self.graphic.toggle_sin = not self.graphic.toggle_sin if not self.graphic.toggle_sin else ...
            self.graphic.toggle_sin = not self.graphic.toggle_sin
        if key[K_c]:
            # self.graphic.reset_func()
            # self.graphic.toggle_cos = not self.graphic.toggle_cos if not self.graphic.toggle_cos else ...
            self.graphic.toggle_cos = not self.graphic.toggle_cos
        if key[K_t]:
            # self.graphic.reset_func()
            # self.graphic.toggle_tan = not self.graphic.toggle_tan if not self.graphic.toggle_tan else ...
            self.graphic.toggle_tan = not self.graphic.toggle_tan
        if key[K_d]:
            # self.graphic.reset_func()
            # self.graphic.toggle_circle = not self.graphic.toggle_circle if not self.graphic.toggle_circle else ...
            self.graphic.toggle_circle = not self.graphic.toggle_circle
        if key[K_i]:
            self.graphic.toggle_info = not self.graphic.toggle_info


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
                game.controller()

        game.update()
        clock.tick(60)
