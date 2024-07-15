import time
import random
import sys
from threading import Thread

class SmoothAnimation:
    def __init__(self):
        self.running = False
        self.thread = None
        self.displayed = False
        self.initialized = False

    def generate_waveform_data(self, num_points=50):
        return [random.uniform(-1, 1) for _ in range(num_points)]

    def render_waveform(self, data):
        bars_chars = '▁▂▃▄▅▆▇█'
        wave_chars = '░▒▓█'
        combined_chars = [bars_chars[min(int((value + 1) * 4), 7)] if i % 2 == 0 else wave_chars[min(int((value + 1) * 2), 3)] for i, value in enumerate(data)]
        return ''.join(combined_chars)

    def animate(self):
        while self.running:
            data = self.generate_waveform_data(num_points=30)
            waveform = self.render_waveform(data)
            sys.stdout.write('\r' + '🎵 ' + waveform + ' 🎵')
            sys.stdout.flush()
            time.sleep(0.1)

    def start(self):
        self.running = True
        self.thread = Thread(target=self.animate)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        self.clear_animation()

    def ensure_new_line(self):
        if not self.displayed:
            sys.stdout.write('\n')
            self.displayed = True

    def clear_animation(self):
        sys.stdout.write('\r' + ' ' * 50 + '\r')
        sys.stdout.flush()

    def initialize(self):
        self.initialized = True

animation = SmoothAnimation()

def init_animation():
    animation.initialize()

def start_animation():
    if animation.initialized:
        animation.ensure_new_line()
        animation.start()

def stop_animation():
    animation.stop()

def clear_animation():
    animation.clear_animation()