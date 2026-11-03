import math
import os
import random
import sys

# Qt can't position windows on Wayland, so use XWayland on Linux
if sys.platform.startswith("linux") and "QT_QPA_PLATFORM" not in os.environ:
    os.environ["QT_QPA_PLATFORM"] = "xcb"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
from PySide6.QtCore import QRect, Qt, QTimer
from PySide6.QtGui import QKeySequence, QPainter, QPixmap, QShortcut, QTransform
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

# ---------------- SETTINGS ----------------
IMAGES_DIR = "images"      # folder with your png/jpg/gif/webp images
AUDIO_FILE = "music.mp3"   # your audio (mp3, wav, ogg)
NUM_WINDOWS = 12           # how many popups in total
SPAWN_EVERY_MS = 600       # delay between each new popup
SIZE_RANGE = (140, 260)    # popup size in pixels
SPEED_RANGE = (3, 8)       # movement speed
FPS = 30
MAX_SECONDS = 0            # auto-stop after N seconds (0 = never)
# ------------------------------------------

BASE = (os.path.dirname(sys.executable) if getattr(sys, "frozen", False)
        else os.path.dirname(os.path.abspath(__file__)))


def load_pixmaps():
    folder = os.path.join(BASE, IMAGES_DIR)
    exts = (".png", ".jpg", ".jpeg", ".gif", ".webp")
    files = []
    if os.path.isdir(folder):
        files = [os.path.join(folder, f) for f in sorted(os.listdir(folder))
                 if f.lower().endswith(exts)]
    pixmaps = [QPixmap(f) for f in files]
    return [p for p in pixmaps if not p.isNull()]


def make_frames(pix, size, steps=24):
    """Pre-render a swaying animation (rotation back and forth)."""
    base = pix.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    frames = []
    for i in range(steps):
        angle = 18 * math.sin(2 * math.pi * i / steps)
        frames.append(base.transformed(QTransform().rotate(angle),
                                       Qt.SmoothTransformation))
    return frames


class Dancer(QWidget):
    def __init__(self, pix, bounds):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        size = random.randint(*SIZE_RANGE)
        self.side = int(size * 1.35) + 4
        self.setFixedSize(self.side, self.side)
        self.frames = make_frames(pix, size)

        self.bounds = bounds
        self.x = float(random.randint(bounds.left(), max(bounds.left(), bounds.right() - self.side)))
        self.y = float(random.randint(bounds.top(), max(bounds.top(), bounds.bottom() - self.side)))
        speed = random.uniform(*SPEED_RANGE)
        ang = random.uniform(0, 2 * math.pi)
        self.vx, self.vy = speed * math.cos(ang), speed * math.sin(ang)
        self.t = random.randint(0, 100)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000 // FPS)

    def tick(self):
        b = self.bounds
        self.x += self.vx
        self.y += self.vy
        max_x, max_y = b.right() - self.side, b.bottom() - self.side
        if self.x < b.left() or self.x > max_x:
            self.vx = -self.vx
            self.x = min(max(self.x, b.left()), max_x)
        if self.y < b.top() or self.y > max_y:
            self.vy = -self.vy
            self.y = min(max(self.y, b.top()), max_y)
        self.t += 1
        hop = abs(math.sin(self.t / 4)) * 25  # little dance hop
        self.move(int(self.x), int(self.y - hop))
        self.update()

    def paintEvent(self, _):
        f = self.frames[self.t % len(self.frames)]
        p = QPainter(self)
        p.drawPixmap((self.width() - f.width()) // 2,
                     (self.height() - f.height()) // 2, f)

    def mousePressEvent(self, _):  # click = close this one
        self.timer.stop()
        self.close()


class Control(QWidget):
    def __init__(self, on_stop):
        super().__init__()
        self.on_stop = on_stop
        self.setWindowTitle("mei mei")
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        btn = QPushButton("STOP  (Esc)")
        btn.setMinimumHeight(50)
        btn.clicked.connect(on_stop)
        layout = QVBoxLayout(self)
        layout.addWidget(btn)
        QShortcut(QKeySequence("Esc"), self, activated=on_stop)

    def closeEvent(self, event):
        self.on_stop()
        event.accept()


def start_audio():
    path = os.path.join(BASE, AUDIO_FILE)
    if not os.path.exists(path):
        print(f"Audio file not found: {path} (continuing without sound)")
        return
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)  # loop forever
    except Exception as e:
        print(f"Could not play audio: {e}")


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    pixmaps = load_pixmaps()
    if not pixmaps:
        sys.exit(f"Put some images in the '{IMAGES_DIR}' folder next to the app.")

    def stop():
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        app.quit()

    bounds = QRect()
    for s in app.screens():  # covers all monitors
        bounds = bounds.united(s.geometry())

    start_audio()

    ctrl = Control(stop)
    ctrl.move(bounds.left() + 20, bounds.top() + 20)
    ctrl.show()

    dancers = []
    spawn_timer = QTimer()

    def spawn():
        if len(dancers) >= NUM_WINDOWS:
            spawn_timer.stop()
            return
        d = Dancer(random.choice(pixmaps), bounds)
        dancers.append(d)
        d.show()
        ctrl.raise_()

    spawn_timer.timeout.connect(spawn)
    spawn_timer.start(SPAWN_EVERY_MS)
    spawn()

    raise_timer = QTimer()
    raise_timer.timeout.connect(ctrl.raise_)  # keep STOP button above the popups
    raise_timer.start(500)

    if MAX_SECONDS:
        QTimer.singleShot(MAX_SECONDS * 1000, stop)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
