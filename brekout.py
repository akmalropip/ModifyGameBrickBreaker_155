import tkinter as tk
import math

# ------------------------------------------------------------
# BRICK BREAKER: MINI 4WD vs. ELECTRIC ORB (FULL RESPONSIVE)
# Kontrol: Mouse/Trackpad, Panah kiri/kanan atau A/D.
#          Space = Mulai, R = Ulang.
#          F/F11 = Fullscreen (Layar Penuh Skala), Esc = Keluar.
# ------------------------------------------------------------

LOGICAL_WIDTH = 760
LOGICAL_HEIGHT = 520
BG = "#071426"


class Ball:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = 12
        self.vx = 3.8
        self.vy = -4.2
        self.is_held = True
        self._draw()

    def _draw(self):
        c = self.canvas
        x, y, r = self.x, self.y, self.radius
        c.create_oval(x-r-8, y-r-8, x+r+8, y+r+8, fill="#073d67", outline="#087eaa", width=2, tags="ball")
        c.create_oval(x-r, y-r, x+r, y+r, fill="#25cfff", outline="#d8ffff", width=2, tags="ball")
        c.create_oval(x-r+4, y-r+4, x+r-4, y+r-4, fill="#b8ffff", outline="#ffffff", width=1, tags="ball")
        for angle in (25, 145, 265):
            a = math.radians(angle)
            x1, y1 = x + math.cos(a) * (r + 7), y + math.sin(a) * (r + 7)
            x2, y2 = x + math.cos(a + .25) * (r + 15), y + math.sin(a + .25) * (r + 15)
            x3, y3 = x + math.cos(a - .12) * (r + 21), y + math.sin(a - .12) * (r + 21)
            c.create_line(x1, y1, x2, y2, x3, y3, fill="#7df7ff", width=2, tags="ball")

    def move_to(self, new_x, new_y, scale_x, scale_y):
        dx = new_x - self.x
        dy = new_y - self.y
        self.canvas.move("ball", dx * scale_x, dy * scale_y)
        self.x, self.y = new_x, new_y

    def logical_bbox(self):
        r = self.radius
        return (self.x - r, self.y - r, self.x + r, self.y + r)

    def delete(self):
        self.canvas.delete("ball")


class CarPaddle:
    WIDTH = 104
    HEIGHT = 42

    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.ball = None
        self.draw()

    def draw(self):
        c, x, y = self.canvas, self.x, self.y
        c.create_oval(x-43, y+8, x-22, y+27, fill="#101820", outline="#aab7c5", width=2, tags="car")
        c.create_oval(x+22, y+8, x+43, y+27, fill="#101820", outline="#aab7c5", width=2, tags="car")
        c.create_polygon(x-52, y+7, x-39, y-8, x-22, y-18, x+25, y-18, x+43, y-7, x+53, y+8,
                         x+43, y+17, x-43, y+17, fill="#1269d3", outline="#dff8ff", width=2, tags="car")
        c.create_polygon(x-25, y-15, x-12, y-25, x+17, y-25, x+31, y-13, x+22, y-5, x-20, y-5,
                         fill="#f4fbff", outline="#9bdcff", width=2, tags="car")
        c.create_polygon(x-8, y-23, x+7, y-23, x+18, y-8, x-18, y-8, fill="#0b4da4",
                         outline="#dff8ff", width=1, tags="car")
        c.create_line(x-43, y+4, x+43, y+4, fill="#ffffff", width=3, tags="car")
        c.create_line(x-8, y-17, x+8, y-17, fill="#ffffff", width=2, tags="car")
        c.create_oval(x-48, y+1, x-39, y+8, fill="#eaffff", outline="#ffffff", tags="car")
        c.create_oval(x+39, y+1, x+48, y+8, fill="#eaffff", outline="#ffffff", tags="car")
        c.create_line(x-48, y+16, x+48, y+16, fill="#d9e8f5", width=4, tags="car")

    def move(self, dx, scale_x, scale_y):
        min_x = 5 + 52
        max_x = LOGICAL_WIDTH - 5 - 53

        new_x = self.x + dx
        if new_x < min_x: new_x = min_x
        if new_x > max_x: new_x = max_x

        actual_dx = new_x - self.x
        if actual_dx != 0:
            self.canvas.move("car", actual_dx * scale_x, 0)
            self.x = new_x
            if self.ball and getattr(self.ball, 'is_held', False):
                self.ball.move_to(self.x, self.ball.y, scale_x, scale_y)

    def logical_bbox(self):
        return (self.x - 52, self.y - 25, self.x + 53, self.y + 27)