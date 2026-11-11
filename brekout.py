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


class LavaBrick:
    COLORS = {
        1: ("#a93613", "#ff7a18", "#ffc247"),
        2: ("#702316", "#d94b16", "#ff9b22"),
        3: ("#4c1c19", "#a93613", "#f06a18"),
    }

    def __init__(self, canvas, x, y, hits, tag):
        self.canvas = canvas
        self.x, self.y = x, y
        self.width, self.height = 66, 24
        self.hits = hits
        self.tag = tag
        self.draw()

    def draw(self):
        c = self.canvas
        x1, y1 = self.x-self.width/2, self.y-self.height/2
        x2, y2 = self.x+self.width/2, self.y+self.height/2
        dark, mid, hot = self.COLORS[self.hits]
        
        # Mendaftarkan tags "brick" agar bisa dizoom secara massal bersamaan
        c.create_rectangle(x1, y1, x2, y2, fill=dark, outline="#ff9a32", width=2, tags=(self.tag, self.tag+"_bg", "brick"))
        blocks = [
            (x1+4, y1+4, x1+17, y1+10, mid, "_m1"), (x1+21, y1+3, x1+34, y1+9, hot, "_h1"),
            (x1+42, y1+4, x1+59, y1+10, mid, "_m2"), (x1+10, y1+13, x1+24, y1+20, hot, "_h2"),
            (x1+30, y1+13, x1+43, y1+20, mid, "_m3"), (x1+49, y1+13, x1+62, y1+20, hot, "_h3"),
        ]
        for a, b, d, e, color, subtag in blocks:
            c.create_rectangle(a, b, d, e, fill=color, outline=dark, width=1, tags=(self.tag, self.tag+subtag, "brick"))

    def update_colors(self):
        dark, mid, hot = self.COLORS[self.hits]
        self.canvas.itemconfig(self.tag+"_bg", fill=dark, outline="#ff9a32")
        for subtag in ["_m1", "_m2", "_m3"]: self.canvas.itemconfig(self.tag+subtag, fill=mid, outline=dark)
        for subtag in ["_h1", "_h2", "_h3"]: self.canvas.itemconfig(self.tag+subtag, fill=hot, outline=dark)

    def hit(self):
        self.hits -= 1
        if self.hits <= 0:
            self.canvas.delete(self.tag)
            return True
        self.update_colors()
        return False

    def logical_bbox(self):
        return (self.x - self.width/2, self.y - self.height/2, self.x + self.width/2, self.y + self.height/2)


class BrickBreaker(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.master = master
        self.master.configure(bg=BG)
        self.pack(fill=tk.BOTH, expand=True)

        self.scale_x = 1.0
        self.scale_y = 1.0

        self.canvas = tk.Canvas(self, width=LOGICAL_WIDTH, height=LOGICAL_HEIGHT, bg=BG, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_resize)
        
        self.running = False
        self.finished = False
        self.lives = 3
        self.score = 0
        self.speed_level = 1
        self.bricks = []
        
        self.keys = set()
        self.master.bind("<KeyPress>", self.key_press)
        self.master.bind("<KeyRelease>", self.key_release)
        self.canvas.bind("<Motion>", self.mouse_move)
        self.master.bind("<space>", self.start)
        self.master.bind("<r>", self.restart)
        self.master.bind("<R>", self.restart)
        
        self.is_fullscreen = False
        self.master.bind("<f>", self.toggle_fullscreen)
        self.master.bind("<F>", self.toggle_fullscreen)
        self.master.bind("<F11>", self.toggle_fullscreen)
        self.master.bind("<Escape>", self.exit_fullscreen)
        self.master.bind("<m>", self.minimize_window)
        self.master.bind("<M>", self.minimize_window)

        self.new_game()
        self.check_inputs()
        self.master.focus_force()

    def on_resize(self, event):
        # Trigger zoom jika ukuran jendela membesar (Fullscreen) atau mengecil
        if event.widget == self.canvas:
            if event.width <= 1 or event.height <= 1: return
            
            new_scale_x = event.width / LOGICAL_WIDTH
            new_scale_y = event.height / LOGICAL_HEIGHT
            
            if new_scale_x == self.scale_x and new_scale_y == self.scale_y: return
            
            ratio_x = new_scale_x / self.scale_x
            ratio_y = new_scale_y / self.scale_y
            
            self.canvas.scale("all", 0, 0, ratio_x, ratio_y)
            self.scale_fonts(new_scale_x, new_scale_y)
            
            self.scale_x, self.scale_y = new_scale_x, new_scale_y

    def scale_fonts(self, sx, sy):
        # Font ikut menyesuaikan skala agar tidak kekecilan
        avg = (sx + sy) / 2
        self.canvas.itemconfig("title_text", font=("Arial", max(8, int(15 * avg)), "bold"))
        self.canvas.itemconfig("hud_text", font=("Arial", max(8, int(12 * avg)), "bold"))
        self.canvas.itemconfig("msg_title", font=("Arial", max(12, int(25 * avg)), "bold"))
        self.canvas.itemconfig("msg_sub", font=("Arial", max(8, int(10 * avg))))
        self.canvas.itemconfig("msg_end1", font=("Arial", max(20, int(48 * avg)), "bold"))
        self.canvas.itemconfig("msg_end2", font=("Arial", max(8, int(13 * avg)), "bold"))
        self.canvas.itemconfig("msg_end3", font=("Arial", max(8, int(12 * avg)), "bold"))

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.master.attributes("-fullscreen", self.is_fullscreen)

    def exit_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.master.attributes("-fullscreen", False)
        
    def minimize_window(self, event=None):
        self.master.iconify()

    def check_inputs(self):
        if hasattr(self, 'car') and self.car:
            if "Left" in self.keys or "a" in self.keys or "A" in self.keys:
                self.car.move(-16, self.scale_x, self.scale_y)
            if "Right" in self.keys or "d" in self.keys or "D" in self.keys:
                self.car.move(16, self.scale_x, self.scale_y)
        self.master.after(16, self.check_inputs)

    def key_press(self, event):
        if hasattr(event, 'keysym'): self.keys.add(event.keysym)

    def key_release(self, event):
        if hasattr(event, 'keysym'): self.keys.discard(event.keysym)

    def mouse_move(self, event):
        if not self.finished and hasattr(self, 'car') and self.car:
            # Memperhitungkan efek zoom pada pelacakan mouse
            logical_x = event.x / self.scale_x
            dx = logical_x - self.car.x
            self.car.move(dx, self.scale_x, self.scale_y)

    def draw_background(self):
        c = self.canvas
        c.create_rectangle(0, 0, LOGICAL_WIDTH, LOGICAL_HEIGHT, fill=BG, outline="", tags="background")
        for x in range(35, LOGICAL_WIDTH, 90):
            c.create_line(x, 0, x-35, LOGICAL_HEIGHT, fill="#102b48", width=1, tags="background")
        c.create_line(0, 116, LOGICAL_WIDTH, 116, fill="#16476b", width=1, tags="background")
        c.create_text(LOGICAL_WIDTH/2, 18, text="ELECTRIC MINI 4WD  •  BRICK BREAKER", fill="#8cefff", font=("Arial", 15, "bold"), tags=("background", "title_text"))

    def new_game(self):
        self.canvas.delete("all")
        self.draw_background()
        self.lives = 3
        self.score = 0
        self.speed_level = 1
        self.bricks = []
        self.car = CarPaddle(self.canvas, LOGICAL_WIDTH/2, LOGICAL_HEIGHT-54)
        
        start_x = 55
        for row in range(4):
            for col in range(10):
                hits = 1 if row in (0, 1) else 2
                brick = LavaBrick(self.canvas, start_x + col * 72, 155 + row * 31, hits, "brick_%d_%d" % (row, col))
                self.bricks.append(brick)
                
        self.ball = Ball(self.canvas, LOGICAL_WIDTH/2, LOGICAL_HEIGHT-95)
        self.car.ball = self.ball
        self.running = False
        self.finished = False

        # Aplikasikan skala zoom jika saat game dibuat ulang layar sudah berukuran penuh
        if self.scale_x != 1.0 or self.scale_y != 1.0:
            self.canvas.scale("background", 0, 0, self.scale_x, self.scale_y)
            self.canvas.scale("brick", 0, 0, self.scale_x, self.scale_y)
            self.canvas.scale("car", 0, 0, self.scale_x, self.scale_y)
            self.canvas.scale("ball", 0, 0, self.scale_x, self.scale_y)
            self.scale_fonts(self.scale_x, self.scale_y)

        self.update_hud()
        self.show_message("PRESS SPACE TO START", "#a8f6ff", "Kendali: Mouse / Trackpad / ← → / A D")

    def update_hud(self):
        self.canvas.delete("hud")
        avg = (self.scale_x + self.scale_y) / 2
        fnt = ("Arial", max(8, int(12 * avg)), "bold")
        
        self.canvas.create_text(75, 53, text="NYAWA: %d" % self.lives, fill="#ffffff", font=fnt, tags=("hud", "hud_text"))
        self.canvas.create_text(LOGICAL_WIDTH/2, 53, text="SKOR: %d" % self.score, fill="#ffffff", font=fnt, tags=("hud", "hud_text"))
        self.canvas.create_text(LOGICAL_WIDTH-100, 53, text="KECEPATAN: %.1fx" % self.speed_level, fill="#7df7ff", font=fnt, tags=("hud", "hud_text"))
        
        if self.scale_x != 1.0 or self.scale_y != 1.0:
            self.canvas.scale("hud", 0, 0, self.scale_x, self.scale_y)

    def show_message(self, title, color, subtitle):
        self.canvas.delete("message")
        self.canvas.create_rectangle(105, 220, LOGICAL_WIDTH-105, 310, fill="#081a2b", outline=color, width=3, tags="message")
        
        avg = (self.scale_x + self.scale_y) / 2
        self.canvas.create_text(LOGICAL_WIDTH/2, 253, text=title, fill=color, font=("Arial", max(12, int(25 * avg)), "bold"), tags=("message", "msg_title"))
        self.canvas.create_text(LOGICAL_WIDTH/2, 286, text=subtitle, fill="#e4faff", font=("Arial", max(8, int(10 * avg))), tags=("message", "msg_sub"))
        
        if self.scale_x != 1.0 or self.scale_y != 1.0:
            self.canvas.scale("message", 0, 0, self.scale_x, self.scale_y)

    def start(self, event=None):
        if self.finished or self.running: return
        self.canvas.delete("message")
        self.ball.is_held = False 
        self.running = True
        self.loop()

    def restart(self, event=None):
        self.new_game()

    def increase_speed(self):
        current = math.hypot(self.ball.vx, self.ball.vy)
        new_speed = min(current + 0.22, 11.5)
        factor = new_speed / current if current else 1
        self.ball.vx *= factor
        self.ball.vy *= factor
        self.speed_level = new_speed / 5.66
        self.update_hud()

    @staticmethod
    def overlaps(a, b):
        return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]

    def loop(self):
        if not self.running: return

        b = self.ball
        next_x = b.x + b.vx
        next_y = b.y + b.vy
        r = b.radius

        if next_x - r <= 2 or next_x + r >= LOGICAL_WIDTH - 2:
            b.vx *= -1
            next_x = b.x + b.vx
        if next_y - r <= 76:
            b.vy = abs(b.vy)
            next_y = b.y + b.vy

        b.move_to(next_x, next_y, self.scale_x, self.scale_y)

        car_box = self.car.logical_bbox()
        ball_box = b.logical_bbox()
        if self.overlaps(ball_box, car_box) and b.vy > 0:
            relative = (b.x - self.car.x) / (CarPaddle.WIDTH / 2)
            b.vx = max(-7.5, min(7.5, relative * 6.5))
            b.vy = -abs(b.vy)
            self.increase_speed()

        for brick in list(self.bricks):
            if self.overlaps(ball_box, brick.logical_bbox()):
                destroyed = brick.hit()
                b.vy *= -1
                self.score += 10
                self.increase_speed()
                if destroyed:
                    self.bricks.remove(brick)
                    self.score += 20
                self.update_hud()
                break

        if b.y - r > LOGICAL_HEIGHT:
            self.lives -= 1
            self.update_hud()
            if self.lives <= 0:
                self.end_game(False)
                return
                
            self.ball.delete()
            self.ball = Ball(self.canvas, self.car.x, LOGICAL_HEIGHT-95)
            # Jika dalam mode fullscreen, zoom bola yang baru dibuat
            if self.scale_x != 1.0 or self.scale_y != 1.0:
                self.canvas.scale("ball", 0, 0, self.scale_x, self.scale_y)
                
            self.car.ball = self.ball
            self.running = False
            self.keys.clear() 
            self.show_message("TRY AGAIN", "#ff9a45", "Tekan SPACE untuk melanjutkan")
            return

        if not self.bricks:
            self.end_game(True)
            return

        delay = max(12, int(34 - self.speed_level * 1.2))
        self.master.after(delay, self.loop)

    def end_game(self, won):
        self.running = False
        self.finished = True
        self.canvas.delete("message")
        
        color = "#8ffaff" if won else "#ff7a28"
        bg_col = "#062b43" if won else "#35140f"
        out_col = "#38eaff" if won else "#ff6a1a"
        
        self.canvas.create_rectangle(65, 175, LOGICAL_WIDTH-65, 365, fill=bg_col, outline=out_col, width=5, tags="message")
        
        avg = (self.scale_x + self.scale_y) / 2
        f1, f2, f3 = ("Arial", max(20, int(48 * avg)), "bold"), ("Arial", max(8, int(13 * avg)), "bold"), ("Arial", max(8, int(12 * avg)), "bold")
        
        self.canvas.create_text(LOGICAL_WIDTH/2, 235, text="YOU WIN!" if won else "YOU LOSE", fill="#baffff" if won else "#ff9b3d", font=f1, tags=("message", "msg_end1"))
        self.canvas.create_text(LOGICAL_WIDTH/2, 295, text="SEMUA BALOK LAVA BERHASIL DIHANCURKAN!" if won else "BOLA LISTRIK JATUH! COBA LAGI.", fill="#54dfff" if won else "#ffd0a0", font=f2, tags=("message", "msg_end2"))
        self.canvas.create_text(LOGICAL_WIDTH/2, 335, text="Tekan R untuk bermain lagi", fill=color, font=f3, tags=("message", "msg_end3"))
        
        if self.scale_x != 1.0 or self.scale_y != 1.0:
            self.canvas.scale("message", 0, 0, self.scale_x, self.scale_y)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Electric Mini 4WD - Brick Breaker (Responsive)")
    
    # Menetapkan ukuran bawaan sebelum dimaksimalkan
    root.geometry(f"{LOGICAL_WIDTH}x{LOGICAL_HEIGHT}")
    root.configure(bg=BG)
    
    game = BrickBreaker(root)
    root.mainloop()