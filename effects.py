import time
import random
import numpy as np
import simpleaudio as sa
from datetime import datetime
from rich.text import Text
from rich.style import Style
from rich.progress import Progress, SpinnerColumn, TextColumn

class ParticleSystem:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.particles = []

    def emit(self, x, y, count=10):
        """Emit new particles from a point"""
        for _ in range(count):
            angle = random.uniform(0, 2 * np.pi)
            speed = random.uniform(0.5, 2.0)
            self.particles.append({
                'x': x,
                'y': y,
                'dx': np.cos(angle) * speed,
                'dy': np.sin(angle) * speed,
                'life': 1.0,
                'char': random.choice("*+·•○◦")
            })

    def update(self):
        """Update particle positions and lifetimes"""
        self.particles = [p for p in self.particles if p['life'] > 0]
        for p in self.particles:
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['life'] -= 0.05

class EnhancedRetroEffects:
    def __init__(self):
        self.console_width = 80  # Default width
        self.console_height = 24  # Default height
        self.phosphor_persistence = 0.15
        self.particles = ParticleSystem(self.console_width, self.console_height)
        self.season = self.determine_season()
        self.initialize_sounds()

    def determine_season(self):
        """Determine the current season based on the month."""
        month = datetime.now().month
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        elif month in [9, 10, 11]:
            return "autumn"
        return "unknown"

    def create_glitch_effect(self, text):
        """Create a glitch effect for the given text."""
        glitched_text = ""
        for char in text:
            if random.random() < 0.1:  # 10% chance to glitch
                glitched_text += random.choice(['#', '@', '%', '&', '*'])  # Random glitch characters
            else:
                glitched_text += char
        return glitched_text
    def create_glowing_text(self, text):
        """Create a glowing effect for the given text."""
        glowing_text = Text(text, style=Style(color="cyan", bgcolor="black", bold=True))
        return glowing_text
    def update(self):
        """Update all animation states"""
        self.particles.update()
        self._update_seasonal_effects()

    def initialize_sounds(self):
        """Initialize sound effects"""
        sample_rate = 44100
        
        # Boot sound
        boot_duration = 0.3
        t = np.linspace(0, boot_duration, int(sample_rate * boot_duration))
        boot_freqs = [440, 880, 1320, 220, 660]
        boot_audio = np.zeros_like(t)
        
        for i, freq in enumerate(boot_freqs):
            envelope = np.exp(-3 * t / boot_duration)
            boot_audio += np.sin(2 * np.pi * freq * t) * envelope * (0.8 ** i)
        
        self.boot_sound = (boot_audio * 0.3 * 32767).astype(np.int16)

        # Key press sound
        key_duration = 0.05
        t = np.linspace(0, key_duration, int(sample_rate * key_duration))
        self.key_sound = (np.sin(2 * np.pi * 440 * t) * 32767).astype(np.int16)

    def play_sound(self, sound):
        """Play a sound effect"""
        play_obj = sa.play_buffer(sound, 1, 2, 44100)
        play_obj.wait_done()

    def render_matrix_effect(self):
        """Render the matrix effect"""
        matrix_chars = ['0', '1']
        output = []
        
        for y in range(self.console_height):
            line = ""
            for x in range(self.console_width):
                if random.random() < 0.02:  # Adjust density
                    char = random.choice(matrix_chars)
                    intensity = random.uniform(0.5, 1.0)
                    green = int(255 * intensity)
                    line += f"\x1b[38;2;0;{green};0m{char}"
                else:
                    line += " "
            output.append(line)
        
        return "\n".join(output)

    def trigger_debug_easter_egg(self):
        """Debug easter egg animation"""
        skull_art = """
          .---.
         /     \\
        | () () |
         \\  ^  /
          |||||
          |||||
        """
        return self.create_glowing_text(skull_art)

    def trigger_diagnostic_easter_egg(self):
        """Diagnostic easter egg animation"""
        robot_art = """
         /[][][]\\
        |  o  o  |
        |   ▼    |
        |  ___   |
         \\     /
          -----
        """
        return self.create_glowing_text(robot_art)

    def _create_snow_effect(self):
        """Create snow particles"""
        snowflakes = []
        for _ in range(self.console_width // 4):
            snowflakes.append({
                'x': random.randint(0, self.console_width),
                'y': random.randint(0, self.console_height),
                'speed': random.uniform(0.2, 0.5),
                'char': '❄'
            })
        return snowflakes

    def _create_falling_leaves_effect(self):
        """Create falling leaves particles"""
        leaves = []
        leaf_chars = ["🍁", "🍂", "🍃"]
        for _ in range(self.console_width // 6):
            leaves.append({
                'x': random.randint(0, self.console_width),
                'y': random.randint(0, self.console_height),
                'speed': random.uniform(0.3, 0.7),
                'char': random.choice(leaf_chars)
            })
        return leaves

    def _update_seasonal_effects(self):
        """Update seasonal particle effects"""
        if hasattr(self, 'seasonal_particles'):
            for particle in self.seasonal_particles:
                particle['y'] += particle['speed']
                if particle['y'] > self.console_height:
                    particle['y'] = 0
                    particle['x'] = random.randint(0, self.console_width)

    def get_seasonal_particles(self):
        """Get current seasonal particle effect"""
        if not hasattr(self, 'seasonal_particles'):
            if self.season == "winter":
                self.seasonal_particles = self._create_snow_effect()
            elif self.season == "autumn":
                self.seasonal_particles = self._create_falling_leaves_effect()
            else:
                self.seasonal_particles = []
        
        return self.seasonal_particles