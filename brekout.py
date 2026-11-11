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