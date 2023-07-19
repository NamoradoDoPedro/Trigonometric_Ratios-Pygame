import pygame as pg
from pygame import Vector2 as v
from pygame.locals import *
from pygame.draw import line, arc, circle, rect

from math import sin, cos, tan, radians, degrees
from sys import exit

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
FONT = pg.font.get_default_font()


class Display:
    dimension = v(600, 600)
    display = pg.display.set_mode(dimension)
    title = pg.display.set_caption("Graphic")


class Math:
    amplitude = 40
    frequency = amplitude/(amplitude*amplitude)
    angle_ajust = 0.69722222222222222222222222222222


class Graphic:
    def __init__(self) -> None:
        self.reset()
        self.circle_color = (255, 255, 255)
        self.sin_color = (0, 0, 255)
        self.cos_color = (255, 0, 0)
        self.tan_color = (255, 0, 255)

    def reset(self) -> None:
        self.DIMENSION = v(1, 1)
        self.amplitude = Math.amplitude
        self.frequency = Math.frequency
        self.circle_value = 0
        self.circle_size = 1
        self.arc_size = v(30*self.circle_size, 30*self.circle_size)
        self.sin_size = 1
        self.cos_size = 1
        self.tan_size = 1

        self.toggle_sin = False
        self.toggle_cos = False
        self.toggle_tan = False
        self.toggle_circle = True
        self.toggle_info = True
        self.toggle_help = False

        self.toggle_axes = True
        self.toggle_background_axes = True

    def change_size(self, x):
        self.circle_size = x
        self.cos_size = x
        self.sin_size = x
        self.tan_size = x

    @staticmethod
    def axes() -> None:
        mid = (Display.dimension/2)

        # Axes X
        line(Display.display, WHITE, (0, mid.y), (Display.dimension.x, mid.y))
        # Axes Y
        line(Display.display, WHITE, (mid.x, 0), (mid.x, Display.dimension.y))

    def background_axes(self) -> None:
        if self.toggle_background_axes:
            if (Display.dimension.x/Math.amplitude) == int(Display.dimension.x/Math.amplitude) and \
                    (Display.dimension.y/Math.amplitude) == int(Display.dimension.y/Math.amplitude):
                if (Display.dimension.x/Math.amplitude) % 2 != 0:
                    for i in range(int(Display.dimension.x/Math.amplitude)):
                        line(Display.display, GRAY,
                             ((i*Math.amplitude)+Math.amplitude/2, 0), ((i*Math.amplitude)+Math.amplitude/2, Display.dimension.y))

                else:
                    for i in range(int(Display.dimension.x/Math.amplitude)):
                        line(Display.display, GRAY,
                             ((i*Math.amplitude), 0), ((i*Math.amplitude), Display.dimension.y))

                if (Display.dimension.y/Math.amplitude) % 2 != 0:
                    for i in range(int(Display.dimension.y/Math.amplitude)):
                        line(Display.display, GRAY,
                             (0, (i*Math.amplitude)+Math.amplitude/2), (Display.dimension.x, (i*Math.amplitude)+Math.amplitude/2))

                else:
                    for i in range(int(Display.dimension.y/Math.amplitude)):
                        line(Display.display, GRAY,
                             (0, (i*Math.amplitude)), (Display.dimension.x, (i*Math.amplitude)))

            else:
                print("The background_axes() function cannot be executed because it does not have an integer division of the result between Display.dimension and Math.amplitude")
                self.toggle_background_axes = not self.toggle_background_axes

    def sin(self, trigger: int = None) -> None:
        mid = (Display.dimension/2)

        for i in range(-int(Display.dimension.x*self.sin_size), int(Display.dimension.x*self.sin_size)):
            center_line = self.DIMENSION.x * (i+mid.x)

            x = sin(i*self.frequency/self.sin_size) * \
                -(self.amplitude*self.sin_size)+mid.y

            if trigger is None:
                if not self.toggle_circle:
                    rect(Display.display, self.sin_color,
                         ((center_line, int(x)), (self.DIMENSION)))
            else:
                rect(Display.display, self.sin_color,
                     ((center_line+trigger, int(x)), (self.DIMENSION)))

    def cos(self, trigger: int = None) -> None:
        mid = (Display.dimension/2)

        for i in range(-int(Display.dimension.x*self.cos_size), int(Display.dimension.x*self.cos_size)):
            center_line = self.DIMENSION.x * (i+mid.x)

            x = cos(i*self.frequency/self.cos_size) * \
                -(self.amplitude*self.cos_size)+mid.y

            if trigger is None:
                if not self.toggle_circle:
                    rect(Display.display, self.cos_color,
                         ((center_line, int(x)), (self.DIMENSION)))
            else:
                rect(Display.display, self.cos_color,
                     ((center_line+trigger, int(x)), (self.DIMENSION)))

    def tan(self) -> None:
        mid = (Display.dimension/2)

        for i in range(int(-mid.x), int(+mid.x)):
            center_line = self.DIMENSION.x * (i+mid.x)

            x = tan(i*self.frequency/self.tan_size)*- \
                (self.amplitude*self.tan_size)+mid.y

            rect(Display.display, self.tan_color,
                 ((center_line, int(x)), (self.DIMENSION)))

    def circle(self) -> None:
        mid = (Display.dimension/2)

        _sin = self.circle_size * \
            sin(self.circle_value*Math.frequency)*-Math.amplitude+mid.y
        _cos = -self.circle_size * \
            cos(self.circle_value*Math.frequency)*-Math.amplitude+mid.x

        self.angle = degrees(radians(self.circle_value/Math.angle_ajust))

        if self.angle > 360:
            self.circle_value = 0
        if self.angle < 0:
            self.circle_value = 360*Math.angle_ajust

        circle(Display.display, self.circle_color,
               mid, self.circle_size*Math.amplitude, 1)

        # hypotenuse
        line(Display.display, self.circle_color,
             mid, (_cos, _sin), 2)

        # sin
        line(Display.display, self.sin_color,
             (_cos, mid.y), (_cos, _sin), 2)

        # cos
        line(Display.display, self.cos_color,
             mid, (_cos, mid.y), 2)

        # arc sangle
        arc(Display.display, self.circle_color,
            ((mid.x-self.arc_size.x/2, mid.y-self.arc_size.y/2), self.arc_size), 0, radians(self.angle), 1)

        SIZE = 20
        blit = Display.display.blit
        render_text = pg.font.SysFont(FONT, SIZE).render
        # SIN INFO GRAPHIC TEXT
        blit(render_text(f"{round(sin(radians(self.angle)), 2)}", True, WHITE),
             (mid.x+(Math.amplitude*self.circle_size), _sin))
        # COS INFO GRAPHIC TEXT
        blit(render_text(f"{round(cos(radians(self.angle)), 2)}", True, WHITE),
             (_cos, mid.y+(Math.amplitude*self.circle_size)))

        if self.toggle_sin:
            self.sin(-int(self.circle_value*self.circle_size))
        if self.toggle_cos:
            self.cos(-int(self.circle_value*self.circle_size))

    def show_info(self) -> None:
        SIZE = 30

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

        if self.toggle_circle:
            circleInfos = [
                f"Angle: {round(self.angle, 2)}°",
                f"sin({round(radians(self.angle), 2)}rad) = {round(sin(radians(self.angle)), 2)}",
                f"cos({round(radians(self.angle), 2)}rad) = {round(cos(radians(self.angle)), 2)}"
            ]

            _sin = round((self.circle_value)/66, 2)
            _cos = round((self.circle_value)/66, 2)
            if self.circle_size == 1:
                if _sin != 0:
                    if Amplitude == 1 and Frequency == 1:
                        circleSinInfo = f"f(x) = sin(x+{_sin})"
                    elif Amplitude != 1 and Frequency != 1:
                        circleSinInfo = f"f(x) = sin(x+{_sin}*{Frequency})*{Amplitude}"
                    elif Amplitude != 1:
                        circleSinInfo = f"f(x) = sin(x+{_sin})*{Amplitude}"
                    else:
                        circleSinInfo = f"f(x) = sin(x+{_sin}*{Frequency})"
                else:
                    circleSinInfo = sinInfos

                if _cos != 0:
                    if Amplitude == 1 and Frequency == 1:
                        circleCosInfo = f"f(x) = cos(x+{_cos})"
                    elif Amplitude != 1 and Frequency != 1:
                        circleCosInfo = f"f(x) = cos(x+{_cos}*{Frequency})*{Amplitude}"
                    elif Amplitude != 1:
                        circleCosInfo = f"f(x) = cos(x+{_cos})*{Amplitude}"
                    else:
                        circleCosInfo = f"f(x) = cos(x+{_cos}*{Frequency})"
                else:
                    circleCosInfo = cosInfos
            else:
                if _sin != 0:
                    if Amplitude == 1 and Frequency == 1:
                        circleSinInfo = f"f(x) = {self.circle_size}sin((x+{_sin})/{self.circle_size})"
                    elif Amplitude != 1 and Frequency != 1:
                        circleSinInfo = f"f(x) = {self.circle_size}sin((x+{_sin}*{Frequency})*{Amplitude}/{self.circle_size})"
                    elif Amplitude != 1:
                        circleSinInfo = f"f(x) = {self.circle_size}sin((x+{_sin})*{Amplitude}/{self.circle_size})"
                    else:
                        circleSinInfo = f"f(x) = {self.circle_size}sin((x+{_sin}*{Frequency})/{self.circle_size})"
                else:
                    circleSinInfo = sinInfos

                if _cos != 0:
                    if Amplitude == 1 and Frequency == 1:
                        circleCosInfo = f"f(x) = {self.circle_size}cos((x+{_cos})/{self.circle_size})"
                    elif Amplitude != 1 and Frequency != 1:
                        circleCosInfo = f"f(x) = {self.circle_size}cos((x+{_cos}*{Frequency})*{Amplitude}/{self.circle_size})"
                    elif Amplitude != 1:
                        circleCosInfo = f"f(x) = {self.circle_size}cos((x+{_cos})*{Amplitude}/{self.circle_size})"
                    else:
                        circleCosInfo = f"f(x) = {self.circle_size}cos((x+{_cos}*{Frequency})/{self.circle_size})"
                else:
                    circleCosInfo = cosInfos

        blit = Display.display.blit
        render_text = pg.font.SysFont(FONT, SIZE).render
        mid = v(Display.dimension/2)

        if self.toggle_circle:
            blit(render_text(
                circleInfos[0], True, WHITE), (10, 10))
            blit(render_text(
                f"x^2 + y^2 = {self.circle_size}^2", True, WHITE),
                (mid.x+10, 10))

            if self.toggle_sin and self.toggle_cos:
                blit(render_text(
                    circleInfos[1], True, WHITE), (10, 35))
                blit(render_text(
                    circleInfos[2], True, WHITE), (10, 60))

                # Default
                blit(render_text(circleSinInfo, True, WHITE),
                     (mid.x+10, 35))
                blit(render_text(circleCosInfo, True, WHITE),
                     (mid.x+10, 60))

            elif self.toggle_sin:
                blit(render_text(
                    circleInfos[1], True, WHITE), (10, 35))

                # Default
                blit(render_text(circleSinInfo, True, WHITE),
                     (mid.x+10, 35))

            elif self.toggle_cos:
                blit(render_text(
                    circleInfos[2], True, WHITE), (10, 35))

                # Default
                blit(render_text(circleCosInfo, True, WHITE),
                     (mid.x+10, 35))

        else:
            _infos_active = 0
            if self.toggle_sin or self.toggle_cos or self.toggle_tan:
                blit(render_text(Amplitude_Text, True, WHITE), (10, 10))
                blit(render_text(Frequency_Text, True, WHITE), (10, 35))

            if self.toggle_sin:
                blit(render_text(sinInfos, True, WHITE),
                     (mid.x+10, 10+(25*_infos_active)))
                _infos_active += 1

            if self.toggle_cos:
                blit(render_text(cosInfos, True, WHITE),
                     (mid.x+10, 10+(25*_infos_active)))
                _infos_active += 1

            if self.toggle_tan:
                blit(render_text(tanInfos, True, WHITE),
                     (mid.x+10, 10+(25*_infos_active)))
                _infos_active += 1

    def show_help(self) -> None:
        SIZE = 25
        mid = v(Display.dimension/2)

        if self.toggle_circle:
            controlers = [
                "[S] Toggle sine",
                "[C] Toggle cosine",
                "[T] Toggle tangent",
                "[D] Toggle circle",
                "[I] Toggle info",
                "[R] Reset",
                "[UP] Increase angle",
                "[DOWN] Decrease angle",
                "[NUMBER] Change size",
            ]
        else:
            controlers = [
                "[S] Toggle sine",
                "[C] Toggle cosine",
                "[T] Toggle tangent",
                "[D] Toggle circle",
                "[I] Toggle info",
                "[R] Reset",
                "[UP] Increase amplitude",
                "[DOWN] Decrease amplitude",
                "[RIGHT] Increase frequency",
                "[LEFT] Decrease frequency",
                "[NUMBER] Change size",
            ]

        class square:
            dim = v(255, SIZE*len(controlers)+SIZE)
            pos = v(mid.x - (dim.x/2),
                    mid.y - Math.amplitude*(len(controlers)/2))

        rect(Display.display, WHITE,
             (square.pos-(1, 1), square.dim+(2, 2)))
        rect(Display.display, BLACK,
             (square.pos, square.dim))

        blit = Display.display.blit
        render_text = pg.font.SysFont(FONT, SIZE).render

        for index, info in enumerate(controlers):
            blit(render_text(info, True, WHITE),
                 (square.pos.x+10, square.pos.y+10 + (index*SIZE)))

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
                self.circle_value += 0.5
            if key[K_DOWN]:
                self.circle_value -= 0.5

        for i, K in enumerate([K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]):
            if key[K]:
                self.change_size(i+1)

        if key[K_r]:
            self.reset()


class Game:
    def __init__(self) -> None:
        self.graphic = Graphic()

    def update(self) -> None:
        Display.display.fill((0, 0, 0))

        self.graphic.background_axes() if self.graphic.toggle_background_axes else ...
        self.graphic.axes() if self.graphic.toggle_axes else ...
        if not self.graphic.toggle_help:
            self.graphic.controller()
            self.graphic.sin() if self.graphic.toggle_sin else ...
            self.graphic.cos() if self.graphic.toggle_cos else ...
            self.graphic.tan() if self.graphic.toggle_tan else ...
            self.graphic.circle() if self.graphic.toggle_circle else ...
            self.graphic.show_info() if self.graphic.toggle_info else ...
        self.graphic.show_help() if self.graphic.toggle_help else ...

        if not self.graphic.toggle_help:
            SIZE = 25
            blit = Display.display.blit
            render_text = pg.font.SysFont(FONT, SIZE).render

            blit(render_text("[H] for help", True, WHITE),
                 (Display.dimension.x-100, Display.dimension.y-SIZE))

        pg.display.update()

    def controller(self, all=True) -> None:
        key = pg.key.get_pressed()
        if all:
            if key[K_s]:
                self.graphic.toggle_sin = not self.graphic.toggle_sin
            if key[K_c]:
                self.graphic.toggle_cos = not self.graphic.toggle_cos
            if key[K_t]:
                self.graphic.toggle_tan = not self.graphic.toggle_tan
            if key[K_d]:
                self.graphic.toggle_circle = not self.graphic.toggle_circle
            if key[K_i]:
                self.graphic.toggle_info = not self.graphic.toggle_info
            if key[K_h]:
                self.graphic.toggle_help = not self.graphic.toggle_help
        else:
            if key[K_h]:
                self.graphic.toggle_help = not self.graphic.toggle_help


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
                if game.graphic.toggle_help:
                    game.controller(False)
                else:
                    game.controller()

        game.update()
        clock.tick(60)
